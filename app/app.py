import os

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def get_database_connection():
    return psycopg2.connect(
        host=os.getenv("DATABASE_HOST", "localhost"),
        port=os.getenv("DATABASE_PORT", "5432"),
        database=os.getenv("DATABASE_NAME", "capstone"),
        user=os.getenv("DATABASE_USER", "capstone"),
        password=os.getenv("DATABASE_PASSWORD", "capstonepassword")
    )


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cloud Deployment Capstone</title>
    </head>
    <body>
        <h1>Cloud Deployment Capstone</h1>
        <p>Application successfully running.</p>
        <p>Environment: Docker + PostgreSQL</p>
        <p><a href="/health">Check Application Health</a></p>
        <p><a href="/database">Check Database Connection</a></p>
    </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/database")
def database():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT version();")
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return jsonify({
            "status": "connected",
            "database": "PostgreSQL",
            "version": result[0]
        }), 200

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)