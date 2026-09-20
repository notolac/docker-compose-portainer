# n8n @ K3s

Workflow automation ([upstream](https://n8n.io)). Deployment with external task-runner
sidecar (needed for Code nodes) + PostgreSQL 16 StatefulSet. Fresh, empty deploy —
no data migration included.

| Item | Value |
|------|-------|
| Namespace | `n8n` |
| Images | `docker.n8n.io/n8nio/n8n:2.39.8` + sidecar `n8nio/runners:2.39.8` |
| DB | PostgreSQL 16 StatefulSet (`ceph-block`, 5Gi) |
| Data | PVC `n8n-data` (5Gi) → `/home/node/.n8n` |
| Secret | `n8n-env` — see `n8n-k3s.env.example` |

**Task runners:** n8n runs `N8N_RUNNERS_MODE=external`; the sidecar connects to
`http://127.0.0.1:5679` with the shared `N8N_RUNNERS_AUTH_TOKEN`.

## Deploy

```bash
kubectl apply -f k3s/apps/n8n/namespace.yaml
kubectl -n n8n create secret generic n8n-env --from-env-file=k3s/apps/n8n/n8n-k3s.env
kubectl apply -f k3s/apps/n8n/postgres.yaml
kubectl apply -f k3s/apps/n8n/app.yaml
kubectl apply -f k3s/apps/n8n/ingress.yaml   # after setting your host
```

Set `N8N_HOST` / `N8N_EDITOR_BASE_URL` / `WEBHOOK_URL` in `app.yaml` to your public
URL and adjust `storageClassName` (`ceph-block` by default). First visit: create the
owner account in the UI.
