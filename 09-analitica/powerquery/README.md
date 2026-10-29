# Power Query — scripts M

Scripts para cargar los CSV en Excel o Power BI sin escribir tipos a mano.

## Uso en Excel

1. **Datos → Obtener datos → De otras fuentes → Consulta en blanco**.
2. **Editor avanzado** → pegar `00_parametros.pq` → renombrar la consulta a `RutaDatos`.
3. Ajustar la ruta a `09-analitica/data` del clon local.
4. Repetir con cada script; el nombre de la consulta debe ser el nombre lógico de la tabla (ver tabla de abajo).
5. **Cerrar y cargar en → Solo conexión** para el modelo de datos; para una hoja, **Cerrar y cargar**.
6. Crear relaciones en **Administrar modelo de datos**.

## Uso en Power BI

1. **Obtener datos → Consulta en blanco → Editor avanzado**.
2. Pegar `00_parametros.pq`; renombrar a `RutaDatos`.
3. Pegar cada consulta; renombrar según la tabla.
4. **Cerrar y aplicar**.

## Mapa de consultas

| Archivo | Consulta / tabla |
|---|---|
| `dim_fecha.pq` | `dim_date` |
| `dim_cliente.pq` | `dim_customer` |
| `dim_cuenta.pq` | `dim_account` |
| `dim_regla.pq` | `dim_rule` |
| `dim_prioridad.pq` | `dim_priority` |
| `dim_moneda.pq` | `dim_currency` |
| `fact_transacciones.pq` | `fact_transactions` |
| `fact_pagos_local.pq` | `fact_payment_sla` |
| `fact_alertas.pq` | `fact_alerts` |
| `fact_casos.pq` | `fact_cases` |
| `fact_diario_ops.pq` | `fact_daily_ops` |
| `fact_libro_diario.pq` | `fact_ledger_daily` |
| `consulta_conciliacion.pq` | `consulta_conciliacion` (opcional) |

## Notas

- `RutaDatos` debe ser una consulta de tipo texto. Si Power BI intenta cargarla como tabla, dejarla como **Solo conexión**.
- Los CSV están en UTF-8 con BOM; `Encoding = 65001` evita acentos rotos.
- `fact_cases.pq` agrega `opened_date` para relacionar con `dim_date`.
- `dim_fecha.pq` agrega `month_name`.
- `fact_transacciones.pq` agrega `year_month`.
- `consulta_conciliacion.pq` une hechos y libro por `Clave` y calcula `Diferencia`/`Resultado`; no reemplaza la conciliación contable del core, es una vista analítica.
- No hay credenciales ni rutas de red en los scripts.
