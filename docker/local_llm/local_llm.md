# local_llm — AI stacks for Docker

Self-hosted AI workloads: **Onyx** (RAG assistant over your documents),
**LiteLLM** (OpenAI-compatible LLM proxy) and **Bifrost** (LLM gateway, concept only).

## Files

| File | Mode | GPU | Use |
| ---- | ---- | --- | --- |
| `onyx-standalone-nvidia.yaml` | Docker Compose | NVIDIA | Single-node Onyx with local GPU model servers + code-interpreter |
| `onyx-standalone-amd.yaml` | Docker Compose | AMD / CPU | Single-node Onyx using host Ollama (ROCm); no model servers |
| `onyx-swarm-nvidia.yaml` | Docker Swarm | NVIDIA | Cluster Onyx with GPU model servers (no code-interpreter) |
| `onyx-swarm-amd.yaml` | Docker Swarm | AMD / CPU | Cluster Onyx using host Ollama; no model servers |
| `litellm-standalone.yaml` | Docker Compose | — | LiteLLM proxy + PostgreSQL on a single node |
| `litellm-swarm.yaml` | Docker Swarm | — | LiteLLM proxy + PostgreSQL in a cluster |
| `bifrost-standalone.yaml` | Docker Compose | — | **Concept only, NOT tested** — reference starting point |

> **Retired:** `proxy-gpt-*.yaml` (Open WebUI + LiteLLM bundles) were removed —
> use `litellm-*.yaml` plus any chat UI you prefer. The upstream `onyx-app.yaml`
> reference copy was also removed; the four `onyx-*` variants above are the source
> of truth. Onyx uses port **3080** by default, LiteLLM uses **4000**.

### Differences between Standalone and Swarm

| Aspect | Standalone | Swarm |
| ------ | ---------- | ----- |
| `restart:` | `always` (native) | `deploy.restart_policy` |
| `depends_on:` | Supported (startup order) | Not supported (ignored) |
| `shm_size:` | Direct in PostgreSQL | tmpfs on `/dev/shm` (workaround) |
| `ulimits:` | Direct in OpenSearch | Not supported (requires host sysctl) |
| `container_name:` | `onyx-<service>` | Assigned by swarm |
| Network | `bridge` | `overlay` |
| Volumes | Direct bind mount | Bind mount with `driver_opts` |
| Default data path | `/opt/onyx` | `/opt/onyx` (on every node that may host the services) |
| High availability | No | Yes (automatic re-schedule) |
| GPU (NVIDIA) | Yes (`onyx-standalone-nvidia.yaml`, `deploy` reservations) | Yes (`onyx-swarm-nvidia.yaml`, `deploy` reservations — pin a GPU node, see below) |
| Code interpreter | Yes, standalone-nvidia only (mounts `docker.sock`) | Not included |

---

## Onyx architecture

| Service | Image | Description |
| ------- | ----- | ----------- |
| `api_server` | `onyxdotapp/onyx-backend` | REST API + Alembic migrations |
| `background` | `onyxdotapp/onyx-backend` | Indexing workers, connectors, supervisord |
| `web_server` | `onyxdotapp/onyx-web-server` | Next.js frontend |
| `inference_model_server` | `onyxdotapp/onyx-model-server` | ML server for inference (nvidia variants only) |
| `indexing_model_server` | `onyxdotapp/onyx-model-server` | ML server for indexing (nvidia variants only) |
| `relational_db` | `postgres:15.2-alpine` | PostgreSQL database |
| `index` | `vespaengine/vespa:8.609.39` | Vespa search engine |
| `opensearch` | `opensearchproject/opensearch:3.4.0` | Full-text search |
| `nginx` | `nginx:1.25.5-alpine` | Reverse proxy (entry point) |
| `cache` | `redis:7.4-alpine` | Ephemeral cache |
| `minio` | `minio/minio` | S3-compatible object storage |
| `code-interpreter` | `onyxdotapp/code-interpreter` | Code execution (**only** standalone-nvidia; needs Docker socket) |

---

## Host requirements

### 1. Kernel parameter for OpenSearch

