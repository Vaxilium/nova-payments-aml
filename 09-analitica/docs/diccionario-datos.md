# Diccionario de datos analítico

**Documento:** AN-NB-001
**Versión:** 1.0
**Fecha:** 2026-10-29
**Fuente:** `09-analitica/data/*.csv`, exportados desde SQLite con `scripts/export_analytics.py`.

> Datos sintéticos, sin PII real. Los campos monetarios `*_minor` de la base se exportan como importes mayores (`amount`, `fee`, `importe`) para facilitar el consumo en Excel, Power BI y Tableau. En PYG no hay decimales; en USD y EUR se usan dos decimales.

---

## 1. Convenciones

| Convención | Descripción |
|---|---|
| `date_key` | Fecha ISO `YYYY-MM-DD`; clave de `dim_date`. |
| `currency` | Código ISO 4217: `PYG`, `USD`, `EUR`. |
| `amount` / `importe` | Importe en unidad mayor de la moneda; en PYG es entero. |
| `priority` | `P1`, `P2`, `P3`. |
| `status` | Estado del catálogo de alertas o casos AML. |
| `is_*` | Indicador booleano exportado como `1`/`0`. |
| `truth_*` | Etiqueta de verdad sintética de Fase 3, solo para evaluación. |

## 2. `dim_date.csv`

| Campo | Tipo | Descripción |
|---|---|---|
| `date_key` | texto | Fecha ISO. Clave primaria. |
| `year` | entero | Año. |
| `quarter` | entero | Trimestre 1–4. |
| `month` | entero | Mes 1–12. |
| `year_month` | texto | Año-mes `YYYY-MM`. |
| `week` | entero | Semana ISO. |
| `weekday` | entero | Día de la semana 1–7 (lunes = 1). |
| `weekday_name` | texto | Nombre del día en inglés (generado por Python). |
| `is_weekend` | 0/1 | 1 si sábado o domingo. |

## 3. `dim_customer.csv`

| Campo | Tipo | Descripción |
|---|---|---|
| `customer_id` | texto | Identificador ficticio `CUS-######`. Clave. |
| `customer_type` | texto | `INDIVIDUAL` o `BUSINESS`. |
| `display_name` | texto | Nombre ficticio para mostrar. |
| `document_type` | texto | `CI`, `RUC` o `PASSPORT`. |
| `country_code` | texto | ISO 3166-1 alfa-3; el caso usa `PRY`. |
| `city` | texto | Ciudad ficticia. |
| `segment` | texto | `RETAIL`, `PREMIUM`, `SME`, `CORPORATE`. |
| `risk_rating` | texto | Riesgo del core: `LOW`, `MEDIUM`, `HIGH`. |
| `kyc_status` | texto | `PENDING`, `VERIFIED`, `REJECTED`. |
| `is_active` | 0/1 | Cliente activo. |
| `created_at` | texto | Fecha/hora de alta. |
| `kyc_score` | entero | Score KYC 0–100 de Fase 5. |
| `risk_category` | texto | Categoría derivada del score: `LOW`, `MEDIUM`, `HIGH`. |
| `requires_edd` | 0/1 | Requiere debida diligencia ampliada. |
| `is_pep` | 0/1 | Persona expuesta políticamente (ficticia). |
| `occupation` | texto | Ocupación o actividad ficticia. |
| `activity_risk` | texto | Riesgo de actividad `LOW`, `MEDIUM`, `HIGH`. |
| `onboarding_channel` | texto | `BRANCH`, `WEB`, `MOBILE`, `API`. |
| `product_complexity` | texto | `BASIC`, `MEDIUM`, `COMPLEX`. |
| `expected_monthly_volume_minor` | entero | Volumen mensual esperado en unidad menor. |

## 4. `dim_account.csv`

| Campo | Tipo | Descripción |
|---|---|---|
| `account_id` | texto | Identificador `ACC-######`. Clave. |
| `customer_id` | texto | Cliente titular. FK a `dim_customer`. |
| `account_number` | texto | Número ficticio de 14 dígitos. |
| `account_type` | texto | `SAVINGS` o `CHECKING`. |
| `currency` | texto | Moneda de la cuenta. |
| `status` | texto | `ACTIVE`, `BLOCKED`, `CLOSED`. |
| `balance` | numérico | Saldo operativo en unidad mayor. |
| `opened_at` | texto | Fecha/hora de apertura. |
| `segment` | texto | Segmento del cliente (desnormalizado para filtros). |
| `risk_rating` | texto | Riesgo del cliente (desnormalizado). |
| `kyc_score` | entero | Score KYC del cliente. |

