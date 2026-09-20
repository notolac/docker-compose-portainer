# WordPress

CMS with MySQL ([upstream](https://wordpress.org)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `wordpress-standalone.yaml` | Compose standalone | `wordpress` + `mysql` (bind-mount data paths) |
| `wordpress-swarm.yaml` | Docker Swarm | `wordpress` + MySQL (named volumes + deploy policies) |

## Deploy

```bash
docker compose -f wordpress-standalone.yaml up -d
# or
docker stack deploy -c wordpress-swarm.yaml wordpress
```

## Variables

WordPress DB linkage (`WORDPRESS_DB_*` ↔ `MYSQL_*` — keep them consistent),
data paths (`WORDPRESS_DATA_PATH`, `MYSQL_DATA_PATH`), exposed ports
(`WORDPRESS_PORT`, `MYSQL_PORT`). MySQL root uses a random password by default.
