# Workbook Excel avanzado

**Documento:** AN-NB-002
**Versión:** 1.0
**Fecha:** 2026-10-29
**Archivo:** `09-analitica/excel/NovaBank_analitica.xlsx`
**Generador:** `09-analitica/scripts/build_excel.py`

> El workbook se genera con openpyxl y **no** guarda valores calculados. Excel recalcula al abrir el archivo (`fullCalcOnLoad`). Si se abre en un visor que no calcula fórmulas, las celdas aparecerán vacías o con el último valor en caché; abrir en Excel o LibreOffice para actualizar.

---

## 1. Hojas

| Hoja | Contenido | Tabla |
|---|---|---|
| `Portada` | Contexto, notas de lectura e índice. | — |
| `KPIs` | Tablero ejecutivo con 17 indicadores y semáforo. | `tblKPIs` |
| `Parámetros` | Comisiones, umbrales, metas y tipos de cambio. | `tblTiposCambio` |
| `Conciliación` | Conciliación diaria por fecha/moneda con XLOOKUP, INDEX/MATCH y SUMIFS. | `tblConciliacion` |
| `Hechos_Diarios` | Operaciones, importe, comisión y STP por día/moneda. | `tblHechosDiarios` |
| `Libro_Diario` | Débitos, créditos y asientos por día/moneda. | `tblLibroDiario` |
| `Alertas` | Alertas AML con prioridad, SLA y resultado. | `tblAlertas` |
| `Casos` | Casos, cierres y ROS. | `tblCasos` |
| `Pagos_Local` | Detalle de transferencias locales y latencia sintética. | `tblPagosLocal` |
| `Simulador` | Calculadora de comisiones y escenarios. | `tblEscenarios` |
| `Reglas` | Catálogo R01–R12 y SLA por prioridad. | `tblReglas`, `tblSLA` |

## 2. Rangos con nombre

| Nombre | Celda | Uso |
|---|---|---|
| `Param_ComisionLocalPct` | `Parámetros!$C$5` | Comisión porcentual local. |
| `Param_ComisionIntlUSD` | `Parámetros!$C$6` | Comisión fija internacional. |
| `Param_ComisionFX_Pct` | `Parámetros!$C$7` | Comisión de conversión. |
| `Param_ComisionMinimaLocal_PYG` | `Parámetros!$C$8` | Piso de comisión local. |
| `Param_DescuentoPremium` | `Parámetros!$C$9` | Descuento premium. |
| `Param_TopeLocalPYG` | `Parámetros!$C$10` | Tope por operación local. |
| `Param_SLA_Instantaneo_ms` | `Parámetros!$C$11` | SLA de 5.000 ms. |
| `Param_Meta_STP` | `Parámetros!$C$12` | 95 %. |
| `Param_Meta_FalsosPositivos` | `Parámetros!$C$13` | 30 %. |
| `Param_Meta_P1_a_tiempo` | `Parámetros!$C$14` | 95 %. |
| `Param_Meta_Conciliacion` | `Parámetros!$C$15` | 99,5 %. |
| `Lista_Tipos` | `Parámetros!$A$25:$A$26` | Validación LOCAL/INTERNACIONAL. |
| `Lista_Monedas` | `Parámetros!$A$20:$A$22` | Validación PYG/USD/EUR. |
| `Lista_SiNo` | `Parámetros!$A$27:$A$28` | Validación SI/NO. |

## 3. Fórmulas principales

### 3.1 Conciliación

| Columna | Fórmula | Función demostrada |
|---|---|---|
| `Operaciones_sistema` | `=SUMIFS(tblHechosDiarios[Operaciones],tblHechosDiarios[Fecha],$B5,tblHechosDiarios[Moneda],$C5)` | `SUMIFS` con dos criterios. |
| `Importe_operaciones` | `=SUMIFS(tblHechosDiarios[Importe],...)` | `SUMIFS` sobre importes. |
| `Debitos_libro` | `=_xlfn.XLOOKUP($A5,tblLibroDiario[Clave],tblLibroDiario[Debitos],"SIN DATO")` | `XLOOKUP` por clave compuesta. |
| `Creditos_libro` | `=IFERROR(INDEX(tblLibroDiario[Creditos],MATCH($A5,tblLibroDiario[Clave],0)),"SIN DATO")` | `INDEX` + `MATCH` como alternativa. |
| `Diferencia` | `=ROUND(F5-G5,2)` | Débitos − créditos. |
| `Resultado` | `=IF(ABS(H5)<0.01,"CUADRADO","DIFERENCIA")` | Tolerancia de un centavo. |
| `Verificacion` | `=IF(ABS(H5)<0.01,"OK","REVISAR")` | Semáforo textual. |

