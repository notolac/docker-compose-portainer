# Linkding @ K3s

Bookmark manager ([upstream](https://linkding.link)). Single Deployment + data PVC,
ClusterIP Service, optional Ingress.

| Item | Value |
|------|-------|
| Namespace | `linkding` |
| Image | `sissbruecker/linkding:1.47.0` |
| Data | PVC `linkding-data` (2Gi) → `/etc/linkding/data` |

## Deploy

```bash
kubectl apply -f k3s/apps/linkding/namespace.yaml
kubectl apply -f k3s/apps/linkding/app.yaml
kubectl apply -f k3s/apps/linkding/ingress.yaml   # after setting your host
```

Set `LD_CSRF_TRUSTED_ORIGINS` in `app.yaml` to your public URL, and adjust
`storageClassName` (`ceph-block` by default). Optional superuser bootstrap via
`linkding-k3s.env.example`.
