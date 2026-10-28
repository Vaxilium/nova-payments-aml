# Requerimientos no funcionales (NFR)

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub  
**Documento:** NFR-NB-001  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Autor:** Franco Tillería Centurión — Business Analyst  
**Fase:** 2 — Requerimientos

> Caso 100 % ficticio. Las metas son objetivos de diseño, no resultados medidos. Los valores marcados como parámetro deben validarse con TI, Operaciones, Riesgos y Cumplimiento antes de un uso real.

---

## 1. Propósito y alcance

Definir los atributos de calidad que deben cumplir los pagos locales, los pagos internacionales, el onboarding, el monitoreo AML, la contabilidad y la auditoría. Los NFR complementan las historias funcionales (`historias-usuario.md`) y se verifican en pruebas técnicas, UAT y operación.

**Categorías cubiertas:** disponibilidad 24/7, rendimiento, seguridad, auditoría, idempotencia, conciliación, escalabilidad, observabilidad, recuperación, privacidad, interoperabilidad, usabilidad, mantenibilidad, calidad de datos, localización y protección contra abuso.

---

## 2. Convenciones

- **Prioridad:** `Must` (obligatorio para el MVP) o `Should` (relevante, puede evolucionar).
- **Métrica:** valor observable y verificable; no se declara cumplimiento sin evidencia.
- **Verificación:** método previsto (prueba de carga, revisión, monitoreo, UAT, análisis estático).
- **Trazabilidad:** historia(s) funcional(es) y requerimiento del BRD relacionados.
- **Parámetro:** valor inicial del caso; requiere aprobación formal antes de producción.

---

## 3. Catálogo de NFR

