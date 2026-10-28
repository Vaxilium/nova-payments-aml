# Épicas del producto

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub  
**Documento:** EPI-NB-001  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Autor:** Franco Tillería Centurión — Business Analyst  
**Fase:** 2 — Requerimientos

> Caso 100 % ficticio. Las épicas agrupan el backlog por resultado de negocio y se alinean con los objetivos O-01 a O-06 del BRD.

---

## 1. Resumen

- **Épicas:** 10.
- **Historias:** 40.
- **Story points totales:** 198.
- **Prioridad:** MoSCoW (`Must`, `Should`, `Could`). En esta fase no se usa `Won't`; lo excluido está en el BRD (E-01 a E-10).
- **Estimación:** Fibonacci (1, 2, 3, 5, 8, 13). La unidad es el story point relativo, no horas.

### 1.1 Distribución por prioridad

| Prioridad | Épicas | Historias | Story points |
|---|---:|---:|---:|
| Must | 7 | 26 | 135 |
| Should | 3 | 12 | 52 |
| Could | 0 | 2 | 11 |

### 1.2 Distribución por épica

| Épica | Nombre | Prioridad | Historias | Story points | Objetivo | Procesos |
|---|---|---|---:|---:|---|---|
| EP-01 | Pagos locales instantáneos | Must | 5 | 19 | O-01 | PR-02, PR-07 |
| EP-02 | Cross-border ISO 20022 | Must | 5 | 28 | O-02 | PR-03 |
| EP-03 | Onboarding y KYC digital | Must | 5 | 28 | O-03 | PR-01, PR-14 |
| EP-04 | Monitoreo AML y gestión de alertas | Must | 5 | 26 | O-03, O-04 | PR-04, PR-05 |
| EP-05 | Investigación y ROS | Must | 3 | 16 | O-04, O-06 | PR-06 |
| EP-06 | Contabilidad, conciliación y auditoría | Must | 4 | 21 | O-06 | PR-08, PR-13 |
| EP-07 | Reporting y analítica | Should | 3 | 13 | O-04, O-05, O-06 | PR-09 |
| EP-08 | Experiencia de cliente y autoservicio | Should | 3 | 11 | O-05 | PR-07 |
| EP-09 | Parametrización y gobierno de reglas | Should | 3 | 18 | O-04 | PR-10 |
| EP-10 | Plataforma, seguridad e idempotencia | Must | 4 | 18 | O-06 | PR-11, PR-13 |

---

## 2. Fichas de épicas

### EP-01 — Pagos locales instantáneos

| Campo | Valor |
|---|---|
| Prioridad MoSCoW | Must |
| Objetivos de negocio | O-01 — Lanzar transferencias instantáneas locales |
| Requerimientos BRD | BR-01, BR-02, BR-03, BR-04 |
| Procesos | PR-02, PR-07 |
| KPIs | K-01, K-02, K-03, K-04, K-14 |
| Historias | 5 (US-001, US-002, US-003, US-004, US-005) |
| Story points | 19 |

**Descripción.** Habilitar transferencias P2P y P2B en guaraníes, 24/7, con alias o cuenta, confirmación, estado en tiempo real y devoluciones controladas. Es la épica que materializa el objetivo O-01 y el proceso PR-02.

**Resultado esperado.** Un cliente puede pagar a otra persona o empresa en segundos, con confirmación y trazabilidad, sin intervención manual.

**Criterio de salida de la épica:** todas sus historias `Must` están en producción o en UAT con evidencia, y los KPIs asociados tienen fuente instrumentada.

### EP-02 — Cross-border ISO 20022

| Campo | Valor |
|---|---|
| Prioridad MoSCoW | Must |
| Objetivos de negocio | O-02 — Habilitar transferencias internacionales salientes ISO 20022 |
| Requerimientos BRD | BR-03, BR-05, BR-06, BR-15 |
| Procesos | PR-03 |
| KPIs | K-05, K-06 |
| Historias | 5 (US-006, US-007, US-008, US-009, US-010) |
| Story points | 28 |

**Descripción.** Procesar pagos internacionales salientes en USD/EUR con validación de IBAN, BIC, moneda e importe, generación de pacs.008, procesamiento de pacs.002 y gestión de rechazos, devoluciones y reintentos idempotentes. Materializa O-02 y PR-03.

**Resultado esperado.** Un pago internacional se valida, se envía como mensaje ISO 20022 y se sigue hasta su estado final sin reparación manual.

**Criterio de salida de la épica:** todas sus historias `Must` están en producción o en UAT con evidencia, y los KPIs asociados tienen fuente instrumentada.

