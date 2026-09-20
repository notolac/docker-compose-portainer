# Coolify

Self-hosted PaaS for deploying apps, databases and services from Git ([upstream](https://coolify.io)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `coolify.yaml` | Compose standalone | `coolify` + `postgres:15` + `redis:7` + `soketi` (realtime) |

## Deploy

```bash
docker compose -f coolify.yaml up -d
```

Coolify expects its data under `/home/coolify/...` bind mounts (see the YAML) —
adjust them if your host uses different paths.

## Variables

Key ones (see the YAML header for the full list): `APP_ENV`, `PHP_MEMORY_LIMIT`,
`REGISTRY_URL` / `LATEST_IMAGE` (image pins).
