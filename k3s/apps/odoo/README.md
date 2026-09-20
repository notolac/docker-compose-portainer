# Odoo @ K3s

ERP ([upstream](https://www.odoo.com)) with PostgreSQL 16. Single instance with its
own namespace, database, and filestore PVC.

| Item | Value |
|------|-------|
| Namespace | `odoo` |
| Image | `odoo:19` |
| DB | PostgreSQL 16 StatefulSet (`ceph-block`, 10Gi), role `odoo` |
| Data | PVC `odoo-filestore` (10Gi) → `/var/lib/odoo` |
| Secrets | `odoo-config` (rendered `odoo.conf`) + `odoo-db-env` (DB password) |

## Deploy

```bash
kubectl apply -f k3s/apps/odoo/namespace.yaml
# 1. Render odoo.conf from the template with your passwords:
cp k3s/apps/odoo/odoo.conf.template odoo.conf  # keep out of git!
kubectl -n odoo create secret generic odoo-config --from-file=odoo.conf=odoo.conf
kubectl -n odoo create secret generic odoo-db-env --from-literal=POSTGRES_PASSWORD='change-me-db-password'
rm odoo.conf
# 2. Apply:
kubectl apply -f k3s/apps/odoo/postgres.yaml
kubectl apply -f k3s/apps/odoo/app.yaml
kubectl apply -f k3s/apps/odoo/ingress.yaml   # after setting your host
```

First boot: open the host and create the database using the master password
(`admin_passwd`). Adjust `storageClassName` (`ceph-block` by default).
