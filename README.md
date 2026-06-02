# Ejemplo de Servicios Web

Web services para probar como consumir ws desde react (en la semana 7 y 8), este repositorio contiene los servicios web.

---

## Índice

1. [Conceptos que aprenderás en este ejercicio](#1-conceptos-que-aprenderás-en-este-ejercicio)
2. [Estructura del repositorio](#2-estructura-del-repositorio)
3. [Configuración de MySQL](#3-configuración-de-mysql)
   - 3.1 [¿Qué es Docker y por qué lo usamos aquí?](#31-qué-es-docker-y-por-qué-lo-usamos-aquí)
   - 3.2 [Iniciar la instancia de MySQL en Docker](#32-iniciar-la-instancia-de-mysql-en-docker)
   - 3.3 [El archivo `jedi.sql`: definición del esquema](#33-el-archivo-jedisql-definición-del-esquema)
   - 3.4 [Conectarse al contenedor a través de la herramienta de línea de comandos](#34-conectarse-al-contenedor-a-través-de-la-herramienta-de-línea-de-comandos)
4. [Probar código Python que se conecta al servidor](#4-probar-código-python-que-se-conecta-al-servidor)
   - 4.1 [El conector `mysql-connector-python`: ¿qué es y cómo funciona?](#41-el-conector-mysql-connector-python-qué-es-y-cómo-funciona)
   - 4.2 [Instala conector python-MySQL y flask](#42-instala-conector-python-mysql-y-flask)
   - 4.3 [Explora el contenido del archivo `crudMySQL.py`](#43-explora-el-contenido-del-archivo-crudmysqlpy)
   - 4.4 [En la terminal ejecuta](#44-en-la-terminal-ejecuta)
   - 4.5 [Conectarse al contenedor para verificar que se hayan insertado los datos](#45-conectarse-al-contenedor-para-verificar-que-se-hayan-insertado-los-datos)
5. [Correr Servicios Web](#5-correr-servicios-web)
   - 5.1 [¿Qué es Flask y cómo construye servicios REST?](#51-qué-es-flask-y-cómo-construye-servicios-rest)
   - 5.2 [Corre `ws_jedi.py`](#52-corre-ws_jedipy)
   - 5.3 [¿Qué es `curl` y cómo usarlo?](#53-qué-es-curl-y-cómo-usarlo)
   - 5.4 [Probar con Postman en GitHub Codespaces](#54-probar-con-postman-en-github-codespaces)
6. [CORS: ¿Por qué es necesario en el backend?](#6-cors-por-qué-es-necesario-en-el-backend)
7. [Flujo completo del sistema](#7-flujo-completo-del-sistema)
8. [Actividades sugeridas](#8-actividades-sugeridas)

---

## 1. Conceptos que aprenderás en este ejercicio

Este repositorio está diseñado para que explores de forma práctica la **arquitectura de una aplicación backend completa**: desde la base de datos hasta la exposición de un API REST consumible desde cualquier cliente HTTP.

Los conceptos centrales son:

- **Bases de datos relacionales (MySQL):** cómo modelar datos en tablas, definir esquemas con SQL y ejecutar operaciones CRUD (*Create, Read, Update, Delete*).
- **Conectores de base de datos (`mysql-connector-python`):** cómo Python se comunica con MySQL mediante un driver que traduce instrucciones Python a comandos SQL.
- **Servicios web REST con Flask:** cómo construir endpoints HTTP que reciben peticiones, consultan la base de datos y devuelven respuestas en formato JSON.
- **Consumo de servicios web con `curl`:** cómo probar APIs directamente desde la terminal usando métodos HTTP (GET, POST, PUT, DELETE).
- **Consumo de servicios web con Postman:** cómo usar una herramienta visual para diseñar, ejecutar y documentar pruebas a una API.
- **GitHub Codespaces y reenvío de puertos:** cómo exponer servicios locales al exterior para que Postman (u otras herramientas) pueda alcanzarlos.
- **CORS:** por qué el navegador bloquea peticiones entre orígenes distintos y cómo habilitarlo correctamente en el backend.

---

## 2. Estructura del repositorio

```
ejemplo_ws/
├── .devcontainer/       # Configuración del entorno de GitHub Codespaces
├── jedi.sql             # Script SQL para crear la tabla en MySQL
├── crudMySQL.py         # Script Python que demuestra CRUD directo sobre MySQL
├── ws_jedi.py           # Servicio web Flask con endpoints CRUD completos
└── README.md            # Este archivo
```

---

## 3. Configuración de MySQL

### 3.1 ¿Qué es Docker y por qué lo usamos aquí?

**Docker** es una plataforma de contenedores que permite ejecutar aplicaciones en entornos aislados y reproducibles. En este ejercicio usamos Docker para levantar una instancia de MySQL sin necesidad de instalarlo directamente en el sistema operativo del Codespace. El contenedor tiene todo lo que MySQL necesita, y lo comunicamos con el puerto `3306` del host.

### 3.2 Iniciar la instancia de MySQL en Docker

Para iniciar una instancia de **MySQL** en un contenedor Docker, ejecuta el siguiente comando en la terminal de tu **GitHub Codespace**:

```bash
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=contrasena -e MYSQL_DATABASE=testdb -p 3306:3306 -d mysql:latest
```

**¿Qué hace este comando?**

| Parámetro | Significado |
|-----------|-------------|
| `--name mysql-container` | Le asigna un nombre al contenedor para referenciarlo fácilmente después |
| `-e MYSQL_ROOT_PASSWORD=contrasena` | Define la contraseña del usuario `root` de MySQL como variable de entorno |
| `-e MYSQL_DATABASE=testdb` | Crea automáticamente una base de datos llamada `testdb` al iniciar |
| `-p 3306:3306` | Mapea el puerto 3306 del contenedor al puerto 3306 del host (Codespace) |
| `-d` | Ejecuta el contenedor en modo *detached* (en segundo plano) |
| `mysql:latest` | Usa la imagen oficial de MySQL más reciente desde Docker Hub |

### 3.3 El archivo `jedi.sql`: definición del esquema

El archivo `jedi.sql` contiene el DDL (*Data Definition Language*) que crea la tabla `jedi` dentro de la base de datos `testdb`:

```sql
USE testdb;

CREATE TABLE jedi (
    id_jedi     INT AUTO_INCREMENT PRIMARY KEY,
    nombre_jedi VARCHAR(100) NOT NULL,
    email_jedi  VARCHAR(100) UNIQUE NOT NULL
);
```

**Conceptos clave:**

- `INT AUTO_INCREMENT PRIMARY KEY`: la columna `id_jedi` se genera automáticamente y nunca se repite. Esto es la **llave primaria** de la tabla.
- `VARCHAR(100) NOT NULL`: cadena de texto de hasta 100 caracteres que **no puede estar vacía**.
- `UNIQUE NOT NULL` en `email_jedi`: garantiza que no existan dos jedis con el mismo correo electrónico. Esta es una **restricción de integridad**.

### 3.4 Conectarse al contenedor a través de la herramienta de linea de comandos

El siguiente comando ejecuta el script SQL dentro del contenedor para crear la tabla:

```bash
docker exec -i mysql-container mysql -u root -pcontrasena testdb < jedi.sql
```

**Desglose del comando:**

- `docker exec -i mysql-container`: ejecuta un comando *dentro* del contenedor activo.
- `mysql -u root -pcontrasena testdb`: invoca el cliente MySQL con el usuario `root`, la contraseña `contrasena` y selecciona la base de datos `testdb`.
- `< jedi.sql`: redirige el contenido del archivo SQL como entrada estándar al cliente MySQL.

Esto debe generar una tabla.

---

## 4. Probar código Python que se conecta al servidor

### 4.1 El conector `mysql-connector-python`: ¿qué es y cómo funciona?

Un **conector de base de datos** (también llamado *driver*) es una librería que implementa un protocolo de comunicación entre tu lenguaje de programación y el motor de base de datos. En este caso, `mysql-connector-python` es el driver oficial de Oracle para conectar Python con MySQL.

El flujo de trabajo es siempre el mismo:
1. **Conectar** → estableces una sesión TCP con el servidor MySQL.
2. **Obtener un cursor** → es el objeto que envía consultas SQL y recibe resultados.
3. **Ejecutar consultas** → `cursor.execute(sql, params)` envía la instrucción.
4. **Confirmar cambios** → para INSERT/UPDATE/DELETE, debes llamar a `conn.commit()`.
5. **Cerrar** → `cursor.close()` y `conn.close()` liberan los recursos.

### 4.2 Instala conector python-MySQL y flask

```bash
pip install mysql-connector-python flask flask-cors
```

- **`mysql-connector-python`**: driver para conectar Python con MySQL.
- **`flask`**: microframework web que permite crear servicios HTTP con pocas líneas de código.
- **`flask-cors`**: extensión de Flask que agrega soporte para CORS (ver sección [6](#6-cors-por-qué-es-necesario-en-el-backend)).

### 4.3 Explora el contenido del archivo `crudMySQL.py`

Observa como se conecta a la instancia base de datos que creaste al inicio de este ejercicio, usa las credenciales que se definieron cuando creaste el contenedor docker.

```python
import mysql.connector

# Configurar conexión
conn = mysql.connector.connect(
    host="127.0.0.1",   # Docker expone en localhost
    user="root",
    password="contrasena",
    database="testdb",
    port=3306            # Puerto mapeado en Docker
)
cursor = conn.cursor()
```

**Puntos de atención:**

- `host="127.0.0.1"` equivale a `localhost`. Docker mapeó el puerto 3306 del contenedor al 3306 del host, por eso Python puede alcanzarlo como si fuera un servidor local.
- El objeto `cursor` es el intermediario entre Python y MySQL: envía SQL y retorna resultados.

Las cuatro operaciones CRUD implementadas demuestran el patrón básico:

```python
# CREATE
def create_jedi(nombre_jedi, email_jedi):
    cursor.execute(
        "INSERT INTO jedi (nombre_jedi, email_jedi) VALUES (%s, %s)",
        (nombre_jedi, email_jedi)
    )
    conn.commit()  # ⚠️ Sin commit(), el INSERT no se persiste
```

> **Nota sobre SQL injection:** el uso de `%s` como *placeholder* (en lugar de concatenar strings) es fundamental para evitar inyección SQL. El driver se encarga de escapar los valores correctamente.

### 4.4 En la terminal ejecuta

```bash
python crudMySQL.py
```

Esto creará un par de registros en la tabla.

### 4.5 Conectarse al contenedor a través de la herramienta de linea de comandos para verificar que se hayan insertado los datos

```bash
docker exec -it mysql-container mysql -u root -pcontrasena
```

La diferencia con el comando anterior es `-it` (*interactive + tty*): abre una sesión interactiva en la que puedes escribir comandos SQL uno a uno.

Dentro de MySQL:

```sql
USE testdb;
```

```sql
SELECT * FROM jedi;
```

Deberías ver algo así:

```
+---------+------------------+-------------------------+
| id_jedi | nombre_jedi      | email_jedi              |
+---------+------------------+-------------------------+
|       1 | Luke Skywalker   | luke@jedi.com           |
|       2 | Obi-Wan Kenobi   | obiwan@jedi.com         |
+---------+------------------+-------------------------+
```

Para salir escriba *quit* y presione enter.

---

## 5. Correr Servicios Web

### 5.1 ¿Qué es Flask y cómo construye servicios REST?

**Flask** es un microframework web para Python. A diferencia de frameworks más grandes (como Django), Flask es minimalista: tú decides qué componentes agregar. Es ideal para construir **APIs REST**.

Un **servicio web REST** (*Representational State Transfer*) es una interfaz HTTP donde:
- La **URL** identifica el recurso (p. ej. `/jedi` o `/jedi/1`).
- El **método HTTP** indica la operación: `GET` = leer, `POST` = crear, `PUT` = actualizar, `DELETE` = eliminar.
- La **respuesta** está en formato JSON con un código de estado HTTP (200, 201, 404, 500…).

El archivo `ws_jedi.py` implementa el CRUD completo del recurso `jedi`:

| Endpoint | Método | Operación | Código de éxito |
|---|---|---|---|
| `/jedi` | GET | Obtener todos los jedis | 200 OK |
| `/jedi/<id>` | GET | Obtener un jedi por ID | 200 OK |
| `/jedi` | POST | Crear un jedi | 201 Created |
| `/jedi/<id>` | PUT | Actualizar un jedi | 200 OK |
| `/jedi/<id>` | DELETE | Eliminar un jedi | 200 OK |

### 5.2 Corre `ws_jedi.py`

```bash
python ws_jedi.py
```

Flask levantará el servidor en `http://localhost:5000`. Verás en la terminal un mensaje como:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Abrir **otra terminal** para probar los servicios web (el servidor debe seguir corriendo en la primera).

### 5.3 ¿Qué es `curl` y cómo usarlo?

`curl` (*Client URL*) es una herramienta de línea de comandos para transferir datos usando protocolos de red, principalmente HTTP. Es la forma más directa de probar una API sin necesidad de una interfaz gráfica.

Sintaxis general:
```bash
curl -X <MÉTODO> <URL> [-H "<Encabezado>"] [-d '<Body>']
```

---

**1. Servicio web para consultar todos los jedis (método GET). Deberás probarlo así:**

```bash
curl -X GET http://localhost:5000/jedi
```

Respuesta esperada (JSON con la lista de jedis):
```json
[
  {"id_jedi": 1, "nombre_jedi": "Luke Skywalker", "email_jedi": "luke@jedi.com"},
  {"id_jedi": 2, "nombre_jedi": "Obi-Wan Kenobi",  "email_jedi": "obiwan@jedi.com"}
]
```

**2. Servicio web para consultar solo un jedi (método GET). Deberás probarlo así:**

```bash
curl -X GET http://localhost:5000/jedi/1
```

El número `1` al final de la URL es el `id_jedi`. Flask lo captura con `<int:id_jedi>` en la definición del endpoint y lo pasa como parámetro a la función Python.

Respuesta esperada:
```json
{"id_jedi": 1, "nombre_jedi": "Luke Skywalker", "email_jedi": "luke@jedi.com"}
```

Si el ID no existe, el servidor responde con `404 Not Found`:
```json
{"error": "Jedi no encontrado"}
```

**3. Servicio web para crear solo un jedi (método POST). Deberás probarlo así:**

```bash
curl -X POST http://localhost:5000/jedi \
     -H "Content-Type: application/json" \
     -d '{"nombre_jedi": "yoda", "email_jedi": "yoda@gmail.com"}'
```

**Desglose:**

- `-H "Content-Type: application/json"`: le indica al servidor que el cuerpo de la petición está en formato JSON. Sin este encabezado, Flask no puede parsear el body.
- `-d '{"nombre_jedi": ...}'`: el cuerpo (*body*) de la petición con los datos del nuevo jedi.

Respuesta esperada:
```json
{"message": "Jedi creado", "id_jedi": 3}
```

**4. Actualizar un jedi (método PUT):**

```bash
curl -X PUT http://localhost:5000/jedi/1 \
     -H "Content-Type: application/json" \
     -d '{"nombre_jedi": "Luke S.", "email_jedi": "lukeskywalker@jedi.com"}'
```

**5. Eliminar un jedi (método DELETE):**

```bash
curl -X DELETE http://localhost:5000/jedi/2
```

### 5.4 Probar con Postman en GitHub Codespaces

**Postman** es una aplicación gráfica para diseñar, ejecutar y documentar peticiones HTTP. Es ampliamente usada en equipos de desarrollo para colaborar en la definición y prueba de APIs.

Para que Postman (ejecutándose en tu computadora local) pueda alcanzar el servidor Flask que corre dentro de tu Codespace, necesitas **hacer público el puerto 5000**. Esto es necesario porque el Codespace es una máquina virtual en la nube, y por defecto sus puertos sólo son accesibles internamente.

#### 5.4.1 Cómo hacer público el puerto 5000 en GitHub Codespaces

1. En VS Code (dentro del Codespace), abre la pestaña **Ports** (Puertos), que aparece junto a la terminal.
2. Localiza el puerto **5000** en la lista (aparece automáticamente cuando Flask está corriendo).
3. Haz clic derecho sobre él y selecciona **Port Visibility → Public**.
4. Copia la URL pública que se genera (tiene la forma `https://<nombre-codespace>-5000.app.github.dev`).

> ⚠️ **Importante:** al hacer el puerto público, cualquier persona con la URL puede hacer peticiones a tu servidor. Esto es aceptable para propósitos de desarrollo y prueba, pero nunca dejes puertos públicos con credenciales reales o datos sensibles.

#### 5.4.2 Usar la URL pública en Postman

1. Abre Postman y crea una nueva petición.
2. Selecciona el método (GET, POST, etc.).
3. Pega la URL pública del Codespace seguida del endpoint, por ejemplo:
   ```
   https://<nombre-codespace>-5000.app.github.dev/jedi
   ```
4. Para peticiones POST o PUT, ve a la pestaña **Body**, selecciona **raw** y el tipo **JSON**, y escribe el cuerpo de la petición.
5. Haz clic en **Send** y observa la respuesta.

---

## 6. CORS: ¿Por qué es necesario en el backend?

Cuando el frontend (en el puerto `5173`) le hace una petición al backend (en el puerto `5000`), el navegador detecta que son **orígenes distintos** y bloquea la respuesta por seguridad. Esto se llama la política **Same-Origin Policy**.

**¿Qué es un "origen"?** Un origen se define por la combinación de esquema + dominio + puerto. Dos URLs tienen el mismo origen *sólo si los tres elementos son idénticos*:

| URL | Mismo origen que `http://localhost:5000`? |
|-----|---|
| `http://localhost:5000/jedi` | ✅ Sí |
| `http://localhost:5173/` | ❌ No (puerto diferente) |
| `https://localhost:5000/` | ❌ No (esquema diferente) |

Para permitir que el frontend consuma el backend desde cualquier origen, se habilitó CORS en Flask:

```python
from flask_cors import CORS
CORS(app, origins="*")   # Acepta peticiones de cualquier origen
```

Esto le agrega el encabezado `Access-Control-Allow-Origin: *` a todas las respuestas HTTP, indicándole al navegador que está bien recibir esas respuestas.

> **Nota para producción:** `origins="*"` es conveniente durante el desarrollo, pero en una aplicación real deberías especificar solo los dominios autorizados, por ejemplo: `origins=["https://mi-app.com"]`.

---

## 7. Flujo completo del sistema

Para consolidar todos los conceptos, el siguiente diagrama muestra cómo interactúan los componentes en este ejercicio:

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Codespace                      │
│                                                          │
│   ┌──────────────┐   HTTP/JSON   ┌──────────────────┐  │
│   │  curl /      │◄─────────────►│  ws_jedi.py      │  │
│   │  Postman     │               │  (Flask :5000)   │  │
│   └──────────────┘               └────────┬─────────┘  │
│                                           │             │
│                                    mysql-connector      │
│                                           │             │
│                                  ┌────────▼─────────┐  │
│                                  │  MySQL en Docker  │  │
│                                  │  (contenedor      │  │
│                                  │   puerto :3306)   │  │
│                                  └───────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

El flujo de una petición POST para crear un jedi es:

1. `curl` (o Postman) envía `POST /jedi` con body JSON al puerto 5000.
2. Flask recibe la petición, parsea el JSON con `request.get_json()`.
3. `ws_jedi.py` abre una conexión a MySQL usando `mysql-connector-python`.
4. Ejecuta `INSERT INTO jedi ...` y hace `conn.commit()`.
5. MySQL persiste el registro en disco y retorna el ID generado.
6. Flask construye una respuesta JSON `{"message": "Jedi creado", "id_jedi": N}` con código 201.
7. `curl` imprime la respuesta en la terminal.

---

## 8. Actividades

Una vez que tengas el ejercicio funcionando, te proponemos los siguientes retos para profundizar:

1. **Agrega un nuevo campo** a la tabla `jedi` (por ejemplo, `nivel_fuerza INT`) y modifica los endpoints de Flask para soportarlo.
2. **Implementa un endpoint de búsqueda**: `GET /jedi?nombre=luke` que filtre jedis por nombre usando `LIKE` en SQL.
3. **Manejo de errores mejorado**: qué pasa si insertas dos jedis con el mismo email? Captura el error de duplicado (`errno 1062`) y retorna un mensaje claro al cliente.
4. **Prueba con Postman Collections**: crea una colección en Postman con las 5 peticiones del CRUD y compártela con tus compañeros exportando el archivo JSON.
5. **Analiza los encabezados HTTP**: en Postman, revisa los *response headers* de cada petición. Identifica `Content-Type`, `Access-Control-Allow-Origin` y el código de estado HTTP.
