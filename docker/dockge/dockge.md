# Dockge

Web UI for managing Docker Compose stacks ([upstream](https://github.com/louislam/dockge)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `dockge.yaml` | Compose standalone | `louislam/dockge` (mounts the Docker socket + `/opt/stacks`) |

## Deploy

```bash
docker compose -f dockge.yaml up -d
```

UI on `${HOST_PORT:-5001}`. Stacks live under `/opt/stacks` — the host path and
`DOCKGE_STACKS_DIR` **must** match (full paths, no relative ones), otherwise data
lands in the wrong place. See the warnings in the YAML header.
