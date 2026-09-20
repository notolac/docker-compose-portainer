# LiteLLM @ K3s

Unified OpenAI-compatible LLM proxy ([upstream](https://www.litellm.ai)) with
PostgreSQL (model registry when `STORE_MODEL_IN_DB=True`) and authenticated Redis
(router state, budgets, cache).

| Item | Value |
|------|-------|
| Namespace | `litellm` |
| Image | `ghcr.io/berriai/litellm:v1.101.0` |
| DB | PostgreSQL 16 StatefulSet (`ceph-block`, 10Gi) |
| Cache | Redis 7.4 StatefulSet, auth + AOF (`ceph-block`, 5Gi) |
| Secret | `litellm-env` — see `litellm-k3s.env.example` |

`drop_params: true` in the ConfigMap avoids 400s from providers that reject
unknown OpenAI params. A ConfigMap change needs a pod restart to take effect.

## Deploy

```bash
kubectl apply -f k3s/apps/litellm/namespace.yaml
kubectl -n litellm create secret generic litellm-env --from-env-file=k3s/apps/litellm/litellm-k3s.env
kubectl apply -f k3s/apps/litellm/postgres.yaml
kubectl apply -f k3s/apps/litellm/redis.yaml
kubectl apply -f k3s/apps/litellm/litellm.yaml
kubectl apply -f k3s/apps/litellm/ingress.yaml   # after setting your host
```

Set `PROXY_BASE_URL` in `litellm.yaml` to your public URL and adjust
`storageClassName` (`ceph-block` by default). Models/keys are managed via the
proxy UI or API after deploy.
