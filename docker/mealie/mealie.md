# Mealie

Recipe manager and meal planner ([upstream](https://mealie.io)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `mealie-standalone.yaml` | Compose standalone | `mealie` v3.12.0 (bind mount data dir) |
| `mealie-swarm.yaml` | Docker Swarm | `mealie` v3.5.0 (named volume) |

Web UI on port `9925` in both variants.

## Deploy

```bash
docker compose -f mealie-standalone.yaml up -d
# or
docker stack deploy -c mealie-swarm.yaml mealie
```

## Variables

`MEALIE_DATA_DIR`, `MEALIE_PUID`/`MEALIE_PGID`, `BASE_URL`, `ALLOW_SIGNUP`, plus
SMTP/OpenAI options — see the YAML headers. A K3s variant lives in `k3s/apps/mealie/`.