| ID | Categoría | Requerimiento | Métrica / objetivo | Verificación | Prioridad | Trazabilidad |
|---|---|---|---|---|---|---|
| NFR-01 | Disponibilidad | El canal de pagos opera 24/7, incluidos feriados, con tolerancia a fallos de dependencias. | Disponibilidad mensual ≥ 99,9 %, excluyendo mantenimientos aprobados y comunicados. | Monitoreo sintético cada minuto, registro de incidentes y prueba de failover. | Must | BR-01, BR-03, NFR-01 BRD; US-040 |
| NFR-02 | Rendimiento | La acreditación local y la evaluación de riesgo cumplen los SLA del negocio. | p95 acreditación local ≤ 5 s; p95 evaluación de riesgo ≤ 2 s; p95 consulta de estado ≤ 500 ms. | Prueba de carga con 100 pagos concurrentes y medición de percentiles. | Must | BR-01, BR-07; US-001, US-016, US-040 |
| NFR-03 | Seguridad | Autenticación fuerte, autorización por rol, cifrado en tránsito y en reposo, mínimo privilegio y gestión de secretos. | TLS 1.2+; cifrado en reposo; 100 % de endpoints con autorización; 0 secretos en repositorio. | Revisión de configuración, pruebas de autorización y análisis de secretos. | Must | BR-12, NFR-03 BRD; US-037 |
| NFR-04 | Auditoría | Todo evento relevante se registra en una bitácora de solo agregado, correlacionada y consultable. | 100 % de operaciones con cadena de eventos completa; retención inicial de 5 años (parámetro). | Consulta de traza por operación, prueba de inmutabilidad y muestreo de auditoría. | Must | BR-12, NFR-04 BRD; US-027, US-038 |
| NFR-05 | Idempotencia | Las operaciones que crean o modifican pagos aceptan una clave de idempotencia y no duplican efectos. | 100 % de APIs mutantes con `Idempotency-Key`; misma clave + mismo payload = misma respuesta; misma clave + payload distinto = 409. | Pruebas de reintento, timeout simulado y concurrencia. | Must | BR-15; US-009, US-039 |
| NFR-06 | Conciliación | Los asientos se concilian diariamente contra el riel y el core, con diferencias trazables. | ≥ 99,5 % de asientos conciliados automáticamente; 100 % de diferencias con dueño y plazo. | Cierre diario con dataset sintético y revisión de la cola de diferencias. | Must | BR-11, NFR-10 BRD; US-024, US-025, US-026 |
| NFR-07 | Escalabilidad | La plataforma soporta picos de campañas y cierres sin degradar los SLA. | 50 TPS locales y 5 TPS internacionales sostenidos; pico de 3× por 15 min sin errores críticos. | Prueba de carga y análisis de capacidad. | Should | BR-01, BR-05, NFR-05 BRD; US-001, US-007 |
| NFR-08 | Observabilidad | Métricas, logs y trazas permiten detectar degradaciones por componente. | 100 % de servicios con health check, métricas de latencia/error y correlación; alerta en ≤ 1 min. | Revisión de tableros, prueba de alerta y análisis de trazas. | Must | BR-13, NFR-06 BRD; US-040 |
| NFR-09 | Recuperación | Existe plan de continuidad y recuperación probado para los componentes críticos. | RTO ≤ 30 min; RPO ≤ 5 min para pagos y libro mayor; prueba de recuperación al menos trimestral. | Simulacro documentado y revisión de resultados. | Must | NFR-07 BRD; US-040 |
| NFR-10 | Privacidad | Se aplican minimización, enmascaramiento y control de acceso a datos personales y de AML. | 0 datos personales en logs; enmascaramiento en pantallas y notificaciones; acceso por necesidad de saber. | Revisión de logs, pruebas de acceso y análisis de datos. | Must | NFR-10 BRD; US-027, US-031, US-033 |
| NFR-11 | Interoperabilidad | Los contratos de API están versionados y la mensajería usa estándares financieros. | API `/v1` con OpenAPI; ISO 20022 para cross-border; ISO 4217 para monedas; ISO 13616 para IBAN. | Revisión de contrato, validación de esquema y pruebas de mapeo. | Must | BR-05, BR-06, NFR-09 BRD; US-006, US-007 |
| NFR-12 | Usabilidad | El flujo de pago es corto, claro y con errores accionables. | ≤ 4 pasos para un pago local; 100 % de errores con causa y próximo paso; objetivo WCAG 2.1 AA. | Prueba de usabilidad y revisión de accesibilidad. | Should | BR-03, NFR-08 BRD; US-001, US-031, US-032 |
| NFR-13 | Mantenibilidad | El código y las reglas se organizan por dominio, con pruebas automatizadas de los flujos críticos. | Cobertura ≥ 80 % en reglas de dominio y flujos críticos; deuda técnica priorizada. | Análisis estático, revisión de código y suite de pruebas. | Should | NFR-09 BRD; US-017, US-024, US-039 |
| NFR-14 | Calidad de datos | Los datos sintéticos son reproducibles, íntegros y sin PII real. | Semilla fija `NOVABANK_SEED=20261027`; integridad referencial 100 %; 0 PII real. | Script de seed, pruebas de integridad y revisión de datos. | Must | NFR-10 BRD; todas las historias con datos |
| NFR-15 | Localización | Importes, fechas y zonas horarias se presentan correctamente al usuario paraguayo. | PYG con separadores es-PY; almacenamiento en UTC; visualización en `America/Asuncion`. | Pruebas de formato y revisión de conversión. | Should | BR-01, BR-03; US-001, US-003 |
| NFR-16 | Protección contra abuso | Se aplican límites de tasa y controles antiabuso en APIs y canales. | Límite inicial de 100 req/min por cliente; respuesta 429 con `Retry-After`; bloqueo temporal tras intentos fallidos. | Prueba de carga negativa y revisión de configuración. | Should | NFR-03 BRD; US-037, US-039 |

---

## 4. Fichas detalladas de los NFR críticos

### 4.1 NFR-01 — Disponibilidad 24/7

| Campo | Valor |
|---|---|
| Definición | El servicio acepta y procesa pagos en todo momento, salvo ventanas de mantenimiento aprobadas y comunicadas. |
| Meta | ≥ 99,9 % mensual. |
| Ventana de medición | Mes calendario; se excluyen mantenimientos aprobados y se reportan aparte. |
| Fuente | Monitoreo sintético, APM, registro de incidentes. |
| Dueño | TI — Operaciones de Servicios. |
| Alerta | Disponibilidad < 99,95 % en ventana móvil de 24 h o caída > 5 min. |
| Dependencias | Core, SPI, SWIFT, screening, base de datos y red. |
| Riesgo asociado | R-04 (indisponibilidad). |

**Criterios de aceptación**

```gherkin
Escenario: Cálculo mensual de disponibilidad
  Dado que el monitoreo sintético ejecuta una prueba cada minuto
  Cuando se calcula la disponibilidad del mes
  Entonces el resultado excluye solo mantenimientos aprobados y comunicados
  Y el valor es mayor o igual a 99,9 %

Escenario: Caída de una dependencia crítica
  Dado que el core deja de responder por más de 5 minutos
  Cuando el monitoreo detecta la caída
  Entonces se abre un incidente con severidad y dueño
  Y se activa el plan de continuidad definido en NFR-09
```

### 4.2 NFR-02 — Rendimiento y tiempos de respuesta

