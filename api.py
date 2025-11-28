#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": "localhost",
    "user": "mqtt_user",
    "password": "",   # <-- sinun salasana
    "database": "mqtt_chat"
}

@app.route('/api/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        """Hae viestit tietokannasta."""
        limit = request.args.get('limit', 50, type=int)
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT id, nickname, message, client_id, created_at
            FROM messages ORDER BY created_at DESC LIMIT %s
        ''', (limit,))
        messages = cursor.fetchall()
        for msg in messages:
            msg['created_at'] = msg['created_at'].isoformat()
        cursor.close()
        conn.close()
        return jsonify(messages[::-1])

    elif request.method == 'POST':
        """Tallenna uusi viesti tietokantaan."""
        data = request.get_json()
        nickname = data.get("nickname", "Anonyymi")
        message = data.get("message", "")
        client_id = data.get("client_id", "web_" + str(datetime.now().timestamp()))

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (nickname, message, client_id, created_at)
            VALUES (%s, %s, %s, %s)
        ''', (nickname, message, client_id, datetime.now()))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "ok", "nickname": nickname, "message": message}), 201

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
