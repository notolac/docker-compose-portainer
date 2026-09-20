# Vaultwarden @ K3s

Password manager ([upstream](https://github.com/dani-garcia/vaultwarden)).
Single Deployment + data PVC, ClusterIP Service, optional Ingress.

| Item | Value |
|------|-------|
| Namespace | `vaultwarden` |
| Image | `vaultwarden/server:1.37.3` |
| Data | PVC `vaultwarden-data` (5Gi) → `/data` |
| Secret | `vaultwarden-env` — see `vaultwarden-k3s.env.example` |

Signups default to **closed** here (`SIGNUPS_ALLOWED=false`) — create your account,
then invite users if needed. The source setup allowed verified signups; adjust to taste.

## Deploy

```bash
kubectl apply -f k3s/apps/vaultwarden/namespace.yaml
kubectl -n vaultwarden create secret generic vaultwarden-env --from-env-file=k3s/apps/vaultwarden/vaultwarden-k3s.env
kubectl apply -f k3s/apps/vaultwarden/app.yaml
kubectl apply -f k3s/apps/vaultwarden/ingress.yaml   # after setting your host
```

Set `DOMAIN` in `app.yaml` to your public URL, adjust `storageClassName`
(`ceph-block` by default) and the SMTP values. Serve HTTPS at the ingress —
the pod itself listens on plain HTTP `:80`.
