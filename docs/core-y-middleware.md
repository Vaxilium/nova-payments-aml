# Core bancario y middleware — lectura conceptual

**Fase:** 3 — Core bancario y middleware  
**Caso:** NovaBank Instant & Cross-Border Payments + AML Hub (100 % ficticio)  
**Implementación:** `05-core-middleware/`  
**Fecha:** 2026-10-28

> Este documento explica cómo el prototipo SQLite + FastAPI se relaciona, a nivel
> conceptual, con un core bancario y un middleware/ESB reales. No describe la
> arquitectura interna de ningún banco ni producto comercial. Todas las cuentas,
> clientes, importes y patrones son sintéticos.

---

## 1. Qué construimos y qué no

El repositorio implementa un **core bancario didáctico** y un **middleware de pagos
en proceso**. No es un core productivo ni un ESB real.

| Pieza | En el portafolio | En un entorno productivo |
|---|---|---|
| Clientes y cuentas | Tablas SQLite con constraints | CIF/cliente único, catálogo de productos, sucursales, condiciones |
| Libro mayor | Plan de 10 cuentas y asientos por partida doble | Plan contable completo, centros de costo, moneda funcional y reportes regulatorios |
| Saldos | `accounts.balance_minor` conciliado contra el libro | Saldos diarios, disponibles, retenidos, contables y de liquidez |
| Cierre | `daily_balances` calculado desde asientos | Cierre diario/mensual con jobs, bloqueos y conciliación interbancaria |
| Middleware | Clase `PaymentMiddleware` en proceso | ESB, bus de eventos u orquestador con colas, reintentos y observabilidad |
| API | FastAPI `/v1` con OpenAPI | API gateway con autenticación, cuotas y políticas |
| Persistencia | SQLite en un archivo | RDBMS transaccional, réplicas, backups y alta disponibilidad |
| Mensajería | Pendiente (Fase 4) | ISO 20022/SWIFT, colas, firmas y certificados |
| AML | Dataset etiquetado (Fase 3), reglas (Fase 5) | Screening, monitoreo, casos, ROS y gobierno de modelos |

La simplificación es deliberada: el objetivo del portafolio es demostrar criterio
funcional, modelado de datos, controles contables, contrato de API y pruebas, no
operar infraestructura bancaria.

---

## 2. Arquitectura lógica

```text
Canal (web/móvil/API)
        |
        v
Middleware de pagos  <-- idempotencia, correlación, validación de contrato
        |
        v
Core bancario simulado
  - clientes y cuentas
  - motor de contabilización
  - libro mayor (partida doble)
  - cierre diario
        |
        v
SQLite (datos sintéticos, triggers de integridad)
```

En el código:

- `app/api.py`: capa HTTP, validación Pydantic, errores y cabeceras.
- `app/middleware.py`: fachada estable que representa al orquestador/ESB.
- `app/service.py`: casos de uso (consulta, crédito, débito, transferencia, estado).
- `app/ledger.py`: motor de asientos y utilidades contables.
- `app/closing.py`: cálculo de cierres diarios.
- `app/seed.py`: generador reproducible de datos y patrones sospechosos.
- `db/schema.sql`: DDL, índices y triggers.

La separación es intencional: la API no escribe SQL contable directamente y el
core no conoce HTTP. Eso permite cambiar el transporte sin reescribir las reglas
de negocio, igual que en una integración real.

---

## 3. El core bancario real, a nivel conceptual

Un core bancario suele ser el sistema de registro de productos y saldos. A nivel
funcional incluye, entre otras piezas:

1. **Cliente único y KYC:** identificación, segmento, riesgo y estados de debida
   diligencia.
2. **Catálogo de productos:** tipos de cuenta, monedas, límites, comisiones,
   tasas y condiciones.
3. **Subledger de cuentas:** movimientos, saldos, retenciones y bloqueos.
4. **Libro mayor:** asientos balanceados que reflejan el efecto contable de cada
   operación.
