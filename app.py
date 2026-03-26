from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Flask + PostgreSQL in Docker! 🐳'

@app.route('/db-test')
def db_test():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'db'),
            database=os.getenv('DB_NAME', 'appdb'),
            user=os.getenv('DB_USER', 'user'),
            password=os.getenv('DB_PASSWORD', 'password')
        )
        conn.close()
        return jsonify({'status': 'DB Connected!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)