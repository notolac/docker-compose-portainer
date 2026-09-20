# Homarr

Dashboard for your server/homelab ([upstream](https://homarr.dev)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `homarr-standalone.yaml` | Compose standalone | `homarr` (bind mount `./homarr/data`, optional Docker socket) |
| `homarr-swarm.yaml` | Docker Swarm | `homarr` (named volume `homarr-data`) |

## Deploy

```bash
docker compose -f homarr-standalone.yaml up -d
# or
docker stack deploy -c homarr-swarm.yaml homarr
```

UI on port `7575`.

## Variables

| Variable | Description |
| -------- | ----------- |
| `SECRET_ENCRYPTION_KEY` | Encryption key (**required**) |
| `HOST_IP` | Bind address for the standalone port mapping |