## 5. `dim_rule.csv`

| Campo | Tipo | Descripción |
|---|---|---|
| `rule_id` | texto | `R01`–`R12`. Clave. |
| `rule_name` | texto | Nombre funcional de la regla. |
| `severity` | texto | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`. |
| `base_score` | entero | Score base antes del ajuste KYC. |
| `intended_pattern` | texto | Patrón objetivo o `GENERAL`. |

## 6. `dim_priority.csv`

| Campo | Tipo | Descripción |
|---|---|---|
| `priority` | texto | `P1`, `P2`, `P3`. |
| `assignment_sla_minutes` | entero | Minutos objetivo para asignación. |
| `closure_sla_business_days` | entero | Días hábiles objetivo para cierre. |

## 7. `dim_currency.csv`

| Campo | Tipo | Descripción |
|---|---|---|
| `currency` | texto | Código ISO 4217. |
| `name` | texto | Nombre de la moneda. |
| `minor_unit` | entero | Decimales de la moneda. |

## 8. `fact_transactions.csv`

| Campo | Tipo | Descripción |
|---|---|---|
| `transaction_id` | texto | `TX-#########`. Clave. |
| `date_key` | texto | Fecha de valor; FK a `dim_date`. |
| `created_at` | texto | Fecha/hora de creación. |
| `transaction_type` | texto | `DEPOSIT`, `WITHDRAWAL`, `TRANSFER`, `FEE`, `FX`. |
| `status` | texto | `PENDING`, `POSTED`, `REJECTED`, `REVERSED`. |
| `currency` | texto | Moneda de la operación. |
| `amount` | numérico | Importe en unidad mayor. |
| `fee` | numérico | Comisión asociada. |
| `channel` | texto | Canal de origen (`BATCH` en el seed). |
| `debit_account_id` | texto | Cuenta debitada, si aplica. |
| `credit_account_id` | texto | Cuenta acreditada, si aplica. |
| `customer_id` | texto | Cliente de la cuenta debitada o, si no hay, de la acreditada. |
| `segment` | texto | Segmento del cliente. |
| `risk_rating` | texto | Riesgo del cliente. |
| `kyc_score` | entero | Score KYC. |
| `payment_scope` | texto | `LOCAL` si PYG; `INTERNATIONAL` si no. |
| `truth_label` | texto | `SUSPICIOUS`, `NORMAL` o vacío (dataset de verdad). |
| `truth_pattern` | texto | Patrón etiquetado de Fase 3. |
| `alert_id` | entero | Primera alerta AML vinculada, si existe. |
| `is_stp` | 0/1 | Proxy: operación `POSTED` sin alerta AML vinculada. No mide intervención manual real. |

## 9. `fact_payment_sla.csv`

| Campo | Tipo | Descripción |
|---|---|---|
| `transaction_id` | texto | Transferencia local PYG. |
| `date_key` | texto | Fecha de valor. |
| `customer_id` | texto | Cliente. |
| `segment` | texto | Segmento. |
| `channel` | texto | Canal. |
| `amount` | numérico | Importe PYG. |
| `latency_ms` | entero | Latencia sintética determinística. |
| `within_sla` | 0/1 | 1 si `latency_ms <= 5000`. |

> `latency_ms` **no** es una medición del core. Se genera a partir del ID para demostrar el tablero de SLA y se documenta como simulación.

## 10. `fact_alerts.csv`

| Campo | Tipo | Descripción |
|---|---|---|
| `alert_id` | entero | Clave de alerta. |
| `date_key` | texto | Fecha de la última operación detectada. |
| `created_at` | texto | Fecha/hora de creación analítica. |
| `alert_type` | texto | Nombre del tipo de alerta. |
| `rule_id` | texto | Regla que la originó. FK a `dim_rule`. |
| `rule_name` | texto | Nombre de la regla. |
| `severity` | texto | Severidad base. |
| `priority` | texto | `P1`, `P2`, `P3`. |
| `risk_score` | entero | Score 0–100. |
| `status` | texto | `NUEVA`, `EN_ANALISIS`, `ESCALADA`, `CERRADA_FALSO_POSITIVO`, `REPORTADA`. |
| `transaction_count` | entero | Operaciones agrupadas por deduplicación. |
| `customer_id` | texto | Cliente alertado. |
| `account_id` | texto | Cuenta alertada. |
| `transaction_id` | texto | Operación representativa. |
| `assigned_to` | texto | Analista ficticio. |
| `assigned_at` | texto | Fecha/hora de asignación. |
| `assignment_minutes` | entero | Minutos desde la creación hasta la asignación. |
| `due_at` | texto | Vencimiento del SLA de asignación. |
| `closed_at` | texto | Fecha/hora de cierre. |
| `closure_notes` | texto | Motivo de cierre. |
| `case_id` | entero | Caso vinculado. |
| `segment` | texto | Segmento del cliente. |
| `risk_rating` | texto | Riesgo del cliente. |
| `kyc_score` | entero | Score KYC. |
| `is_false_positive` | 0/1 | 1 si `CERRADA_FALSO_POSITIVO`. |
| `is_closed` | 0/1 | 1 si falso positivo o reportada. |
| `is_escalated` | 0/1 | 1 si escalada/reportada o con caso. |