| Campo | Valor |
|---|---|
| p95 acreditación local | ≤ 5 s desde la aceptación hasta la confirmación de acreditación. |
| p95 evaluación de riesgo | ≤ 2 s desde la solicitud de scoring hasta la decisión. |
| p95 consulta de estado | ≤ 500 ms. |
| p95 API internacional | ≤ 1 s para validación de instrucción; el envío depende del corresponsal. |
| Carga de referencia | 100 pagos locales concurrentes; 20 validaciones internacionales concurrentes. |
| Fuente | APM, logs de eventos y pruebas de carga. |
| Dueño | TI — Riesgo y Datos / Operaciones. |

**Criterios de aceptación**

```gherkin
Escenario: Carga sostenida de pagos locales
  Dado que se ejecutan 100 pagos locales concurrentes durante 15 minutos
  Cuando se calcula el percentil 95 de acreditación
  Entonces el valor es menor o igual a 5 segundos
  Y la tasa de error es menor al 1 %

Escenario: Evaluación de riesgo bajo carga
  Dado que se ejecutan 200 evaluaciones de riesgo por minuto
  Cuando se mide el tiempo de decisión
  Entonces el p95 es menor o igual a 2 segundos
  Y no se pierde ninguna evaluación
```

### 4.3 NFR-03 — Seguridad

| Control | Requisito | Verificación |
|---|---|---|
| Autenticación | MFA para usuarios internos con acceso a AML o configuración. | Prueba de inicio de sesión y revisión de configuración. |
| Autorización | RBAC/ABAC por rol y necesidad de saber. | Matriz de permisos y pruebas de acceso denegado. |
| Cifrado | TLS 1.2+ en tránsito; cifrado en reposo para datos sensibles. | Revisión de configuración y escaneo. |
| Secretos | Sin credenciales en código ni en git; uso de variables de entorno o gestor de secretos. | Análisis de secretos en CI. |
| Registro | Sin PII ni datos de tarjeta en logs; enmascaramiento. | Revisión de muestras de logs. |
| Vulnerabilidades | Dependencias auditadas y parcheo priorizado. | Análisis de dependencias. |
| Segregación | Funciones de configuración, investigación y aprobación separadas. | Prueba de roles y revisión RACI. |

**Criterios de aceptación**

```gherkin
Escenario: Acceso denegado por rol
  Dado que un usuario tiene rol de analista AML
  Cuando intenta acceder a la configuración de umbrales
  Entonces el sistema responde 403
  Y registra el intento en la bitácora

Escenario: Datos sensibles en logs
  Dado que se procesa un pago con datos del cliente
  Cuando se revisan los logs de la operación
  Entonces no aparecen documentos, cuentas completas ni datos personales sin enmascarar
```

### 4.4 NFR-04 — Auditoría y retención

| Campo | Valor |
|---|---|
| Eventos mínimos | Creación, validación, decisión de riesgo, envío, confirmación, rechazo, devolución, cambio de regla, asignación/cierre de alerta, aprobación de ROS. |
| Atributos | `event_id`, `correlation_id`, `occurred_at`, `actor`, `action`, `entity_type`, `entity_id`, `result`, `reason`. |
| Inmutabilidad | Solo agregado; sin update ni delete; hash o sello de integridad. |
| Retención | Inicial 5 años como parámetro del caso; validar con Cumplimiento/Legal (`SUPUESTO NO VERIFICADO`). |
| Consulta | Por operación, cliente, usuario, regla y rango de fechas, con control de acceso. |

**Criterios de aceptación**

```gherkin
Escenario: Traza completa de una operación
  Dado que un pago fue creado, evaluado, enviado y acreditado
  Cuando el auditor consulta la operación por su identificador de correlación
  Entonces ve todos los eventos en orden cronológico con actor y resultado
  Y no existe ningún evento obligatorio faltante

Escenario: Intento de alterar la bitácora
  Dado que un usuario intenta modificar un evento de auditoría
  Cuando envía la solicitud
  Entonces el sistema la rechaza
  Y registra el intento con el usuario y la fecha
```

### 4.5 NFR-05 — Idempotencia

| Campo | Valor |
|---|---|
| Alcance | APIs de creación de pago, envío internacional, devolución, reclamo, configuración de reglas y webhooks. |
| Clave | `Idempotency-Key` enviada por el cliente o generada por el orquestador. |
| Ventana | Mínimo 24 h; parámetro configurable. |
| Comportamiento | Misma clave + mismo payload → misma respuesta y mismo recurso. Misma clave + payload distinto → 409. |
| Persistencia | Registro de clave, hash del payload, estado y respuesta. |
| Conciliación | La clave se vincula al `payment_id` y al `correlation_id`. |

