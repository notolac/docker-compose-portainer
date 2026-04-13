# Onyx App - Guía de Despliegue

Onyx es una plataforma de búsqueda y asistente AI que conecta con tus documentos,
Slack, Google Drive, Confluence y más. Esta guía cubre el despliegue tanto en
**Docker Swarm** como en **Docker Compose Standalone** mediante Portainer.

> **Nota:** Este despliegue es independiente del stack de ProxyGPT (OpenWebUI + LiteLLM).
> Ambos pueden coexistir sin conflicto de puertos
> (Onyx usa el puerto **3080** por defecto, OpenWebUI usa **8088**).

> `**onyx-app-standalone.yaml` (esta versión):** incluye **GPU NVIDIA** en los model servers (si el host cumple requisitos) y el servicio **code-interpreter** (monta el socket de Docker; **riesgo de seguridad**). Detalle en la sección [Onyx-app-standalone: GPU y Code interpreter](#onyx-app-standalone-gpu-y-code-interpreter). En **Swarm** (`onyx-app-swarm.yaml`) el code interpreter **no** está incluido.

## Archivos disponibles


| Archivo                    | Modo             | Uso                                          |
| -------------------------- | ---------------- | -------------------------------------------- |
| `onyx-app.yaml`            | Original oficial | Referencia, no modificar                     |
| `onyx-app-swarm.yaml`      | Docker Swarm     | Despliegue en clúster Swarm vía Portainer    |
| `onyx-app-standalone.yaml` | Docker Compose   | Despliegue en nodo único vía Portainer o CLI |


### Diferencias entre Standalone y Swarm


| Aspecto             | Standalone                     | Swarm                                     |
| ------------------- | ------------------------------ | ----------------------------------------- |
| `restart:`          | `always` (nativo)              | `deploy.restart_policy`                   |
| `depends_on:`       | Soportado (orden de arranque)  | No soportado (ignorado)                   |
| `shm_size:`         | Directo en PostgreSQL          | tmpfs en `/dev/shm` (workaround)          |
| `ulimits:`          | Directo en OpenSearch          | No soportado (requiere sysctl en host)    |
| `container_name:`   | `onyx-<servicio>`              | Asignado por swarm                        |
| Red                 | `bridge`                       | `overlay`                                 |
| Volúmenes           | Bind mount directo             | Bind mount con `driver_opts` sobre CephFS |
| Ruta datos default  | `/home/notolac/onyx-app`       | `/mnt/cephfs/onyx-app`                    |
| Alta disponibilidad | No                             | Sí (re-schedule automático)               |
| GPU (NVIDIA)        | Sí en model servers (`deploy`) | No en el YAML de Swarm de este repo       |
| Code interpreter    | Sí (monta `docker.sock`)       | No incluido                               |


---

## Arquitectura de servicios


| Servicio                 | Imagen                               | Descripción                                                                  |
| ------------------------ | ------------------------------------ | ---------------------------------------------------------------------------- |
| `api_server`             | `onyxdotapp/onyx-backend`            | API REST + migraciones Alembic                                               |
| `background`             | `onyxdotapp/onyx-backend`            | Workers de indexación, conectores, supervisord                               |
| `web_server`             | `onyxdotapp/onyx-web-server`         | Frontend Next.js                                                             |
| `inference_model_server` | `onyxdotapp/onyx-model-server`       | Servidor ML para inferencia                                                  |
| `indexing_model_server`  | `onyxdotapp/onyx-model-server`       | Servidor ML para indexación                                                  |
| `relational_db`          | `postgres:15.2-alpine`               | Base de datos PostgreSQL                                                     |
| `index`                  | `vespaengine/vespa:8.609.39`         | Motor de búsqueda Vespa                                                      |
| `opensearch`             | `opensearchproject/opensearch:3.4.0` | Búsqueda full-text                                                           |
| `nginx`                  | `nginx:1.25.5-alpine`                | Proxy inverso (punto de entrada)                                             |
| `cache`                  | `redis:7.4-alpine`                   | Caché efímero                                                                |
| `minio`                  | `minio/minio`                        | Almacenamiento de objetos S3                                                 |
| `code-interpreter`       | `onyxdotapp/code-interpreter`        | Ejecución de código (**solo** `onyx-app-standalone`; requiere socket Docker) |


---

## Requisitos del host

### 1. Kernel parameter para OpenSearch

OpenSearch requiere `vm.max_map_count >= 262144`. Ejecutar en el host:

```bash
sudo sysctl -w vm.max_map_count=262144
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

> Para Swarm, ejecutar en **cada nodo** que pueda alojar estos servicios.

### 2. Recursos mínimos recomendados

- **RAM:** 16 GB mínimo (OpenSearch pide 3-5 GB, Vespa y los model servers también consumen)
- **Disco:** 40 GB libres para datos, modelos e índices
- **CPU:** 4+ cores recomendado

---

## Pre-despliegue

### Paso 1: Crear directorios de datos

**Para Standalone:**

```bash
mkdir -p /home/notolac/onyx-app/{postgres-data,vespa-data,opensearch-data,minio-data,file-system,nginx-templates,model-cache-hf,indexing-model-cache-hf}
mkdir -p /home/notolac/onyx-app/logs/{api-server,background,inference-model-server,indexing-model-server}
sudo chown -R $(id -u):$(id -g) /home/notolac/onyx-app
```

**Para Swarm (almacenamiento compartido):**

```bash
sudo mkdir -p /mnt/cephfs/onyx-app/{postgres-data,vespa-data,opensearch-data,minio-data,file-system,nginx-templates,model-cache-hf,indexing-model-cache-hf}
sudo mkdir -p /mnt/cephfs/onyx-app/logs/{api-server,background,inference-model-server,indexing-model-server}
sudo chown -R 1000:1000 /mnt/cephfs/onyx-app
```

> Si usas una ruta diferente, configura la variable `ONYX_DATA_PATH` al desplegar.

### Paso 2: Descargar archivos de configuración de Nginx

Onyx necesita archivos de configuración nginx personalizados del repositorio oficial.
Descárgalos al directorio de datos correspondiente:

```bash
# Ajustar la ruta según tu modo de despliegue
cd /home/notolac/onyx-app/nginx-templates    # Standalone
# cd /mnt/cephfs/onyx-app/nginx-templates    # Swarm

# Descargar template de configuración nginx
# (ruta actual en upstream; la antigua deployment/docker_compose/data/nginx/ devuelve 404)
curl -LO https://raw.githubusercontent.com/onyx-dot-app/onyx/main/deployment/data/nginx/app.conf.template

# Descargar script de arranque nginx
curl -LO https://raw.githubusercontent.com/onyx-dot-app/onyx/main/deployment/data/nginx/run-nginx.sh
chmod +x run-nginx.sh
```

**Verificar que ambos archivos existen y son válidos** (si `curl` apunta a una URL antigua, GitHub devuelve texto `404: Not Found` y nginx fallará al arrancar):

```bash
ls -la nginx-templates/
# Debe mostrar:
#   app.conf.template
#   run-nginx.sh

head -n 1 run-nginx.sh
# Debe empezar por #! (shebang), no por "404"

head -n 1 app.conf.template
# Debe ser comentario nginx (# ...) o directiva, no "404"
```

> **Si los URLs no funcionan**, clona el repositorio completo y copia los archivos:
>
> ```bash
> git clone --depth 1 https://github.com/onyx-dot-app/onyx.git /tmp/onyx-repo
> cp /tmp/onyx-repo/deployment/data/nginx/* /home/notolac/onyx-app/nginx-templates/
> rm -rf /tmp/onyx-repo
> ```

### Paso 3: Generar credenciales

**PostgreSQL (`POSTGRES_PASSWORD`)**

Puedes usar una cadena aleatoria en hexadecimal (válida para PostgreSQL):

```bash
openssl rand -hex 16
```

**OpenSearch (`OPENSEARCH_ADMIN_PASSWORD`)**

La imagen **OpenSearch 3.x** valida la contraseña inicial del usuario `admin`. **No sirve** un valor generado solo con `openssl rand -hex`: solo contiene dígitos y letras `a-f`, y la imagen exige **al menos** una mayúscula, una minúscula, un dígito y un **carácter especial** (regex del contenedor; ver [documentación Docker de OpenSearch](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/)).

- Si **no** defines `OPENSEARCH_ADMIN_PASSWORD`, el compose usa el default `StrongPassword123!` (solo para entornos de prueba).
- Si defines tu propia contraseña, genera una que cumpla la política. Por ejemplo con Python (suele estar instalado en el host):

```bash
python3 <<'PY'
import secrets, string as s
chars = s.ascii_letters + s.digits + "!@#$%^&*"
print("".join(secrets.choice(chars) for _ in range(24)))
PY
```

Alternativa con `openssl` (salida base64; revisa que el resultado tenga mayúsculas, minúsculas, dígitos y algún símbolo; si no, vuelve a ejecutar o usa el script de Python):

```bash
openssl rand -base64 18
```

> **Misma variable en todo el stack:** `OPENSEARCH_ADMIN_PASSWORD` alimenta tanto el contenedor OpenSearch (`OPENSEARCH_INITIAL_ADMIN_PASSWORD`) como el backend Onyx. Usa **un solo valor** generado como arriba y configúralo en Portainer o en el `.env`.

---

## Despliegue Standalone en Portainer

> Usar el archivo: `**onyx-app-standalone.yaml`**

1. En Portainer, ir a **Stacks > Add stack**
2. Dar nombre al stack: `onyx`
3. Subir el archivo `onyx-app-standalone.yaml` o pegar su contenido
4. En la sección **Environment variables**, agregar:


| Variable                    | Valor                                                                  | Requerida |
| --------------------------- | ---------------------------------------------------------------------- | --------- |
| `POSTGRES_USER`             | `onyx`                                                                 | **Sí**    |
| `POSTGRES_PASSWORD`         | *(tu password generado)*                                               | **Sí**    |
| `OPENSEARCH_ADMIN_PASSWORD` | *(opcional; ver Paso 3 — si la omites, se usa el default del compose)* | No        |


1. Click en **Deploy the stack**
2. Esperar 3-5 minutos (la primera vez los model servers descargan modelos)

**Despliegue por CLI:**

```bash
docker compose -f onyx-app-standalone.yaml up -d
```

Con variables personalizadas:

```bash
POSTGRES_USER=onyx \
POSTGRES_PASSWORD=mi_password_seguro \
docker compose -f onyx-app-standalone.yaml up -d
```

---

## Despliegue Swarm en Portainer

> Usar el archivo: `**onyx-app-swarm.yaml**`

1. En Portainer, ir a **Stacks > Add stack**
2. Dar nombre al stack: `onyx`
3. Subir el archivo `onyx-app-swarm.yaml` o pegar su contenido
4. En la sección **Environment variables**, agregar:


| Variable                    | Valor                                                                  | Requerida |
| --------------------------- | ---------------------------------------------------------------------- | --------- |
| `POSTGRES_USER`             | `onyx`                                                                 | **Sí**    |
| `POSTGRES_PASSWORD`         | *(tu password generado)*                                               | **Sí**    |
| `OPENSEARCH_ADMIN_PASSWORD` | *(opcional; ver Paso 3 — si la omites, se usa el default del compose)* | No        |


> **IMPORTANTE:** NO usar comillas alrededor de los valores en Portainer.

1. Click en **Deploy the stack**
2. Esperar 3-5 minutos para que todos los servicios inicien

**Despliegue por CLI:**

```bash
POSTGRES_USER=onyx \
POSTGRES_PASSWORD=mi_password_seguro \
docker stack deploy -c onyx-app-swarm.yaml onyx
```

---

## Acceso a la interfaz

Una vez desplegado, acceder a:

```
http://<IP_DEL_HOST>:3080
```

La primera vez que accedas, Onyx te pedirá crear una cuenta de administrador
(cuando `AUTH_TYPE=basic`).

---

## Onyx-app-standalone: GPU y Code interpreter

Esta sección aplica solo a `**onyx-app-standalone.yaml**`.

### GPU (NVIDIA)

El compose reserva GPU para `**inference_model_server**` e `**indexing_model_server**` (`deploy.resources` con driver `nvidia`). En el host deben estar el **driver NVIDIA**, **nvidia-container-toolkit** y comprobarse antes con:

```bash
docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
```

**Validar tras desplegar Onyx:**

```bash
docker exec onyx-inference-model-server nvidia-smi
docker exec onyx-indexing-model-server nvidia-smi
```

Si ambos muestran tu GPU, el passthrough es correcto. Si aparece error del tipo *could not select device driver* o *nvidia-smi not found*, los contenedores están en CPU: revisa el toolkit y el runtime de Docker antes de reportar un fallo de Onyx.

En los logs del API pueden aparecer líneas sobre disponibilidad de GPU en indexación (p. ej. multipass); no es el único indicador, pero ayuda:

```bash
docker logs onyx-api-server 2>&1 | grep -i gpu
```

### Code interpreter (activado; implicaciones de seguridad)

En `**onyx-app-standalone.yaml**` el servicio `**code-interpreter**` está **incluido** y monta el socket de Docker del host (`DOCKER_SOCK_PATH`, por defecto `/var/run/docker.sock`). Es el comportamiento *docker-out-of-docker* del [compose oficial](https://github.com/onyx-dot-app/onyx): el intérprete puede crear contenedores en el mismo daemon para ejecutar código.

**Riesgos:**

- El acceso al **socket de Docker** desde un contenedor es muy sensible: en escenarios abusivos puede acercarse a **control efectivo del host** (p. ej. lanzar contenedores privilegiados o con montajes peligrosos).
- Cualquier usuario que pueda usar Code interpreter en la UI introduce una **superficie de ataque** alta; en entornos expuestos a Internet exige **autenticación fuerte**, confianza en los usuarios y valorar **no** habilitar el servicio (habría que quitar el servicio `code-interpreter` del YAML y la variable `CODE_INTERPRETER_BASE_URL` del `api_server`, y la entrada en `depends_on`).
- **Docker rootless:** define `DOCKER_SOCK_PATH` apuntando al socket real (p. ej. bajo `XDG_RUNTIME_DIR`).

**Logs del intérprete:**

```bash
docker logs onyx-code-interpreter -f
```

**Swarm:** `onyx-app-swarm.yaml` **no** incluye code-interpreter (el socket en Swarm es especialmente problemático); seguiría siendo un despliegue aparte si lo necesitas en clúster.

---

## Variables de entorno completas

### Variables requeridas


| Variable            | Descripción           | Ejemplo                           |
| ------------------- | --------------------- | --------------------------------- |
| `POSTGRES_USER`     | Usuario PostgreSQL    | `onyx`                            |
| `POSTGRES_PASSWORD` | Contraseña PostgreSQL | *(p. ej. `openssl rand -hex 16`)* |


### Variables opcionales


| Variable                     | Default                                                                | Descripción                                                                                                                                |
| ---------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `IMAGE_TAG`                  | `latest`                                                               | Tag de las imágenes de Onyx                                                                                                                |
| `ONYX_PORT`                  | `3080`                                                                 | Puerto externo de la UI                                                                                                                    |
| `AUTH_TYPE`                  | `basic`                                                                | Tipo de autenticación (`basic`, `google_oauth`, `oidc`, `saml`, `disabled`)                                                                |
| `POSTGRES_DB`                | `onyx_db`                                                              | Nombre de la BD                                                                                                                            |
| `ONYX_DATA_PATH`             | `/home/notolac/onyx-app` (standalone) o `/mnt/cephfs/onyx-app` (swarm) | Ruta base de datos persistentes                                                                                                            |
| `OPENSEARCH_ADMIN_PASSWORD`  | `StrongPassword123!`                                                   | Password admin de OpenSearch (OpenSearch 3.x exige mayúscula, minúscula, dígito y carácter especial; **no** uses solo `openssl rand -hex`) |
| `MINIO_ROOT_USER`            | `minioadmin`                                                           | Usuario admin de MinIO                                                                                                                     |
| `MINIO_ROOT_PASSWORD`        | `minioadmin`                                                           | Password admin de MinIO                                                                                                                    |
| `DISABLE_MODEL_SERVER`       | *(vacío)*                                                              | Poner `True` para deshabilitar model servers (si usas API externa)                                                                         |
| `DOMAIN`                     | `localhost`                                                            | Dominio para nginx                                                                                                                         |
| `CODE_INTERPRETER_BASE_URL`  | `http://code-interpreter:8000`                                         | URL interna del code interpreter (casi nunca hace falta cambiarla)                                                                         |
| `CODE_INTERPRETER_IMAGE_TAG` | `latest`                                                               | Tag de `onyxdotapp/code-interpreter`                                                                                                       |
| `DOCKER_SOCK_PATH`           | `/var/run/docker.sock`                                                 | Socket Docker del host para code-interpreter (rootless: ver sección dedicada)                                                              |


---

## Servicios no incluidos

### Code Interpreter (solo Swarm)

- `**onyx-app-standalone.yaml`:** incluye `**code-interpreter`** (ver [Onyx-app-standalone: GPU y Code interpreter](#onyx-app-standalone-gpu-y-code-interpreter)).
- `**onyx-app-swarm.yaml`:** **no** incluye `code-interpreter` (montar `/var/run/docker.sock` en Swarm es problemático). Si lo necesitas en clúster, despliégalo como stack o servicio aparte con criterio propio de seguridad.

### MCP Server

El servicio MCP (Model Context Protocol) está comentado en el compose original
y no se incluye aquí. Puede habilitarse en una versión futura.

---

## Troubleshooting

### Verificar estado de servicios

**Standalone:**

```bash
docker compose -f onyx-app-standalone.yaml ps
docker logs onyx-api-server -f
docker logs onyx-relational-db -f
docker logs onyx-nginx -f
docker logs onyx-code-interpreter -f
```

**Swarm:**

```bash
docker stack services onyx
docker service ps onyx_api_server
docker service logs onyx_api_server -f
docker service logs onyx_relational_db -f
docker service logs onyx_nginx -f
```

### Problemas comunes

#### 1. OpenSearch no arranca o se reinicia constantemente

```
ERROR: [1] bootstrap checks failed.
bootstrap check failure [1] of [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```

**Solución:** Ejecutar en el nodo host:

```bash
sudo sysctl -w vm.max_map_count=262144
```

#### 1b. OpenSearch: contraseña rechazada (`Password does not match validation regex`)

Si en los logs de OpenSearch aparece que la contraseña no cumple la política, definiste `OPENSEARCH_ADMIN_PASSWORD` con un valor inválido (p. ej. solo hexadecimal de `openssl rand -hex`). OpenSearch 3.x exige mayúsculas, minúsculas, dígitos y un carácter especial.

**Solución:** Genera una contraseña como en el **Paso 3** (comando con Python) o elimina la variable para usar el default del compose; si el volumen `opensearch-data` quedó en estado inconsistente, tras corregir la contraseña puede ser necesario vaciar ese directorio en un entorno de prueba y volver a desplegar.

#### 2. Nginx muestra "502 Bad Gateway"

El api_server o web_server aún no están listos. Esperar unos minutos y verificar:

```bash
# Standalone
docker logs onyx-api-server -f
docker logs onyx-web-server -f

# Swarm
docker service logs onyx_api_server -f
docker service logs onyx_web_server -f
```

#### 3. api_server falla con error de base de datos

Verificar que PostgreSQL está healthy:

```bash
# Standalone
docker logs onyx-relational-db -f

# Swarm
docker service logs onyx_relational_db -f
```

El api_server crea la BD automáticamente con Alembic migrations.

#### 4. Model servers tardan mucho en arrancar

La primera ejecución descarga modelos de HuggingFace (~1-2 GB). Esto es normal.
Los modelos se cachean en los directorios `model-cache-hf` e `indexing-model-cache-hf`.

```bash
# Standalone
docker logs onyx-inference-model-server -f

# Swarm
docker service logs onyx_inference_model_server -f
```

#### 5. Permisos de volúmenes

```bash
# Standalone
sudo chown -R $(id -u):$(id -g) /home/notolac/onyx-app

# Swarm
sudo chown -R 1000:1000 /mnt/cephfs/onyx-app
```

#### 6. Verificar variables de entorno de un servicio

```bash
# Standalone
docker inspect onyx-api-server | grep -A 20 Env

# Swarm
docker service inspect onyx_api_server --pretty
```

---

## Eliminar el stack (limpieza)

**Standalone:**

```bash
docker compose -f onyx-app-standalone.yaml down

# (Opcional) Eliminar datos persistentes
rm -rf /home/notolac/onyx-app
```

**Swarm:**

```bash
docker stack rm onyx

# (Opcional) Eliminar datos persistentes
sudo rm -rf /mnt/cephfs/onyx-app
```

---

## Comparación con OpenWebUI (ProxyGPT)


| Característica  | OpenWebUI + LiteLLM            | Onyx                                             |
| --------------- | ------------------------------ | ------------------------------------------------ |
| **Enfoque**     | Chat con LLMs                  | Búsqueda + Chat + RAG sobre documentos           |
| **Conectores**  | Ollama, APIs de LLM            | Slack, Google Drive, Confluence, GitHub, +40 más |
| **Búsqueda**    | No                             | Vespa + OpenSearch (semántica + full-text)       |
| **Servicios**   | 3 (WebUI, LiteLLM, PostgreSQL) | 12 en standalone (incl. code-interpreter)        |
| **RAM mínima**  | ~2 GB                          | ~16 GB                                           |
| **Caso de uso** | Proxy de modelos LLM + chat    | Asistente AI empresarial con acceso a documentos |


Ambos pueden coexistir. OpenWebUI es ideal para chat puro con LLMs,
mientras que Onyx es para cuando necesitas que el AI busque y responda
basándose en tus documentos internos.