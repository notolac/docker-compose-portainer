# AGENTS — LLM only

**Last modified:** 2026-09-20

Human intro + repo map: [README.md](README.md).
Service catalog: [STACKS.md](STACKS.md).
K3s layout + conventions: [k3s/README.md](k3s/README.md).

---

## RULES (this file)

- **RULE:** Show **last modified** date at top; bump when you change this file.
- **RULE:** Write **English** only here.
- **RULE:** Keep this file concise; prefer links over copied tables.
- **RULE:** **Destructive** stuff = stop, warn user, need **explicit yes** before run.
- **RULE:** Point to other docs with **real links**; do not copy big tables here.
- **RULE:** This is a **public** repo. **Never** commit hostnames, internal IPs,
  personal paths, real domains, passwords, API keys, or kubeconfigs.
  If a source file contains any of those, sanitize to variables/placeholders first.
- **RULE:** Human docs may be **Spanish** elsewhere; this file stays **English**.
  Match the language of the file you edit.
- **RULE:** Do **not** invent paths, IPs, or commands. Prefer links to source-of-truth docs.
- **RULE:** Docker stacks here are deployed via **Portainer or the Docker CLI**.
  Do not assume a private orchestrator, SSH access, or auto-redeploy webhooks exist.

---

## What this repo is (real)

Public, shareable infra manifests. **Not** an app codebase with a build/test pipeline.

Main layout:

| Tree | Role |
|------|------|
| [`docker/`](docker/) | Docker Compose / Swarm stacks — one folder per service |
| [`k3s/`](k3s/) | Generic K3s manifests — `apps/<app>/`, `helm/`, `scripts/`, `docs/`, `configs/` |
| [`STACKS.md`](STACKS.md) | Service catalog (variants + links) |

No root CI yet. No top-level Makefile/package manager project.

---

## Source of truth map (use this first)

| Need | Read |
|------|------|
| Repo layout + operator summary | [README.md](README.md) |
| Service catalog (standalone vs Swarm) | [STACKS.md](STACKS.md) |
| K3s layout + per-app conventions | [k3s/README.md](k3s/README.md) |
| K3s apps + Helm values | [k3s/apps/README.md](k3s/apps/README.md) · [k3s/helm/README.md](k3s/helm/README.md) |
| Docker deploy (Portainer + CLI) | [README.md](README.md) (`Deploying a stack`) |
| Docker install (Ubuntu / Debian) | [README.md](README.md) (`Installing Docker`) |
| Portainer versions (2.45 LTS vs 3.x) | [README.md](README.md) (`Installing Portainer`) · [3.0 announcement](https://www.portainer.io/blog/portainer-3-0-is-coming) |
| Portainer API (agents/automation) | [API docs (EE 2.45.1)](https://api-docs.portainer.io/?edition=ee&version=2.45.1) |

---

## Layout conventions

### Docker (`docker/<service>/`)

`*.yaml` (Compose or `*-swarm.yaml`) · optional `.env.example` · optional `README.md`

### K3s (`k3s/apps/<app>/`)

`README.md` · `namespace.yaml` · `app.yaml` (+ `postgres.yaml`, `ingress.yaml`, … when needed) ·
optional `*.env.example`. Details: [k3s/README.md](k3s/README.md).

### Shared rules (both trees)

- **No hardcoded user home paths** — `${APP_DATA_PATH:-/opt/appname}`
- **No internal IPs or personal domains** — `${SERVICE_URL:-http://service-host:port}` /
  `example.com` placeholders
- **Secrets via env vars** — set in Portainer or a local `.env` (gitignored);
  K3s secrets via Secret references, never committed values
- **Neutral storage defaults** — `/opt/<service>/…`, named volumes, or a documented
  `StorageClass` for K3s
- **Comments document variables** — each manifest header lists required env vars / values
- Naming: existing Docker folders keep their names (e.g. `firefly-III`,
  `linkding_app`, `local_llm`); new K3s apps use lowercase-hyphen names

---

## Essential commands

Run from **repo root** unless noted.

### Docker

```bash
# Validate Compose syntax (needs Docker + Compose plugin)
docker compose -f docker/<service>/<file>.yaml config

# Lint shell helpers
bash -n docker/<service>/*.sh
```

### K3s

```bash
# Dry-run manifests when kube available
kubectl apply --dry-run=client -k k3s/apps/<app>/

# Render Helm values when applicable
helm template <release> <chart> -f k3s/helm/<app>-values.yaml
```

### Practical checks (no global test suite)

- `bash -n <script>` for every shell script touched
- `docker compose -f <file> config` for Compose files
- `kubectl apply --dry-run=client` / `helm template` for K3s manifests
- Never commit output logs; keep `logs/` out of git unless a `.gitkeep` requires it

---

## Secrets / gitignore (do not commit)

Never commit: `.env`, `.env.local`, `*-k3s.env`, `*.kubeconfig` / `kubeconfig*.yaml`,
real passwords, API keys, tokens, personal domains, or per-cluster state.

Commit instead: `.env.example` / `.env.template` / `*-values.yaml` with placeholders,
documented in the manifest header.

---

## Destructive operations policy

Need **explicit user yes** before:

- Deleting volumes, PVCs / PVs, or cluster storage
- Resetting or draining a cluster / node
- Changing ingress, VIP, DNS, or firewall rules
- Force-pushing, rewriting history, or deleting branches/tags
- Committing anything that could leak personal infrastructure details

Env gates (`*_YES=yes`) are **not** a substitute for user approval on destructive work.

---

## If you update this file later

- Keep English.
- Stay concise; prefer links over long tables.
- Bump date line.
- Only document observed facts — never personal data.