La clave `Fecha|Moneda` existe en `Hechos_Diarios`, `Libro_Diario` y `Conciliación` para que las tres técnicas de búsqueda funcionen sobre la misma dimensión.

### 3.2 KPIs

| KPI | Fórmula |
|---|---|
| Operaciones totales | `=SUM(tblHechosDiarios[Operaciones])` |
| Volumen PYG | `=SUMIFS(tblHechosDiarios[Importe],tblHechosDiarios[Moneda],"PYG")` |
| Volumen USD | `=SUMIFS(tblHechosDiarios[Importe],tblHechosDiarios[Moneda],"USD")` |
| Ticket promedio PYG | `=IFERROR(B8/SUMIFS(tblHechosDiarios[Operaciones],tblHechosDiarios[Moneda],"PYG"),0)` |
| STP local | `=IFERROR(SUM(tblHechosDiarios[STP])/SUM(tblHechosDiarios[Operaciones]),0)` |
| p95 latencia local | `=PERCENTILE(tblPagosLocal[latency_ms],0.95)` |
| Pagos locales ≤ 5 s | `=AVERAGE(tblPagosLocal[within_sla])` |
| Alertas totales | `=COUNTA(tblAlertas[alert_id])` |
| Alertas P1 | `=COUNTIF(tblAlertas[prioridad],"P1")` |
| P1 asignadas a tiempo | `=IFERROR(COUNTIFS(tblAlertas[prioridad],"P1",tblAlertas[assignment_minutes],">=0",tblAlertas[assignment_minutes],"<=15")/COUNTIF(tblAlertas[prioridad],"P1"),0)` |
| Falsos positivos | `=IFERROR(SUM(tblAlertas[is_false_positive])/SUM(tblAlertas[is_closed]),0)` |
| Casos cerrados | `=COUNTIF(tblCasos[status],"CERRADO")+COUNTIF(tblCasos[status],"REPORTADO")` |
| Casos en plazo | `=IFERROR(SUM(tblCasos[is_on_time_close])/SUM(tblCasos[is_closed]),0)` |
| Conciliación cuadrada | `=IFERROR(COUNTIF(tblConciliacion[Resultado],"CUADRADO")/COUNTA(tblConciliacion[Clave]),0)` |
| Diferencia total libro | `=SUM(tblConciliacion[Diferencia])` |

El semáforo se calcula con una fórmula que interpreta la dirección de la meta (`MAX`, `MIN` o `ABS`) y devuelve `CUMPLE` o `NO CUMPLE`.

### 3.3 Simulador de comisiones

| Paso | Fórmula |
|---|---|
| Comisión base | `=IF($B$4="LOCAL",MAX(Param_ComisionMinimaLocal_PYG,$B$6*Param_ComisionLocalPct),Param_ComisionIntlUSD*XLOOKUP("USD",tblTiposCambio[Moneda],tblTiposCambio[Tasa_PYG])/XLOOKUP($B$5,tblTiposCambio[Moneda],tblTiposCambio[Tasa_PYG]))` |
| Descuento premium | `=IF(AND($B$4="LOCAL",$B$7="SI"),B10*Param_DescuentoPremium,0)` |
| Comisión final | `=B10-B11` |
| Total a debitar | `=B6+B12` |
| Tope local | `=IF($B$4="LOCAL",IF($B$5<>"PYG","SOLO PYG",IF($B$6<=Param_TopeLocalPYG,"DENTRO","EXCEDE")),"N/A")` |
| Tasa a PYG | `=_xlfn.XLOOKUP($B$5,tblTiposCambio[Moneda],tblTiposCambio[Tasa_PYG],"SIN DATO")` |
| Total en PYG | `=B13*B15` |

La comisión internacional se define en USD y se convierte a la moneda de la operación con los tipos de cambio ficticios: USD 25 equivale a 25 USD, a 23,10 EUR o a 182.500 PYG con las tasas del workbook.

### 3.4 Escenarios

La tabla `tblEscenarios` calcula cinco casos (local estándar, local en el tope, local excedido, internacional USD y EUR) con las mismas fórmulas, sin depender de las celdas de entrada. Sirve para comparar y para probar la validación.

## 4. Validaciones de datos

| Celda | Validación | Mensaje |
|---|---|---|
| `Simulador!B4` | Lista `Lista_Tipos` | LOCAL o INTERNACIONAL. |
| `Simulador!B5` | Lista `Lista_Monedas` | PYG, USD o EUR. |
| `Simulador!B6` | Decimal > 0 | “El importe debe ser mayor que cero.” |
| `Simulador!B7` | Lista `Lista_SiNo` | SI o NO. |
| `Simulador!B8` | Lista `APP,WEB,API,BRANCH` | Canal de origen. |

Las validaciones se aplican solo a las celdas de entrada. Los escenarios son fórmulas y no se editan a mano.

## 5. Formato condicional

