# Uptime Kuma

Uptime monitoring with notifications ([upstream](https://uptime.kuma.pet)). This
variant is pre-wired for Traefik (router + TLS labels).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `uptime-kuma.yaml` | Compose standalone | `uptime-kuma:2.2.1` (data in `${UPTIME_KUMA_DIR}`, no published ports by default) |

## Deploy

```bash
docker compose -f uptime-kuma.yaml up -d
```

Requires the external `traefik-stack` network and your own `UPTIME_KUMA_DOMAIN`,
`cloudflare` certresolver and `secureHeaders@file` middleware — adapt the labels
(uncomment the `ports:` block for direct `IP:port` access instead).

## Variables

| Variable | Description |
| -------- | ----------- |
| `UPTIME_KUMA_DIR` | Host path for `/app/data` |
| `UPTIME_KUMA_DOMAIN` | Public domain for the Traefik router |
| `UPTIME_KUMA_HOST_PORT` | Local port (only if you enable `ports:`) |
