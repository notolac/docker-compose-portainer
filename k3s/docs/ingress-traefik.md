# Publishing K3s apps with Traefik

How apps under [`../apps/`](../apps/) reach the outside world.
Docker stacks in this repo publish through **Nginx Proxy Manager**;
on K3s the standard reverse proxy is **Traefik** (Helm install:
[`../helm/traefik/`](../helm/traefik/)).

## Docker vs K3s

| Aspect | Docker (`docker/`) | K3s (`k3s/`) |
|--------|-------------------|--------------|
| Reverse proxy | Nginx Proxy Manager (see `docker/nginx-proxy-manager-goaccess/`, `docker/traefik/` for the Traefik-based Docker stack) | Traefik (Helm chart, [`../helm/traefik/`](../helm/traefik/)) |
| TLS | NPM Let's Encrypt / DNS challenge | Traefik `cloudflare` ACME DNS-01 resolver |
| Per-app config | NPM UI or Docker labels | `ingress.yaml` in each app folder, or a Traefik file-provider router |
| SSO | Per-app / NPM access lists | Authentik forwardAuth ([`../helm/authentik/`](../helm/authentik/)) |
| Cluster UI | Portainer CE container | Portainer in-cluster ([`../helm/portainer/`](../helm/portainer/)) |

## Prerequisites

1. **Traefik** installed from [`../helm/traefik/`](../helm/traefik/)
   (LoadBalancer + MetalLB VIP, ACME DNS-01, file provider enabled).
2. **MetalLB** address pool with free LAN IPs — see
   [`../configs/metallb/ipaddresspool.yaml.example`](../configs/metallb/ipaddresspool.yaml.example).
   Traefik and Portainer need **different** VIPs.
3. **DNS** pointing each app host at the Traefik VIP (public DNS via
   Cloudflare and/or LAN split-DNS — your choice, out of scope here).
4. (Optional) **Authentik** from [`../helm/authentik/`](../helm/authentik/)
   for SSO-gated apps and the Traefik dashboard.

## Dual model: Ingress first, file provider when needed

Every app in [`../apps/`](../apps/) ships a standard `ingress.yaml`
(`*.example.com` hosts — set yours). That is the **default path**:
plain `networking.k8s.io/v1` Ingress, no Traefik-specific resources.

```yaml
spec:
  ingressClassName: traefik
  rules:
    - host: myapp.example.com   # set YOUR host
```

Terminate TLS at the ingress (the app itself serves plain HTTP —
see each app's README for the in-app URL setting that must match
the public host, e.g. `DOMAIN`, `BASE_URL`, `APP_URL`).

Reach for the **file-provider router** (see
[`../helm/traefik/dynamic-app-example.yaml`](../helm/traefik/dynamic-app-example.yaml))
only when you need something a plain Ingress cannot express well:

- shared Cloudflare allowlist / header chains from `middlewares.yaml`
- Authentik `forwardAuth` on a subset of paths (login callbacks, OAuth endpoints)
- HTTPS backends with self-signed certs (`insecureSkipVerify`, e.g. Portainer `:9443`)
- custom timeouts (`serversTransport`, e.g. LLM apps)

Both paths can coexist: keep `ingress.yaml` for the app, add a file-provider
router only for the special cases.

## Exposing a new app

### A. Standard Ingress (default)

1. Copy any `ingress.yaml` from [`../apps/`](../apps/), set
   `ingressClassName: traefik`, YOUR host, and the Service name/port.
2. Add TLS (`certResolver: cloudflare` via Ingress annotations, or your
   own `Certificate` — see the whoami example in
   [`../helm/traefik/whoami.yaml`](../helm/traefik/whoami.yaml)).
3. Sync the public host into the app config (`DOMAIN` / `BASE_URL` /
   `APP_URL` / trusted origins — each app README lists them).
4. Dry-run and apply:
   `kubectl apply --dry-run=client -k k3s/apps/<app>/`, then without `--dry-run`.

### B. File-provider router (advanced)

1. Copy [`../helm/traefik/dynamic-app-example.yaml`](../helm/traefik/dynamic-app-example.yaml)
   to `<app>.yaml`, set host / namespace / Service / port.
2. Pick a middleware chain from `middlewares.yaml`:
   `cloudflare@file` → `cloudflareHeaders@file` → `secureHeaders@file`
   (+ `realClientIP@file` / `authentikForwardAuth@file` when applicable, see below).
