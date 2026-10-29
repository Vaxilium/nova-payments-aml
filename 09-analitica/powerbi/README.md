# Power BI — modelo y construcción

**Documento:** AN-NB-004
**Versión:** 1.0
**Fecha:** 2026-10-29
**Artefactos:** `medidas.dax`, `tema-novabank.json` y este instructivo.

> El `.pbix` no se versiona: es un binario que se construye manualmente en Power BI Desktop. Este documento deja el paso a paso y las medidas listas para pegar. No se declara haber publicado el tablero.

---

## 1. Requisitos

- Power BI Desktop actualizado (Windows).
- Los CSV de `09-analitica/data/` en la ruta local.
- Conexión a Internet solo para publicar en Power BI Service.
- No se necesitan credenciales para leer los CSV.

## 2. Cargar datos

### Opción A — Consultas M incluidas (recomendada)

1. Abrir Power BI Desktop → **Obtener datos** → **Texto/CSV** solo para validar una muestra; luego cerrar sin cargar.
2. **Obtener datos** → **Consulta en blanco** → **Editor avanzado**.
3. Pegar el contenido de `09-analitica/powerquery/00_parametros.pq` y renombrar la consulta a `RutaDatos`.
4. Ajustar la ruta a la carpeta `09-analitica/data` del clon local.
5. Para cada archivo `.pq` de `powerquery/`, crear **Consulta en blanco** → **Editor avanzado** → pegar el script y renombrar la consulta según esta tabla:

| Archivo | Nombre de consulta / tabla |
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
| `consulta_conciliacion.pq` | `consulta_conciliacion` (opcional, solo conexión) |

6. En **Inicio → Cerrar y aplicar** → **Cerrar y aplicar**.

### Opción B — Carpeta completa

1. **Obtener datos** → **Carpeta** → seleccionar `09-analitica/data`.
2. **Combinar y transformar**.
3. Filtrar `Extension` = `.csv`, quitar columnas de metadatos y usar `Csv.Document` con `Encoding = 65001`.
4. Promover encabezados y asignar tipos.
5. Renombrar cada consulta con el nombre lógico (`dim_customer`, `fact_transactions`, etc.).

> La opción A es más explícita para el portafolio y evita que una consulta rompa la carga de las demás.

## 3. Modelo

1. Ir a **Vista Modelo**.
2. Crear las relaciones:

| Desde | Hacia | Cardinalidad | Dirección | Activa |
|---|---|---|---|---|
| `dim_date[date_key]` | `fact_transactions[date_key]` | 1:* | Única | Sí |
| `dim_date[date_key]` | `fact_payment_sla[date_key]` | 1:* | Única | Sí |
| `dim_date[date_key]` | `fact_alerts[date_key]` | 1:* | Única | Sí |
| `dim_date[date_key]` | `fact_daily_ops[date_key]` | 1:* | Única | Sí |
| `dim_date[date_key]` | `fact_ledger_daily[date_key]` | 1:* | Única | Sí |
| `dim_date[date_key]` | `fact_cases[opened_date]` | 1:* | Única | Sí |
| `dim_customer[customer_id]` | `dim_account[customer_id]` | 1:* | Única | Sí |
| `dim_customer[customer_id]` | `fact_transactions[customer_id]` | 1:* | Única | Sí |
| `dim_customer[customer_id]` | `fact_alerts[customer_id]` | 1:* | Única | Sí |
| `dim_customer[customer_id]` | `fact_cases[customer_id]` | 1:* | Única | Sí |
| `dim_account[account_id]` | `fact_transactions[debit_account_id]` | 1:* | Única | Sí |
| `dim_account[account_id]` | `fact_transactions[credit_account_id]` | 1:* | Única | No |
| `dim_rule[rule_id]` | `fact_alerts[rule_id]` | 1:* | Única | Sí |
| `dim_priority[priority]` | `fact_alerts[priority]` | 1:* | Única | Sí |
| `dim_priority[priority]` | `fact_cases[priority]` | 1:* | Única | Sí |
| `dim_currency[currency]` | `fact_transactions[currency]` | 1:* | Única | Sí |
| `dim_currency[currency]` | `fact_daily_ops[currency]` | 1:* | Única | Sí |
| `dim_currency[currency]` | `fact_ledger_daily[currency]` | 1:* | Única | Sí |

