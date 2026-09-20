# Semaphore

Ansible UI for running playbooks from the browser ([upstream](https://www.semaphoreui.com)).
Includes an MCP service for AI-assisted playbook work.

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `semaphore.yaml` | Compose standalone | `mysql:8.0`, `semaphoreui/semaphore`, `semaphore-mcp` |

## Deploy

```bash
docker compose -f semaphore.yaml up -d
```

Via Portainer: Stacks → Add stack → paste the YAML → set variables → Deploy.

## Variables

Set them in the stack Environment (Portainer) or a local `.env` before deploying.
No real values are committed — names and purpose only.

| Variable | Description |
| -------- | ----------- |
| `HOST_PORT` | Host port mapped to the Semaphore UI (container port 3000). No default — required. |
| `MCP_PORT` | Host port mapped to the `semaphore-mcp` service. No default — required. |
| `SEMAPHORE_URL` | Public URL of the Semaphore instance, used by the MCP service to reach the API. |
| `SEMAPHORE_API_TOKEN` | API token the MCP service uses to authenticate against Semaphore. |
| `MYSQL_PASSWORD` | Password for the `semaphore` MySQL user (required). |
| `SEMAPHORE_DB_PASS` | Database password used by Semaphore (must match the MySQL user password). |
| `SEMAPHORE_ADMIN` | Login name for the initial Semaphore admin user. |
| `SEMAPHORE_ADMIN_EMAIL` | Email address for the initial Semaphore admin user. |
| `SEMAPHORE_ADMIN_PASSWORD` | Password for the initial Semaphore admin user. |
| `SEMAPHORE_ACCESS_KEY_ENCRYPTION` | Passphrase Semaphore uses to encrypt stored access keys. |
| `SEMAPHORE_SSH_RUNNER_PATH` | Host directory with the SSH key for runner jobs, mounted read-only at `/tmp/orch_ssh`. Must be set in the stack Environment **before** the redeploy that introduces it; if missing, the bind falls back to the built-in default and the container may fail to start. |

MySQL uses `MYSQL_RANDOM_ROOT_PASSWORD` and a named volume; no local root password
to manage.
