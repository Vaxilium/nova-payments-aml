# Planificación de sprints

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub  
**Documento:** SPR-NB-001  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Autor:** Franco Tillería Centurión — Business Analyst  
**Fase:** 2 — Requerimientos

> Planificación ficticia del caso. Las fechas, la capacidad y la velocidad son supuestos de trabajo, no resultados históricos. El backlog completo está en `historias-usuario.md` y `epicas.md`.

---

## 1. Supuestos de planificación

| Parámetro | Valor | Nota |
|---|---|---|
| Equipo | 5 desarrolladores, 1 QA, 1 BA, 1 Product Owner | Roles ficticios. |
| Duración del sprint | 2 semanas | Sprint 1: 2026-11-02 a 2026-11-13. Sprint 2: 2026-11-16 a 2026-11-27. |
| Capacidad comprometida | 47 SP en Sprint 1; 52 SP en Sprint 2 | Incluye refinamiento, pruebas y documentación. |
| Velocidad inicial | 45–52 SP por sprint | Se ajusta al cierre del Sprint 1. |
| Backlog total | 40 historias / 198 SP | 10 épicas. |
| Alcance de dos sprints | 19 historias / 99 SP | 50 % del backlog; el resto queda priorizado. |
| Festivos | Sin festivos en la ventana | Si aparece un feriado, se ajusta capacidad. |

**Regla de compromiso:** el equipo no compromete una historia `Must` sin dependencia resuelta. Si una dependencia se bloquea, se activa el plan de contingencia del RAID log y se renegocia el alcance con Producto.

---

## 2. Sprint 1 — Pago local con control de riesgo

**Fechas:** 2026-11-02 a 2026-11-13  
**Capacidad:** 47 SP  
**Objetivo:** habilitar un pago local P2P de punta a punta con alta mínima de cliente, screening previo, confirmación de estado y trazabilidad idempotente.

### 2.1 Sprint goal

> «Un cliente puede iniciar un pago local, ver el beneficiario resuelto, pasar por screening y conocer el estado final, con eventos correlacionados y sin duplicados.»

### 2.2 Historias comprometidas

| ID | Historia | Épica | Prioridad | SP | Dependencias | Criterio de aceptación principal |
|---|---|---|---|---:|---|---|
| US-011 | Iniciar alta digital de cliente | EP-03 | Must | 8 | — | Solicitud creada en `PENDIENTE_VERIFICACION` con datos completos. |
| US-012 | Verificar identidad y documentación | EP-03 | Must | 5 | US-011 | Identidad `VERIFICADA` o `PENDIENTE_DOCUMENTO` con evidencia. |
| US-013 | Ejecutar screening de sanciones y PEP | EP-03 | Must | 5 | US-012 | Resultado `LIMPIO`, `REVISIÓN` o bloqueo con alerta P1. |
| US-001 | Crear transferencia local P2P | EP-01 | Must | 5 | US-011, US-037 | Pago `RECIBIDO` con ID único y comprobante preliminar. |
| US-002 | Resolver alias o cuenta destino | EP-01 | Must | 3 | US-001 | Titular y cuenta enmascarados; alias inválido rechazado. |
| US-003 | Confirmar y consultar estado | EP-01 | Must | 3 | US-001 | Estados consistentes con timestamp y próximo paso. |
| US-005 | Validar límites y saldo | EP-01 | Must | 3 | US-001 | Validación `APTA` o rechazo por saldo/límite. |
| US-016 | Evaluar screening y riesgo antes de liberar | EP-04 | Must | 5 | US-013, US-001 | Decisión `LIBERAR` o `BLOQUEAR` con evidencia. |
| US-037 | Autenticación y autorización por rol | EP-10 | Must | 5 | — | 403 para función no permitida; acceso auditado. |
| US-038 | Registrar eventos con correlación | EP-10 | Must | 5 | US-037 | Evento con `correlation_id`, actor y resultado. |

**Total comprometido:** 10 historias / **47 SP**.

### 2.3 Fuera del Sprint 1

