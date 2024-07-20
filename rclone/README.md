## Documentación para Desplegar `rclone` Usando Docker y Docker Compose

### Español

### 1. ¿Qué es `rclone`?

`rclone` es una herramienta de línea de comandos para gestionar y sincronizar archivos en diferentes servicios de almacenamiento en la nube. Permite copiar, mover y sincronizar archivos entre una amplia variedad de proveedores de almacenamiento en la nube, como Google Drive, OneDrive, Dropbox, y más. Es muy útil para automatizar la sincronización de archivos entre servidores locales y servicios de nube.

### 2. Uso de `rclone` con Docker para Sincronizar Directorios a Google Drive

Para sincronizar directorios de un servidor local a Google Drive usando `rclone` con Docker y Docker Compose, sigue estos pasos:

#### 2.1. Generar el Archivo de Configuración de `rclone`

Primero, debes generar el archivo de configuración de `rclone` para Google Drive. Usa el siguiente comando para ejecutar `rclone` en un contenedor interactivo:

```sh
sudo docker run -it -v ~/.config/rclone:/config/rclone rclone/rclone:latest config
```

Este comando te guiará a través del proceso interactivo para configurar `rclone` y autenticarte con Google Drive. Al finalizar, tendrás un archivo `rclone.conf` en tu directorio `~/.config/rclone`.

#### 2.2. Crear un Proyecto en Google Cloud Platform

Para gestionar la API de Google Drive, necesitas crear un proyecto en Google Cloud Platform (GCP) y configurar una aplicación. Aquí están los pasos:

1. **Ir a [Google Cloud Console](https://console.cloud.google.com/)**.
2. **Crear un nuevo proyecto** o seleccionar uno existente.
3. **Habilitar la API de Google Drive**:
   - Navega a la sección de APIs y Servicios.
   - Habilita la API de Google Drive para tu proyecto.
4. **Crear credenciales**:
   - Ve a la sección de Credenciales y crea una nueva credencial de tipo **ID de cliente de OAuth 2.0**.
   - Configura la pantalla de consentimiento y descarga el archivo JSON con las credenciales.

#### 2.3. Configurar el Archivo `rclone.conf`

Usa las credenciales obtenidas en el paso anterior para completar la configuración en el archivo `rclone.conf`. Asegúrate de incluir el `client_id` y el `client_secret` obtenidos de Google Cloud.

#### 2.4. Desplegar con Docker Compose

Aquí tienes un archivo `docker-compose.yml` para desplegar `rclone` usando Docker Compose. Este archivo sincroniza directorios locales con Google Drive.

```yaml
version: "3.8"

services:
  rclone_sync:
    image: rclone/rclone:latest
    container_name: rclone_sync
    volumes:
      - ~/.config/rclone:/config/rclone:ro
      - /home/media/multimedia:/data/multimedia
      - /home/media/Plex:/data/Plex
    entrypoint:
      [
        "/bin/sh",
        "-c",
        "rclone sync /data/multimedia gdrive:/path/in/shared/drive/multimedia && rclone sync /data/Plex gdrive:/path/in/shared/drive/Plex",
      ]
    environment:
      - RCLONE_CONFIG=/config/rclone/rclone.conf
    user: "${UID}:${GID}"
    restart: unless-stopped
```

### Inglés

### 1. What is `rclone`?

`rclone` is a command-line tool for managing and syncing files across different cloud storage services. It allows you to copy, move, and synchronize files between a wide variety of cloud storage providers, such as Google Drive, OneDrive, Dropbox, and more. It is highly useful for automating file synchronization between local servers and cloud services.

### 2. Using `rclone` with Docker to Sync Directories to Google Drive

To sync directories from a local server to Google Drive using `rclone` with Docker and Docker Compose, follow these steps:

#### 2.1. Generate the `rclone` Configuration File

First, you need to generate the `rclone` configuration file for Google Drive. Use the following command to run `rclone` in an interactive container:

```sh
sudo docker run -it -v ~/.config/rclone:/config/rclone rclone/rclone:latest config
```

This command will guide you through the interactive process to configure `rclone` and authenticate with Google Drive. Upon completion, you will have an `rclone.conf` file in your `~/.config/rclone` directory.

#### 2.2. Create a Project in Google Cloud Platform

To manage the Google Drive API, you need to create a project in Google Cloud Platform (GCP) and configure an application. Here are the steps:

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**.
2. **Create a new project** or select an existing one.
3. **Enable the Google Drive API**:
   - Navigate to the API & Services section.
   - Enable the Google Drive API for your project.
4. **Create credentials**:
   - Go to the Credentials section and create a new OAuth 2.0 Client ID credential.
   - Set up the consent screen and download the JSON file with your credentials.

#### 2.3. Configure the `rclone.conf` File

Use the credentials obtained in the previous step to complete the configuration in the `rclone.conf` file. Make sure to include the `client_id` and `client_secret` obtained from Google Cloud.

#### 2.4. Deploy with Docker Compose

Here is a `docker-compose.yml` file to deploy `rclone` using Docker Compose. This file synchronizes local directories with Google Drive.

```yaml
version: "3.8"

services:
  rclone_sync:
    image: rclone/rclone:latest
    container_name: rclone_sync
    volumes:
      - ~/.config/rclone:/config/rclone:ro
      - /home/media/multimedia:/data/multimedia
      - /home/media/Plex:/data/Plex
    entrypoint:
      [
        "/bin/sh",
        "-c",
        "rclone sync /data/multimedia gdrive:/path/in/shared/drive/multimedia && rclone sync /data/Plex gdrive:/path/in/shared/drive/Plex",
      ]
    environment:
      - RCLONE_CONFIG=/config/rclone/rclone.conf
    user: "${UID}:${GID}"
    restart: unless-stopped
```
