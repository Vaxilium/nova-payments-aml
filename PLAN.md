# PLAN.md — Hoja de ruta del proyecto

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub (caso ficticio)
**Rol:** Business Analyst end-to-end
**Estado actual:** Fase 5 completada; pendientes manuales heredados de fases 1 y 2 (EV-001 a EV-005).
**Última actualización:** 2026-10-29

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

- [x] Modelo de datos SQLite (clientes, cuentas, movimientos, libro mayor, asientos).
- [x] DDL y script de creación/migración.
- [x] Generador de datos sintéticos reproducible (semilla fija, sin PII real).
- [x] Libro mayor con partida doble e invariantes contables.
- [x] API FastAPI `/v1`: clientes, cuentas, transferencias, estado.
- [x] Adaptador de core/middleware simulado (interfaz estable).
- [x] Exportación de contrato OpenAPI.
- [x] Tests pytest: unitarios, integración, invariantes contables y errores.
- [x] Evidencias de Fase 3 (automáticas: seed, consultas SQL, pytest y OpenAPI; sin herramientas externas).
- [x] Commit(s) + push de cierre de fase.

**Entregables clave:** esquema SQLite con 15 triggers, dataset sintético con 341 operaciones sospechosas etiquetadas, 23 consultas SQL, API `/v1` con idempotencia, suite de 69 pruebas y `openapi.yaml`.

---

## Fase 4 — Mensajería financiera

**Objetivo:** modelar, validar y simular mensajes de pago locales e internacionales.

- [x] Catálogo ISO 20022 (pacs.008, pacs.002, pain.001, camt.053) con campos usados.
- [x] Mapeo MT103 ↔ ISO 20022 (campos obligatorios y equivalencias).
- [x] Validador de mensajes (IBAN, BIC, ISO 4217, importes, campos obligatorios).
- [x] Simulador de pago instantáneo tipo SPI con máquina de estados.
- [x] Casos de error, rechazos y reintentos.
- [x] Tests de validación y de mapeo.
- [x] Evidencias de Fase 4 (automáticas: ejemplos validados y `pytest`; sin herramientas externas).
- [x] Commit(s) + push de cierre de fase.

**Entregables clave:** catálogo con 4 tipos de mensaje, mapeo MT103↔pacs.008 con 14 filas, validador, simuladores local e internacional, 6 ejemplos (5 XML + 1 MT103), 4 diagramas Mermaid y 89 pruebas de mensajería (158 en total con el core).

---

## Fase 5 — AML y compliance

**Objetivo:** demostrar KYC, monitoreo transaccional, screening y reporte de sospechas.

- [x] Modelo KYC/CDD y estados del cliente.
- [x] Reglas de monitoreo en SQL (umbrales, velocidad, geografía, contraparte, estructuración).
- [x] Screening de listas ficticias (sanciones/PEP) con coincidencia difusa.
- [x] Motor de alertas: generación, priorización por riesgo, asignación.
- [x] Flujo de investigación y ROS ficticio (formato y campos).
- [x] Mapeo normativo (SEPRELAD, GAFI) con fuentes oficiales citadas.
- [x] Tests de reglas AML (positivos y negativos).
- [x] Evidencias de Fase 5 (automáticas: seed AML, evaluación, pytest y hook; sin herramientas externas).
- [x] Commit(s) + push de cierre de fase.

**Entregables clave:** scoring KYC, 12 reglas SQL, screening difuso, alertas/casos con SLA, evaluación contra la verdad (494 alertas, 341 TP, precisión 99,13 % sobre etiquetadas), dos ROS ficticios, matriz normativa y 25 pruebas AML (183 totales).

---

## Fase 6 — UX y analítica

**Objetivo:** mostrar diseño de pantallas y capacidad analítica sobre el dataset del caso.

- [x] Especificación de wireframes para Balsamiq/Figma (transferencia, bandeja de alertas, detalle de caso).
- [x] Flujo de prototipo y componentes reutilizables.
- [x] Excel avanzado: tablas, validaciones, Power Query, dashboard.
- [x] Dataset analítico y diccionario de datos.
- [x] Modelo y medidas DAX para Power BI.
- [x] Especificación de dashboard para Tableau.
- [ ] Evidencias manuales de Fase 6.
- [x] Commit(s) + push de cierre de fase.

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
| 2026-10-28 | 3 | Esquema SQLite con triggers, generador reproducible (500 clientes, 800 cuentas, 49.582 movimientos, 341 sospechosos etiquetados), 23 consultas SQL, API FastAPI `/v1` con idempotencia y auditoría, 69 pruebas pytest y `openapi.yaml`. Push realizado. |
| 2026-10-28 | 4 | Catálogo ISO 20022 (pacs.008/pacs.002/pain.001/camt.053), mapeo MT103↔pacs.008, validador (IBAN/BIC/ISO 4217/importes/UETR), simuladores local e internacional con idempotencia/reintentos/AML simulado, 6 ejemplos, 4 diagramas Mermaid, 89 pruebas nuevas (158 totales). Pendiente: verificación manual de fuentes bloqueadas (P-008). |
| 2026-10-29 | 5 | Scoring KYC 0–100, 12 reglas SQL calibradas, screening difuso con listas ficticias, 775 alertas deduplicadas (P1 110/P2 665), workflow de casos con SLA, evaluación contra 341 sospechosas (recall 100 %, precisión 99,13 % sobre etiquetadas), dos ROS ficticios, mapeo SEPRELAD/GAFI y 25 pruebas (183 totales). |
