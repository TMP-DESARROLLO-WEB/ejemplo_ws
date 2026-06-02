# Ejemplo de servicios Web
Web services para probar como consumir ws desde react, este repositorio contiene los servicios web.

## Configuración de MySQL

### Iniciar la instancia de MySQL en Docker

Para iniciar una instancia de **MySQL** en un contenedor Docker, ejecuta el siguiente comando en la terminal de tu **GitHub Codespace**:

```sh
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=contrasena -e MYSQL_DATABASE=testdb -p 3306:3306 -d mysql:latest
```

### Conectarse al contenedor a través de la herramienta de linea de comandos
```sh
docker exec -i mysql-container mysql -u root -pcontrasena testdb < jedi.sql
```

Esto debe generar una tabla.

# Probar código python que se conecta a servidor

### Instala conector python-MySQL y flask
```sh
pip install mysql-connector-python flask flask-cors
```

### Explora el contenido del archivo crudMySQL.py
Observa como se conecta a la instancia base de datos que creaste al inicio de este ejercicio, usa las credenciales que se definieron cuando creaste el contenedor docker.

### En la terminal ejecuta
```sh
python crudMySQL.py
```
Esto creará un par de registros en la tabla

### Conectarse al contenedor a través de la herramienta de linea de comandos para verificar que se hayan insertado los datos
```sh
docker exec -it mysql-container mysql -u root -pcontrasena
```

Dentro de mysql:
```sql
USE testdb;
```

```sql
SELECT * from jedi;
```
Para salir escriba *quit* y presione enter


## Correr Servicios Web

Corre ws_jedi.py

``` Bash
python ws_jedi.py
```

Abrir otra terminal para probar los servicios web:

1) Servicio web para consultar todos los jedis (método GET). Deberás probarlo así:
``` Bash
curl -X GET http://localhost:5000/jedi
```
2) Servicio web para consultar solo un jedi (método GET). Deberás probarlo así:
``` Bash
curl -X GET http://localhost:5000/jedi/1
```
3) Servicio web para crear solo un jedi (método POST). Deberás probarlo así:
``` Bash
curl -X POST http://localhost:5000/jedi \
     -H "Content-Type: application/json" \
     -d '{"nombre_jedi": "yoda", "email_jedi": "yoda@gmail.com"}'
```

## CORS: ¿Por qué es necesario en el backend?

Cuando el frontend (en el puerto `5173`) le hace una petición al backend (en el puerto `5000`), el navegador detecta que son **orígenes distintos** y bloquea la respuesta por seguridad. Esto se llama la política **Same-Origin Policy**.

Para permitir que el frontend consuma el backend desde cualquier origen, se habilitó CORS en Flask:

```python
from flask_cors import CORS
CORS(app, origins="*")   # Acepta peticiones de cualquier origen
```

Esto le agrega el encabezado `Access-Control-Allow-Origin: *` a todas las respuestas HTTP, indicándole al navegador que está bien recibir esas respuestas.

> **Nota para producción:** `origins="*"` es conveniente durante el desarrollo, pero en una aplicación real deberías especificar solo los dominios autorizados, por ejemplo: `origins=["https://mi-app.com"]`.

---