5. **Contabilidad y cierre:** balance de comprobación, cierres diarios y
   conciliaciones.
6. **Integraciones:** canales, medios de pago, corresponsalía, riesgo y
   cumplimiento.

El prototipo reproduce los puntos 1 a 5 de forma mínima y deja el 6 para las
fases siguientes. La decisión de diseño principal es que **el libro mayor es la
fuente de verdad contable** y que el saldo operativo se concilia contra él.

### 3.1 Plan de cuentas simplificado

| Código | Cuenta | Naturaleza | Uso |
|---|---|---|---|
| 1101/1102 | Caja y bancos PYG/USD | Activo | Contrapartida de depósitos y retiros |
| 1901/1902 | Posición de cambio PYG/USD | Activo | Puente contable de conversiones FX |
| 2101/2102 | Depósitos de clientes PYG/USD | Pasivo | Subledger de cuentas de clientes |
| 3101/3102 | Patrimonio de apertura | Patrimonio | Saldos iniciales del dataset |
| 4101/4102 | Ingresos por comisiones | Ingreso | Comisiones de servicio |

Un plan real tendría cientos o miles de cuentas, centros de costo, moneda
funcional y reglas de mapeo por producto. Aquí se usan diez cuentas para que cada
asiento sea legible y verificable.

### 3.2 Partida doble y controles

Cada operación genera al menos dos líneas. Los controles implementados son:

- **CHECK de línea:** exactamente un débito o un crédito, importes no negativos.
- **Trigger de asiento:** al pasar a `POSTED`, la suma de débitos debe igualar la
  suma de créditos **por moneda**, y debe haber al menos dos líneas.
- **Inmutabilidad:** un asiento contabilizado no se modifica ni se elimina; sus
  líneas tampoco.
- **Moneda:** la línea con `account_id` debe usar la moneda de la cuenta.
- **Sobregiro:** una cuenta no puede quedar por debajo de su límite autorizado.
- **Operación:** una transacción contabilizada no cambia de importe, cuentas ni
  moneda.

Estos controles se validan también en Python antes de escribir, pero la base
actúa como última barrera. En un core real se suman segregación de funciones,
aprobaciones, pistas de auditoría inmutables y controles de cambio.

### 3.3 Saldo operativo vs. libro mayor

La tabla `accounts.balance_minor` es el saldo operativo que consume la API. El
libro mayor se calcula sumando `credit_minor - debit_minor` de las líneas
vinculadas a la cuenta. La consulta
`sql/01_conciliacion_saldos_libro_mayor.sql` compara ambos y debe devolver cero
diferencias. La prueba `test_seed_ledger_is_balanced_and_reconciled` lo verifica
sobre el dataset completo.

En producción esta conciliación suele correr como job de control y dispara
incidentes cuando aparece una diferencia. Aquí es una consulta y una prueba.

### 3.4 Cierre diario

`app/closing.py` reconstruye `daily_balances` a partir de los asientos:

- saldo de apertura = acumulado hasta el día anterior;
- débitos y créditos del día;
- saldo de cierre = apertura + créditos − débitos.

El cierre es idempotente por `(fecha, cuenta)`. La consulta
`sql/14_cierre_vs_libro.sql` compara el último cierre con el saldo actual y con el
libro. En un banco real el cierre incluye cortes, bloqueos, intereses,
provisiones, conciliación con cámaras y reportes regulatorios.

---

## 4. El middleware/ESB real, a nivel conceptual

Un middleware de pagos o ESB no "hace la contabilidad": **orquesta**. Sus
responsabilidades típicas son:

1. **Enrutamiento:** decidir a qué servicio o sistema va cada mensaje.
2. **Transformación:** mapear el contrato del canal al contrato del core.
3. **Orquestación:** coordinar validaciones, riesgo, límites, contabilidad y
   notificaciones.
