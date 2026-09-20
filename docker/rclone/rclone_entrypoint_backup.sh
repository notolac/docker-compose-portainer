#!/bin/sh

RCLONE_REMOTE="${RCLONE_REMOTE:-gdrive}"

# Sync every 24 hours
while true; do
  rclone -vv sync /data/multimedia "${RCLONE_REMOTE}:/multimedia"
  rclone -vv sync /data/Plex "${RCLONE_REMOTE}:/Plex"
  rclone -vv sync /data/proxmox "${RCLONE_REMOTE}:/proxmox"
  sleep 86400
done
