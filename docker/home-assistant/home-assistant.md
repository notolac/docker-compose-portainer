# Home Assistant

Home automation hub ([upstream](https://www.home-assistant.io)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `home-assistant.yaml` | Compose standalone | `homeassistant` (host networking, privileged for device access) |

## Deploy

```bash
docker compose -f home-assistant.yaml up -d
```

Uses `network_mode: host` (required for device discovery) plus `/run/dbus` access.

## Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `HA_CONFIG_PATH` | `/opt/home-assistant` | Config directory |
