# Authentik

Identity provider / SSO (OAuth2, SAML, LDAP, forward-auth) ([upstream](https://goauthentik.io)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `authentik.yaml` | Compose standalone | `postgresql:16-alpine`, `redis:alpine`, `server` + `worker` (`ghcr.io/goauthentik/server`) |

## Deploy

```bash
docker compose -f authentik.yaml up -d
```

Via Portainer: Stacks → Add stack → paste the YAML → set variables → Deploy.

## Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `PG_PASS` | *(required)* | PostgreSQL password |
| `PG_DB` / `PG_USER` | `authentik` | Database name / user |
| `AUTHENTIK_DIR` | — | Host path for the database volume (required) |
| `AUTHENTIK_TAG` | `2026.2.1` | Server image tag |

See the YAML header for the full variable list (ports, secret key, error reporting).
