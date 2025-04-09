# 📦 ETL DEVOPS

Este projeto inicialmente consome dados (via API) de uma organização do Azure Devops os transforma e armazena em tabelas do SQLite separados por:

- Epic
- Feature
- User Story
- Taks

---

## 🧰 Pré-requisitos

- Python 3.12 ou superior
- [Git](https://git-scm.com/)
- [Poetry](https://python-poetry.org/)
- [SQlite3]()
- [Requests]()
- [dotenv]()

---

## 🚀 Como rodar este projeto

### 1. Clone o repositório:
```bash
git clone https://github.com/poso-douglas/ETL_DEVOPS.git
cd ETL_DEVOPS
```

### 2. Instale o Poetry
#### 2.1 Via bash
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
#### 2.2 Via cmd
```cmd
Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```
#### 2.3 Via powershell
```powershell
(Invoke-WebRequest https://install.python-poetry.org -UseBasicParsing).Content | py -
```

3. Instale as dependencias
```bash
poetry install
```

4. Rode o projeto:
```bash
poetry run python src/main.py
```

