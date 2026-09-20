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

| Variable | Description |
| -------- | ----------- |
| `MYSQL_PASSWORD` | Password for the `semaphore` MySQL user (required) |

MySQL uses `MYSQL_RANDOM_ROOT_PASSWORD` and a named volume; no local root password
to manage. Check the YAML header for the MCP service options.
