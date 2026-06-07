# fastapi-task-api

REST API de gestión de tareas con autenticación JWT. Demuestra FastAPI + Pydantic v2 + SQLAlchemy 2.0 + Alembic en una estructura lista para producción.

## Stack

- **FastAPI** 0.115 — framework async con OpenAPI automático
- **Pydantic v2** — validación y serialización de schemas
- **SQLAlchemy 2.0** — ORM con mapped_column y type hints nativos
- **Alembic** — migraciones de base de datos
- **python-jose + passlib** — JWT y hash de contraseñas
- **SQLite** — base de datos para desarrollo (fácilmente intercambiable con PostgreSQL)

## Cómo correrlo

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Arrancar (crea las tablas automáticamente en el primer inicio)
uvicorn app.main:app --reload
```

La documentación interactiva estará disponible en `http://localhost:8000/docs`.

## Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/auth/register` | — | Registrar usuario |
| POST | `/auth/token` | — | Login → JWT |
| GET | `/auth/me` | ✓ | Usuario actual |
| GET | `/tasks/` | ✓ | Listar tareas (paginado) |
| POST | `/tasks/` | ✓ | Crear tarea |
| GET | `/tasks/{id}` | ✓ | Detalle de tarea |
| PATCH | `/tasks/{id}` | ✓ | Actualizar (parcial) |
| DELETE | `/tasks/{id}` | ✓ | Eliminar |

## Decisiones técnicas

**SQLAlchemy 2.0 con mapped_column**: la API moderna de ORM usa type hints directamente en los modelos, eliminando la necesidad de `Column(...)` verboso y haciendo el tipado más preciso.

**Pydantic v2**: `model_dump(exclude_unset=True)` permite updates parciales sin tener que gestionar manualmente qué campos cambiar — el PATCH funciona con cero boilerplate.

**Lifespan en lugar de eventos deprecados**: `@app.on_event("startup")` está deprecado en FastAPI. Usar `asynccontextmanager` como lifespan es la forma correcta y moderna.

**Separación services/routes**: las rutas solo hacen parsing + delegación; los services tienen la lógica de negocio; los modelos son solo mapeado de datos. La dependencia es unidireccional.
