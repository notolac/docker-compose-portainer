#!/bin/sh
while true; do
  # Sincronizar desde Google Drive a multimedia local
  rclone -vv sync chiguire-bot-gdrive:/multimedia /data/multimedia
  # Sincronizar desde Google Drive a Plex local
  rclone -vv sync chiguire-bot-gdrive:/Plex /data/Plex
  # Esperar 24 horas antes de la siguiente sincronización
  sleep 86400  # 86400 segundos = 24 horas
done
