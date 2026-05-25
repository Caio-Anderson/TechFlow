
#models.py - Funções de validação e lógica de negócio para tarefas.


VALID_STATUSES = ["pending", "in_progress", "done"]
VALID_PRIORITIES = ["low", "medium", "high"]


def validate_task_data(data: dict, require_title: bool = True) -> tuple[bool, str]:

    if require_title:
        if not data.get("title"):
            return False, "O campo 'title' é obrigatório"
        if len(data["title"].strip()) < 3:
            return False, "O título deve ter pelo menos 3 caracteres"

    if "status" in data and data["status"] not in VALID_STATUSES:
        return False, f"Status inválido. Use: {VALID_STATUSES}"

    if "priority" in data and data["priority"] not in VALID_PRIORITIES:
        return False, f"Prioridade inválida. Use: {VALID_PRIORITIES}"

    return True, ""


def format_task(task_row) -> dict:

    return {
        "id": task_row["id"],
        "title": task_row["title"],
        "description": task_row["description"] or "",
        "status": task_row["status"],
        "priority": task_row["priority"],
        "created_at": task_row["created_at"],
        "updated_at": task_row["updated_at"],
    }
