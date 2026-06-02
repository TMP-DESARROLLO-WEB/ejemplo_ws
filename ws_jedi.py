from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app, origins="*")  # Permite peticiones desde cualquier origen

# ─── Configuración de la base de datos ───────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "contrasena",
    "database": "testdb"
}


def get_connection():
    """Crea y retorna una conexión a MySQL."""
    return mysql.connector.connect(**DB_CONFIG)


# ─── CREATE ───────────────────────────────────────────────────────────────────
@app.route("/jedi", methods=["POST"])
def create_jedi():
    """
    Crea un nuevo Jedi.
    Body JSON esperado:
        { "nombre_jedi": "Obi-Wan Kenobi", "email_jedi": "obi@jedi.org" }
    """
    data = request.get_json()

    nombre = data.get("nombre_jedi")
    email  = data.get("email_jedi")

    if not nombre or not email:
        return jsonify({"error": "nombre_jedi y email_jedi son obligatorios"}), 400

    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO jedi (nombre_jedi, email_jedi) VALUES (%s, %s)",
            (nombre, email)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        return jsonify({"message": "Jedi creado", "id_jedi": nuevo_id}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ─── READ ALL ─────────────────────────────────────────────────────────────────
@app.route("/jedi", methods=["GET"])
def get_all_jedi():
    """Retorna la lista completa de Jedis."""
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jedi")
        jedis = cursor.fetchall()
        return jsonify(jedis), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ─── READ ONE ─────────────────────────────────────────────────────────────────
@app.route("/jedi/<int:id_jedi>", methods=["GET"])
def get_jedi(id_jedi):
    """Retorna un Jedi por su ID."""
    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jedi WHERE id_jedi = %s", (id_jedi,))
        jedi = cursor.fetchone()

        if not jedi:
            return jsonify({"error": "Jedi no encontrado"}), 404

        return jsonify(jedi), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ─── UPDATE ───────────────────────────────────────────────────────────────────
@app.route("/jedi/<int:id_jedi>", methods=["PUT"])
def update_jedi(id_jedi):
    """
    Actualiza nombre y/o email de un Jedi.
    Body JSON esperado (uno o ambos campos):
        { "nombre_jedi": "Anakin Skywalker", "email_jedi": "anakin@sith.org" }
    """
    data   = request.get_json()
    nombre = data.get("nombre_jedi")
    email  = data.get("email_jedi")

    if not nombre and not email:
        return jsonify({"error": "Se debe enviar al menos nombre_jedi o email_jedi"}), 400

    campos = []
    valores = []

    if nombre:
        campos.append("nombre_jedi = %s")
        valores.append(nombre)
    if email:
        campos.append("email_jedi = %s")
        valores.append(email)

    valores.append(id_jedi)

    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE jedi SET {', '.join(campos)} WHERE id_jedi = %s",
            tuple(valores)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Jedi no encontrado"}), 404

        return jsonify({"message": "Jedi actualizado"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ─── DELETE ───────────────────────────────────────────────────────────────────
@app.route("/jedi/<int:id_jedi>", methods=["DELETE"])
def delete_jedi(id_jedi):
    """Elimina un Jedi por su ID."""
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jedi WHERE id_jedi = %s", (id_jedi,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Jedi no encontrado"}), 404

        return jsonify({"message": "Jedi eliminado"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


# ─── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
