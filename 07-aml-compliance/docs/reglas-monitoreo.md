# Reglas de monitoreo transaccional

**Motor:** SQLite sobre la base del core de Fase 3.  
**Implementación:** `07-aml-compliance/sql/rules/*.sql`, orquestadas por `aml/rules.py`.  
**Parámetros:** `07-aml-compliance/data/rule_params.json` y tabla `aml_rule_params`.

## 1. Catálogo

| ID | Regla | Patrón objetivo | Lógica resumida | Parámetros principales |
|---|---|---|---|---|
| R01 | Estructuración por debajo del umbral | STRUCTURING | Depósitos cercanos al umbral, repetidos en 7 días, con acumulado relevante. | Umbral 10.000.000; ratio 0,9; 7 días; mínimo 5; total 15.000.000. |
| R02 | Velocidad por cantidad | HIGH_VELOCITY | Transferencias salientes agrupadas por cuenta y día; mínimo de operaciones. | Mínimo 10 transferencias en 24 h. |
| R03 | Velocidad por monto | HIGH_VELOCITY | Transferencias salientes agrupadas por cuenta y día; mínimo de cantidad y monto. | Mínimo 5 y total 2.800.000 en 24 h. |
| R04 | Cuenta de paso | PASS_THROUGH | Depósito seguido de transferencia saliente rápida y proporcional. | Ventana 120 min; salida ≥80 % de la entrada; mínimo 1.000.000. |
| R05 | Depósitos redondos reiterados | ROUND_MULE | Depósitos múltiplos de 1.000.000, repetidos en 90 días. | Mínimo 5; unidad 1.000.000; mínimo 1.000.000. |
| R06 | Reactivación de cuenta inactiva | DORMANT_ACTIVATION | Proxy: cuenta con antigüedad, sin movimientos 48 h y depósito relevante. | Depósito ≥5.000.000; inactividad 2 días; antigüedad 180 días. |
| R07 | Jurisdicción de alto riesgo | — | Cliente residente en país de la lista interna ficticia. | Lista `aml_high_risk_countries`. |
| R08 | Importe atípico frente al perfil | — | Operación ≥5.000.000 y ≥3 veces el promedio histórico del cliente. | Mínimo 5.000.000; multiplicador 3; historial mínimo 5. |
| R09 | Cambio abrupto de comportamiento | — | Volumen mensual del cliente ≥5 veces su promedio de los 3 meses previos. | Multiplicador 5; total mensual 80.000.000; ventana 30 días. |
| R10 | Transferencias circulares | — | Salida y retorno entre las mismas cuentas, con monto similar, en 7 días. | Ventana 7 días; tolerancia 5 %; mínimo 1.000.000. |
| R11 | Concentración de contraparte | — | Salidas de una cuenta concentradas ≥80 % en una contraparte. | Mínimo 5 transferencias; total 5.000.000; share 0,8. |
| R12 | Fan-in de múltiples remitentes | — | Semana calendario con ≥6 remitentes distintos y total relevante. | 6 remitentes; total 10.000.000; ventana 7 días. |

## 2. Decisiones de implementación

- **R01, R04, R05 y R10** trabajan sobre pares o ventanas de operaciones; devuelven todas las transacciones que integran la ventana para que el analista vea el contexto.
- **R02 y R03** usan agrupación diaria porque el parámetro de ventana es de 24 horas; esto evita un self-join costoso sobre 18.452 transferencias.
- **R06** es un proxy: el core no tiene un campo de dormancia. Se documenta la limitación en P-015 y se prueba la lógica con datos sintéticos de dormancia real.
- **R08** usa el promedio histórico disponible del cliente, no una ventana móvil por transacción, para mantener el costo acotado en SQLite.
- **R11** evalúa concentración sobre el período completo; la ventana de 30 días queda como referencia operativa en el detalle de la alerta.
- **R12** usa semanas calendario (`%Y-%W`) para acotar el fan-in a 7 días sin un `COUNT(DISTINCT)` costoso por ventana móvil.
- Todas las reglas filtran `status = 'POSTED'`; R02, R03, R10, R11 y R12 exigen `debit_account_id IS NOT NULL`.

## 3. Resultado de calibración

Sobre el dataset de Fase 3 (49.582 transacciones, 341 sospechosas etiquetadas):

| Métrica | Valor |
|---|---:|
| Transacciones alertadas | 494 |
| Verdaderos positivos | 341 |
| Falsos positivos etiquetados | 3 |
| Falsos negativos | 0 |
| Recall | 100 % |
| Precisión sobre etiquetadas | 99,13 % |
| Precisión conservadora | 69,03 % |
| Alertadas sin etiqueta | 150 |

Cobertura por patrón: STRUCTURING 100/100; HIGH_VELOCITY 67/67; PASS_THROUGH 96/96; ROUND_MULE 75/75; DORMANT_ACTIVATION 3/3.

R07, R10 y R11 devuelven cero filas en este dataset porque no hay clientes en países de la lista, transferencias circulares ni concentraciones que superen los umbrales. Su funcionamiento se prueba con casos sintéticos en `07-aml-compliance/tests/test_rules.py`.

## 4. Lectura de resultados

- La precisión principal solo considera transacciones etiquetadas; la precisión conservadora suma las alertadas sin etiqueta como falsos positivos.
- La muestra NORMAL de Fase 3 es una muestra, no el universo de operaciones normales.
- Las reglas R09 y R12 aportan alertas sin etiqueta; se mantienen porque cubren comportamientos genéricos y se reportan de forma transparente.
- Los umbrales son parámetros de diseño y deben validarse con Cumplimiento y Riesgos.