### EP-03 — Onboarding y KYC digital

| Campo | Valor |
|---|---|
| Prioridad MoSCoW | Must |
| Objetivos de negocio | O-03 — Integrar screening y scoring de riesgo en el pago |
| Requerimientos BRD | BR-07, BR-10 |
| Procesos | PR-01, PR-14 |
| KPIs | K-07, K-11 |
| Historias | 5 (US-011, US-012, US-013, US-014, US-015) |
| Story points | 28 |

**Descripción.** Permitir el alta digital de personas y empresas con verificación de identidad, screening de sanciones/PEP, scoring de riesgo, debida diligencia proporcional y revisión periódica. Materializa O-03 y PR-01/PR-14.

**Resultado esperado.** Un cliente queda dado de alta con identidad verificada, perfil de riesgo y evidencia de debida diligencia.

**Criterio de salida de la épica:** todas sus historias `Must` están en producción o en UAT con evidencia, y los KPIs asociados tienen fuente instrumentada.

### EP-04 — Monitoreo AML y gestión de alertas

| Campo | Valor |
|---|---|
| Prioridad MoSCoW | Must |
| Objetivos de negocio | O-03, O-04 — Integrar screening y scoring de riesgo en el pago, Reducir la gestión manual de pagos y alertas |
| Requerimientos BRD | BR-07, BR-08, BR-09 |
| Procesos | PR-04, PR-05 |
| KPIs | K-07, K-08, K-09, K-10, K-11 |
| Historias | 5 (US-016, US-017, US-018, US-019, US-020) |
| Story points | 26 |

**Descripción.** Evaluar screening y riesgo antes de liberar pagos, ejecutar reglas de monitoreo transaccional, priorizar alertas y gestionarlas con dueño, SLA, investigación y evidencia. Materializa O-03/O-04 y PR-04/PR-05.

**Resultado esperado.** Toda señal de riesgo se convierte en una alerta priorizada, asignada y resuelta con evidencia auditable.

**Criterio de salida de la épica:** todas sus historias `Must` están en producción o en UAT con evidencia, y los KPIs asociados tienen fuente instrumentada.

### EP-05 — Investigación y ROS

| Campo | Valor |
|---|---|
| Prioridad MoSCoW | Must |
| Objetivos de negocio | O-04, O-06 — Reducir la gestión manual de pagos y alertas, Asegurar trazabilidad y evidencia para auditoría |
| Requerimientos BRD | BR-09, BR-12 |
| Procesos | PR-06 |
| KPIs | K-10, K-12 |
| Historias | 3 (US-021, US-022, US-023) |
| Story points | 16 |

**Descripción.** Escalar casos sospechosos, reunir evidencia, preparar el borrador de ROS, aprobarlo y registrarlo de forma ficticia con control de reserva. Materializa PR-06 y el componente de cumplimiento de O-04/O-06.

**Resultado esperado.** Un caso sospechoso queda documentado, aprobado y registrado con narrativa y evidencia consistentes.

**Criterio de salida de la épica:** todas sus historias `Must` están en producción o en UAT con evidencia, y los KPIs asociados tienen fuente instrumentada.

### EP-06 — Contabilidad, conciliación y auditoría

| Campo | Valor |
|---|---|
| Prioridad MoSCoW | Must |
| Objetivos de negocio | O-06 — Asegurar trazabilidad y evidencia para auditoría |
| Requerimientos BRD | BR-11, BR-12 |
| Procesos | PR-08, PR-13 |
| KPIs | K-16, K-17 |
| Historias | 4 (US-024, US-025, US-026, US-027) |
| Story points | 21 |

**Descripción.** Registrar cada movimiento con partida doble, conciliar contra el riel y el core, gestionar diferencias y exponer una bitácora de auditoría inmutable y correlacionada. Materializa PR-08/PR-13 y O-06.

**Resultado esperado.** El libro mayor cuadra, las diferencias tienen dueño y cada operación puede reconstruirse desde la auditoría.

**Criterio de salida de la épica:** todas sus historias `Must` están en producción o en UAT con evidencia, y los KPIs asociados tienen fuente instrumentada.

### EP-07 — Reporting y analítica

| Campo | Valor |
|---|---|
| Prioridad MoSCoW | Should |
| Objetivos de negocio | O-04, O-05, O-06 — Reducir la gestión manual de pagos y alertas, Mejorar la experiencia y la transparencia del estado del pago, Asegurar trazabilidad y evidencia para auditoría |
| Requerimientos BRD | BR-13 |
| Procesos | PR-09 |
| KPIs | K-01, K-02, K-03, K-05, K-09, K-10, K-11, K-12, K-14, K-17 |
| Historias | 3 (US-028, US-029, US-030) |
| Story points | 13 |

