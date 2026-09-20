# Onyx @ K3s

RAG assistant — chats over your documents ([upstream](https://www.onyx.app)).
Native manifests (no Helm chart): api + background + web + nginx gateway, backed by
PostgreSQL, Vespa, OpenSearch, MinIO, Redis, GPU model servers, and an optional
Kubernetes code interpreter. Heavy stack — check the requirements first.

| Item | Value |
|------|-------|
| Namespace | `onyx` (+ `onyx-sandbox` for the code interpreter) |
| Images | `onyxdotapp/onyx-backend`, `onyx-web-server`, `onyx-model-server` tag **`v4.7.7`** |
| DB | PostgreSQL 15.2 StatefulSet (`ceph-block`, 5Gi, `max_connections=250`) |
| Index | Vespa `8.609.39` (15Gi) + OpenSearch `3.4.0` single-node (10Gi) |
| Files | MinIO + PVC `onyx-file-system` (5Gi) |
| Cache | Ephemeral Redis (no persistence) |
| GPU | `model-server` Deployment (inference `:9000` + indexing `:9001`) needs **one NVIDIA GPU** node (`runtimeClassName: nvidia`, `nodeSelector: gpu: nvidia`) — see `k3s/configs/nvidia-device-plugin/` |
| Secrets | `onyx-env` — see `onyx-k3s.env.example` |

Alembic migrations run at `api-server` startup. Change the default MinIO
credentials for anything beyond a local test.

## Deploy (order matters)

```bash
kubectl apply -f k3s/apps/onyx/namespace.yaml
kubectl -n onyx create secret generic onyx-env --from-env-file=k3s/apps/onyx/onyx-k3s.env
kubectl apply -f k3s/apps/onyx/configmap.yaml
kubectl create configmap onyx-nginx-templates -n onyx \
  --from-file=k3s/apps/onyx/nginx/app.conf.template \
  --from-file=k3s/apps/onyx/nginx/run-nginx.sh
kubectl apply -f k3s/apps/onyx/files.yaml
kubectl apply -f k3s/apps/onyx/postgres.yaml
kubectl apply -f k3s/apps/onyx/redis.yaml
kubectl apply -f k3s/apps/onyx/minio.yaml
kubectl apply -f k3s/apps/onyx/opensearch.yaml
kubectl apply -f k3s/apps/onyx/vespa.yaml
kubectl apply -f k3s/apps/onyx/model-server.yaml   # needs the GPU node
kubectl apply -f k3s/apps/onyx/app.yaml
kubectl apply -f k3s/apps/onyx/code-interpreter.yaml   # optional
kubectl apply -f k3s/apps/onyx/ingress.yaml   # after setting your host
```

Set `WEB_DOMAIN` / `DOMAIN` / `VALID_EMAIL_DOMAINS` in `configmap.yaml` to your
host, and adjust `storageClassName` (`ceph-block` by default).

Python in chat: `CODE_INTERPRETER_BASE_URL=http://code-interpreter:8000`. The API
spawns single-use pods in `onyx-sandbox` (RBAC-scoped, quota + NetworkPolicy
locked down, periodic GC CronJob). No Docker socket, no privileged containers.

## Files

| File | Role |
|------|------|
| `namespace.yaml` `configmap.yaml` `files.yaml` | NS, non-secret env, shared files PVC |
| `postgres.yaml` `redis.yaml` `vespa.yaml` `opensearch.yaml` `minio.yaml` | Data layer |
| `model-server.yaml` | GPU inference + indexing (one pod, two containers) |
| `app.yaml` | api / background / web / nginx |
| `code-interpreter.yaml` | Sandbox API + RBAC + GC (optional) |
| `nginx/` | Gateway templates (mounted as `onyx-nginx-templates` ConfigMap) |
| `onyx-k3s.env.example` | Secret template (real `onyx-k3s.env` gitignored) |
