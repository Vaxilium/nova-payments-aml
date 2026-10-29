# Tableau — campos calculados y construcción

**Documento:** AN-NB-005
**Versión:** 1.0
**Fecha:** 2026-10-29
**Herramientas:** Tableau Public / Tableau Desktop.
**Datos:** `09-analitica/data/*.csv` (sintéticos).

---

## 1. Conexión

1. Abrir Tableau Public/Desktop → **Conectar → Texto**.
2. Seleccionar `09-analitica/data/fact_transactions.csv`.
3. En **Hoja de datos**, arrastrar las demás fuentes a la capa lógica y crear **relaciones** (no joins físicos):

| Tabla izquierda | Tabla derecha | Campo |
|---|---|---|
| `fact_transactions` | `dim_customer` | `customer_id` |
| `fact_transactions` | `dim_account` | `debit_account_id = account_id` |
| `fact_transactions` | `dim_date` | `date_key` |
| `fact_transactions` | `dim_currency` | `currency` |
| `fact_payment_sla` | `dim_date` | `date_key` |
| `fact_alerts` | `dim_date` | `date_key` |
| `fact_alerts` | `dim_customer` | `customer_id` |
| `fact_alerts` | `dim_rule` | `rule_id` |
| `fact_alerts` | `dim_priority` | `priority` |
| `fact_cases` | `dim_customer` | `customer_id` |
| `fact_cases` | `dim_date` | `opened_date` |
| `fact_daily_ops` | `dim_date` | `date_key` |
| `fact_ledger_daily` | `dim_date` | `date_key` |

4. Verificar que Tableau detecte `date_key`/`opened_date` como fecha y `amount`/`debit`/`credit` como número.
5. Crear un **extracto** para mejorar el rendimiento y fijar los datos de la demo.

> Si se usa una sola conexión por CSV, crear una fuente de datos por hecho y usar **Relacionar** en el modelo lógico. Evitar un join físico entre hechos y dimensiones para no duplicar importes.

## 2. Campos calculados

> Los nombres entre corchetes son los encabezados de los CSV. Si Tableau los renombra, usar el nombre visible entre corchetes.

### 2.1 Operaciones

| Campo | Fórmula |
|---|---|
| `Total Operations` | `COUNTD([transaction_id])` |
| `Total Amount` | `SUM([amount])` |
| `Total Amount PYG` | `SUM(IF [currency] = "PYG" THEN [amount] END)` |
| `Total Amount USD` | `SUM(IF [currency] = "USD" THEN [amount] END)` |
| `Total Fees` | `SUM([fee])` |
| `Avg Ticket PYG` | `SUM(IF [currency] = "PYG" THEN [amount] END) / COUNTD(IF [currency] = "PYG" THEN [transaction_id] END)` |
| `STP Rate (proxy)` | `SUM([is_stp]) / COUNTD([transaction_id])` |
| `Local Operations` | `COUNTD(IF [payment_scope] = "LOCAL" THEN [transaction_id] END)` |
| `International Operations` | `COUNTD(IF [payment_scope] = "INTERNATIONAL" THEN [transaction_id] END)` |
| `Operations MoM %` | `(SUM([ops]) - LOOKUP(SUM([ops]), -1)) / LOOKUP(SUM([ops]), -1)` |

`Operations MoM %` es una **tabla calculada** (Configuración de cálculo → Dirección: a lo largo de la fecha; usar `ZN` para evitar nulos). En una hoja diaria usar `[fact_daily_ops].[ops]`.

### 2.2 SLA local

| Campo | Fórmula |
|---|---|
| `Local Payments` | `COUNTD([transaction_id])` (fuente `fact_payment_sla`) |
| `Local p95 Latency (ms)` | `PERCENTILE([latency_ms], 0.95)` |
| `Local Avg Latency (ms)` | `AVG([latency_ms])` |
| `Payments Within SLA %` | `AVG([within_sla])` |
| `Payments Outside SLA` | `COUNTD(IF [within_sla] = 0 THEN [transaction_id] END)` |
| `SLA Status` | `IF [Payments Within SLA %] >= 0.95 THEN "CUMPLE" ELSE "NO CUMPLE" END` |
| `Latency Bucket` | `IF [latency_ms] < 1000 THEN "< 1 s" ELSEIF [latency_ms] < 2000 THEN "1–2 s" ELSEIF [latency_ms] < 3000 THEN "2–3 s" ELSEIF [latency_ms] < 5000 THEN "3–5 s" ELSE "> 5 s" END` |

