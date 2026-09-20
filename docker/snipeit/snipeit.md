# Snipe-IT

IT asset management ([upstream](https://snipeitapp.com)) with MySQL/MariaDB.

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `snipeit-standalone.yaml` | Compose standalone | `snipe/snipe-it:v8.3.5` + `mariadb:11.5.2` |
| `snipeit-swarm.yaml` | Docker Swarm | Same stack (v8.4.0) with named volumes + deploy policies |

An `.env.example` template is included — copy to `.env` for CLI deploys (never
commit real values).

## Deploy

```bash
docker compose -f snipeit-standalone.yaml up -d
# or
docker stack deploy -c snipeit-swarm.yaml snipeit
```

Web UI on `${APP_PORT:-8080}`.

## Variables

`APP_KEY` (generate one), `APP_URL` (public URL), `APP_TIMEZONE`, DB credentials,
mail settings — see the YAML headers and `.env.example`.