- Cross-border (EP-02): pasa al Sprint 2.
- Devoluciones (US-004), revisión periódica (US-015), alertas avanzadas (US-017 a US-020) y contabilidad (US-024): backlog priorizado.
- Reporting y UX: Fase 6 o sprints posteriores.

### 2.4 Riesgos del sprint

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Screening depende de listas ficticias incompletas | Alto | Definir dataset mínimo antes del día 3; usar casos de prueba de Fase 5. |
| El core simulado no expone saldo | Alto | Contrato de adaptador acordado con TI antes del día 2. |
| Reglas de límite sin validación de negocio | Medio | Usar parámetros marcados y registrar decisión en RAID. |
| Falta de datos sintéticos | Medio | Semilla fija y dataset mínimo de 50 clientes/cuentas. |

### 2.5 Criterios de salida del Sprint 1

- [ ] Pago local P2P demostrable con estado final.
- [ ] Screening previo registrado en el 100 % de los pagos de prueba.
- [ ] Idempotencia y correlación verificadas en los flujos del sprint.
- [ ] Sin defectos críticos abiertos.
- [ ] Casos `TC-001`, `TC-002`, `TC-003`, `TC-005`, `TC-011`, `TC-012`, `TC-013`, `TC-016`, `TC-037`, `TC-038` actualizados.
- [ ] Demo y retrospectiva realizadas.

---

## 3. Sprint 2 — Cross-border, monitoreo y contabilidad base

**Fechas:** 2026-11-16 a 2026-11-27  
**Capacidad:** 52 SP  
**Objetivo:** habilitar el pago internacional ISO 20022 con seguimiento y reintentos, el motor de monitoreo con alertas priorizadas, y el registro contable de partida doble.

### 3.1 Sprint goal

> «Un pago internacional puede validarse, enviarse como pacs.008 y seguirse por pacs.002; el monitoreo genera alertas priorizadas y cada pago deja un asiento balanceado.»

### 3.2 Historias comprometidas

| ID | Historia | Épica | Prioridad | SP | Dependencias | Criterio de aceptación principal |
|---|---|---|---|---:|---|---|
| US-006 | Validar IBAN, BIC, moneda e importe | EP-02 | Must | 5 | US-037 | Instrucción válida o rechazo con campo y motivo. |
| US-007 | Generar y validar pacs.008 | EP-02 | Must | 8 | US-006 | Mensaje con UETR y esquema válido. |
| US-008 | Procesar pacs.002 y actualizar estado | EP-02 | Must | 5 | US-007 | Estado correlacionado por UETR. |
| US-017 | Ejecutar reglas de monitoreo | EP-04 | Must | 8 | US-016 | Alerta con regla, contexto y evidencia. |
| US-018 | Priorizar alertas P1/P2/P3 | EP-04 | Must | 3 | US-017 | P1 con SLA de 15 min; P3 en cola. |
| US-019 | Asignar y gestionar bandeja | EP-04 | Must | 5 | US-018 | Alerta `ASIGNADA` con dueño y SLA. |
| US-020 | Investigar y cerrar alerta | EP-04 | Must | 5 | US-019 | Cierre con motivo y evidencia; sin evidencia no cierra. |
| US-024 | Registrar asiento de partida doble | EP-06 | Must | 8 | US-001, US-008 | Débito = crédito; asiento vinculado al pago. |
| US-039 | Garantizar idempotencia de API | EP-10 | Must | 5 | US-037 | Misma clave no duplica; payload distinto → 409. |

**Total comprometido:** 9 historias / **52 SP**.

### 3.3 Fuera del Sprint 2

- Devolución local (US-004), devolución internacional (US-010), revisión periódica (US-015).
- Investigación/ROS (US-021 a US-023): candidatas al Sprint 3.
- Conciliación y diferencias (US-025, US-026), auditoría (US-027): Sprint 3.
- Reporting, UX y parametrización: sprints posteriores / Fase 6.

### 3.4 Riesgos del sprint

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Esquema ISO 20022 incompleto o versión incorrecta | Alto | Usar catálogo de Fase 4 y validar con esquema antes de enviar. |
| Ausencia de corresponsal simulado | Alto | Adaptador stub con estados y pacs.002 sintético. |
| Reglas de monitoreo generan ruido | Medio | Simular con dataset y calibrar umbrales; medir falsos positivos. |
| Partida doble sin contrapartes completas | Alto | Definir plan de cuentas mínimo y pruebas de invariantes. |