4. **Idempotencia:** evitar doble ejecución ante reintentos.
5. **Correlación:** propagar un identificador de extremo a extremo.
6. **Resiliencia:** timeouts, reintentos, circuit breaker y colas.
7. **Observabilidad:** logs, métricas, trazas y auditoría.
8. **Seguridad:** autenticación, autorización, cifrado y control de cuotas.

En el prototipo, `PaymentMiddleware` es una fachada delgada. La idempotencia y la
correlación sí están implementadas en `app/service.py` y `app/api.py`; la
resiliencia distribuida, las colas y la seguridad de producción quedan fuera del
alcance de la Fase 3.

### 4.1 Idempotencia

Toda operación monetaria exige `Idempotency-Key` (8–128 caracteres). El servicio:

1. Calcula un hash canónico del contenido de la petición.
2. Abre una transacción `BEGIN IMMEDIATE`.
3. Si la clave ya existe con el mismo hash, devuelve la respuesta guardada
   (`Idempotent-Replayed: true`).
4. Si la clave existe con otro contenido, responde `409 IDEMPOTENCY_CONFLICT`.
5. Si no existe, ejecuta la operación, guarda respuesta y clave, y confirma.

Esto protege contra reintentos del canal y contra dos hilos concurrentes con la
misma clave. En un ESB real la clave suele tener TTL, almacenamiento distribuido y
políticas por operación; aquí se conserva en SQLite sin expiración.

### 4.2 Errores y correlación

La API devuelve errores con código estable, mensaje y `correlation_id`. Los
códigos principales son:

| Código | HTTP | Cuándo |
|---|---|---|
| `VALIDATION_ERROR` | 422 | El cuerpo no cumple el contrato Pydantic |
| `IDEMPOTENCY_KEY_REQUIRED` | 400 | Falta la cabecera en una operación monetaria |
| `IDEMPOTENCY_CONFLICT` | 409 | La clave se reutilizó con otro contenido |
| `ACCOUNT_NOT_FOUND` / `CUSTOMER_NOT_FOUND` | 404 | Recurso inexistente |
| `ACCOUNT_NOT_ACTIVE` | 409 | Cuenta bloqueada o cerrada |
| `INSUFFICIENT_FUNDS` | 422 | Saldo disponible insuficiente |
| `CURRENCY_MISMATCH` | 422 | Moneda distinta a la de la cuenta |
| `CONCURRENT_MODIFICATION` | 409 | La versión de la cuenta cambió |
| `INVALID_OPERATION` | 422 | Regla de negocio inválida |

Cada petición recibe un `X-Correlation-ID` (o reutiliza el enviado por el cliente)
que se devuelve en la respuesta, se registra en el log y se guarda en
`audit_log` para las mutaciones.

---

## 5. Modelo de datos

| Tabla | Rol |
|---|---|
| `currencies` | Monedas y escala decimal (PYG 0, USD 2). |
| `customers` | Clientes ficticios con segmento, riesgo y KYC. |
| `accounts` | Cuentas de ahorro/corriente en PYG/USD, saldo y versión. |
| `gl_accounts` | Plan de cuentas contable. |
| `journal_entries` | Cabecera del asiento y su estado. |
| `journal_lines` | Débitos/créditos, cuenta contable y cuenta de cliente. |
| `transactions` | Movimientos de negocio (depósito, retiro, transferencia, comisión, FX). |
| `fees` | Comisiones asociadas a operaciones. |
| `fx_rates` | Tipos de cambio diarios USD/PYG. |
| `daily_balances` | Cierre diario por cuenta. |
| `idempotency_keys` | Claves de idempotencia y respuestas guardadas. |
| `audit_log` | Bitácora de eventos. |
| `_aml_ground_truth` | Verdad sintética para validar reglas AML (interna). |

**Convención monetaria:** los importes se guardan como enteros en la unidad menor
(PYG: guaraníes; USD: centavos). La API muestra decimales formateados. Esto evita
errores de punto flotante en la contabilidad.