**Descripción.** Publicar tableros operativos y de cumplimiento con definiciones versionadas, filtros y exportación controlada. Materializa BR-13 y PR-09; los datasets y dashboards se construyen en Fase 6.

**Resultado esperado.** Producto, Operaciones y Cumplimiento consultan los mismos KPIs con dueño, periodo y fuente.

**Criterio de salida de la épica:** todas sus historias `Must` están en producción o en UAT con evidencia, y los KPIs asociados tienen fuente instrumentada.

### EP-08 — Experiencia de cliente y autoservicio

| Campo | Valor |
|---|---|
| Prioridad MoSCoW | Should |
| Objetivos de negocio | O-05 — Mejorar la experiencia y la transparencia del estado del pago |
| Requerimientos BRD | BR-03, BR-04, BR-16 |
| Procesos | PR-07 |
| KPIs | K-13, K-14 |
| Historias | 3 (US-031, US-032, US-033) |
| Story points | 11 |

**Descripción.** Dar visibilidad del estado, permitir reclamos y enviar notificaciones claras y enmascaradas. Materializa O-05 y BR-16; las pantallas se especifican en Fase 6.

**Resultado esperado.** El cliente entiende qué pasó con su pago y puede resolver consultas o reclamos sin contactar al banco.

**Criterio de salida de la épica:** todas sus historias `Must` están en producción o en UAT con evidencia, y los KPIs asociados tienen fuente instrumentada.

### EP-09 — Parametrización y gobierno de reglas

| Campo | Valor |
|---|---|
| Prioridad MoSCoW | Should |
| Objetivos de negocio | O-04 — Reducir la gestión manual de pagos y alertas |
| Requerimientos BRD | BR-14 |
| Procesos | PR-10 |
| KPIs | K-09, K-11 |
| Historias | 3 (US-034, US-035, US-036) |
| Story points | 18 |

**Descripción.** Permitir que Riesgos y Cumplimiento administren límites, umbrales y reglas con versionado, aprobación, vigencia y simulación de impacto. Materializa BR-14 y PR-10.

**Resultado esperado.** Un cambio de regla se propone, simula, aprueba y activa con trazabilidad, sin desplegar código.

**Criterio de salida de la épica:** todas sus historias `Must` están en producción o en UAT con evidencia, y los KPIs asociados tienen fuente instrumentada.

### EP-10 — Plataforma, seguridad e idempotencia

| Campo | Valor |
|---|---|
| Prioridad MoSCoW | Must |
| Objetivos de negocio | O-06 — Asegurar trazabilidad y evidencia para auditoría |
| Requerimientos BRD | BR-12, BR-15, NFR-03, NFR-06 |
| Procesos | PR-11, PR-13 |
| KPIs | K-02, K-08, K-16 |
| Historias | 4 (US-037, US-038, US-039, US-040) |
| Story points | 18 |

**Descripción.** Proveer autenticación por rol, autorización, eventos correlacionados, idempotencia de API y monitoreo de salud/SLA. Es una épica habilitadora de O-06 y de todos los flujos de pago.

**Resultado esperado.** La plataforma es segura, observable, reintentable sin duplicar efectos y auditable por diseño.

**Criterio de salida de la épica:** todas sus historias `Must` están en producción o en UAT con evidencia, y los KPIs asociados tienen fuente instrumentada.

---

## 3. Reglas de priorización

1. Una épica `Must` no puede quedar fuera del MVP; si no cabe en dos sprints, se reduce el alcance de sus historias, no la épica.
2. Una historia `Must` sin dependencia resuelta no entra a un sprint (ver Definition of Ready).
3. Las historias `Could` no se comprometen en los dos primeros sprints; se reevalúan al cierre de cada sprint.
4. Un cambio de prioridad requiere decisión de Producto y queda registrado en el RAID log o en el acta correspondiente.

## 4. Referencias

- `01-negocio/BRD.md` — objetivos O-01 a O-06 y requerimientos BR-01 a BR-16.
- `01-negocio/kpis.md` — fichas K-01 a K-17.
- `02-procesos/mapa-procesos.md` — procesos PR-01 a PR-14.
- `historias-usuario.md` — detalle de las historias y Gherkin.
- `matriz-trazabilidad.csv` — vínculo objetivo → requerimiento → historia → proceso → caso de prueba.

**Fin del documento.**