`SLA Status` funciona como agregado si se usa con `AVG([within_sla])`; si Tableau exige una fórmula por fila, usar `IF [within_sla] = 1 THEN "DENTRO" ELSE "FUERA" END` para el detalle y una hoja aparte para el KPI.

### 2.3 Alertas y casos

| Campo | Fórmula |
|---|---|
| `Total Alerts` | `COUNTD([alert_id])` |
| `Open Alerts` | `COUNTD(IF [is_closed] = 0 THEN [alert_id] END)` |
| `Closed Alerts` | `COUNTD(IF [is_closed] = 1 THEN [alert_id] END)` |
| `P1 Alerts` | `COUNTD(IF [priority] = "P1" THEN [alert_id] END)` |
| `P1 Assigned On Time %` | `COUNTD(IF [priority] = "P1" AND [assignment_minutes] <= 15 THEN [alert_id] END) / COUNTD(IF [priority] = "P1" THEN [alert_id] END)` |
| `False Positive Rate` | `SUM([is_false_positive]) / SUM([is_closed])` |
| `Escalated Alerts` | `COUNTD(IF [is_escalated] = 1 THEN [alert_id] END)` |
| `Avg Alert Risk Score` | `AVG([risk_score])` |
| `Alerts per 1k Ops` | `COUNTD([alert_id]) / COUNTD([transaction_id]) * 1000` |
| `Total Cases` | `COUNTD([case_id])` |
| `Closed Cases` | `COUNTD(IF [is_closed] = 1 THEN [case_id] END)` |
| `Cases On Time %` | `SUM([is_on_time_close]) / SUM([is_closed])` |
| `Reported Cases` | `COUNTD(IF [is_reported] = 1 THEN [case_id] END)` |
| `Case Conversion Rate` | `COUNTD([case_id]) / COUNTD([alert_id])` |

`Alerts per 1k Ops` requiere que ambas medidas se calculen en la misma hoja con relaciones activas; si Tableau muestra `*` por ambigüedad, crear una hoja de alertas y una de operaciones y calcular la razón en una hoja de texto con ambas cifras fijas, o usar `SUM([transaction_count])` como aproximación documentada.

### 2.4 Conciliación

| Campo | Fórmula |
|---|---|
| `Reconciliation Difference` | `SUM([debit]) - SUM([credit])` |
| `Reconciliation Status` | `IF ABS([Reconciliation Difference]) < 0.01 THEN "CUADRADO" ELSE "DIFERENCIA" END` |
| `Reconciliation Rate` | `COUNTD(IF ABS([debit] - [credit]) < 0.01 THEN [date_key] END) / COUNTD([date_key])` |

`Reconciliation Rate` debe calcularse por fecha y moneda; crear una hoja con `date_key` y `currency`, y usar `MIN`/`AVG` según el nivel.

## 3. Hojas y dashboards

### 3.1 Operaciones y volumen

1. Hoja **KPI**: `Total Operations`, `Total Amount PYG`, `Total Amount USD`, `Avg Ticket PYG`, `STP Rate (proxy)` como textos independientes.
2. Hoja **Volumen mensual**: `date_key` (mes continuo) en Columnas; `Total Amount PYG` y `Total Amount USD` en Filas; doble eje o líneas separadas.
3. Hoja **Mezcla por segmento**: `segment` en Filas; `Total Amount` en Columnas; ordenar descendente.
4. Hoja **Tipo de operación**: `transaction_type` en Color; `Total Operations` en Ángulo; gráfico circular.
5. Dashboard: 5 KPI arriba, volumen a la izquierda, mezcla a la derecha, filtros de fecha/moneda/segmento/canal.