| Hoja | Rango | Regla |
|---|---|---|
| `KPIs` | `E7:E23` | Verde para `CUMPLE`, rojo para `NO CUMPLE`. |
| `KPIs` | `B7:B23` | Escala de color rojo → ámbar → verde. |
| `Conciliación` | `H5:H370` | Diferencia distinta de 0 en rojo. |
| `Conciliación` | `I5:I370` | `DIFERENCIA` rojo, `CUADRADO` verde. |
| `Conciliación` | `J5:J370` | `REVISAR` ámbar. |
| `Hechos_Diarios` | `D5:E370` | Barras de datos en importes/comisiones. |
| `Alertas` | `D5:D381` | P1 rojo, P2 ámbar. |
| `Alertas` | `J5:J381` | Minutos de asignación > 15 en rojo. |
| `Alertas` | `M5:M381` | Falso positivo con fondo gris. |
| `Casos` | `D5:D63` | P1 rojo. |
| `Casos` | `L5:L63` | Caso cerrado en verde. |
| `Pagos_Local` | `H5:H10824` | Fuera de SLA en rojo. |
| `Pagos_Local` | `G5:G10824` | Barras de datos de latencia. |
| `Simulador` | `G20:G24` | `EXCEDE` rojo, `DENTRO` verde. |

## 6. Cómo armar una tabla dinámica

### 6.1 Operaciones por mes y moneda

1. Seleccionar una celda de `Hechos_Diarios` (por ejemplo `A4`).
2. Ir a **Insertar → Tabla dinámica → De una tabla o rango**.
3. Elegir **Nueva hoja de cálculo** y aceptar.
4. Arrastrar `Fecha` a **Filas**; Excel agrupa por año/trimestre/mes.
5. Arrastrar `Moneda` a **Columnas**.
6. Arrastrar `Operaciones` a **Valores** (suma) y `Importe` a **Valores** (suma).
7. En **Analizar tabla dinámica → Insertar segmentación de datos**, agregar `Moneda` y `Fecha`.
8. Aplicar formato de moneda al campo `Importe` y ordenar por fecha ascendente.

### 6.2 Alertas por regla y prioridad

1. Seleccionar `Alertas!A4`.
2. **Insertar → Tabla dinámica → Nueva hoja**.
3. `rule_id` en **Filas**, `prioridad` en **Columnas**, `alert_id` en **Valores** con función **Cuenta**.
4. Agregar `risk_score` en **Valores** con **Promedio** y formato de un decimal.
5. Insertar una segmentación por `status` y otra por `segments`.
6. Crear un gráfico de columnas apiladas a partir de la tabla dinámica.
7. Para el KPI de falsos positivos, agregar `is_false_positive` a **Valores** y mostrar como promedio; el resultado es la tasa sobre el total filtrado.

### 6.3 Conciliación por mes

1. Seleccionar `Conciliación!A4`.
2. Crear tabla dinámica con `Fecha` en **Filas** (agrupada por mes).
3. `Resultado` en **Columnas** y `Clave` en **Valores** (cuenta).
4. `Diferencia` en **Valores** (suma).
5. Filtrar `Resultado = DIFERENCIA` para revisar excepciones.
6. Agregar formato condicional a los totales.

> Las tablas dinámicas no se generan con openpyxl. Estos pasos son manuales y deben documentarse con captura en `docs/EVIDENCIAS.md` si se usan como evidencia.

## 7. Power Query en Excel

Los scripts M de `09-analitica/powerquery/` se pueden pegar en **Datos → Obtener datos → De otras fuentes → Consulta en blanco → Editor avanzado**. El parámetro `RutaDatos` debe apuntar a la carpeta `09-analitica/data` (por ejemplo `<ruta-del-repositorio>\09-analitica\data`).

Pasos resumidos:

1. Crear una consulta en blanco y pegar `00_parametros.pq` para definir la ruta.
2. Crear una consulta por archivo (`dim_customer.pq`, `fact_transactions.pq`, etc.).
3. En cada consulta, reemplazar o parametrizar la ruta con `RutaDatos`.
4. Cargar las consultas como **Solo conexión** y luego agregar al modelo de datos.
5. Crear las relaciones en **Administrar modelo de datos**.
6. Actualizar todo con **Datos → Actualizar todo**.

## 8. Limitaciones

- openpyxl no calcula fórmulas ni crea tablas dinámicas; el workbook se recalcula en Excel.
- `XLOOKUP` requiere Excel 365/2021 con funciones dinámicas. La columna de `INDEX/MATCH` queda como alternativa.
- Los importes PYG y USD se muestran como números; la moneda está en la columna `Moneda`, no en la celda.
- La latencia es sintética; no se debe presentar como resultado operativo medido.
- Los estados de alertas y casos son un ciclo de vida analítico de demostración.
