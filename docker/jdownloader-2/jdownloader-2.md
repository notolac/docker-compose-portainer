# JDownloader 2

Download manager with web UI ([upstream](https://jdownloader.org), image by jlesage).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `jdownloader2.yaml` | Compose standalone | `jlesage/jdownloader-2` (web UI on `:5800`) |

## Deploy

```bash
docker compose -f jdownloader2.yaml up -d
```

## Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `HOST_PORT` | — | Exposed web UI port |
| `JDOWNLOADER_CONFIG_PATH` | `/opt/jdownloader` | Config dir |
| `JDOWNLOADER_OUTPUT_PATH` | `/data/downloads` | Download dir |
