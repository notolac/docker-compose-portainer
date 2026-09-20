# PhotoPrism

AI-powered photo management ([upstream](https://photoprism.app)) with MariaDB.

## Contents

| File | Mode | GPU | Services |
| ---- | ---- | --- | -------- |
| `Photoprisma.yaml` | Compose standalone | NVIDIA (default) | `photoprism` + `mariadb:11` |
| `Photoprisma-amd.yaml` | Compose standalone | AMD / CPU | Same stack without NVIDIA runtime |

## Deploy

```bash
docker compose -f Photoprisma.yaml up -d
# or, without NVIDIA:
docker compose -f Photoprisma-amd.yaml up -d
```

## Variables

`PHOTOPRISM_IP`/`PHOTOPRISM_PORT`, initial admin `PHOTOPRISM_ADMIN_USER`/
`PHOTOPRISM_ADMIN_PASSWORD`, and persistent paths (`ORIGINALS`/`IMPORT`/`STORAGE`/
`DB_DATA`) — full list with examples in each YAML header.
