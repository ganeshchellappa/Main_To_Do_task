from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import re
import requests
from translate import translate_text, LANG_CODES


load_dotenv()

app = Flask(__name__)

DB_HOST = os.getenv("NEON_HOST")
DB_PORT = os.getenv("NEON_PORT", 5432)
DB_NAME = os.getenv("NEON_DB")
DB_USER = os.getenv("NEON_USER")
DB_PASSWORD = os.getenv("NEON_PASSWORD")

def get_db_connection():
    conn_str = os.getenv("NEON_CONN_STRING")
    conn = psycopg2.connect(conn_str, sslmode='require')
    return conn

@app.route('/db_test')
def db_test():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result and result[0] == 1:
            return "Database connection is successful!"
        else:
            return "Unexpected result from DB.", 500
    except Exception as e:
        return f"Database connection failed: {e}", 500


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, task_text, completed FROM tasks ORDER BY id;")
    tasks_data = cur.fetchall()
    print("all the data in db",tasks_data)
    cur.close()
    conn.close()

    # Convert tasks to dict list with keys matching your HTML template
    tasks = [{"id": t[0], "description": t[1], "completed": t[2]} for t in tasks_data]
    # print("tasks", tasks)

    # Example languages for translation dropdown
    languages = ["English", "Hindi", "Spanish", "French", "German"]

    return render_template("index.html", tasks=tasks, languages=languages)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, task_text, completed FROM tasks ORDER BY id;")
    tasks = cur.fetchall()
    print("get method task:",tasks)
    cur.close()
    conn.close()
    tasks_list = [{"id": t[0], "task": t[1], "completed": t[2]} for t in tasks]
    return jsonify(tasks_list)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    task_text = data.get('task')
    if not task_text:
        return jsonify({"error": "Task text is required"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task_text) VALUES (%s) RETURNING id;", (task_text,))
    task_id = cur.fetchone()[0]
    print("task_id", task_id)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": task_id, "task": task_text, "completed": False}), 201

@app.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed = TRUE WHERE id = %s;", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"Task {task_id} marked as completed."})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": f"Task {task_id} deleted."})


@app.route('/tasks/<int:task_id>/translate', methods=['POST'])
def translate_task(task_id):
    data = request.json
    target_lang = data.get("target_lang")
    if not target_lang:
        return jsonify({"error": "Target language is required"}), 400

    # Fetch the original task text from DB
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT task_text FROM tasks WHERE id = %s;", (task_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Task not found"}), 404

    original_text = row[0]
    print("original text", original_text)
    print("target language", target_lang)

    # Call your translation function here
    translated_text = translate_text(original_text, target_lang)

    return jsonify({"translated_text": translated_text})


if __name__ == "__main__":
    app.run(debug=True)
