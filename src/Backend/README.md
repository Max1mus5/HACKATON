# Backend para Chatbot LEAN

## Estructura

- `api.py`: Entrypoint de la API FastAPI.
- `database.py`: Configuración de la base de datos y ORM.
- `models/`: Modelos SQLAlchemy.
- `schemas/`: Esquemas Pydantic.
- `repositories/`: Lógica de acceso a datos.
- `requirements.txt`: Dependencias Python.

## Uso rápido

1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta la API:
   ```bash
   uvicorn api:app --reload
   ```

La base de datos SQLite se crea automáticamente en la carpeta `Backend`.
