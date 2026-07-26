#!/bin/sh

RCLONE_REMOTE="${RCLONE_REMOTE:-gdrive}"

if [ "$1" = "multimedia" ]; then
  rclone -vv copy "${RCLONE_REMOTE}:/multimedia" /data/multimedia
fi

if [ "$1" = "plex" ]; then
  rclone -vv copy "${RCLONE_REMOTE}:/Plex" /data/Plex
fi

if [ "$1" = "proxmox" ]; then
  rclone -vv copy "${RCLONE_REMOTE}:/proxmox" /data/proxmox
fi
