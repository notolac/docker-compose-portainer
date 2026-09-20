# Audiobookshelf

Self-hosted audiobook and podcast server ([upstream](https://www.audiobookshelf.org)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `audiobookshelf.yaml` | Compose standalone | `audiobookshelf` (`ghcr.io/advplyr/audiobookshelf`) |

## Deploy

```bash
docker compose -f audiobookshelf.yaml up -d
```

Web UI on `${ABS_PORT:-13378}`. Via Portainer: Stacks → Add stack → paste the YAML →
set variables → Deploy.

## Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `AUDIOBOOKS_PATH` | `/data/media/audiobooks` | Audiobook library |
| `PODCASTS_PATH` | `/data/media/podcasts` | Podcast library |
| `ABS_CONFIG_PATH` | `/opt/audiobookshelf/config` | App config |
| `ABS_METADATA_PATH` | `/opt/audiobookshelf/metadata` | Metadata store |
| `ABS_PORT` | `13378` | Web UI port |
| `TZ` | `UTC` | Timezone |
