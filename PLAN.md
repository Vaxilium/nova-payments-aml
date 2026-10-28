# PLAN.md — Hoja de ruta del proyecto

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub (caso ficticio)
**Rol:** Business Analyst end-to-end
**Estado actual:** Fase 2 completada en artefactos; pendientes evidencias manuales EV-001, EV-002 y EV-003.
**Última actualización:** 2026-10-28

> Convención: marcar `[x]` solo cuando el artefacto exista y esté verificado.
> Cada tarea cerrada lleva commit convencional. Cada fase cerrada lleva `git push origin main`.

---

## Fase 0 — Preparación del repositorio

- [x] Crear `AGENTS.md` con reglas, contexto y estructura.
- [x] Crear estructura de carpetas `01`–`09` + `docs`, con README corto en cada una.
- [x] Crear `PLAN.md` con checklist por fases.
- [x] Crear `.gitignore`, `.env.example` y `requirements.txt`.
- [x] Crear entorno virtual `.venv` e instalar dependencias.
- [x] Crear documentos de gobernanza: `SUPUESTOS.md`, `PENDIENTES.md`, `FUENTES.md`, `EVIDENCIAS.md`.
- [x] Crear `README.md` inicial con resumen ejecutivo en inglés, caso de negocio, matriz de herramientas y estructura.
- [x] Commit y push a `origin main`.

---

## Fase 1 — Negocio y procesos

**Objetivo:** entender el problema, el contexto regulatorio y modelar el negocio antes de especificar.

- [x] BRD: contexto, objetivos, alcance, fuera de alcance, KPIs, restricciones.
- [x] Mapa de stakeholders y matriz RACI.
- [x] Registro de riesgos (probabilidad, impacto, mitigación, dueño).
- [x] Glosario bilingüe ES/EN (pagos, mensajería, AML).
- [x] Mapa de procesos AS-IS y TO-BE (onboarding, pagos, alertas).
- [x] BPMN 2.0: onboarding/KYC.
- [x] BPMN 2.0: transferencia instantánea local (SPI-like).
- [x] BPMN 2.0: transferencia internacional (SWIFT / ISO 20022).
- [x] BPMN 2.0: gestión de alertas AML y escalamiento.
- [x] BPMN 2.0: investigación y ROS.
- [x] DMN: scoring de riesgo de cliente.
- [x] DMN: enrutamiento y priorización de alertas.
- [x] DMN: límites, bloqueos y aprobaciones.
- [x] Diagramas: contexto C4 (L1), flujo de datos, journeys.
- [x] Investigación normativa oficial (BCP/SPI, SEPRELAD, GAFI) y registro en `docs/FUENTES.md`.
- [x] Artefactos importables para Bizagi/Camunda/Signavio (`.bpmn`, `.dmn`) y guía para Lucidchart/Visio/Miro.
- [ ] Evidencias manuales de Fase 1 en `docs/EVIDENCIAS.md` (EV-004, EV-005: requieren acción del autor).
- [x] Commit(s) + push de cierre de fase.

**Entregables clave:** BRD, BPMN, DMN, matriz de riesgos, glosario, mapa de fuentes.

---

## Fase 2 — Requerimientos

**Objetivo:** convertir el negocio en un backlog trazable y listo para Jira/Confluence/ADO.

- [x] Épicas del producto (pagos locales, cross-border, AML, reporting, UX).
- [x] Historias de usuario con criterios de aceptación en Gherkin.
- [x] Priorización MoSCoW y estimación relativa.
- [x] CSV de importación para Jira (campos, labels, épicas, sprints).
- [x] CSV de importación para Azure DevOps (work items, area paths, iterations).
- [x] Páginas Confluence en Markdown (índice, BRD, decisiones, runbook).
- [x] Matriz de trazabilidad requisito → historia → caso de prueba.
- [x] Definition of Ready / Definition of Done.
- [ ] Evidencias manuales de Fase 2 (EV-001, EV-002, EV-003: requieren acción del autor).
- [x] Commit(s) + push de cierre de fase.

**Entregables clave:** backlog de 10 épicas y 40 historias (198 SP), 16 NFR, dos sprints, CSV Jira/ADO, kit Confluence con 6 ADR, RAID log y matriz de trazabilidad con `TC-001` a `TC-040` reservados.

---

## Fase 3 — Core bancario y middleware

**Objetivo:** construir el núcleo funcional del caso con datos sintéticos y API probada.

- [ ] Modelo de datos SQLite (clientes, cuentas, movimientos, libro mayor, asientos).
- [ ] DDL y script de creación/migración.
- [ ] Generador de datos sintéticos reproducible (semilla fija, sin PII real).
- [ ] Libro mayor con partida doble e invariantes contables.
- [ ] API FastAPI `/v1`: clientes, cuentas, transferencias, estado.
- [ ] Adaptador de core/middleware simulado (interfaz estable).
- [ ] Exportación de contrato OpenAPI.
- [ ] Tests pytest: unitarios, integración, invariantes contables y errores.
- [ ] Evidencias manuales de Fase 3.
- [ ] Commit(s) + push de cierre de fase.

