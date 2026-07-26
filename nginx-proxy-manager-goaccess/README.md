# Nginx Proxy Manager + GoAccess

Reverse proxy with built-in Let's Encrypt and log analytics via GoAccess.

See [GoAccess.md](GoAccess.md) for log format notes and [npm-goaccess.yaml](npm-goaccess.yaml) for the stack manifest.

## Quick start

1. Copy `_hsts.conf` to `${NPM_DATA_ROOT}/_hsts.conf` on the host
2. Create data directories: `mkdir -p /opt/nginx-proxy-manager/{data,letsencrypt}`
3. Deploy via Portainer or `docker compose -f npm-goaccess.yaml up -d`
4. Open NPM admin on port `8181` (default) and create your admin user

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NPM_DATA_ROOT` | `/opt/nginx-proxy-manager` | Persistent NPM data |
| `TRAEFIK_LOG_PATH` | `…/data/logs` | Log directory for GoAccess |
| `LOG_TYPE` | `NPM` | `NPM` or `TRAEFIK` |
| `GOACCESS_PORT` | `7880` | GoAccess web UI port |
