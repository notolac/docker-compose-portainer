---

# Documentación de GoAccess y Nginx Proxy Manager (NPM)

## Introducción

GoAccess es una herramienta de análisis de logs de acceso web en tiempo real. Proporciona reportes visuales y detallados sobre el tráfico de tu servidor web. Con GoAccess, puedes monitorizar y analizar el rendimiento de tu sitio web, identificar errores, y entender mejor el comportamiento de los usuarios.

Nginx Proxy Manager (NPM) es una interfaz gráfica para manejar hosts proxy y redirigir tráfico web a diferentes servicios. Integrar GoAccess con NPM te permite analizar los logs generados por NPM, proporcionando una visión completa del tráfico y rendimiento de tus proxies.

## ¿Qué es GoAccess?

GoAccess es un analizador de logs de acceso web en tiempo real que transforma los datos de los logs en reportes visuales interactivos. Estos reportes pueden ser visualizados en un navegador web y permiten una rápida interpretación de los datos. GoAccess soporta varios formatos de logs y puede integrarse fácilmente con servidores web como Nginx y Apache.

### Características principales de GoAccess

- **Análisis en tiempo real**: Permite monitorizar el tráfico web en tiempo real, mostrando actualizaciones instantáneas en el reporte.
- **Interfaz web**: Proporciona una interfaz web interactiva que facilita la visualización de los datos.
- **Personalizable**: Soporta múltiples formatos de logs y permite personalizar la configuración según las necesidades específicas.
- **Reportes detallados**: Genera reportes con información detallada sobre el tráfico, incluyendo visitas, páginas vistas, tiempos de respuesta, y más.

## Tipos de Logs Analizados

Al integrar GoAccess con NPM, puedes analizar varios tipos de logs generados por NPM. Estos logs incluyen información crucial sobre el tráfico y el rendimiento de tus proxies.

### Logs de acceso

Los logs de acceso contienen información sobre cada solicitud HTTP que llega a tus servidores proxy. Estos logs incluyen:

- **Dirección IP del cliente**: La dirección IP desde donde se realizó la solicitud.
- **Fecha y hora**: El momento exacto en que se realizó la solicitud.
- **Método HTTP**: El método utilizado en la solicitud (GET, POST, etc.).
- **URL solicitada**: La URL que se solicitó.
- **Código de estado HTTP**: El código de respuesta del servidor (200, 404, 500, etc.).
- **Tamaño de la respuesta**: El tamaño de la respuesta enviada al cliente.
- **Referente**: La URL desde la cual se llegó a la solicitud actual.
- **Agente de usuario**: El navegador o cliente que realizó la solicitud.

### Logs de errores

Los logs de errores registran cualquier problema que ocurra en tus servidores proxy. Estos logs incluyen:

- **Fecha y hora**: El momento en que ocurrió el error.
- **Nivel de error**: La severidad del error (por ejemplo, error, aviso, etc.).
- **Mensaje de error**: Una descripción del error ocurrido.
- **Ubicación**: Información sobre dónde ocurrió el error en el servidor (archivo y línea de código).

### Ejemplo de Log de Acceso

Un ejemplo típico de un log de acceso de Nginx puede verse así:

```
192.168.1.1 - - [05/Jul/2024:14:23:14 +0000] "GET /index.html HTTP/1.1" 200 1024 "http://example.com" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
```

Este log proporciona la siguiente información:

- IP del cliente: `192.168.1.1`
- Fecha y hora: `05/Jul/2024:14:23:14 +0000`
- Método y URL solicitada: `GET /index.html`
- Código de estado: `200`
- Tamaño de la respuesta: `1024`
- Referente: `http://example.com`
- Agente de usuario: `Mozilla/5.0 (Windows NT 10.0; Win64; x64)`

### Ejemplo de Log de Error

Un ejemplo típico de un log de error de Nginx puede verse así:

```
2024/07/05 14:23:14 [error] 12345#0: *6789 open() "/var/www/html/404.html" failed (2: No such file or directory), client: 192.168.1.1, server: example.com, request: "GET /nonexistent.html HTTP/1.1", host: "example.com"
```

