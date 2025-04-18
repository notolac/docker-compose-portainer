#!/bin/sh
while true; do
  # Descargar desde Google Drive a multimedia local (sin borrar archivos)
  rclone -vv copy chiguire-bot-gdrive:/multimedia /data/multimedia
  
  # Descargar desde Google Drive a Plex local (sin borrar archivos)
  # Comentado temporalmente ya que no es necesario en este momento
  rclone -vv copy chiguire-bot-gdrive:/Plex /data/Plex
  
  # Descargar desde Google Drive a Proxmox local (sin borrar archivos)
  # Comentado temporalmente ya que no es necesario en este momento
  rclone -vv copy chiguire-bot-gdrive:/proxmox /data/proxmox
  
  # Esperar 24 horas antes de la siguiente sincronización
  sleep 86400  # 86400 segundos = 24 horas
done