---

## 6. Flujo de una transferencia

```text
POST /v1/transfers
  Idempotency-Key: ...
        |
        v
Validación Pydantic
        |
        v
BEGIN IMMEDIATE
  - verificar clave de idempotencia
  - leer cuentas y versiones
  - validar estado, moneda y saldo
  - debitar origen y acreditar destino (versión optimista)
  - insertar transacción POSTED
  - insertar asiento con dos líneas: Dr pasivo origen / Cr pasivo destino
  - registrar auditoría
  - guardar clave de idempotencia
COMMIT
        |
        v
201 Created + asiento + correlation_id
```

Si falla cualquier paso, se hace `ROLLBACK`: no queda ni movimiento ni asiento ni
clave. Si dos transferencias compiten por la misma cuenta, la versión optimista y
el trigger de sobregiro impiden dejar saldo negativo.

---

## 7. Dataset sintético y verdad AML

`scripts/seed.py` genera, con semilla fija:

- 500 clientes ficticios;
- ~800 cuentas en PYG y USD;
- ~50.000 movimientos en seis meses (2026-04-01 a 2026-09-30);
- asientos, comisiones, tipos de cambio y cierres diarios;
- patrones sospechosos etiquetados en `_aml_ground_truth`:
  estructuración, pass-through, alta velocidad, montos redondos y reactivación
  de cuentas dormidas.

La tabla de verdad también guarda una muestra de operaciones normales para medir
falsos positivos. **No se expone por la API** y no representa una lista real de
sanciones ni un juicio sobre personas. Es un insumo de prueba para la Fase 5.

---

## 8. Límites del prototipo

- SQLite permite un solo escritor a la vez; sirve para demostrar invariantes, no
  para alta concurrencia productiva.
- La API no implementa autenticación, autorización, cuotas ni cifrado de canal.
- La transferencia es síncrona y de una sola moneda; la conversión FX existe en
  el dataset, pero no como endpoint público en esta fase.
- No hay integración real con SPI, SWIFT, ISO 20022 ni corresponsales; eso se
  modela en la Fase 4.
- KYC, screening y reglas AML se implementan en la Fase 5 sobre este dataset.
- No se usan datos reales ni se afirma haber operado herramientas externas.

Estos límites están registrados en `docs/SUPUESTOS.md` y `docs/PENDIENTES.md`.

---

## 9. Cómo ejecutarlo

```powershell
# Dependencias
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Base sintética (semilla fija)
python 05-core-middleware/scripts/seed.py --reset

# Contrato OpenAPI
python 05-core-middleware/scripts/export_openapi.py

# API
python -m uvicorn app.main:app --app-dir 05-core-middleware --reload

# Pruebas
pytest -q

# Cierre diario manual
python 05-core-middleware/scripts/close_day.py --date 2026-09-30
```

Documentación interactiva: `http://127.0.0.1:8000/docs` y contrato en
`05-core-middleware/openapi.yaml`.

---

## 10. Trazabilidad con el resto del portafolio

| Fase | Relación |
|---|---|
| 1 — Negocio y procesos | Los procesos BPMN de transferencia y alertas definen el flujo que aquí se implementa. |
| 2 — Requerimientos | Historias de cuentas, transferencias y auditoría se materializan en la API y el libro mayor. |
| 3 — Core y middleware | Este documento y el código de `05-core-middleware/`. |
| 4 — Mensajería | Los mensajes ISO 20022/SWIFT usarán estas cuentas y asientos como destino. |
| 5 — AML | Las reglas se validarán contra `_aml_ground_truth` y los movimientos sintéticos. |
| 6 — Analítica | Los datasets y dashboards consumirán el modelo y las consultas de control. |
| 7 — QA/UAT | Los casos UAT y pipelines reutilizarán la suite pytest y el contrato OpenAPI. |
