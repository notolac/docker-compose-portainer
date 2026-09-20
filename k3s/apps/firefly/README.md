# Firefly III @ K3s

Personal finance manager ([upstream](https://www.firefly-iii.org)). Core app +
PostgreSQL 16, data importer, and nightly cron job.

| Item | Value |
|------|-------|
| Namespace | `firefly` |
| Images | `fireflyiii/core:version-6.7.3`, `fireflyiii/data-importer:latest` |
| DB | PostgreSQL 16 StatefulSet (`ceph-block`, 5Gi) |
| Data | PVC `firefly-upload` (2Gi) |
| Secrets | `firefly-env` — see `firefly-k3s.env.example` |

Only the core app is exposed (see `ingress.yaml`); the importer stays ClusterIP
internal. `TRUSTED_PROXIES=**` is per Firefly docs when running behind a proxy.

## Deploy

```bash
kubectl apply -f k3s/apps/firefly/namespace.yaml
kubectl -n firefly create secret generic firefly-env --from-env-file=k3s/apps/firefly/firefly-k3s.env
kubectl apply -f k3s/apps/firefly/postgres.yaml
kubectl apply -f k3s/apps/firefly/app.yaml
kubectl apply -f k3s/apps/firefly/importer-cron.yaml
kubectl apply -f k3s/apps/firefly/ingress.yaml   # after setting your host
```

Set `APP_URL` / `SANCTUM_STATEFUL_DOMAINS` in `app.yaml` to your public host and
adjust `storageClassName` (`ceph-block` by default).