### 3.5 Criterios de salida del Sprint 2

- [ ] Pago internacional demostrable con pacs.008/pacs.002 y estado final.
- [ ] Reintento idempotente verificado en cross-border.
- [ ] Alerta priorizada, asignada y cerrada con evidencia.
- [ ] Asiento balanceado y conciliable para pagos locales e internacionales.
- [ ] Casos `TC-006`, `TC-007`, `TC-008`, `TC-017`, `TC-018`, `TC-019`, `TC-020`, `TC-024`, `TC-039` actualizados.
- [ ] Demo, revisión de NFR críticos y retrospectiva realizadas.

---

## 4. Vista integrada de los dos sprints

| Sprint | Foco | Historias | SP | Épicas tocadas |
|---|---|---:|---:|---|
| Sprint 1 | Pago local + onboarding + riesgo previo + trazabilidad | 10 | 47 | EP-01, EP-03, EP-04, EP-10 |
| Sprint 2 | Cross-border + monitoreo/alertas + contabilidad base + idempotencia | 9 | 52 | EP-02, EP-04, EP-06, EP-10 |
| **Total** | **MVP demostrable** | **19** | **99** | **6 de 10 épicas** |

**Backlog restante:** 21 historias / 99 SP. Incluye devoluciones, revisión periódica, investigación/ROS, conciliación avanzada, auditoría, reporting, UX y parametrización.

---

## 5. Ceremonias y artefactos

| Ceremonia | Frecuencia | Participantes | Salida |
|---|---|---|---|
| Sprint planning | Inicio de sprint | Producto, BA, TI, QA | Sprint goal y backlog comprometido. |
| Daily | Diaria (15 min) | Equipo | Impedimentos y avance. |
| Refinamiento | Semanal | Producto, BA, TI | Historias listas (DoR). |
| Review | Fin de sprint | Equipo, stakeholders | Demo y aceptación funcional. |
| Retrospectiva | Fin de sprint | Equipo | Acciones con dueño y fecha. |
| Comité de riesgo | Quincenal | Riesgos, Cumplimiento, BA | Decisiones de umbrales y excepciones. |

**Artefactos de seguimiento:** tablero Jira (CSV en `jira_import.csv`), tablero Azure DevOps (CSV en `ado_workitems.csv`), matriz de trazabilidad y RAID log.

---

## 6. Definition of Done aplicable

Cada historia debe cumplir la DoD de `definition-of-ready-done.md`. Además, para estos dos sprints:

- Todo pago debe tener traza con `correlation_id`.
- Toda operación que crea recursos debe ser idempotente.
- Todo asiento debe balancear.
- Toda alerta debe tener prioridad, dueño y SLA.
- No se aceptan datos reales ni secretos en el repositorio.

---

## 7. Plan de contingencia

| Escenario | Acción | Dueño |
|---|---|---|
| Una dependencia externa no está disponible | Usar adaptador simulado y registrar el supuesto; no bloquear el sprint completo. | TI |
| La capacidad cae por debajo de 45 SP | Retirar historias `Should` y mantener las `Must` del sprint goal. | Producto |
| Un riesgo regulatorio se materializa | Congelar la funcionalidad afectada y escalar a Cumplimiento/Legal. | BA / Cumplimiento |
| Un defecto crítico aparece en demo | No se libera el incremento; se prioriza la corrección. | QA / TI |

---

## 8. Referencias

- `historias-usuario.md` — detalle de historias y Gherkin.
- `epicas.md` — épicas y resultados.
- `definition-of-ready-done.md` — DoR/DoD.
- `requerimientos-no-funcionales.md` — NFR.
- `matriz-trazabilidad.csv` — trazabilidad.
- `../01-negocio/riesgos.md` — riesgos.
- `../docs/SUPUESTOS.md` — supuestos de capacidad y fechas.

**Fin del documento.**