### 3.2 SLA local

1. Hoja **SLA KPI**: `Local Payments`, `Local p95 Latency (ms)`, `Payments Within SLA %`, `Payments Outside SLA`.
2. Hoja **Latencia diaria**: `date_key` en Columnas; `Local p95 Latency (ms)` y `Local Avg Latency (ms)` en Filas; línea de referencia en 5.000 ms.
3. Hoja **Cumplimiento por canal**: `channel` en Filas; `Payments Within SLA %` en Columnas; color por umbral 95 %.
4. Hoja **Histograma**: `Latency Bucket` en Columnas; `Local Payments` en Filas.
5. Dashboard: KPI, línea, barras y histograma; nota de latencia sintética.

### 3.3 Alertas AML y falsos positivos

1. Hoja **AML KPI**: `Total Alerts`, `Open Alerts`, `P1 Alerts`, `P1 Assigned On Time %`, `False Positive Rate`, `Avg Alert Risk Score`.
2. Hoja **Alertas por regla**: `rule_id` en Filas; `Total Alerts` en Columnas; color por `severity`.
3. Hoja **Evolución por estado**: `date_key` (mes) en Columnas; `Total Alerts` en Filas; `status` en Color.
4. Hoja **Dispersión**: `assignment_minutes` en Columnas; `risk_score` en Filas; detalle `alert_id`; color `priority`; tamaño `transaction_count`.
5. Hoja **Embudo**: `Total Alerts`, `Escalated Alerts`, `Total Cases`, `Reported Cases` como pasos.
6. Dashboard: KPI, reglas, evolución, dispersión y embudo; filtros de prioridad, estado, regla, segmento y riesgo.

### 3.4 Casos y conciliación (opcional)

- `Total Cases`, `Closed Cases`, `Cases On Time %`, `Reported Cases`.
- Evolución mensual de casos abiertos/cerrados.
- `Reconciliation Difference` por fecha/moneda y semáforo.

## 4. Filtros y acciones

- Filtro de fecha global (últimos 90 días por defecto).
- Filtros de moneda, segmento, canal, prioridad y estado según la página.
- Acción de filtro: seleccionar una regla en el gráfico de barras → filtrar la tabla de alertas.
- Tooltips con período, operaciones, importe y tasa.
- Ordenar `Latency Bucket` por una medida/orden manual; no alfabético.
- Mostrar “Datos sintéticos” en el pie de cada dashboard.

## 5. Tableau Public — publicación

1. Descargar Tableau Public desde el sitio oficial e instalar.
2. Conectar los CSV y crear las relaciones y cálculos de este documento.
3. Crear las hojas y dashboards de la sección 3.
4. **Servidor → Iniciar sesión en Tableau Public** (cuenta gratuita).
5. **Servidor → Publicar libro de trabajo**.
   - Nombre: `NovaBank — Pagos y AML (sintético)`.
   - Incluir extracto; no incluir credenciales.
   - Los datos de un libro publicado en Tableau Public son públicos: usar solo los CSV sintéticos.
6. Copiar la URL del libro y registrarla en `docs/EVIDENCIAS.md`.
7. Exportar imágenes/PDF de los dashboards para el portafolio.

## 6. Validación

- `Total Operations` = 49.582.
- `Total Alerts` = 377.
- `Total Cases` = 59.
- `Reconciliation Difference` = 0.
- `Payments Within SLA %` y `False Positive Rate` coinciden con Excel/Power BI.
- Las fechas y los acentos se ven correctamente en el extracto.
- No hay datos personales reales ni credenciales en el libro.

## 7. Limitaciones

- Tableau Public no permite ocultar los datos subyacentes; publicar solo datos ficticios.
- La latencia y el ciclo de vida de alertas/casos son sintéticos.
- Las relaciones entre hechos pueden requerir hojas separadas para evitar ambigüedad; documentar la aproximación usada.
- El tablero de Tableau es una alternativa de portafolio, no una réplica exacta del de Power BI.
