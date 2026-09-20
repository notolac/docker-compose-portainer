# rclone — sync programado (Docker / Portainer)

Stack Compose para sincronizar directorios locales con un remoto `rclone` (p. ej. Google Drive).

Archivos:

| File | Role |
|------|------|
| [rclone.yaml](rclone.yaml) | Compose (Portainer Git / `docker compose`) |
| [rclone_entrypoint_backup.sh](rclone_entrypoint_backup.sh) | Loop backup (`sync` local → remoto) |
| [rclone_entrypoint_restore.sh](rclone_entrypoint_restore.sh) | Restore puntual (`copy` remoto → local) |

## Variables de entorno (Portainer → Environment)

Sin comillas. Nombres exactos usados por `rclone.yaml`:

| Variable | Default | Descripción |
|----------|---------|-------------|
| `RCLONE_CONFIG_PATH` | `/opt/rclone/config/rclone.conf` | Ruta **host** a `rclone.conf` |
| `RCLONE_BACKUP_SCRIPT` | `./rclone_entrypoint_backup.sh` | Ruta **host** al script de backup |
| `RCLONE_RESTORE_SCRIPT` | `./rclone_entrypoint_restore.sh` | Ruta **host** al script de restore |
| `RCLONE_SCRIPT` | `backup` | `backup` o `restore` (elige `/backup.sh` o `/restore.sh`) |
| `RCLONE_REMOTE` | `gdrive` | Nombre del remote en `rclone.conf` (si el script lo usa) |
| `MULTIMEDIA_PATH` | `/data/multimedia` | Datos multimedia en el host |
| `PLEX_PATH` | `/data/plex` | Librería Plex en el host |
| `PROXMOX_PATH` | `/data/proxmox` | Opcional (backups Proxmox) |

### Homelab `.11` (Portainer — valores validados)

```env
RCLONE_CONFIG_PATH=/home/notolac/.config/rclone/rclone.conf
RCLONE_BACKUP_SCRIPT=/home/notolac/scripts/rclone_entrypoint_backup.sh
RCLONE_RESTORE_SCRIPT=/home/notolac/scripts/rclone_entrypoint_restore.sh
MULTIMEDIA_PATH=/srv/multimedia
PLEX_PATH=/srv/Plex
RCLONE_SCRIPT=backup
RCLONE_REMOTE=chiguire-bot-gdrive
```

Copia de referencia también en el repo `home-lab`:
`servicios-apps/docker-compose/media-11/rclone.yaml.env`.

Notas `.11`:

- Los scripts bajo `/home/notolac/scripts/` tienen el remote **hardcodeado** (`chiguire-bot-gdrive`); `RCLONE_REMOTE` no cambia ese comportamiento, pero sí aplica si montas los entrypoints de este repo.
- `PROXMOX_PATH` se puede omitir (default `/data/proxmox`).

## Despliegue Portainer (Git)

1. Stack → Git: repo `docker-compose-portainer`, path `rclone/rclone.yaml` (o carpeta `rclone/` según cómo esté el stack).
2. Pegar las variables de entorno (tabla / bloque `.11` arriba).
3. Deploy / Update the stack.
4. Comprobar: logs sin `Permission denied`; mounts de `/backup.sh` y `rclone.conf` como **ficheros**, no directorios.

```bash
docker inspect rclone_sync --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}'
docker logs --tail 50 rclone_sync
```

## Gotcha: `/bin/sh: /backup.sh: Permission denied`

Si una ruta de bind **no existe** en el host en el primer deploy, Docker crea un **directorio** vacío con ese nombre. Montar ese directorio como `/backup.sh` produce `Permission denied`.

Lo mismo puede pasar con `rclone.conf` → directorio en `/opt/rclone/config/rclone.conf`.

Mitigación:

1. Usar rutas **absolutas** a ficheros reales (`RCLONE_BACKUP_SCRIPT`, `RCLONE_CONFIG_PATH`, …).
2. Antes de redeploy: parar el contenedor y borrar solo los **directorios fantasma** (nunca borrar el `rclone.conf` real ni `/srv/...`).
3. El entrypoint invoca `sh /backup.sh` (no requiere `+x` en el mount).

## Generar / refrescar `rclone.conf`

```sh
docker run -it -v /home/notolac/.config/rclone:/config/rclone rclone/rclone:latest config
```

(Ajusta el volumen al `RCLONE_CONFIG_PATH` del host.)

## Scripts de este repo

- **backup**: `rclone sync` de `/data/multimedia`, `/data/Plex`, `/data/proxmox` → `${RCLONE_REMOTE}:/...` cada 24 h.
- **restore**: `rclone copy` por argumento (`multimedia` | `plex` | `proxmox`).

Los mounts del Compose mapean paths del host a `/data/...` dentro del contenedor.
