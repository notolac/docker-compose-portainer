# K3s

Generic, shareable **K3s / Kubernetes manifests** for the same services that live under [`../docker/`](../docker/).

This tree is the counterpart to `docker/`: one orchestrator per top-level folder,
one folder per service inside each of them.

> **Status:** 10 apps ported as generic, reusable manifests (see [`apps/README.md`](apps/README.md)).
> Each one was sanitized: no personal hosts, IPs, secrets, or node names.

## Layout

```text
k3s/
├── README.md          ← This file
├── apps/              ← Per-app manifests: k3s/apps/<app>/
├── helm/              ← Helm values / chart references
├── scripts/           ← Helper scripts (install, validate, sync)
├── docs/              ← K3s-only guides
└── configs/           ← Shared, non-secret configuration
```

### Per-app layout (`k3s/apps/<app>/`)

```text
k3s/apps/<app>/
├── README.md          ← What it deploys, required values/secrets
├── namespace.yaml     ← Namespace definition
├── app.yaml           ← Deployment + Service (split further when large)
├── postgres.yaml      ← Optional bundled DB (prefer external/managed when possible)
├── ingress.yaml       ← Optional Ingress / HTTPRoute (neutral hostnames only)
└── *.env.example      ← Optional template — never real secrets
```

Bigger apps split manifests by component (`namespace.yaml`, `postgres.yaml`,
`app.yaml`, `ingress.yaml`, …) instead of one giant file.

## Conventions (same spirit as `docker/`)

| Rule | Example |
|------|---------|
| **No hardcoded nodes, IPs, or host paths** | Use `storageClassName` + variables, never a personal `/srv/...` path |
| **No personal hostnames or domains** | `example.com` / placeholder hosts only |
| **Secrets via env vars / Sealed Secrets template** | Commit `*.env.example`, never `*.env` or real tokens |
| **Neutral storage defaults** | Document the expected `StorageClass`; default to a widely available one |
| **Comments document variables** | Each manifest header lists required values and secrets |
| **One concern per file** | Namespace, app, DB, ingress, and PVCs stay in separate files |

See the repo-wide rules in [`../AGENTS.md`](../AGENTS.md) and the Docker conventions in
[`../README.md`](../README.md).

## Deploying (generic)

```bash
# Dry-run first
kubectl apply --dry-run=client -k k3s/apps/<app>/

# Then apply for real
kubectl apply -k k3s/apps/<app>/
```

With Helm:

```bash
helm upgrade --install <release> <chart> -f k3s/helm/<app>-values.yaml
```

Copy any `*.env.example` to your own secret management — never commit real values
(see [`.gitignore`](../.gitignore)).

## Adding a new app here

1. Create `k3s/apps/<app>/` following the per-app layout above.
2. Keep hostnames, IPs, and storage personalizations out — use variables/placeholders.
3. Add a short `README.md` inside the app folder (what, requirements, how to deploy).
4. Link it from [`../STACKS.md`](../STACKS.md) once it is usable.
5. Validate with `kubectl apply --dry-run=client` / `helm template` before opening a PR.
