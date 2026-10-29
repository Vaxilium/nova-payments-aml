# 07 — AML y compliance

Ciclo AML integrado del caso NovaBank: conocer al cliente, monitorear, investigar y reportar.

## Contenido

| Área | Artefacto | Estado |
|---|---|---|
| KYC/CDD | Scoring 0–100, factores, EDD y persistencia | Implementado y probado |
| Reglas SQL | R01–R12 sobre el dataset de Fase 3 | Implementadas y calibradas |
| Screening | Listas ficticias, Jaro-Winkler y decisión BLOCK/REVIEW | Implementado y probado |
| Alertas | Deduplicación, score y prioridad P1/P2/P3 | Implementado y probado |
| Casos y SLA | Transiciones, asignación, escalamiento y cierre | Implementado y probado |
| Evaluación | Métricas contra `_aml_ground_truth` | Generadas |
| ROS | Plantilla y dos casos ficticios | Documentado |
| Normativa | Mapeo SEPRELAD/GAFI | Documentado con fuentes |
| Integración | Hook AML del simulador internacional | Implementado y probado |

## Estructura

```text
07-aml-compliance/
├─ aml/                  # kyc, screening, rules, alerts, workflow, evaluation, hook
├─ data/                 # parámetros, listas ficticias y países de riesgo
├─ docs/                 # enfoque, reglas, screening, alertas, ROS, normativa, evaluación
├─ scripts/              # setup_aml.py, evaluate_rules.py
├─ sql/rules/            # R01–R12
└─ tests/                # pruebas positivas y negativas
```

## Comandos

```powershell
# Inicializar esquema AML, perfiles y reglas sobre la base del core
.\.venv\Scripts\python.exe 07-aml-compliance\scripts\setup_aml.py --db 05-core-middleware\db\novabank.db

# Generar el reporte de evaluación
.\.venv\Scripts\python.exe 07-aml-compliance\scripts\evaluate_rules.py --db 05-core-middleware\db\novabank.db

# Pruebas de la fase
.\.venv\Scripts\python.exe -m pytest 07-aml-compliance/tests -q
```

## Resultado de la calibración

- 494 transacciones alertadas.
- 341 verdaderos positivos, 3 falsos positivos etiquetados y 150 alertadas sin etiqueta.
- Precisión sobre etiquetadas: 99,13 %; precisión conservadora: 69,03 %.
- Recall: 100 % sobre las 341 operaciones sospechosas.
- Cobertura completa de los cinco patrones etiquetados.

El detalle está en [`docs/evaluacion-verdad.md`](docs/evaluacion-verdad.md).

## Regla de honestidad

Las listas de sanciones, PEP y países son ficticias. Los umbrales y SLA son parámetros de diseño, no disposiciones regulatorias. No se presentó ningún ROS ante una autoridad real. Las limitaciones se registran en `docs/PENDIENTES.md` y `docs/SUPUESTOS.md`.

## Documentos

- [Enfoque basado en riesgo](docs/enfoque-riesgo.md)
- [Reglas de monitoreo](docs/reglas-monitoreo.md)
- [Screening](docs/screening.md)
- [Alertas, casos y SLA](docs/alertas-casos-sla.md)
- [ROS](docs/ros.md)
- [Mapeo normativo](docs/mapeo-normativo.md)
- [Evaluación contra la verdad](docs/evaluacion-verdad.md)