Este log proporciona la siguiente información:

- Fecha y hora: `2024/07/05 14:23:14`
- Nivel de error: `[error]`
- Mensaje de error: `open() "/var/www/html/404.html" failed (2: No such file or directory)`
- Cliente: `192.168.1.1`
- Servidor: `example.com`
- Solicitud: `"GET /nonexistent.html HTTP/1.1"`
- Host: `"example.com"`

## Integración de GoAccess con NPM usando Docker

### Archivo de configuración de GoAccess

Primero, necesitamos crear un archivo de configuración para GoAccess. Crea un archivo llamado `goaccess.conf` con el siguiente contenido:

```bash
time-format %H:%M:%S
date-format %d/%b/%Y
log-format %h %^ %e [%d:%t %^] "%r" %s %b "%R" "%u"
```

### Crear Docker Compose File

Vamos a crear un archivo `docker-compose.yml` que incluya tanto NPM como GoAccess. Si ya tienes NPM corriendo en Docker, solo necesitarás agregar el servicio de GoAccess.

Crea o edita el archivo `docker-compose.yml`:

```yaml
version: "3.8"
services:
  app:
    image: jc21/nginx-proxy-manager:latest
    container_name: nginx-proxy
    restart: always
    ports:
      - 8080:80
      - 8181:81
      - 443:443
    volumes:
      - /home/notolac/nginx-proxy-manager/data:/data
      - /home/notolac/nginx-proxy-manager/letsencrypt:/etc/letsencrypt
      - /home/notolac/nginx-proxy-manager/_hsts.conf:/app/templates/_hsts.conf:ro

  goaccess:
    image: "xavierh/goaccess-for-nginxproxymanager:latest"
    container_name: goaccess
    restart: always
    ports:
      - "7880:7880"
    environment:
      - TZ=Europe/Madrid
      - SKIP_ARCHIVED_LOGS=False #optional
      - DEBUG=False #optional
      - BASIC_AUTH=False #optional
      - BASIC_AUTH_USERNAME= #optional
      - BASIC_AUTH_PASSWORD= #optional
      - EXCLUDE_IPS=127.0.0.1 #optional - comma delimited
      - LOG_TYPE=NPM #optional - more information below
      - ENABLE_BROWSERS_LIST=True #optional - more information below
      - CUSTOM_BROWSERS=Kuma:Uptime,TestBrowser:Crawler #optional - comma delimited, more information below
      - HTML_REFRESH=5 #optional - Refresh the HTML report every X seconds. https://goaccess.io/man
      - KEEP_LAST=90 #optional - Keep the last specified number of days in storage. https://goaccess.io/man
      - PROCESSING_THREADS=1 #optional - This parameter sets the number of concurrent processing threads in the program's execution, affecting log data analysis, typically adjusted based on CPU cores. Default is 1. https://goaccess.io/man
    volumes:
      - /home/notolac/nginx-proxy-manager/data/logs:/opt/log:ro #required - path to your Nginx Proxy Manager logs
      #- /path/to/host/custom:/opt/custom #optional, required if using log_type = CUSTOM #change to the location of your choice
```

### Levantar los contenedores

Con el archivo `docker-compose.yml` configurado, podemos levantar los contenedores:

```sh
docker-compose up -d
```

Esto descargará las imágenes necesarias y levantará tanto NPM como GoAccess.

### Acceder al Reporte en Tiempo Real

Para habilitar la funcionalidad en tiempo real de GoAccess, necesitaremos configurar WebSocket. Ya hemos expuesto el puerto 7890 en el archivo `docker-compose.yml`.

Accede a tu servidor en `http://<your-server-ip>:7890/report.html` para ver el informe en tiempo real.

## Conclusión

Con GoAccess y Nginx Proxy Manager trabajando juntos, puedes obtener una visión detallada y en tiempo real del tráfico y rendimiento de tus servidores proxy. Esta integración te permite identificar rápidamente problemas, optimizar el rendimiento y entender mejor el comportamiento de los usuarios.

Para más información sobre GoAccess, puedes consultar su [documentación oficial](https://goaccess.io/documentation).

---
