# Homarr @ K3s

Dashboard ([upstream](https://homarr.dev)). Single Deployment + data PVC,
ClusterIP Service, optional Ingress.

| Item | Value |
|------|-------|
| Namespace | `homarr` |
| Image | `ghcr.io/homarr-labs/homarr:v2` |
| Data | PVC `homarr-data` (2Gi) → `/appdata` |
| Secret | `homarr-env` — see `homarr-k3s.env.example` |

## Deploy

```bash
kubectl apply -f k3s/apps/homarr/namespace.yaml
kubectl -n homarr create secret generic homarr-env --from-env-file=k3s/apps/homarr/homarr-k3s.env
kubectl apply -f k3s/apps/homarr/app.yaml
kubectl apply -f k3s/apps/homarr/ingress.yaml   # after setting your host
```

Adjust `storageClassName` (`ceph-block` by default) and the Ingress host first.