OpenSearch requires `vm.max_map_count >= 262144`. Run on the host:

```bash
sudo sysctl -w vm.max_map_count=262144
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

> For Swarm, run on **every node** that may host these services.

### 2. Minimum recommended resources

- **RAM:** 16 GB minimum (OpenSearch takes 3–5 GB; Vespa and model servers too)
- **Disk:** 40 GB free for data, models and indexes
- **CPU:** 4+ cores recommended

### 3. GPU

- **NVIDIA variants:** proprietary NVIDIA driver + `nvidia-container-toolkit`.
  Verify first: `docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi`.
  In Swarm, label a GPU node (`docker node update --label-add gpu=nvidia <node>`)
  and add `- node.labels.gpu == nvidia` to the model servers' placement constraints.
- **AMD variants:** AMD GPU with ROCm + **Ollama on the host** listening on port
  11434 (`ollama pull llama3.2` for chat, `ollama pull nomic-embed-text` for RAG
  embeddings). Containers reach it via `http://host.docker.internal:11434`.
  In Swarm, run Ollama on the manager (api/background are manager-constrained).

---

## Pre-deploy

### Step 1: Create data directories

**Standalone NVIDIA:**

```bash
mkdir -p /opt/onyx/{postgres-data,vespa-data,opensearch-data,minio-data,file-system,nginx-templates,model-cache-hf,indexing-model-cache-hf}
mkdir -p /opt/onyx/logs/{api-server,background,inference-model-server,indexing-model-server}
sudo chown -R $(id -u):$(id -g) /opt/onyx
```

**Standalone AMD** (no HuggingFace caches, no model-server logs):

```bash
mkdir -p /opt/onyx/{postgres-data,vespa-data,opensearch-data,minio-data,file-system,nginx-templates}
mkdir -p /opt/onyx/logs/{api-server,background}
sudo chown -R $(id -u):$(id -g) /opt/onyx
```

**Swarm** (shared storage, same layout as your variant; AMD omits model caches):

```bash
sudo mkdir -p /opt/onyx/{postgres-data,vespa-data,opensearch-data,minio-data,file-system,nginx-templates,model-cache-hf,indexing-model-cache-hf}
sudo mkdir -p /opt/onyx/logs/{api-server,background,inference-model-server,indexing-model-server}
sudo chown -R 1000:1000 /opt/onyx
```

> If you use a different path, set `ONYX_DATA_PATH` when deploying.

**LiteLLM:**

```bash
# Standalone
mkdir -p /opt/litellm/litellm-db
sudo chown -R $(id -u):$(id -g) /opt/litellm

# Swarm (on the manager)
sudo mkdir -p /opt/litellm/litellm-db
sudo chown -R 1000:1000 /opt/litellm
```

### Step 2: Download the Onyx nginx config files

Onyx needs custom nginx configs from the official repository:

```bash
cd /opt/onyx/nginx-templates
curl -LO https://raw.githubusercontent.com/onyx-dot-app/onyx/main/deployment/data/nginx/app.conf.template
curl -LO https://raw.githubusercontent.com/onyx-dot-app/onyx/main/deployment/data/nginx/run-nginx.sh
chmod +x run-nginx.sh
```

Verify both files exist and are valid (`head -n 1` should not print `404: Not Found`).
Fallback: `git clone --depth 1 https://github.com/onyx-dot-app/onyx.git /tmp/onyx-repo`
and copy `/tmp/onyx-repo/deployment/data/nginx/*` over.

### Step 3: Generate credentials

**PostgreSQL (`POSTGRES_PASSWORD`):**

```bash
openssl rand -hex 16
```

**OpenSearch (`OPENSEARCH_ADMIN_PASSWORD`):**

OpenSearch 3.x requires a password with at least one uppercase, one lowercase,
one digit and one **special character** — plain `openssl rand -hex` output is
rejected. Generate one with Python:

```bash
python3 <<'PY'
import secrets, string as s
chars = s.ascii_letters + s.digits + "!@#$%^&*"
print("".join(secrets.choice(chars) for _ in range(24)))
PY
```

