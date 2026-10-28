# Definition of Ready y Definition of Done

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub  
**Documento:** DOD-NB-001  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Autor:** Franco Tillería Centurión — Business Analyst  
**Fase:** 2 — Requerimientos

> Criterios de calidad del backlog y de las entregas. Se aplican a las historias de `historias-usuario.md` y a los sprints de `planificacion-sprints.md`.

---

## 1. Definition of Ready (DoR)

Una historia está **lista** para entrar a un sprint cuando cumple todos estos criterios:

| # | Criterio | Evidencia |
|---|---|---|
| 1 | Tiene ID único, título claro y épica asignada. | Ficha de la historia. |
| 2 | Sigue el formato «Como… quiero… para…» con actor identificable. | Ficha de la historia. |
| 3 | Tiene al menos un criterio de aceptación en Gherkin, verificable. | Bloque `gherkin`. |
| 4 | Tiene prioridad MoSCoW y story points estimados por el equipo. | Tabla de la historia. |
| 5 | Sus dependencias están identificadas y resueltas o planificadas en el mismo sprint. | Campo `Dependencias`. |
| 6 | Los requerimientos de negocio y el proceso BPMN están vinculados. | Campo `Requerimientos` y `Proceso`. |
| 7 | Los NFR aplicables están identificados. | `requerimientos-no-funcionales.md`. |
| 8 | Los datos necesarios existen o están especificados (sintéticos, con semilla). | Diccionario/seed de Fase 3. |
| 9 | Los criterios de aceptación no dependen de una herramienta que el equipo no tiene. | Revisión del BA y TI. |
| 10 | El equipo entiende la historia y no hay preguntas bloqueantes. | Refinamiento registrado. |
| 11 | El caso de prueba reservado (`TC-###`) está vinculado en la matriz de trazabilidad. | `matriz-trazabilidad.csv`. |
| 12 | El riesgo asociado está identificado cuando aplica. | `01-negocio/riesgos.md`. |

### 1.1 Regla de bloqueo

Una historia **no entra** al sprint si:

- depende de una historia no terminada y no hay una estrategia de stub o contrato acordada;
- no tiene criterios de aceptación observables;
- requiere una definición regulatoria aún marcada `SUPUESTO NO VERIFICADO` y el riesgo no está aceptado;
- no tiene dueño de negocio para validar el resultado.

---

## 2. Definition of Done (DoD)

Una historia está **terminada** cuando cumple todos estos criterios:

| # | Criterio | Evidencia |
|---|---|---|
| 1 | El código o artefacto implementa todos los criterios de aceptación. | Revisión y demo. |
| 2 | Las pruebas automatizadas del flujo crítico pasan. | Reporte de `pytest` o equivalente. |
| 3 | Los casos negativos y de error definidos en Gherkin están cubiertos. | Suite de pruebas. |
| 4 | Los NFR aplicables fueron verificados o existe un plan con fecha. | Registro de prueba. |
| 5 | La traza de auditoría registra los eventos obligatorios. | Consulta de bitácora. |
| 6 | La idempotencia se verificó cuando la historia crea o modifica recursos. | Prueba de reintento. |
| 7 | La documentación funcional y técnica está actualizada. | README, OpenAPI, ADR o runbook. |
| 8 | El código pasó revisión por pares y no introduce secretos ni datos reales. | Pull request y análisis. |
| 9 | La historia está demostrada en la review del sprint. | Acta o grabación (ficticia). |
| 10 | El caso de prueba `TC-###` está actualizado con resultado. | Matriz de trazabilidad / Fase 7. |
| 11 | El producto o proceso quedó desplegado en el ambiente de prueba. | Evidencia de despliegue. |
| 12 | No quedan defectos críticos o altos abiertos sin aceptación. | Defect log. |

### 2.1 DoD específico por tipo de historia

| Tipo | Criterios adicionales |
|---|---|
| Pago local | Estado final consistente, asiento balanceado, notificación enviada o reintentada, sin duplicados. |
| Cross-border | pacs.008 validado, pacs.002 correlacionado, UETR trazable, rechazo/devolución con caso. |
| Onboarding/KYC | Evidencia de identidad, screening y scoring; decisión y motivo registrados. |
| AML/alertas | Regla versionada, alerta con contexto, prioridad, dueño, SLA y cierre con evidencia. |
| ROS | Campos obligatorios completos, aprobación, hash y marca de ficticio. |
| Contabilidad | Partida doble balanceada, conciliación ejecutada, diferencia con dueño. |
| Reporting | KPI con fórmula, periodo, fuente y dueño; sin datos inventados. |
| Plataforma | Autorización probada, evento correlacionado, health check y alerta operativa. |

---

## 3. Definition of Done del sprint

Un sprint se considera terminado cuando:

- [ ] Todas las historias comprometidas cumplen la DoD o fueron renegociadas con Producto.
- [ ] El incremento es demostrable en el ambiente de prueba.
- [ ] La suite de regresión pasa.
- [ ] Los NFR críticos del incremento fueron verificados.
- [ ] La matriz de trazabilidad está actualizada.
- [ ] Los riesgos e impedimentos nuevos están en el RAID log.
- [ ] La retrospectiva se realizó y las acciones tienen dueño y fecha.
- [ ] No hay incidentes críticos abiertos sin plan.

---

## 4. Definition of Done de la fase

La Fase 2 se considera terminada cuando:

- [x] Épicas e historias creadas y priorizadas.
- [x] Criterios de aceptación en Gherkin.
- [x] NFR documentados y trazados.
- [x] Planificación de dos sprints.
- [x] CSV de Jira y Azure DevOps con guía de importación.
- [x] Kit Confluence (inicio, BRD, ADR, glosario, actas, RAID).
- [x] Matriz de trazabilidad con IDs de prueba reservados.
- [ ] Evidencias manuales EV-001, EV-002 y EV-003 completadas por el autor.
- [ ] Revisión de calidad y aprobación ficticia de Producto.

> Las evidencias manuales dependen de herramientas que el agente no opera; se registran en `docs/EVIDENCIAS.md`.

---

## 5. Roles y responsabilidades

| Actividad | Responsable | Consulta | Informa |
|---|---|---|---|
| Refinamiento y DoR | BA | Producto, TI, Operaciones | Equipo |
| Estimación | Equipo | BA, TI | Producto |
| Implementación y pruebas | TI / QA | BA, Cumplimiento | Producto |
| Aceptación funcional | Producto | BA, Operaciones | Sponsor |
| Aceptación de riesgo/AML | Cumplimiento | Riesgos | Producto |
| Cierre de sprint | Producto | BA, TI | Sponsor |

---

## 6. Referencias

- `historias-usuario.md` — historias y Gherkin.
- `planificacion-sprints.md` — objetivos y alcance de sprints.
- `requerimientos-no-funcionales.md` — atributos de calidad.
- `matriz-trazabilidad.csv` — trazabilidad y casos reservados.
- `../01-negocio/riesgos.md` — riesgos y controles.

**Fin del documento.**
