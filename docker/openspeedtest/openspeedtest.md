# OpenSpeedTest

Self-hosted HTML5 speed test ([upstream](https://openspeedtest.com)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `openspeedtest.yaml` | Compose standalone | `openspeedtest` (HTTP `:3000`, HTTPS `:3001`) |

## Deploy

```bash
docker compose -f openspeedtest.yaml up -d
```

Set `HOST_PORT1`/`HOST_PORT2` for the HTTP/HTTPS ports.
