# Odoo

ERP / business apps ([upstream](https://www.odoo.com)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `odoo.yaml` | Compose standalone | `odoo` + `postgres:15` (named volumes, config/addons under `${ODOO_DATA_ROOT}`) |

## Deploy

```bash
docker compose -f odoo.yaml up -d
```

Web UI on `${ODOO_PORT:-8077}` (→ container `:8069`).

## Variables

`ODOO_DATA_ROOT` (default `/opt/odoo`), `USER`/`PASSWORD` (Odoo↔DB), `POSTGRES_USER`/
`POSTGRES_PASSWORD`. A K3s variant lives in `k3s/apps/odoo/`.
