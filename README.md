# Log Aggregator API 

Um sistema centralizado de agregação e monitoramento de logs em tempo real, desenvolvido em Python com **FastAPI** e **SQLAlchemy**. O objetivo deste projeto é simular uma ferramenta corporativa de auditoria onde múltiplos microserviços enviam seus logs de erro e operação para um único ponto central, permitindo consultas filtradas e métricas rápidas.

---

## Tecnologias Utilizadas
* **Python 3.11+**
* **FastAPI** (Framework web de alta performance)
* **SQLAlchemy** (ORM para gerenciamento de banco de dados relacional)
* **SQLite** (Banco de dados leve e embutido)
* **Uvicorn** (Servidor ASGI)

---

## Estrutura do Projeto
```text
log-aggregator/
│── database.py      # Configuração da conexão com o SQLite
│── models.py        # Definição da tabela de Logs (SQLAlchemy)
│── main.py          # Rotas da API (FastAPI) e regras de negócio
│── requirements.txt # Dependências do projeto
└── README.md        # Documentação do projeto
