# Evaluación de reglas contra la verdad de Fase 3

Generado: 2026-10-29T04:04:23+00:00

## Resumen

| Métrica | Valor |
|---|---:|
| Transacciones totales | 49.582 |
| Transacciones etiquetadas | 833 |
| Sospechosas (truth) | 341 |
| Normales muestreadas (truth) | 492 |
| Transacciones alertadas | 494 |
| Verdaderos positivos | 341 |
| Falsos positivos | 3 |
| Falsos negativos | 0 |
| Alertadas sin etiqueta | 150 |
| Precisión (solo etiquetadas) | 99.1% |
| Precisión conservadora (no etiquetadas = FP) | 69.0% |
| Recall | 100.0% |
| F1 | 0.9956 |

## Detalle por regla

| Regla | Nombre | Alertadas | TP | FP | FN | Sin etiqueta | Precisión | Precisión conservadora | Recall | F1 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R01 | Estructuración por debajo del umbral | 100 | 100 | 0 | 241 | 0 | 100.0% | 100.0% | 29.3% | 0.4536 |
| R02 | Velocidad transaccional por cantidad | 67 | 67 | 0 | 274 | 0 | 100.0% | 100.0% | 19.7% | 0.3285 |
| R03 | Velocidad transaccional por monto | 67 | 67 | 0 | 274 | 0 | 100.0% | 100.0% | 19.7% | 0.3285 |
| R04 | Cuenta de paso (entrada y salida rápida) | 160 | 96 | 1 | 245 | 63 | 99.0% | 60.0% | 28.1% | 0.4383 |
| R05 | Depósitos redondos reiterados | 75 | 75 | 0 | 266 | 0 | 100.0% | 100.0% | 22.0% | 0.3605 |
| R06 | Reactivación de cuenta inactiva | 29 | 29 | 0 | 312 | 0 | 100.0% | 100.0% | 8.5% | 0.1567 |
| R07 | Jurisdicción de alto riesgo | 0 | 0 | 0 | 341 | 0 | 0.0% | 0.0% | 0.0% | 0.0000 |
| R08 | Importe atípico frente al perfil | 139 | 139 | 0 | 202 | 0 | 100.0% | 100.0% | 40.8% | 0.5791 |
| R09 | Cambio abrupto de comportamiento | 143 | 60 | 2 | 281 | 81 | 96.8% | 42.0% | 17.6% | 0.2978 |
| R10 | Transferencias circulares | 0 | 0 | 0 | 341 | 0 | 0.0% | 0.0% | 0.0% | 0.0000 |
| R11 | Concentración de contraparte | 0 | 0 | 0 | 341 | 0 | 0.0% | 0.0% | 0.0% | 0.0000 |
| R12 | Fan-in de múltiples remitentes | 6 | 0 | 0 | 341 | 6 | 0.0% | 0.0% | 0.0% | 0.0000 |

## Cobertura por patrón

| Patrón | Casos truth | Detectados | Recall |
|---|---:|---:|---:|
| DORMANT_ACTIVATION | 3 | 3 | 100.0% |
| HIGH_VELOCITY | 67 | 67 | 100.0% |
| PASS_THROUGH | 96 | 96 | 100.0% |
| ROUND_MULE | 75 | 75 | 100.0% |
| STRUCTURING | 100 | 100 | 100.0% |

## Lectura metodológica

- La muestra `NORMAL` de Fase 3 es una muestra, no el universo de transacciones normales.
- La precisión principal solo cuenta transacciones etiquetadas; la precisión conservadora suma las alertadas sin etiqueta como falsos positivos.
- El recall se calcula sobre las 341 transacciones sospechosas etiquetadas.
- R07 (geografía) y R09 (cambio de comportamiento) pueden alertar transacciones normales no muestreadas; se reportan por separado y no se ocultan.
- Los resultados son reproducibles con la semilla fija del seed de Fase 3.
