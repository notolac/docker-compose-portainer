# No-IP DDNS

Keeps No-IP dynamic hostnames in sync ([upstream](https://www.noip.com), official DUC image).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `noip-ddns.yaml` | Compose standalone | `noip-duc` |

## Deploy

```bash
docker compose -f noip-ddns.yaml up -d
```

## Variables

| Variable | Description |
| -------- | ----------- |
| `NOIP_USERNAME` / `NOIP_PASSWORD` | DDNS key credentials (**required**) |
| `NOIP_HOSTNAMES` | Hostnames to update (default in file: `all.ddnskey.com`) |
