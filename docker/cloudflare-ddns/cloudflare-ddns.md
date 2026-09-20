# Cloudflare DDNS

Keeps a Cloudflare DNS record in sync with your dynamic IP ([upstream](https://github.com/oznu/docker-cloudflare-ddns)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `cloudflare-ddns.yaml` | Compose standalone | `oznu/cloudflare-ddns` |

## Deploy

```bash
docker compose -f cloudflare-ddns.yaml up -d
```

## Variables

| Variable | Description |
| -------- | ----------- |
| `API_KEY` | Cloudflare API key/token (**required**) |
| `ZONE` | Zone, e.g. `domain.com` |
| `SUBDOMAIN` | Record to update, e.g. `sub.domain.com` |
| `PROXIED` | `true`/`false` (CDN proxying) |
