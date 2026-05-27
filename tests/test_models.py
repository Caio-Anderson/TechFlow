
#tests/test_models.py - Testes unitários para as funções de validação.


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from models import validate_task_data


class TestValidateTaskData:
    def test_valid_data_passes(self):
        """Dados válidos não devem gerar erros."""
        is_valid, msg = validate_task_data({
            "title": "Tarefa válida",
            "status": "pending",
            "priority": "high"
        })
        assert is_valid is True
        assert msg == ""

    def test_missing_title_fails(self):
        """Ausência de título deve falhar na validação."""
        is_valid, msg = validate_task_data({})
        assert is_valid is False
        assert "title" in msg.lower()

    def test_title_too_short_fails(self):
        """Título curto deve falhar na validação."""
        is_valid, msg = validate_task_data({"title": "ab"})
        assert is_valid is False

    def test_invalid_status_fails(self):
        """Status inválido deve falhar na validação."""
        is_valid, msg = validate_task_data({
            "title": "Tarefa ok",
            "status": "nao_existe"
        })
        assert is_valid is False
        assert "status" in msg.lower()

    def test_invalid_priority_fails(self):
        """Prioridade inválida deve falhar na validação."""
        is_valid, msg = validate_task_data({
            "title": "Tarefa ok",
            "priority": "ultra"
        })
        assert is_valid is False
        assert "prioridade" in msg.lower()

    def test_optional_title_with_flag(self):
        """Com require_title=False, dados sem título devem passar."""
        is_valid, msg = validate_task_data(
            {"status": "done"},
            require_title=False
        )
        assert is_valid is True