3. Marcar `dim_date` como **Tabla de fechas** usando `dim_date[date_key]` (la consulta M ya la convierte a tipo fecha).
4. Ocultar columnas técnicas: `date_key` en hechos, `customer_id` en `dim_account`, IDs en dimensiones cuando exista una clave legible.
5. Ordenar `month_name` por `month`; `priority` por `priority_order`.
6. Revisar que no haya relaciones bidireccionales ni rutas ambiguas. `fact_cases` queda sin relación con `fact_alerts` para evitar ambigüedad.

## 4. Medidas

1. Ir a **Vista Datos** → seleccionar `fact_transactions` → **Nueva medida**.
2. Pegar cada medida de `medidas.dax` (una por vez) con el nombre exacto.
3. Asignar formato: entero, moneda, porcentaje o decimal según la sección 6 del archivo.
4. Crear las columnas calculadas `Latency Bin` y `Latency Bin Order` en `fact_payment_sla`.
5. Crear una tabla de parámetro `SLA objetivo` (modelado → nuevo parámetro) con 5.000 ms por defecto y usarla en `SLA Status` si se desea parametrizar.

Validación rápida:

- `Total Operations` = 49.582.
- `Total Alerts` = 377.
- `Total Cases` = 59.
- `Reconciliation Difference` = 0.
- `Payments Within SLA %` y `False Positive Rate` deben coincidir con el Excel y `export_report.json`.

## 5. Páginas

Seguir `09-analitica/docs/tablero.md`:

1. **Operaciones y volumen**.
2. **SLA de pagos instantáneos**.
3. **Alertas AML y falsos positivos**.
4. **Casos y conciliación** (opcional).

Pasos comunes:

1. Insertar un rectángulo de cabecera con el título, la fecha de corte y la etiqueta “Datos sintéticos”.
2. Insertar tarjetas KPI y fijar el tamaño en la grilla.
3. Insertar los visuales de la tabla de la especificación.
4. Configurar filtros de página y sincronizar fecha/segmento.
5. Agregar textos alternativos en **Formato → General → Propiedades → Texto alternativo**.
6. Guardar como `NovaBank_AML.pbix` (no commitear; está ignorado por `.gitignore`).

## 6. Tema

1. **Vista** → **Temas** → **Examinar temas**.
2. Seleccionar `09-analitica/powerbi/tema-novabank.json`.
3. Verificar contraste y colores semánticos en cada página.

## 7. Publicar en Power BI Service

1. Guardar el `.pbix`.
2. **Publicar** → elegir un workspace de práctica (por ejemplo `NovaBank-Portfolio`).
3. En el servicio, abrir el informe y **Anclar** los visuales a un dashboard si se quiere una vista ejecutiva.
4. **Configuración del conjunto de datos** → programar actualización.
   - Si los CSV están locales, instalar Power BI Gateway y configurar la fuente.
   - Si se cargan desde SharePoint/OneDrive, usar esa ruta y credenciales del conector.
5. Compartir solo con usuarios de prueba; no publicar datos reales.
6. Exportar evidencia: **Archivo → Exportar → PDF** o captura de las 3 páginas.
7. Registrar URL y fecha en `docs/EVIDENCIAS.md` (dejar el espacio si aún no se publicó).

## 8. Actualización y troubleshooting

| Síntoma | Causa probable | Acción |
|---|---|---|
| `RutaDatos` no encontrada | Ruta local distinta | Editar la consulta y apuntar a `09-analitica/data`. |
| Acentos rotos | Codificación | Usar `Encoding = 65001` en `Csv.Document`. |
| Fechas como texto | Tipo no asignado | Cambiar a `type date` / `type datetime`. |
| Relación ambigua | Dos rutas cliente→hecho | Dejar una relación inactiva o quitar la relación casos↔alertas. |
| p95 vacío | Filtro sin pagos locales | Revisar `currency`/`payment_scope`. |
| Medida no encontrada | Nombre distinto | Copiar el nombre exacto o usar “Ctrl+Z” y volver a pegar. |
| Error de actualización | Archivo bloqueado por Excel | Cerrar Excel y actualizar. |

## 9. Checklist de entrega

- [ ] CSV cargados con tipos correctos.
- [ ] Relaciones y tabla de fechas configuradas.
- [ ] 15+ medidas DAX creadas.
- [ ] 3 páginas requeridas con filtros y textos alternativos.
- [ ] Tema aplicado.
- [ ] Validación de cifras contra Excel.
- [ ] PDF/capturas exportadas.
- [ ] URL de publicación registrada o pendiente anotada en `docs/EVIDENCIAS.md`.
