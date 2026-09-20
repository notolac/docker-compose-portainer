# Ghost

Blog/CMS platform ([upstream](https://ghost.org)). Legacy stack — evaluate current
upstream options before adopting it for a new blog.

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `ghost.yaml` | Compose standalone | `ghost:5-alpine` + MySQL |

## Deploy

```bash
docker compose -f ghost.yaml up -d
```

## Variables

| Variable | Description |
| -------- | ----------- |
| `HOST_PORT` | Exposed port (default `8080`) |
| `GHOST_DATA_ROOT` | Data root (default `/opt/ghost`) |
| `url` | Public URL, e.g. `https://blog.example.com` |
| `database__connection__password` / `MYSQL_ROOT_PASSWORD` | MySQL passwords |
