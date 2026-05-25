
#TaskManager - Sistema de Gerenciamento de Tarefas


from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# Caminho do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")


def get_db():
   
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            priority TEXT NOT NULL DEFAULT 'medium',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()




@app.route("/tasks", methods=["GET"])
def get_tasks():

    status = request.args.get("status")
    priority = request.args.get("priority")

    conn = get_db()
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if priority:
        query += " AND priority = ?"
        params.append(priority)

    query += " ORDER BY created_at DESC"
    tasks = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict(t) for t in tasks]), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
  
    conn = get_db()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()

    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    return jsonify(dict(task)), 200


@app.route("/tasks", methods=["POST"])
def create_task():
   
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "O campo 'title' é obrigatório"}), 400

    title = data["title"].strip()
    if len(title) < 3:
        return jsonify({"error": "O título deve ter pelo menos 3 caracteres"}), 400

    valid_statuses = ["pending", "in_progress", "done"]
    valid_priorities = ["low", "medium", "high"]

    status = data.get("status", "pending")
    priority = data.get("priority", "medium")

    if status not in valid_statuses:
        return jsonify({"error": f"Status inválido. Use: {valid_statuses}"}), 400
    if priority not in valid_priorities:
        return jsonify({"error": f"Prioridade inválida. Use: {valid_priorities}"}), 400

    now = datetime.utcnow().isoformat()
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO tasks (title, description, status, priority, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        (title, data.get("description", ""), status, priority, now, now)
    )
    conn.commit()
    task_id = cursor.lastrowid
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()

    return jsonify(dict(task)), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
  
    conn = get_db()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if not existing:
        conn.close()
        return jsonify({"error": "Tarefa não encontrada"}), 404

    data = request.get_json()
    if not data:
        conn.close()
        return jsonify({"error": "Nenhum dado enviado"}), 400

    valid_statuses = ["pending", "in_progress", "done"]
    valid_priorities = ["low", "medium", "high"]

    title = data.get("title", existing["title"])
    description = data.get("description", existing["description"])
    status = data.get("status", existing["status"])
    priority = data.get("priority", existing["priority"])

    if status not in valid_statuses:
        conn.close()
        return jsonify({"error": f"Status inválido. Use: {valid_statuses}"}), 400
    if priority not in valid_priorities:
        conn.close()
        return jsonify({"error": f"Prioridade inválida. Use: {valid_priorities}"}), 400

    now = datetime.utcnow().isoformat()
    conn.execute(
        "UPDATE tasks SET title=?, description=?, status=?, priority=?, updated_at=? WHERE id=?",
        (title, description, status, priority, now, task_id)
    )
    conn.commit()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()

    return jsonify(dict(task)), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
  
    conn = get_db()
    existing = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if not existing:
        conn.close()
        return jsonify({"error": "Tarefa não encontrada"}), 404

    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Tarefa {task_id} removida com sucesso"}), 200



@app.route("/health", methods=["GET"])
def health_check():
    """Verifica se a aplicação está rodando corretamente."""
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()}), 200



if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
