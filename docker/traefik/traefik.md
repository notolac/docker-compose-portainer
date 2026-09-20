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
- A K3s-oriented Traefik setup is out of scope here; see `k3s/` for the app
  manifests this proxy would front.
