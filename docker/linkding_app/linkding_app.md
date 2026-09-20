# Linkding

Bookmark manager ([upstream](https://linkding.link)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `linkding-standalone.yaml` | Compose standalone | `linkding` (bind mount data dir) |
| `linkding-swarm.yaml` | Docker Swarm | `linkding` (named volume) |

## Deploy

```bash
docker compose -f linkding-standalone.yaml up -d
# or
docker stack deploy -c linkding-swarm.yaml linkding
```

## Variables

`LINKDING_CONTAINER_NAME`, `LINKDING_IP`/`LINKDING_PORT`, `LINKDING_DATA_PATH`,
`LINKDING_CONTEXT_PATH` (subpath hosting), plus first-boot admin
`LINKDING_SUPERUSER_NAME`/`LINKDING_SUPERUSER_PASSWORD`. Full list with examples
in each YAML header. A K3s variant lives in `k3s/apps/linkding/`.
