# 08 - QA y UAT

Propósito: verificar que la solución cumple los requisitos y está lista para
operar, y dejar evidencia reproducible de qué se ejecutó y qué queda pendiente.

## Contenidos

| Artefacto | Descripción |
|---|---|
| `estrategia-pruebas.md` | Enfoque, niveles, tipos, ambientes, datos, métricas y riesgos |
| `plan-uat.md` | Alcance, criterios de entrada/salida, calendario, roles y ejecución |
| `acta-cierre-uat.md` | Resultado real de la ejecución y decisión de cierre |
| `uat/cases.py` | Catálogo reproducible de 65 casos |
| `casos-prueba.csv` | Casos con ID, historia, precondiciones, pasos, datos y resultado |
| `casos-prueba-ado-testplans.csv` | Importación en Azure Test Plans (una fila por paso) |
| `casos-prueba.md` | Vista legible del catálogo y cobertura por tipo |
| `matriz-cobertura.csv` | Cobertura por historia y estado de automatización |
| `matriz-ejecucion.xlsx` | Workbook con resumen, casos, matriz, cobertura, defectos, pytest y SQL |
| `defectos.md` | Cinco defectos de ejemplo con severidad, pasos y evidencia |
| `scripts/run_uat.py` | Ejecuta pytest, consolida resultados y genera el workbook |
| `scripts/run_sql_controls.py` | Ejecuta las 23 consultas SQL de control |
| `scripts/build_cases.py` | Regenera CSV, Markdown y matriz de cobertura |
| `scripts/build_workbook.py` | Regenera el workbook desde los resultados |
| `tests/test_uat_boundaries.py` | Casos de borde UAT agregados en Fase 7 |
| `azure-pipelines.yml` | Pipeline de Azure DevOps |
| `../.github/workflows/ci.yml` | Workflow equivalente de GitHub Actions |
| `resultados/` | JUnit, JSON, CSV y salida de la última ejecución real |

## Resultado de la última ejecución (2026-10-29)

| Métrica | Resultado |
|---|---|
| Casos definidos | 65 |
| Casos automatizados aprobados | 51/51 (100 %) |
| Casos manuales pendientes | 6 |
| Casos no implementados | 8 |
| Pruebas pytest | 204/204 |
| Consultas SQL | 23/23 |
| `integrity_check` | `ok` |
| Violaciones de clave foránea | 0 |
| Defectos abiertos | 5 |

## Comandos

```powershell
# Regenerar el catálogo de casos
python 08-qa-uat\scripts\build_cases.py

# Ejecutar UAT completa (pytest + SQL + Excel)
python 08-qa-uat\scripts\run_uat.py

# Solo controles SQL
python 08-qa-uat\scripts\run_sql_controls.py

# Suite completa
python -m pytest -q
```

## Estado

**Fase 7 completada a nivel artefacto y ejecución automatizada.**

Pendiente del autor:

- UAT manual de herramientas externas (EV-001 a EV-011).
- Ejecución de los pipelines en Azure DevOps y GitHub Actions (EV-009, EV-010).
- Publicación del post de LinkedIn (EV-011).

> Los casos manuales y no implementados no se declaran ejecutados. Los resultados
> son locales y reproducibles, no de producción.
