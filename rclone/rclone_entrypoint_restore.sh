#!/bin/sh
while true; do
  # Descargar desde Google Drive a multimedia local (sin borrar archivos)
  rclone -vv copy chiguire-bot-gdrive:/multimedia /data/multimedia
  
  # Descargar desde Google Drive a Plex local (sin borrar archivos)
  rclone -vv copy chiguire-bot-gdrive:/Plex /data/Plex
  
  # Esperar 24 horas antes de la siguiente sincronización
  sleep 86400  # 86400 segundos = 24 horas
done
