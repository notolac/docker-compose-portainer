# Media automation scripts

Optional Python utilities for Plex library management and Notion integration. These are **not required** to deploy the Docker stacks.

## Stacks

| File | Description |
|------|-------------|
| [multimedia-server.yaml](multimedia-server.yaml) | *arr stack + qBittorrent over Gluetun VPN |
| [tdarr-amd.yaml](tdarr-amd.yaml) | Tdarr transcoding (AMD VAAPI) |
| [tdarr-nvidia.yaml](tdarr-nvidia.yaml) | Tdarr transcoding (NVIDIA) |

See [../STACKS.md](../STACKS.md) for deployment conventions.

## Python scripts (optional)

| Script | Purpose |
|--------|---------|
| `plex_dl.py` | Download, transcode, and register media in Notion |
| `plex2notion.py` | Sync Plex library metadata to Notion |
| `create_folders_and_move_files_per_movie.py` | Organize movie folders |

### Prerequisites

- Python 3.12+ (pyenv recommended)
- [uv](https://github.com/astral-sh/uv) for dependency management

```bash
pyenv install 3.12.3
pyenv local 3.12.3
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
```

### Environment variables

| Variable | Description |
|----------|-------------|
| `PLEX_ROOT` | Plex library root (default: `/data/plex`) |
| `NOTION_TOKEN` | Notion integration token |
| `NOTION_DB` | Notion database ID |
| `SKIP_TOP` | Comma-separated top-level folders to skip |

Example:

```bash
export PLEX_ROOT=/data/plex
export NOTION_TOKEN=secret_xxx
export NOTION_DB=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
find "$PLEX_ROOT" -type f -print0 | python plex2notion.py
```

## License

MIT
