# Wallos @ K3s

Subscription tracker ([upstream](https://wallosapp.com)). Single Deployment +
two PVCs (db + logos), ClusterIP Service, optional Ingress. No Secret needed.

| Item | Value |
|------|-------|
| Namespace | `wallos` |
| Image | `bellamy/wallos:5.8.1` |
| Data | PVCs `wallos-db` + `wallos-logos` (1Gi each) |

## Deploy

```bash
kubectl apply -f k3s/apps/wallos/namespace.yaml
kubectl apply -f k3s/apps/wallos/app.yaml
kubectl apply -f k3s/apps/wallos/ingress.yaml   # after setting your host
```

Adjust `storageClassName` (`ceph-block` by default) and `TZ` as needed.
