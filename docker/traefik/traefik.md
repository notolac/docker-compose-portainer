# Traefik + observability

Reverse proxy ([upstream](https://traefik.io)) bundled with log/metrics tooling:
GoAccess dashboards, Loki + Alloy log pipeline, and a `whoami` test service.

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `traefik.yaml` | Compose standalone | `traefik:v3.7.0` (`:80`/`:443`), `goaccess`, `loki`, `alloy`, `whoami` |

## Deploy

```bash
docker compose -f traefik.yaml up -d
```

## Notes

- Let's Encrypt via Cloudflare DNS challenge (`cloudflare` certresolver) — set your
  API credentials and adapt `traefik.http.routers.*` labels to your domains.
- Dynamic config comes from a file provider (`/etc/traefik/dynamic`) — mount your
  own routers/middlewares there.
- The K3s counterpart lives in [`../../k3s/helm/traefik/`](../../k3s/helm/traefik/):
  Helm values, shared middlewares, and the publishing guide
  (`k3s/docs/ingress-traefik.md`). Docker publishes via NPM labels here;
  K3s publishes via Traefik Ingress/file-provider routers there.