If you skip the variable, the compose files default to `StrongPassword123!`
(testing only).

**LiteLLM (`LITELLM_MASTER_KEY`, `LITELLM_SALT_KEY`):**

```bash
echo "sk-$(openssl rand -hex 24)"
echo "sk-$(openssl rand -hex 24)"
```

Then set `DATABASE_URL=postgresql://<user>:<password>@db:5432/<db>` so it matches
your `POSTGRES_*` values exactly.

---

## Deploying Onyx

Pick your variant file. In Portainer: **Stacks → Add stack**, upload/paste the file,
set environment variables (**no quotes** around values), Deploy. CLI commands below.

**Standalone NVIDIA** (`onyx-standalone-nvidia.yaml`):

```bash
POSTGRES_USER=onyx POSTGRES_PASSWORD=<generated> \
docker compose -f onyx-standalone-nvidia.yaml up -d
```

**Standalone AMD** (`onyx-standalone-amd.yaml`): same command with its file. After
deploy, configure models in Onyx Admin → Language Models → Ollama
(`http://host.docker.internal:11434`), plus Search/Embeddings → Ollama provider.

**Swarm NVIDIA** (`onyx-swarm-nvidia.yaml`):

```bash
POSTGRES_USER=onyx POSTGRES_PASSWORD=<generated> \
docker stack deploy -c onyx-swarm-nvidia.yaml onyx
```

**Swarm AMD** (`onyx-swarm-amd.yaml`): same command with its file; Ollama must run
on the manager host.

Required variables: `POSTGRES_USER`, `POSTGRES_PASSWORD`. Optional:
`OPENSEARCH_ADMIN_PASSWORD` (see Step 3), `IMAGE_TAG`, `ONYX_PORT` (default 3080),
`AUTH_TYPE` (default basic), `POSTGRES_DB`, `ONYX_DATA_PATH`.

Wait 3–5 minutes on first boot (model servers download models). Open
`http://<HOST_IP>:3080` and create the admin account (with `AUTH_TYPE=basic`).

### GPU (NVIDIA) validation

```bash
docker exec onyx-inference-model-server nvidia-smi
docker exec onyx-indexing-model-server nvidia-smi
```

If both show your GPU, passthrough works. `could not select device driver` means
the containers run on CPU — check the toolkit and Docker runtime.

### Code interpreter (standalone-nvidia only; security implications)

The `code-interpreter` service mounts the host Docker socket (`DOCKER_SOCK_PATH`,
default `/var/run/docker.sock`) — upstream docker-out-of-docker behavior that can
spawn containers on the same daemon. Treat it as highly sensitive: strong auth,
trusted users only, and consider removing the service (plus `CODE_INTERPRETER_BASE_URL`
and its `depends_on` entry) on Internet-exposed deployments. Swarm variants
**exclude** it (socket mounts in Swarm are especially problematic).

```bash
docker logs onyx-code-interpreter -f
```

### SMTP and email invites

