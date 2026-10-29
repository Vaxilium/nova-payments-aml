# 09 — Analítica

Capa de datos, Excel, Power BI y Tableau para el caso NovaBank. Todo el contenido usa datos **sintéticos** y es reproducible.

## Contenido

| Ruta | Qué contiene |
|---|---|
| `data/` | 12 CSV limpios + `export_report.json` y `README.md` con grano, relaciones y limitaciones. |
| `docs/diccionario-datos.md` | Diccionario campo por campo y reglas de cálculo. |
| `docs/excel.md` | Fórmulas, rangos, validaciones, formato condicional y paso a paso de tabla dinámica. |
| `docs/tablero.md` | Especificación de páginas, visuales, filtros y diseño de los dashboards. |
| `excel/NovaBank_analitica.xlsx` | Workbook con KPIs, parámetros, conciliación, alertas, casos, simulador y reglas. |
| `powerquery/` | Scripts M por archivo, parámetro de ruta y consulta de conciliación. |
| `powerbi/` | `medidas.dax` (36 medidas + columnas), tema JSON e instructivo de construcción/publicación. |
| `tableau/` | Campos calculados equivalentes e instructivo de dashboards y publicación. |
| `scripts/` | `export_analytics.py` y `build_excel.py`. |
| `tests/` | Validaciones de integridad, conteos y estructura del workbook. |

## Ejecución

```powershell
# 1. Exportar CSV desde SQLite (copia en memoria, no toca la base core)
.\.venv\Scripts\python.exe 09-analitica\scripts\export_analytics.py

# 2. Generar el workbook
.\.venv\Scripts\python.exe 09-analitica\scripts\build_excel.py

# 3. Pruebas del módulo
.\.venv\Scripts\python.exe -m pytest 09-analitica -q
```

Salidas:

- `data/*.csv` y `data/export_report.json`.
- `excel/NovaBank_analitica.xlsx`.

## Cifras de control

| Métrica | Valor |
|---|---:|
| Transacciones | 49.582 |
| Pagos locales | 10.820 |
| Alertas deduplicadas | 377 |
| Casos | 59 |
| Clientes | 500 |
| Cuentas | 800 |
| Días de calendario | 183 |
| Diferencia de conciliación | 0 |

## Modelo

Modelo estrella con `dim_date`, `dim_customer`, `dim_account`, `dim_rule`, `dim_priority` y `dim_currency`; hechos `fact_transactions`, `fact_payment_sla`, `fact_alerts`, `fact_cases`, `fact_daily_ops` y `fact_ledger_daily`.

## Cómo abrir el workbook

1. Abrir `excel/NovaBank_analitica.xlsx` en Excel 365/2021 o LibreOffice.
2. Aceptar el recálculo (el archivo se genera sin caché de fórmulas).
3. Revisar `KPIs` y `Conciliación`; el semáforo debe mostrar `CUMPLE` y `CUADRADO`.
4. En `Simulador`, probar LOCAL/PYG, LOCAL/USD, INTERNACIONAL/USD y montos en el tope.

## Limitaciones

- La latencia de `fact_payment_sla` es sintética: el core no registra timestamps separados.
- El ciclo de vida de alertas y casos se simula de forma determinística para demostrar los tableros.
- El corte actual produce 377 alertas; la diferencia con el corte de Fase 5 está en `docs/PENDIENTES.md`.
- Power BI y Tableau se documentan como artefactos manuales; los `.pbix`/`.twbx` no se versionan.
