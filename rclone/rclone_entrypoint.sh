#!/bin/sh
while true; do
  rclone -vv sync /data/multimedia chiguire-bot-gdrive:/multimedia
  rclone -vv sync /data/Plex chiguire-bot-gdrive:/Plex
  sleep 86400  # 86400 segundos = 24 horas
done