**Criterios de aceptación**

```gherkin
Escenario: Reintento después de timeout
  Dado que una solicitud de pago se envió con una clave de idempotencia y terminó en timeout
  Cuando el cliente repite la solicitud con la misma clave y el mismo payload
  Entonces el sistema devuelve la misma respuesta
  Y existe un solo pago asociado a la clave

Escenario: Conflicto de payload
  Dado que una clave de idempotencia ya fue usada con otro importe
  Cuando se envía una nueva solicitud con esa clave
  Entonces el sistema responde 409 IDEMPOTENCY_KEY_CONFLICT
  Y no crea un nuevo pago
```

### 4.6 NFR-06 — Conciliación

| Campo | Valor |
|---|---|
| Frecuencia | Diaria al cierre y bajo demanda para investigación. |
| Fuentes | Libro mayor, core bancario, riel local y mensajes/estados internacionales. |
| Meta | ≥ 99,5 % de asientos conciliados automáticamente. |
| Diferencias | 100 % con dueño, importe, referencia, plazo y evidencia. |
| Cierre | Un día no se considera cerrado si existen diferencias críticas sin explicación. |
| Dueño | Contraloría. |

**Criterios de aceptación**

```gherkin
Escenario: Cierre diario conciliado
  Dado que los registros del libro mayor, el core y el riel están completos
  Cuando se ejecuta la conciliación del día
  Entonces al menos el 99,5 % de los asientos queda conciliado
  Y cada diferencia restante tiene dueño y plazo

Escenario: Diferencia sin contraparte
  Dado que existe un asiento sin movimiento correspondiente en el riel
  Cuando se ejecuta la conciliación
  Entonces se crea una diferencia con la referencia del asiento
  Y el cierre queda en estado CON_DIFERENCIAS
```

---

## 5. Matriz de trazabilidad NFR → BRD

| NFR | BRD | Historias relacionadas | Evidencia prevista |
|---|---|---|---|
| NFR-01 | NFR-01 | US-040 | Monitoreo, incidentes, prueba de failover |
| NFR-02 | NFR-02 | US-001, US-016, US-040 | Prueba de carga y APM |
| NFR-03 | NFR-03 | US-037 | Matriz de roles y análisis de seguridad |
| NFR-04 | NFR-04 | US-027, US-038 | Consulta de traza y prueba de inmutabilidad |
| NFR-05 | BR-15 | US-009, US-039 | Pruebas de reintento y conflicto |
| NFR-06 | BR-11, NFR-10 | US-024, US-025, US-026 | Cierre diario y cola de diferencias |
| NFR-07 | NFR-05 | US-001, US-007 | Prueba de carga y capacidad |
| NFR-08 | NFR-06 | US-040 | Tableros y alertas |
| NFR-09 | NFR-07 | US-040 | Simulacro de recuperación |
| NFR-10 | NFR-10 | US-027, US-031, US-033 | Revisión de logs y accesos |
| NFR-11 | NFR-09 | US-006, US-007 | OpenAPI y validación ISO 20022 |
| NFR-12 | NFR-08 | US-001, US-031, US-032 | Prueba de usabilidad |
| NFR-13 | NFR-09 | US-017, US-024, US-039 | Cobertura y revisión de código |
| NFR-14 | NFR-10 | Todas | Seed reproducible y pruebas de integridad |
| NFR-15 | NFR-08 | US-001, US-003 | Pruebas de formato y zona horaria |
| NFR-16 | NFR-03 | US-037, US-039 | Prueba de límites de tasa |

---

## 6. Supuestos y pendientes

- Los valores de disponibilidad, latencia, capacidad, retención y límites de tasa son **parámetros de diseño** del caso ficticio; no son compromisos contractuales ni resultados medidos.
- La retención de 5 años es un valor inicial y se marca `SUPUESTO NO VERIFICADO` hasta que Cumplimiento/Legal confirme la política aplicable (ver `docs/PENDIENTES.md`).
- La verificación de NFR se completará en Fase 3 (pruebas técnicas), Fase 6 (analítica) y Fase 7 (UAT y CI).
- No se declara cumplimiento de ningún NFR sin evidencia registrada en `docs/EVIDENCIAS.md`.

## 7. Referencias

- `01-negocio/BRD.md` — sección 7.1, NFR-01 a NFR-10.
- `01-negocio/kpis.md` — métricas K-01 a K-17.
- `historias-usuario.md` — historias funcionales.
- `../02-procesos/mapa-procesos.md` — procesos y controles.
- `../docs/SUPUESTOS.md` — supuestos y parámetros.

**Fin del documento.**
