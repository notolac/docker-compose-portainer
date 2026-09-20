# Mealie @ K3s

Recipe manager ([upstream](https://mealie.io)). Single Deployment (SQLite) + data PVC,
ClusterIP Service, optional Ingress.

| Item | Value |
|------|-------|
| Namespace | `mealie` |
| Image | `ghcr.io/mealie-recipes/mealie:v3.27.0` |
| Data | PVC `mealie-data` (5Gi) → `/app/data` |
| Secret | `mealie-env` — see `mealie-k3s.env.example` |

## Deploy

```bash
kubectl apply -f k3s/apps/mealie/namespace.yaml
kubectl -n mealie create secret generic mealie-env --from-env-file=k3s/apps/mealie/mealie-k3s.env
kubectl apply -f k3s/apps/mealie/app.yaml
kubectl apply -f k3s/apps/mealie/ingress.yaml   # after setting your host
```

Adjust `storageClassName` (`ceph-block` by default), `TZ`, and keep `BASE_URL`
in sync with your Ingress host. First visit: create the admin account in the UI
(signups are disabled by default afterwards via `ALLOW_SIGNUP=false`).