3. Merge it into ConfigMap `traefik-file-provider` (namespace `traefik`)
   and apply. Traefik picks it up automatically (watch mode).

## Real client IP behind Cloudflare

With proxied DNS, TCP arrives from Cloudflare edge IPs, so backends see
Cloudflare — not the visitor — unless three pieces agree:

| Piece | Where | What |
|-------|-------|------|
| `forwardedheaders.trustedips` | `traefik-values.yaml` (`additionalArguments`) | Traefik trusts `X-Forwarded-*` only from Cloudflare ranges |
| `externalTrafficPolicy: Local` | `traefik-values.yaml` (`service.spec`) | MetalLB skips SNAT; Traefik sees the real peer IP |
| `realClientIP@file` | `middlewares.yaml` | Drops the incoming `X-Forwarded-For`; Traefik re-adds one hop with the visitor IP |

Rules of thumb:

- Backend reads the client IP (audit logs, app-level IP rules, internal
  rate limits) **and** trusts `X-Forwarded-For` from the cluster →
  add `realClientIP@file` after `cloudflare@file`, and set the app's
  trusted-proxies setting to the pod/service CIDRs.
- Backend already reads `CF-Connecting-IP` or its own trusted XFF chain →
  **skip** `realClientIP` (the app would otherwise see the Traefik pod IP).
- No IP requirements (dashboards, internal tools) → skip it.

## SSO with Authentik

1. Install Authentik ([`../helm/authentik/`](../helm/authentik/)) and create
   a Proxy Provider + Application for Traefik forwardAuth. The outpost URL
   must be the **public** Authentik host so cookies/session match.
2. Set YOUR host in `authentikForwardAuth` (`middlewares.yaml`) or in the
   `authentik-forwardauth` Middleware CRD
   (`middleware-authentik.yaml.example`).
3. Attach it to the router: file-provider `middlewares:` list, Ingress
   annotation `traefik.ingress.kubernetes.io/router.middlewares:`,
   or the dashboard `ingressRoute` in `traefik-values.yaml`.
4. Keep the outpost path reachable: the forwardAuth address must itself
   route through Traefik to Authentik.

Apps where the website builder or OAuth callbacks need same-origin framing
(e.g. Odoo) must **not** combine SSO with `frameDeny` headers — check the
app README first.

## ACME / certificates

- Issuer: Let's Encrypt via the `cloudflare` DNS-01 resolver (no HTTP-01,
  works behind Cloudflare proxying).
- Storage: `acme.json` on the Traefik PVC (`/letsencrypt`, mode `600` —
  the `fix-acme-perms` init container enforces it).
- Token: Secret `traefik-cloudflare-dns` (key `token`), never committed.
- Migrating an existing setup: copy your current `acme.json` into the PVC
  after install to avoid re-issuing; otherwise Traefik issues fresh certs.

## Observability

- Access log: `/logs/access.log` on its PVC (common format, User-Agent +
  Referer kept) — scrape it with your log pipeline.
- Metrics: Prometheus entrypoint `:8082` (`metrics.prometheus`) — point
  your Prometheus/Grafana at it (not exposed on the LoadBalancer by default).

## Troubleshooting

| Symptom | Likely cause |
|---------|--------------|
| `404` on bare dashboard host `/` | IngressRoute only matches `/dashboard` + `/api`; the `traefik-dashboard-redirect` middleware covers `/` |
| TLS `526` / resolver disabled | `acme.json` permissions (must be `600`) or wrong Cloudflare token |
| App sees Cloudflare IPs, not visitors | Missing `realClientIP` / `TRUSTED_PROXIES` in the app, or SNAT (`externalTrafficPolicy` not `Local`) |
| `403` on allowlisted routes | `externalTrafficPolicy: Cluster` hides the peer IP — set `Local` |
| Infinite SSO redirect | forwardAuth address host ≠ public Authentik host (cookie mismatch) |
| File-provider change ignored | ConfigMap not updated in namespace `traefik`, or Traefik restarted with changed `additionalArguments` (that path needs a rollout) |
| App redirect loop `http://` | App doesn't trust `X-Forwarded-Proto` — set its trusted-proxies / base-URL to the public `https://` host |

## Secrets

Never commit: Cloudflare tokens, `acme.json`, Authentik secrets, filled-in
`my-*-values.yaml`, or per-cluster state. Commit templates only
(`*.example`, placeholder `example.com` hosts).
