# Dataset analítico

CSV limpios exportados desde la base SQLite del core y el evaluador AML. Todo el contenido es sintético y reproducible con la semilla del caso.

## Generación

```powershell
.\.venv\Scripts\python.exe 09-analitica\scripts\export_analytics.py
```

El exportador abre una **copia en memoria** de `05-core-middleware/db/novabank.db`; no modifica la base de la Fase 5. Si la copia no tiene el esquema AML, lo inicializa. Luego ejecuta las reglas R01–R12, deduplica alertas y simula un ciclo de vida analítico determinístico para las alertas y los casos.

## Archivos

| Archivo | Grano | Filas | Uso |
|---|---|---:|---|
| `dim_date.csv` | Un día | 183 | Dimensión de calendario. |
| `dim_customer.csv` | Un cliente | 500 | Dimensión de cliente con KYC y perfil AML. |
| `dim_account.csv` | Una cuenta | 800 | Dimensión de cuenta. |
| `dim_rule.csv` | Una regla AML | 12 | Catálogo R01–R12. |
| `dim_priority.csv` | Una prioridad | 3 | SLA de asignación y cierre. |
| `dim_currency.csv` | Una moneda | 3 | Catálogo ISO 4217 usado en el caso. |
| `fact_transactions.csv` | Una transacción | 49.582 | Hecho principal de operaciones. |
| `fact_payment_sla.csv` | Una transferencia local | 10.820 | Detalle para el análisis de SLA. |
| `fact_alerts.csv` | Una alerta deduplicada | 377 | Bandeja y análisis AML. |
| `fact_cases.csv` | Un caso | 59 | Casos y cierres. |
| `fact_daily_ops.csv` | Fecha + moneda | 366 | Agregado diario para Excel y conciliación. |
| `fact_ledger_daily.csv` | Fecha + moneda | 366 | Débitos y créditos del libro mayor. |
| `export_report.json` | Reporte de ejecución | — | Conteos, integridad y notas de alcance. |

## Relaciones

```text
dim_date[date_key] 1 ── N fact_transactions[date_key]
dim_customer[customer_id] 1 ── N dim_account[customer_id]
dim_customer[customer_id] 1 ── N fact_transactions[customer_id]
dim_account[account_id] 1 ── N fact_transactions[debit_account_id]
dim_account[account_id] 1 ── N fact_transactions[credit_account_id]
dim_rule[rule_id] 1 ── N fact_alerts[rule_id]
dim_date[date_key] 1 ── N fact_alerts[date_key]
dim_customer[customer_id] 1 ── N fact_alerts[customer_id]
fact_alerts[alert_id] 1 ── N fact_cases?  (un caso agrupa varias alertas)
dim_date[date_key] 1 ── N fact_daily_ops[date_key]
dim_date[date_key] 1 ── N fact_ledger_daily[date_key]
```

`fact_cases` se relaciona con `dim_customer` y, para el detalle, con `fact_alerts[case_id]`; **no** se crea una relación activa muchos-a-muchos en Power BI. El detalle de alertas por caso se obtiene con una relación inactiva y `USERELATIONSHIP` o con una tabla puente si el modelo lo requiere.

## Reglas de calidad aplicadas

- Una fila por clave en dimensiones; IDs únicos en hechos.
- Importes no negativos y moneda siempre informada.
- `date_key` en formato ISO `YYYY-MM-DD` y presente en `dim_date`.
- Alertas con prioridad P1/P2/P3 y estado del catálogo AML.
- Conciliación diaria: débitos = créditos por fecha y moneda; diferencia cero en el dataset exportado.
- Codificación UTF-8 con BOM para compatibilidad con Excel; separador coma y punto decimal.
- Sin PII real: nombres, cuentas, documentos y direcciones son ficticios.

## Limitaciones y supuestos

1. **Latencia sintética:** el core no registra timestamps separados de aceptación y acreditación. `fact_payment_sla.latency_ms` se genera de forma determinística a partir del ID de la transacción y se documenta como simulación, no como medición.
2. **Ciclo de vida analítico:** los estados, asignaciones y cierres de alertas y casos se simulan con una semilla derivada del ID para poder demostrar bandeja, SLA y cierres. No representan decisiones reales de un analista.
3. **Alertas del corte actual:** la ejecución reproducible sobre la base actual genera **377 alertas deduplicadas** a partir de 786 coincidencias de reglas. La documentación de Fase 5 conserva un corte anterior con 775 alertas; la diferencia queda registrada en `docs/PENDIENTES.md` (P-018) para reconciliar.
4. **Alcance internacional:** el core solo tiene PYG y USD; EUR aparece en catálogos y en el simulador de comisiones, pero no en transacciones contabilizadas.
5. **Sin datos de mercado:** los tipos de cambio del workbook son ficticios y solo se usan para el simulador.
6. **No sustituye un data warehouse:** los CSV son un extracto analítico del caso, no un pipeline productivo.
