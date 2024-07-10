# Despliegue de Apache Guacamole

## Paso 1: Copiar el script de inicialización de Guacamole al host

Ejecuta el siguiente comando en el host donde se hará el despliegue para copiar el script de inicialización de las tablas de la base de datos de Guacamole:

```sh
sudo docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --mysql > initdb.sql
```

## Paso 2: Copiar el script del host al contenedor MySQL

A continuación, copia el script `initdb.sql` generado en el paso anterior al contenedor MySQL:

```sh
sudo docker cp ./initdb.sql guacamoledb:/initdb.sql
```

Con estos pasos, hemos copiado el script de inicio de las tablas de la base de datos para Guacamole.

## Paso 3: Inicializar la base de datos MySQL

Ingresa a la terminal del contenedor de MySQL y ejecuta los siguientes comandos:

1. Haz login como root en MySQL:

   ```sh
   mysql -u root -p
   ```

2. Activa el uso de la base de datos:

   ```sql
   use tu_base_de_datos;
   ```

3. Corre el script de creación de tablas previamente copiado:

   ```sql
   source ./initdb.sql;
   ```

## Configuración del Proxy con Nginx Proxy Manager

Luego de iniciar la base de datos, accede al panel de Nginx Proxy Manager. (Esta configuración solo ha sido probada usando NPM).

### Añadir un Proxy Host

1. Inicia sesión en la interfaz de Nginx Proxy Manager.

2. Ve a la sección de "Proxy Hosts".

3. Haz clic en "Add Proxy Host".

### Configurar el dominio y la redirección

1. **Domain Names:** Escribe el nombre del dominio que deseas usar para acceder a tu aplicación Guacamole (por ejemplo, `guacamole.local`).

2. **Scheme:** Selecciona `http`.

3. **Forward Hostname / IP:** Introduce `IP_DEL_HOST`.

4. **Forward Port:** Introduce `PUERTO`.

### Configurar la URL base y la ruta

En la pestaña "Advanced", añade la siguiente configuración personalizada para asegurarte de que la ruta correcta se utiliza:

```nginx
location / {
    return 301 /guacamole/#/;
}

location /guacamole/ {
    proxy_pass http://hostip:port/guacamole/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Con esta configuración, Nginx Proxy Manager redirigirá correctamente las solicitudes a la URL específica requerida por Apache Guacamole.

¡Listo! Ahora deberías poder acceder a tu instancia de Apache Guacamole a través del dominio configurado.