**Entregables clave:** esquema SQLite, dataset sintético, API documentada, suite de tests.

---

## Fase 4 — Mensajería financiera

**Objetivo:** modelar, validar y simular mensajes de pago locales e internacionales.

- [ ] Catálogo ISO 20022 (pacs.008, pacs.002, pain.001, camt.053) con campos usados.
- [ ] Mapeo MT103 ↔ ISO 20022 (campos obligatorios y equivalencias).
- [ ] Validador de mensajes (IBAN, BIC, ISO 4217, importes, campos obligatorios).
- [ ] Simulador de pago instantáneo tipo SPI con máquina de estados.
- [ ] Casos de error, rechazos y reintentos.
- [ ] Tests de validación y de mapeo.
- [ ] Evidencias manuales de Fase 4.
- [ ] Commit(s) + push de cierre de fase.

**Entregables clave:** catálogo de mensajes, validador, simulador, tests, fuentes citadas.

---

## Fase 5 — AML y compliance

**Objetivo:** demostrar KYC, monitoreo transaccional, screening y reporte de sospechas.

- [ ] Modelo KYC/CDD y estados del cliente.
- [ ] Reglas de monitoreo en SQL (umbrales, velocidad, geografía, contraparte, estructuración).
- [ ] Screening de listas ficticias (sanciones/PEP) con coincidencia difusa.
- [ ] Motor de alertas: generación, priorización por riesgo, asignación.
- [ ] Flujo de investigación y ROS ficticio (formato y campos).
- [ ] Mapeo normativo (SEPRELAD, GAFI) con fuentes oficiales citadas.
- [ ] Tests de reglas AML (positivos y negativos).
- [ ] Evidencias manuales de Fase 5.
- [ ] Commit(s) + push de cierre de fase.

**Entregables clave:** reglas SQL, motor de alertas, ROS, matriz normativa, tests.

---

## Fase 6 — UX y analítica

**Objetivo:** mostrar diseño de pantallas y capacidad analítica sobre el dataset del caso.

- [ ] Especificación de wireframes para Balsamiq/Figma (transferencia, bandeja de alertas, detalle de caso).
- [ ] Flujo de prototipo y componentes reutilizables.
- [ ] Excel avanzado: tablas, validaciones, Power Query, dashboard.
- [ ] Dataset analítico y diccionario de datos.
- [ ] Modelo y medidas DAX para Power BI.
- [ ] Especificación de dashboard para Tableau.
- [ ] Evidencias manuales de Fase 6.
- [ ] Commit(s) + push de cierre de fase.

**Entregables clave:** specs UX, workbook Excel, modelo DAX, guía Tableau, diccionario de datos.

---

## Fase 7 — QA/UAT y cierre

**Objetivo:** cerrar el ciclo con evidencia de calidad, pipelines y comunicación del portafolio.

- [ ] Estrategia de pruebas y plan UAT (alcance, ambientes, datos, criterios de salida).
- [ ] Casos UAT y matriz de cobertura.
- [ ] Pipeline Azure DevOps en YAML.
- [ ] GitHub Actions (lint + tests).
- [ ] README final con resultados, capturas y lecciones aprendidas.
- [ ] Borrador de post para LinkedIn (sin enlaces inventados).
- [ ] Revisión de calidad integral y cierre de pendientes.
- [ ] Commit(s) + push de cierre de fase.

**Entregables clave:** plan UAT, pipelines, README final, borrador LinkedIn.

---

## Hitos

| Hito | Fase | Criterio |
|---|---|---|
| M1 — Negocio entendido | 1 | BRD + BPMN/DMN aprobados internamente |
| M2 — Backlog listo | 2 | Historias con criterios y trazabilidad |
| M3 — Core operativo | 3 | API + tests verdes + libro mayor balanceado |
| M4 — Mensajería validada | 4 | Validador y simulador con tests |
| M5 — AML demostrable | 5 | Reglas, alertas y ROS con tests |
| M6 — Portafolio presentable | 6 | UX + analítica documentadas |
| M7 — Cierre | 7 | UAT, CI y README final |

## Registro de avance

| Fecha | Fase | Nota |
|---|---|---|
| 2026-10-27 | 0 | Scaffold del repositorio, gobernanza y README inicial. |
| 2026-10-27 | 1 | BRD, stakeholders, riesgos, glosario, KPIs, contexto regulatorio, 6 BPMN, 4 DMN, Mermaid, C4/ER/journeys y guía visual. Push realizado. Pendientes: EV-004 y EV-005. |
| 2026-10-28 | 2 | 10 épicas, 40 historias con Gherkin/MoSCoW/SP, 16 NFR, DoR/DoD, 2 sprints, CSV Jira/ADO, kit Confluence con 6 ADR, glosario, 3 actas y RAID log, matriz de trazabilidad con TC-001 a TC-040. Push realizado. Pendientes: EV-001, EV-002 y EV-003. |
