# Alertas, casos y SLA

## 1. Generación y deduplicación

Cada coincidencia de una regla se convierte en una alerta. La clave de deduplicación es:

```text
rule_id + customer_id + account_id + fecha de la operación
```

Si dos operaciones de la misma regla, cliente, cuenta y día generan coincidencia, se actualiza la misma alerta: se incrementa `transaction_count`, se conserva el mayor `risk_score` y se actualiza `last_seen_at`. Así se evita una bandeja inflada por operaciones repetidas del mismo patrón.

Implementación: `07-aml-compliance/aml/alerts.py`.

## 2. Score y prioridad

El score parte de la severidad de la regla (`RULE_META.base_score`) y suma hasta 5 puntos según el score KYC del cliente. La prioridad se deriva del score:

| Score | Prioridad |
|---:|---|
| ≥ 80 | P1 |
| 50–79 | P2 |
| < 50 | P3 |

## 3. SLA

| Prioridad | Asignación | Cierre | Fundamento |
|---|---:|---:|---|
| P1 | 15 minutos | 10 días hábiles | Caso ficticio de riesgo alto. |
| P2 | 240 minutos | 15 días hábiles | Caso ficticio de riesgo medio. |
| P3 | 1.440 minutos | 20 días hábiles | Caso ficticio de riesgo bajo. |

Los SLA son parámetros internos (`SNV-08`) y no plazos regulatorios. El cálculo de días hábiles excluye sábados y domingos; no modela feriados.

## 4. Estados

### Alertas

```text
NUEVA → EN_ANALISIS → ESCALADA → REPORTADA
   ↘          ↘              ↘
    CERRADA_FALSO_POSITIVO ←──┘
```

Transiciones permitidas:

- `NUEVA`: `EN_ANALISIS`, `ESCALADA`, `CERRADA_FALSO_POSITIVO`.
- `EN_ANALISIS`: `ESCALADA`, `CERRADA_FALSO_POSITIVO`, `REPORTADA`.
- `ESCALADA`: `EN_ANALISIS`, `CERRADA_FALSO_POSITIVO`, `REPORTADA`.
- `CERRADA_FALSO_POSITIVO` y `REPORTADA`: estados terminales.

### Casos

```text
ABIERTO → EN_ANALISIS → ESCALADO → REPORTADO
    ↘          ↘            ↘
     └──────────→ CERRADO ←─┘
```

Cada transición se registra en `aml_workflow_transitions` con estado origen, estado destino, analista, motivo y fecha.

## 5. Operación

1. **Asignación:** `assign_alert` asigna analista, calcula `due_at` y pasa la alerta a `EN_ANALISIS` si estaba `NUEVA`.
2. **Escalamiento:** `escalate_alert` crea un caso, vincula la alerta y cambia su estado a `ESCALADA`.
3. **Cierre:** `close_alert_as_false_positive` exige un motivo y deja la alerta en `CERRADA_FALSO_POSITIVO`.
4. **Caso:** `create_case` calcula el vencimiento en días hábiles y toma el mayor riesgo de las alertas vinculadas.
5. **Reporte:** un caso con ROS se marca `REPORTADO`; el ROS se documenta en `ros.md`.

Implementación: `07-aml-compliance/aml/workflow.py`.

## 6. Bandeja y métricas

Consultas disponibles:

- `list_alerts(status, priority, customer_id, limit)`.
- `count_alerts()`: total y conteo por prioridad.
- `list_cases(status, limit)`.
- `case_alerts(case_id)`.

En el dataset de calibración se generan 775 alertas únicas a partir de 1.326 coincidencias de reglas (la diferencia corresponde a deduplicación diaria). La evaluación de transacciones alertadas reporta 494 transacciones únicas: 341 verdaderas positivas, 3 falsas positivas y 150 sin etiqueta.

## 7. Limitaciones

- No hay autenticación, autorización por rol ni interfaz web; el flujo se demuestra por código y pruebas.
- Los feriados no se descuentan del SLA.
- La asignación es manual o por parámetro; no hay balanceo automático de carga.
- La bandeja no reemplaza un case management comercial.
