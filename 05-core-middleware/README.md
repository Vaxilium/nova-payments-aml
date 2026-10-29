# 05 — Core bancario y middleware

Propósito: demostrar el núcleo funcional del caso con datos sintéticos,
contabilidad por partida doble y una API REST probada.

Estado: **Fase 3 completada** (2026-10-28).

## Contenido

| Ruta | Descripción |
|---|---|
| `db/schema.sql` | DDL, constraints, índices y triggers contables. |
| `db/drop.sql` | Limpieza ordenada del esquema. |
| `scripts/seed.py` | Generador reproducible: 500 clientes, ~800 cuentas y ~50.000 movimientos en 6 meses. |
| `scripts/close_day.py` | Cierre diario de saldos. |
| `scripts/export_openapi.py` | Exporta el contrato a `openapi.yaml`. |
| `app/` | API FastAPI `/v1`, servicio, libro mayor, middleware y auditoría. |
| `sql/` | 23 consultas de operación y control con CTEs y window functions. |
| `tests/` | Suite pytest de invariantes, API, idempotencia y concurrencia. |
| `openapi.yaml` | Contrato OpenAPI 3.1. |

## Comandos

```powershell
# Base sintética (semilla fija 20261027)
.\.venv\Scripts\python.exe 05-core-middleware\scripts\seed.py --reset

# API
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir 05-core-middleware --reload

# Contrato
.\.venv\Scripts\python.exe 05-core-middleware\scripts\export_openapi.py

# Pruebas
.\.venv\Scripts\python.exe -m pytest -q
```

- Documentación conceptual: [`docs/core-y-middleware.md`](../docs/core-y-middleware.md).
- La base `*.db` está ignorada por git y se regenera con el seed.
- Sin PII real: todos los nombres, documentos, cuentas y movimientos son ficticios.
