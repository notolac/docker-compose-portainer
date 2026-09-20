# wg-easy

WireGuard VPN with a web UI ([upstream](https://github.com/wg-easy/wg-easy)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `wg-easy-vpn.yaml` | Compose standalone | `wg-easy` (WireGuard `:51820/udp`, UI `:51821`) |

## Deploy

```bash
docker compose -f wg-easy-vpn.yaml up -d
```

## Variables

| Variable | Description |
| -------- | ----------- |
| `WG_HOST` | **Required** — your host's public address (used in client configs) |
| `PASSWORD_HASH` | Optional UI password (bcrypt, `$$`-escaped — see the YAML comments) |
| `PORT` / `WG_PORT` | UI and VPN ports |
| `LANG` | UI language |

Needs `NET_ADMIN`/`SYS_MODULE` capabilities (in the YAML) and UDP access from
the Internet to work as a VPN endpoint.