## 11. `fact_cases.csv`

| Campo | Tipo | Descripción |
|---|---|---|
| `case_id` | entero | Clave del caso. |
| `customer_id` | texto | Cliente. |
| `title` | texto | Título descriptivo. |
| `status` | texto | `ABIERTO`, `EN_ANALISIS`, `ESCALADO`, `CERRADO`, `REPORTADO`. |
| `priority` | texto | Prioridad máxima de las alertas del caso. |
| `risk_score` | entero | Score máximo del caso. |
| `opened_at` | texto | Apertura. |
| `assigned_to` | texto | Analista. |
| `due_at` | texto | Vencimiento del cierre. |
| `closed_at` | texto | Cierre. |
| `ros_reported` | 0/1 | Reporte de operación sospechosa. |
| `alert_count` | entero | Alertas vinculadas. |
| `is_closed` | 0/1 | Caso en estado terminal. |
| `is_reported` | 0/1 | Caso reportado. |
| `is_on_time_close` | 0/1/vacío | Cierre antes del vencimiento; vacío si sigue abierto. |

## 12. `fact_daily_ops.csv`

| Campo | Tipo | Descripción |
|---|---|---|
| `date_key` | texto | Fecha. |
| `currency` | texto | Moneda. |
| `ops` | entero | Operaciones del día/moneda. |
| `amount` | numérico | Importe total. |
| `fee` | numérico | Comisiones totales. |
| `stp_ops` | entero | Operaciones sin alerta AML vinculada (proxy STP). |

## 13. `fact_ledger_daily.csv`

| Campo | Tipo | Descripción |
|---|---|---|
| `date_key` | texto | Fecha del asiento. |
| `currency` | texto | Moneda. |
| `entries` | entero | Asientos distintos. |
| `debit` | numérico | Suma de débitos. |
| `credit` | numérico | Suma de créditos. |

## 14. Reglas de cálculo documentadas

| Métrica | Fórmula / fuente |
|---|---|
| Volumen | `SUM(amount)` por moneda y período. |
| Ticket promedio | `Volumen / operaciones`. |
| STP local (proxy) | `operaciones POSTED sin alerta / operaciones`. |
| p95 de latencia local | `PERCENTILE(latency_ms, 0.95)` sobre `fact_payment_sla`. |
| % dentro de SLA | `AVERAGE(within_sla)`. |
| P1 a tiempo | `alertas P1 asignadas en <= 15 min / alertas P1`. |
| Falsos positivos | `alertas CERRADA_FALSO_POSITIVO / alertas cerradas`. |
| Casos en plazo | `casos cerrados con closed_at <= due_at / casos cerrados`. |
| Conciliación | `débitos del libro = créditos del libro` por fecha y moneda. |

## 15. Claves y relaciones para Power BI / Tableau

- `dim_date[date_key]` → hechos por `date_key`.
- `dim_customer[customer_id]` → `fact_transactions`, `fact_alerts`, `fact_cases`, `dim_account`.
- `dim_account[account_id]` → `fact_transactions` por `debit_account_id` y `credit_account_id` (dos relaciones; una activa y otra inactiva).
- `dim_rule[rule_id]` → `fact_alerts`.
- `dim_priority[priority]` → `fact_alerts`, `fact_cases`.
- `dim_date[date_key]` → `fact_cases[opened_date]` (fecha de apertura derivada en Power Query).
- `fact_cases` se modela como hecho independiente. No se relaciona con `fact_alerts` para evitar rutas ambiguas; el vínculo se resuelve por `case_id` o una página de detalle.
