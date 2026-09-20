# Firefly III

Personal finance manager ([upstream](https://www.firefly-iii.org)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `fireflyiii-standalone.yaml` | Compose standalone | App + PostgreSQL + data importer + cron (env vars in Portainer) |
| `fireflyiii-swarm.yaml` | Docker Swarm | Same stack using Docker **secrets** instead of env vars |

## Deploy

```bash
# Standalone
docker compose -f fireflyiii-standalone.yaml up -d

# Swarm (create the secrets first — see the YAML header for the exact list)
docker stack deploy -c fireflyiii-swarm.yaml firefly
```

## Variables (standalone)

`SITE_OWNER`, `APP_KEY` (`openssl rand -hex 16`), `DB_DATABASE` / `DB_USERNAME` /
`DB_PASSWORD` (+ matching `POSTGRES_*`), mail settings, `STATIC_CRON_TOKEN`.
The swarm variant takes the same values as Docker secrets (`fireflyiii_*`).
