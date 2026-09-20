# Checkmk

Infrastructure monitoring (Raw edition) ([upstream](https://checkmk.com)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `checkmk.yaml` | Compose standalone | `checkmk/check-mk-raw:2.4.0-latest` (ports 8000, 5000, SNMP 162/udp) |

## Deploy

```bash
docker compose -f checkmk.yaml up -d
```

## Variables

| Variable | Description |
| -------- | ----------- |
| `CMK_PASSWORD` | Admin password (**required**) |
| `CMK_SITE_ID` | Monitoring site name (default `cmk`) |

> **Adjust before deploying:** the file ships Traefik labels for `checkmk.home.arpa`
> on an external `frontend` network with a `cloudflare` certresolver — adapt the
> router rule, entrypoints and resolver to your own setup (or remove the labels
> for plain `IP:port` access).
