# Traefik (K3s ingress)

Standard ingress for everything under [`../../apps/`](../../apps/).
Docker stacks in this repo publish through Nginx Proxy Manager;
on K3s Traefik is the reverse proxy (see [`../../docs/ingress-traefik.md`](../../docs/ingress-traefik.md)).

- Chart: `traefik/traefik` (pin a version at install: `helm search repo traefik/traefik`)
- `traefik-values.yaml` — Helm values template (placeholders only, no secrets)
- `middlewares.yaml` — shared file-provider middlewares (`secureHeaders`, `rateLimit`,
  `cloudflare`, `cloudflareHeaders`, `realClientIP`, `authentikForwardAuth`)
- `dynamic-app-example.yaml` — copy-paste file-provider router for one `*.svc.cluster.local` app
- `whoami.yaml` — test Deployment + Service + Ingress (`whoami.example.com`)
- `middleware-authentik.yaml.example` — optional `Middleware` CRD for Authentik forwardAuth
- `cloudflare-dns-secret.yaml.example` — Secret template for the ACME DNS-01 token

## Prerequisites

- MetalLB (or another `LoadBalancer` implementation) — see
  [`../../configs/metallb/ipaddresspool.yaml.example`](../../configs/metallb/ipaddresspool.yaml.example)
- A `StorageClass` for `acme.json` + access logs (defaults to `ceph-block`;
  change it to yours — see [`../../configs/rook/`](../../configs/rook/))
- Cloudflare API token with DNS-edit scope, stored as a Secret (never committed)

## Install

```bash
helm repo add traefik https://traefik.github.io/charts
helm repo update

# 1 — DNS token Secret (copy the example, fill it locally, never commit it)
kubectl -n traefik create namespace traefik --dry-run=client -o yaml | kubectl apply -f -
kubectl -n traefik create secret generic traefik-cloudflare-dns \
  --from-literal=token='<CLOUDFLARE_DNS_API_TOKEN>'

# 2 — shared middlewares as a file-provider ConfigMap (chart key `traefik-file-provider`)
kubectl -n traefik create configmap traefik-file-provider \
  --from-file=middlewares.yaml \
  --from-file=dynamic-app-example.yaml \
  --dry-run=client -o yaml | kubectl apply -f -

# 3 — install / upgrade (copy values first and set YOUR hosts, IPs, StorageClass)
cp k3s/helm/traefik/traefik-values.yaml my-traefik-values.yaml
helm upgrade --install traefik traefik/traefik \
  -n traefik --create-namespace \
  -f my-traefik-values.yaml

# 4 — smoke test
kubectl apply -f k3s/helm/traefik/whoami.yaml
curl -sk https://whoami.example.com/ | head
```

## Exposing an app (dual model)

1. **Standard `Ingress`** (default) — keep `ingress.yaml` in `k3s/apps/<app>/`,
   set `ingressClassName: traefik`, your host, and TLS. Works with any
   Traefik install; no file provider needed.
2. **File-provider router** (optional, Cloudflare + Authentik patterns) —
   copy `dynamic-app-example.yaml` to `<app>.yaml`, set host/service,
   add it to the `traefik-file-provider` ConfigMap.

Full guide: [`../../docs/ingress-traefik.md`](../../docs/ingress-traefik.md).

## Secrets

Never commit: the Cloudflare token, `acme.json`, or `my-*-values.yaml`
with real hosts. Commit templates only (`*.example`, placeholder hosts).
