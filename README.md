# TaskManager — Sistema de Gerenciamento de Tarefas

![CI](https://github.com/SEU_USUARIO/taskmanager/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)

##  Objetivo do Projeto

O TaskManager é um sistema web de gerenciamento de tarefas desenvolvido com Python/Flask, com API RESTful completa (CRUD). O projeto foi criado como parte da disciplina de Engenharia de Software, aplicando metodologias ágeis, versionamento com Git/GitHub, testes automatizados e integração contínua.

---

##  Escopo Inicial

O sistema foi planejado para oferecer:

- Criação, leitura, atualização e exclusão (CRUD) de tarefas
- Filtros por status (`pending`, `in_progress`, `done`) e prioridade (`low`, `medium`, `high`)
- Persistência em banco de dados SQLite
- API REST documentada
- Pipeline de CI com GitHub Actions

---

##  Mudança de Escopo

Justificativa: Durante o desenvolvimento (Sprint 2), identificou-se que os usuários precisavam de controle de acesso básico para separar tarefas por responsável. Por isso, foi adicionada a tabela `users` ao banco de dados.

Esta mudança foi refletida no quadro Kanban com a criação de novos cards e um commit dedicado.

---

##  Metodologia

O projeto adota Kanban como metodologia ágil principal, com o quadro no GitHub Projects organizado em três colunas: A Fazer, Em progresso, Conclúido

---

##  Estrutura de Diretórios

```
taskmanager/
├── src/
│   ├── app.py          # Aplicação Flask principal (rotas e CRUD)
│   └── models.py       # Validações e lógica de negócio
├── tests/
│   ├── test_tasks.py   # Testes de integração das rotas
│   └── test_models.py  # Testes unitários de validação
├── docs/               # Diagramas UML e documentação
├── .github/
│   └── workflows/
│       └── ci.yml      # Pipeline GitHub Actions
├── requirements.txt
└── README.md
```

---

##  Como Executar

### Pré-requisitos

- Python 3.11+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/TechFlow.git
cd TechFlow

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python src/app.py
```

A API estará disponível em `http://localhost:5000`.

---

# Utilização local

Para testar os endpoints da API, recomenda-se o uso do **Thunder Client**,

### Instalação
1. Abra o VS Code
2. Vá em Extensões e pesquise **Thunder Client**
3. Clique em Instalar

### Configuração das requisições
Em toda requisição que enviar dados (POST e PUT), adicione o header:
- **Content-Type**: `application/json`

### Exemplos de uso
| Método | URL | Descrição |
|--------|-----|-----------|
| GET | `http://127.0.0.1:5000/tasks` | Lista todas as tarefas |
| GET | `http://127.0.0.1:5000/tasks/1` | Busca tarefa por ID |
| POST | `http://127.0.0.1:5000/tasks` | Cria nova tarefa |
| PUT | `http://127.0.0.1:5000/tasks/1` | Atualiza tarefa |
| DELETE | `http://127.0.0.1:5000/tasks/1` | Remove tarefa |

##  Executar Testes

```bash
pytest tests/ -v
```

Os testes cobrem:
- Criação de tarefas (válidas e inválidas)
- Listagem e filtros
- Atualização parcial e completa
- Remoção
- Validações de modelo

---

##  Integração Contínua (GitHub Actions)

O pipeline em `.github/workflows/ci.yml` é disparado a cada push/PR e executa:

1. **Job `test`** — roda `pytest` com relatório XML
2. **Job `lint`** — verifica qualidade do código com `flake8`

---
