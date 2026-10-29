# Reporte de operación sospechosa (ROS)

**Naturaleza:** plantilla y dos casos ficticios para el portafolio. No se presentó ningún ROS ante una autoridad real. Los nombres, cuentas y operaciones son sintéticos.

## 1. Cuándo se genera

Un caso pasa a ROS cuando el análisis confirma indicios de operación sospechosa y el oficial de cumplimiento aprueba el reporte. La obligación no depende del monto; el monto es un factor de priorización. El caso se marca `REPORTADO` y se conserva la trazabilidad de alertas, caso y ROS.

## 2. Campos mínimos

| Campo | Descripción |
|---|---|
| `ros_id` | Identificador interno ficticio. |
| `case_id` | Caso AML vinculado. |
| `customer_id` | Cliente involucrado. |
| `created_at` | Fecha de creación del borrador. |
| `status` | `BORRADOR`, `REVISADO`, `ENVIADO`. |
| `narrative` | Relación de hechos, patrones y fundamento. |
| `operations_json` | Operaciones, fechas, montos, cuentas y contrapartes. |
| `submitted_at` | Fecha de envío, si corresponde. |

La tabla `aml_ros` del esquema implementa estos campos. En este caso todos los ROS quedan en `BORRADOR` o `REVISADO`; no se marca `ENVIADO` porque no existe una presentación real.

## 3. Plantilla de narrativa

```text
1. Identificación del cliente y de la relación.
2. Período analizado y operaciones comprendidas.
3. Patrón observado y reglas activadas.
4. Contrapartes y jurisdicciones relevantes.
5. Resultado del screening y del KYC.
6. Explicación del cliente, si fue obtenida.
7. Conclusión del análisis y fundamento de la sospecha.
8. Acciones adoptadas y responsable de la aprobación.
```

## 4. Caso ficticio ROS-2026-001 — Velocidad transaccional

| Campo | Valor |
|---|---|
| Cliente | CUS-000022 — Daniela Paredes López (ficticia) |
| Perfil | Individual, RETAIL, Paraguay |
| Patrón | HIGH_VELOCITY |
| Período | 2026-08-03, 08:00 a 14:36 |
| Operaciones | 18 transferencias salientes |
| Monto agregado | PYG 5.715.000 |
| Reglas | R02 y R03 |
| Screening | Sin coincidencia en listas ficticias |
| Estado | BORRADOR |

**Narrativa:** la cuenta ACC-000022 registró 18 transferencias salientes en menos de siete horas, por un total de PYG 5.715.000, hacia 18 contrapartes distintas. El volumen y la dispersión no guardan relación con el perfil transaccional declarado. Las reglas R02 (cantidad) y R03 (monto) se activaron. No se identificaron coincidencias en sanciones ni PEP. Se recomienda solicitar explicación del origen de fondos y del propósito de las transferencias, y mantener el monitoreo reforzado.

## 5. Caso ficticio ROS-2026-002 — Depósitos redondos reiterados

| Campo | Valor |
|---|---|
| Cliente | CUS-000024 — Lucía Cabrera Ramírez (ficticia) |
| Perfil | Individual, RETAIL, Argentina |
| Patrón | ROUND_MULE |
| Período | 2026-04-24 a 2026-09-18 |
| Operaciones | 15 depósitos |
| Monto agregado | PYG 67.000.000 |
| Reglas | R05, R06 y R08 |
| Screening | Sin coincidencia en listas ficticias |
| Estado | BORRADOR |

**Narrativa:** la cuenta ACC-000024 recibió 15 depósitos en montos redondos, múltiplos de PYG 1.000.000, por un total de PYG 67.000.000, durante aproximadamente cinco meses. Los importes superan el perfil declarado y activaron R05 (depósitos redondos), R06 (reactivación) y R08 (importe atípico). No se observó una actividad económica que explique la regularidad y el monto. Se recomienda revisar la documentación de origen de fondos, identificar a los ordenantes y evaluar la procedencia de un ROS ante la autoridad competente.

## 6. Gobierno del ROS

- El borrador lo prepara el analista AML.
- El oficial de cumplimiento revisa y aprueba.
- El ROS aprobado se conserva con las alertas, el caso y las transiciones de estado.
- La decisión de no reportar también debe quedar documentada.
- Los plazos y formatos concretos deben validarse con Cumplimiento y con la normativa vigente; este documento no afirma un plazo legal.
