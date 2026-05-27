
#tests/test_tasks.py - Testes unitários para o sistema de gerenciamento de tarefas


import pytest
import sys
import os

# Adiciona o diretório src ao path para importar o app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from app import app, init_db, DB_PATH


@pytest.fixture
def client(tmp_path):
   
    # Redireciona DB para pasta temporária
    test_db = str(tmp_path / "test_tasks.db")

    import app as app_module
    original_db = app_module.DB_PATH
    app_module.DB_PATH = test_db

    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    app_module.DB_PATH = original_db




class TestHealthCheck:
    def test_health_returns_ok(self, client):
      
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert "timestamp" in data



class TestCreateTask:
    def test_create_task_success(self, client):
      
        response = client.post("/tasks", json={
            "title": "Estudar Flask",
            "description": "Revisar documentação oficial",
            "priority": "high"
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data["title"] == "Estudar Flask"
        assert data["status"] == "pending"
        assert data["priority"] == "high"
        assert "id" in data

    def test_create_task_without_title_fails(self, client):
        """Garante erro 400 ao criar tarefa sem título."""
        response = client.post("/tasks", json={"description": "sem título"})
        assert response.status_code == 400
        assert "title" in response.get_json()["error"].lower()

    def test_create_task_title_too_short_fails(self, client):
        """Título com menos de 3 caracteres deve retornar erro."""
        response = client.post("/tasks", json={"title": "AB"})
        assert response.status_code == 400

    def test_create_task_invalid_status_fails(self, client):
        """Status inválido deve retornar erro 400."""
        response = client.post("/tasks", json={
            "title": "Tarefa teste",
            "status": "invalido"
        })
        assert response.status_code == 400

    def test_create_task_invalid_priority_fails(self, client):
        """Prioridade inválida deve retornar erro 400."""
        response = client.post("/tasks", json={
            "title": "Tarefa teste",
            "priority": "urgente"
        })
        assert response.status_code == 400

    def test_create_task_default_values(self, client):
        """Verifica valores padrão ao criar tarefa sem status/prioridade."""
        response = client.post("/tasks", json={"title": "Tarefa simples"})
        data = response.get_json()
        assert data["status"] == "pending"
        assert data["priority"] == "medium"



class TestGetTasks:
    def test_get_all_tasks_empty(self, client):
     
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.get_json() == []

    def test_get_all_tasks_with_data(self, client):
       
        client.post("/tasks", json={"title": "Tarefa 1"})
        client.post("/tasks", json={"title": "Tarefa 2"})
        response = client.get("/tasks")
        assert response.status_code == 200
        assert len(response.get_json()) == 2

    def test_get_task_by_id(self, client):
       
        create = client.post("/tasks", json={"title": "Tarefa específica"})
        task_id = create.get_json()["id"]

        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert response.get_json()["title"] == "Tarefa específica"

    def test_get_nonexistent_task(self, client):
      
        response = client.get("/tasks/9999")
        assert response.status_code == 404

    def test_filter_tasks_by_status(self, client):
      
        client.post("/tasks", json={"title": "Pendente", "status": "pending"})
        client.post("/tasks", json={"title": "Em progresso", "status": "in_progress"})

        response = client.get("/tasks?status=pending")
        tasks = response.get_json()
        assert len(tasks) == 1
        assert tasks[0]["status"] == "pending"




class TestUpdateTask:
    def test_update_task_success(self, client):
  
        create = client.post("/tasks", json={"title": "Tarefa original"})
        task_id = create.get_json()["id"]

        response = client.put(f"/tasks/{task_id}", json={
            "title": "Tarefa atualizada",
            "status": "in_progress"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data["title"] == "Tarefa atualizada"
        assert data["status"] == "in_progress"

    def test_update_nonexistent_task(self, client):
        
        response = client.put("/tasks/9999", json={"title": "Nova"})
        assert response.status_code == 404

    def test_update_task_invalid_status(self, client):
        """Atualização com status inválido deve retornar 400."""
        create = client.post("/tasks", json={"title": "Tarefa"})
        task_id = create.get_json()["id"]

        response = client.put(f"/tasks/{task_id}", json={"status": "errado"})
        assert response.status_code == 400


class TestDeleteTask:
    def test_delete_task_success(self, client):
      
        create = client.post("/tasks", json={"title": "Para deletar"})
        task_id = create.get_json()["id"]

        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 200

        # Confirma que foi removida
        get = client.get(f"/tasks/{task_id}")
        assert get.status_code == 404

    def test_delete_nonexistent_task(self, client):
        """Deletar tarefa inexistente deve retornar 404."""
        response = client.delete("/tasks/9999")
        assert response.status_code == 404
