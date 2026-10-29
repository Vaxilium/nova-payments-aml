# Base de datos del core simulado

- `schema.sql`: DDL del modelo, índices y triggers de integridad contable.
- `drop.sql`: eliminación ordenada de objetos.
- `novabank.db`: base generada localmente por el seed. **No se versiona** (`*.db` en `.gitignore`).
- `seed_report.json`: resumen opcional generado por el seed. Tampoco se versiona.

## Regeneración

```powershell
.\.venv\Scripts\python.exe 05-core-middleware\scripts\seed.py --reset
```

Semilla fija por defecto: `NOVABANK_SEED=20261027`.
