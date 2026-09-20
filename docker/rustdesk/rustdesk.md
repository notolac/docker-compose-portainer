# RustDesk (self-hosted server)

Self-hosted remote-desktop rendezvous/relay ([upstream](https://rustdesk.com):
`hbbs` rendezvous + `hbbr` relay).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `rustdesk.yaml` | Compose standalone | `hbbs` (ports 21115–21118) + `hbbr` (ports 21117/21119), data in `/opt/rustdesk/data` |

## Deploy

```bash
docker compose -f rustdesk.yaml up -d
```

> **Adjust before deploying:** `hbbs` is started with `-r your.domain.com:21117` —
> replace it with your public domain/IP. Open the listed TCP+UDP ports on your
> firewall/router, then point RustDesk clients at your server (ID server +
> relay server + key).
