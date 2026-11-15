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

### Ejemplo de configuración

Usa rutas absolutas a los archivos y directorios de tu instalación. Los valores de
la tabla son ejemplos; configura el nombre del remote según tu rclone.conf.
PROXMOX_PATH puede omitirse para usar el valor predeterminado.

## Despliegue Portainer (Git)

1. Stack → Git: repo `docker-compose-portainer`, path `rclone/rclone.yaml` (o carpeta `rclone/` según cómo esté el stack).
2. Pegar las variables de entorno (tabla de configuración anterior).
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
docker run -it -v /opt/rclone/config:/config/rclone rclone/rclone:latest config
```

(Ajusta el volumen al `RCLONE_CONFIG_PATH` del host.)

## Scripts de este repo

- **backup**: `rclone sync` de `/data/multimedia`, `/data/Plex`, `/data/proxmox` → `${RCLONE_REMOTE}:/...` cada 24 h.
- **restore**: `rclone copy` por argumento (`multimedia` | `plex` | `proxmox`).

Los mounts del Compose mapean paths del host a `/data/...` dentro del contenedor.
