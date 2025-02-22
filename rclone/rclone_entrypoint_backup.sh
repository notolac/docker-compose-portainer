#!/bin/sh

# Bucle infinito para ejecutar la sincronización cada 24 horas
while true; do
  
  # Sincronizar la carpeta local /media/multimedia con Google Drive
  # Esto sube cualquier cambio desde el almacenamiento local a la nube
  rclone -vv sync /data/multimedia chiguire-bot-gdrive:/multimedia
  
  # Sincronizar la carpeta local /media/Plex con Google Drive
  # Se asegura de que la versión en Google Drive sea un reflejo exacto de la local
  rclone -vv sync /data/Plex chiguire-bot-gdrive:/Plex
  
  # Esperar 24 horas antes de volver a ejecutar la sincronización
  # 86400 segundos = 24 horas
  sleep 86400

done
