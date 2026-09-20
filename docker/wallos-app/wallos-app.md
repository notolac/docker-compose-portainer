# Wallos

Subscription tracker and manager ([upstream](https://wallosapp.com)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `wallos-standalone.yaml` | Compose standalone | `wallos` (bind mounts `./wallos-app/db` + `./logos`) |
| `wallos-swarm.yaml` | Docker Swarm | `wallos` (named volumes `wallos-db` + `wallos-logos`) |

Web UI on `${WALLOS_PORT:-8282}`.

## Deploy

```bash
docker compose -f wallos-standalone.yaml up -d
# or
docker stack deploy -c wallos-swarm.yaml wallos
```

Only setting is `TZ` (default `Europe/Madrid` — adjust to yours).
A K3s variant lives in `k3s/apps/wallos/`.
