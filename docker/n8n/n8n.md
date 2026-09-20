# n8n

Workflow automation ([upstream](https://n8n.io)). This variant is wired for Traefik
(TLS termination) with an external task-runner for Code nodes.

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `n8n.yaml` | Compose standalone | `n8n` + `n8n-runner` sidecar on the external `traefik-stack` network |

## Deploy

```bash
docker compose -f n8n.yaml up -d
```

Requires an existing external `traefik-stack` network and Traefik with a matching
`secureHeaders@file` middleware and `cloudflare` certresolver — adapt the labels
to your own Traefik setup.

## Variables

`N8N_HOST` (public domain), `WEBHOOK_URL`, `N8N_PORT`, `GENERIC_TIMEZONE`/`TZ`,
`N8N_RUNNERS_AUTH_TOKEN`, DB settings — see the YAML header. A K3s variant lives
in `k3s/apps/n8n/`.
