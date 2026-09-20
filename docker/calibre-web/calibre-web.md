# Calibre Web

E-book library web UI plus the Calibre desktop backend ([upstream](https://github.com/janeczku/calibre-web)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `calibre-web.yaml` | Compose standalone | `calibre-web` + `calibre` (linuxserver images) |

## Deploy

```bash
docker compose -f calibre-web.yaml up -d
```

## Variables

| Variable | Description |
| -------- | ----------- |
| `HOST_PORT1`…`HOST_PORT4` | Exposed ports for the web UI and Calibre services |

> **Adjust before deploying:** the file hardcodes `/media/multimedia/...` host paths
> and `Europe/Madrid` — change them to your own paths/timezone.
