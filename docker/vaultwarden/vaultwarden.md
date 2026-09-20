# Vaultwarden

Lightweight Bitwarden-compatible password manager ([upstream](https://github.com/dani-garcia/vaultwarden)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `vaultwarden-standalone.yaml` | Compose standalone | `vaultwarden/server` (bind mount or named volume) |
| `vaultwarden-swarm.yaml` | Docker Swarm | `vaultwarden/server` (named volume + deploy policies) |

A `.env.template` is included — copy to `.env` for CLI deploys (never commit
real values). Web UI on `${VAULTWARDEN_PORT:-8080}`.

## Deploy

```bash
docker compose -f vaultwarden-standalone.yaml up -d
# or
docker stack deploy -c vaultwarden-swarm.yaml vaultwarden
```

## Variables

`DOMAIN` (public URL — required for invites/attachments), SMTP settings,
`ADMIN_TOKEN`, `SIGNUPS_ALLOWED` and related guards — see the YAML headers.
Serve HTTPS in front (reverse proxy) — the container itself speaks HTTP.
A K3s variant lives in `k3s/apps/vaultwarden/`.
