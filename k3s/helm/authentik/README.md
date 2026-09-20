# Authentik (K3s SSO)

Identity provider for the cluster. Traefik protects apps and its own
dashboard with Authentik forwardAuth (see
[`../traefik/`](../traefik/) and [`../../docs/ingress-traefik.md`](../../docs/ingress-traefik.md)).

- Chart: `authentik/authentik` (pin a version at install: `helm search repo authentik/authentik`)
- `authentik-values.yaml` — Helm values template (placeholders only, no secrets)
- `secrets.env.example` — local env template for the secrets passed via `--set`

Docker equivalent: [`../../../docker/authentik/`](../../../docker/authentik/).

## Install

```bash
helm repo add authentik https://charts.goauthentik.io
helm repo update

# 1 — secrets (copy locally, fill in, never commit the copy)
cp k3s/helm/authentik/secrets.env.example authentik-secrets.env
set -a && source authentik-secrets.env && set +a

# 2 — install / upgrade (copy values first and set YOUR host + StorageClass)
cp k3s/helm/authentik/authentik-values.yaml my-authentik-values.yaml
helm upgrade --install authentik authentik/authentik \
  -n authentik --create-namespace \
  -f my-authentik-values.yaml \
  --set authentik.secret_key="$AUTHENTIK_SECRET_KEY" \
  --set postgresql.auth.username="$PG_USER" \
  --set postgresql.auth.password="$PG_PASS"

# 3 — expose via Traefik (Ingress with TLS, or file-provider router)
# See ../../docs/ingress-traefik.md. The forwardAuth outpost URL must match
# YOUR Authentik host, otherwise outpost cookies/session break.
```

## After install

1. Open `https://auth.example.com` (YOUR host) and create the admin user.
2. Create a Provider + Application for Traefik forwardAuth
   (Proxy Provider, external host `https://auth.example.com/outpost.goauthentik.io/auth/traefik`).
3. Point the Traefik `authentikForwardAuth` middleware (or `authentik-forwardauth`
   CRD) at YOUR host, then attach it to the routers that need SSO.

## Secrets

Never commit: `authentik-secrets.env`, `secrets.env`, passwords, or the
Authentik secret key. Commit templates only.
