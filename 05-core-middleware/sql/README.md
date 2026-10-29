# Consultas SQL de operación y control

Consultas SQLite de solo lectura sobre la base sintética de NovaBank. Cada archivo
incluye un comentario con su propósito de negocio y usa CTEs y/o funciones de
ventana (`OVER`) para resolver el análisis.

| # | Archivo | Propósito de negocio |
|---|---|---|
| 01 | `01_conciliacion_saldos_libro_mayor.sql` | Conciliar saldo operativo de cuentas contra el libro mayor. |
| 02 | `02_balance_comprobacion.sql` | Balance de comprobación por cuenta contable. |
| 03 | `03_saldos_por_moneda.sql` | Saldos de clientes por moneda y tipo de cuenta. |
| 04 | `04_top_clientes_saldo.sql` | Ranking de clientes por saldo normalizado a PYG. |
| 05 | `05_movimientos_duplicados.sql` | Detectar posibles operaciones duplicadas. |
| 06 | `06_cuentas_inactivas.sql` | Cuentas dormidas o sin actividad reciente. |
| 07 | `07_flujo_diario_por_moneda.sql` | Volumen contable diario y promedio móvil de 7 días. |
| 08 | `08_velocidad_transaccional_cliente.sql` | Velocidad transaccional diaria por cliente. |
| 09 | `09_estructuracion_umbral.sql` | Depósitos repetidos por debajo del umbral de ₲10.000.000. |
| 10 | `10_contrapartes_frecuentes.sql` | Concentración de contrapartes por cliente. |
| 11 | `11_comisiones_por_tipo_mes.sql` | Ingresos por comisiones y variación mensual. |
| 12 | `12_rentabilidad_cuenta.sql` | Rendimiento por comisiones y deciles por moneda. |
| 13 | `13_passthrough_rapido.sql` | Cuentas de paso con salida en menos de 60 minutos. |
| 14 | `14_cierre_vs_libro.sql` | Último cierre diario contra saldo actual y libro mayor. |
| 15 | `15_tipos_cambio_utilizados.sql` | Auditoría de tipos de cambio aplicados en FX. |
| 16 | `16_distribucion_montos.sql` | Distribución de importes por rango y moneda. |
| 17 | `17_cuentas_sobregiro_riesgo.sql` | Uso de sobregiro y cuentas cercanas al límite. |
| 18 | `18_cohortes_clientes.sql` | Altas y saldos por cohorte mensual. |
| 19 | `19_operaciones_rechazadas_idempotencia.sql` | Rechazos repetidos y reutilización de idempotency keys. |
| 20 | `20_top_gl_movimientos.sql` | Cuentas contables con mayor volumen. |
| 21 | `21_corresponsalia_paises.sql` | Corredores transfronterizos por país. |
| 22 | `22_cobertura_verdad_aml.sql` | Cobertura de la verdad AML sintética (uso interno). |
| 23 | `23_conciliacion_global_diaria.sql` | Control global de partida doble por día y moneda. |

## Uso

```powershell
.\.venv\Scripts\python.exe -c "import sqlite3,pathlib; c=sqlite3.connect('05-core-middleware/db/novabank.db'); print(c.execute(pathlib.Path('05-core-middleware/sql/01_conciliacion_saldos_libro_mayor.sql').read_text(encoding='utf-8')).fetchall()[:5])"
```

O desde cualquier cliente SQLite compatible (DB Browser for SQLite, DBeaver, etc.).
Las consultas no modifican datos. La tabla `_aml_ground_truth` es de uso interno
para validar la Fase 5 y no se expone por la API.