The backend counts email as "configured" with **SMTP** (`SMTP_SERVER`, `SMTP_USER`,
`SMTP_PASS`) **or** `SENDGRID_API_KEY`. Set `USER_AUTH_SECRET`
(`openssl rand -hex 32`), `WEB_DOMAIN` (public URL for links in emails),
`ENABLE_EMAIL_INVITES=true`, optionally `REQUIRE_EMAIL_VERIFICATION=true`.
Upstream docs: [Basic Auth](https://docs.onyx.app/deployment/authentication/basic).

### Full Onyx variable reference

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` | *(required)* | PostgreSQL credentials |
| `IMAGE_TAG` | `latest` | Onyx image tag |
| `ONYX_PORT` | `3080` | External UI port |
| `AUTH_TYPE` | `basic` | `basic`, `google_oauth`, `oidc`, `saml`, `disabled` |
| `POSTGRES_DB` | `onyx_db` | Database name |
| `ONYX_DATA_PATH` | `/opt/onyx` | Base path for persistent data |
| `OPENSEARCH_ADMIN_PASSWORD` | `StrongPassword123!` | Must meet OpenSearch 3.x policy if customized |
| `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` | `minioadmin` | MinIO admin |
| `DISABLE_MODEL_SERVER` | *(empty)* | Set `True` to skip model servers (AMD variants set it already) |
| `DOMAIN` | `localhost` | Domain for nginx |
| `CODE_INTERPRETER_BASE_URL` | `http://code-interpreter:8000` | Internal interpreter URL |
| `CODE_INTERPRETER_IMAGE_TAG` | `latest` | Interpreter image tag |
| `DOCKER_SOCK_PATH` | `/var/run/docker.sock` | Host Docker socket (rootless: point at the real socket) |
| `USER_AUTH_SECRET` | *(empty)* | Token secret for verification/reset emails |
| `WEB_DOMAIN` | *(empty)* | Public Onyx URL for email links |
| `SMTP_SERVER` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASS` | *(empty)* | SMTP for invites and system mail |
| `EMAIL_FROM` | `SMTP_USER` | Sender address |
| `SENDGRID_API_KEY` | *(empty)* | SMTP alternative |
| `ENABLE_EMAIL_INVITES` | *(empty)* | `true` to send invite emails |
| `REQUIRE_EMAIL_VERIFICATION` | *(empty)* | `true` to require email verification (basic auth) |

The MCP server stays commented out (upstream default); a future version may enable it.

---

## Deploying LiteLLM

**Standalone** (`litellm-standalone.yaml`):

```bash
docker compose -f litellm-standalone.yaml up -d
```

**Swarm** (`litellm-swarm.yaml`):

```bash
docker stack deploy -c litellm-swarm.yaml litellm
```

Set `DATABASE_URL`, `LITELLM_MASTER_KEY`, `LITELLM_SALT_KEY`, `POSTGRES_DB`,
`POSTGRES_USER`, `POSTGRES_PASSWORD` (no quotes in Portainer). The proxy listens
on `:4000`; manage models/keys via its UI or API. Swarm supports Docker Secrets
instead of env vars — see the commented blocks in `litellm-swarm.yaml`.

---

## Bifrost (concept only)

`bifrost-standalone.yaml` runs [Bifrost](https://docs.getbifrost.ai) as a local HTTP
API gateway (Web UI + OpenAI-compatible API on `:8080`, data in `/opt/bifrost`).
It is included as an **untested reference starting point** — validate it on your
own host before any serious use:

```bash
mkdir -p /opt/bifrost && sudo chown -R $(id -u):$(id -g) /opt/bifrost
docker compose -f bifrost-standalone.yaml up -d
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4o-mini", "messages": [{"role": "user", "content": "Hello, Bifrost!"}]}'
```

---

## Troubleshooting

**Service status and logs:**

```bash
# Standalone
docker compose -f <file>.yaml ps
docker logs onyx-api-server -f

# Swarm
docker stack services onyx
docker service logs onyx_api_server -f
```

**Common issues:**

1. **OpenSearch won't start** (`vm.max_map_count too low`) → apply the sysctl from
   Host requirements §1 (on every Swarm node).
2. **OpenSearch rejects the password** → it must contain upper + lower + digit +
   special char; regenerate as in Step 3 or drop the variable (test default).
3. **Nginx 502** → api/web still booting; wait and check their logs.
4. **api_server DB errors** → check `relational_db` logs; Alembic creates the DB.
5. **Model servers slow on first boot** → downloading ~1–2 GB from HuggingFace;
   cached in `model-cache-hf` / `indexing-model-cache-hf`.
6. **Volume permissions** → standalone: `chown -R $(id -u):$(id -g) /opt/onyx`;
   swarm: `chown -R 1000:1000 /opt/onyx`.
7. **LiteLLM "URL must start with postgresql://"** → remove quotes from
   `DATABASE_URL` in Portainer; verify it matches `POSTGRES_*`.

## Removing a stack

```bash
# Standalone
docker compose -f <file>.yaml down
rm -rf /opt/onyx   # optional: delete persistent data

# Swarm
docker stack rm onyx   # or litellm
sudo rm -rf /opt/onyx  # optional
```
