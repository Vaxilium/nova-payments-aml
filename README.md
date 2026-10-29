# NovaBank — Instant & Cross-Border Payments + AML Hub

> Portfolio case study by **Franco Tillería Centurión** — Business Analyst (banking) — Asunción, Paraguay
> Fictional case. No real customer, account or confidential data is used.

## Executive Summary (English)

NovaBank is a fictional Paraguayan bank launching instant domestic transfers (inspired by the BCP's SPI) and cross-border payments over SWIFT/ISO 20022, with AML monitoring and compliance embedded end to end. This repository documents the full Business Analysis lifecycle: discovery, process modeling, requirements, core/middleware design, messaging validation, AML rules, UAT and analytics. It is built as a public portfolio to demonstrate practical BA tools and banking-domain knowledge on a realistic but entirely synthetic scenario.

Phase 1 (business analysis and process modeling) is complete at artifact level: BRD, stakeholder/RACI analysis, risk register, bilingual glossary, KPIs, regulatory context, six BPMN 2.0 processes, four DMN decision tables, Mermaid/C4/ER/journey views and a visual recreation guide. Structural validation was performed with `bpmn-moddle` and `dmn-moddle`; evidence in Bizagi/Camunda/Signavio and Lucidchart/Visio/Miro remains a manual author task.

Phase 2 (requirements) is complete at artifact level: 10 epics, 40 user stories with Gherkin acceptance criteria, MoSCoW priorities and story points, 16 non-functional requirements, two sprint plans, Jira and Azure DevOps import CSVs, a Confluence-ready space (including six ADRs and a RAID log), and a traceability matrix with reserved test-case IDs. Import evidence in Jira, Confluence and Azure DevOps remains a manual author task.

Phase 3 (core banking and middleware) is implemented and tested: a SQLite model with double-entry ledger constraints and triggers, a reproducible dataset of 500 customers, 800 accounts and 49,582 transactions (including 341 labeled suspicious operations), 23 SQL control queries, a FastAPI `/v1` service with idempotency and audit trail, 69 pytest tests and an exported OpenAPI 3.1 contract.

## Caso de negocio (5 líneas)

1. NovaBank, banco ficticio de Paraguay, quiere competir en pagos con una propuesta instantánea local e internacional.
2. El canal local se inspira en el SPI del BCP: transferencias 24/7, con confirmación en segundos y trazabilidad de estado.
3. El canal internacional usa SWIFT e ISO 20022 para pagos cross-border con validación de IBAN/BIC y control de cumplimiento.
4. El riesgo AML se gestiona de forma integrada: KYC, screening, monitoreo transaccional, alertas y reporte de operaciones sospechosas.
5. El BA lidera el ciclo completo —levantamiento, procesos, requerimientos, diseño funcional, UAT y analítica— con evidencia trazable en cada fase.

## Alcance del portafolio

El repositorio recorre siete fases: negocio y procesos; requerimientos; core y middleware; mensajería; AML y compliance; UX y analítica; QA/UAT y cierre. Cada fase produce artefactos listos para revisar o importar en herramientas reales, más un registro honesto de lo que requiere ejecución manual del autor.

## Avance de Fase 1

| Área | Artefactos | Estado |
|---|---|---|
| Negocio | BRD, stakeholders, riesgos, glosario, KPIs, contexto regulatorio | Completado |
| Procesos | 6 BPMN 2.0, 4 DMN, mapa de procesos, Mermaid | Validado estructuralmente |
| Arquitectura | C4 L1/L2, componentes, ER, event storming, journeys | Completado |
| Guía visual | Lucidchart, Visio y Miro | Completado |
| Evidencias | EV-004 y EV-005 | Pendiente de acción manual |

Documentos de entrada:

- [BRD](01-negocio/BRD.md)
- [Mapa de procesos](02-procesos/mapa-procesos.md)
- [Contexto regulatorio](01-negocio/contexto-regulatorio.md)
- [KPIs](01-negocio/kpis.md)
- [Glosario](01-negocio/glosario.md)

## Avance de Fase 2

| Área | Artefactos | Estado |
|---|---|---|
| Backlog | 10 épicas, 40 historias, Gherkin, MoSCoW y 198 story points | Completado |
| Calidad | 16 NFR y Definition of Ready/Done | Completado |
| Planificación | Sprint 1 (47 SP) y Sprint 2 (52 SP) | Completado |
| Jira | `jira_import.csv` + guía de importación | Artefactos listos; evidencia manual pendiente |
| Azure DevOps | `ado_workitems.csv` + tres pasadas de importación | Artefactos listos; evidencia manual pendiente |
| Confluence | Inicio, BRD resumido, 6 ADR, glosario, 3 actas y RAID log | Artefactos listos; evidencia manual pendiente |
| Trazabilidad | Objetivo → requerimiento → historia → proceso → `TC-###` | Completado; pruebas en Fase 7 |

Documentos de Fase 2:

- [Épicas](03-requerimientos/epicas.md)
- [Historias de usuario](03-requerimientos/historias-usuario.md)
- [Requerimientos no funcionales](03-requerimientos/requerimientos-no-funcionales.md)
- [Planificación de sprints](03-requerimientos/planificacion-sprints.md)
- [Definition of Ready/Done](03-requerimientos/definition-of-ready-done.md)
- [Matriz de trazabilidad](03-requerimientos/matriz-trazabilidad.csv)
- [Kit Confluence](03-requerimientos/confluence/README.md)

## Avance de Fase 3

| Área | Artefactos | Estado |
|---|---|---|
| Modelo de datos | 14 tablas, índices, constraints y 15 triggers contables | Completado |
| Libro mayor | Partida doble por moneda, inmutabilidad, conciliación de saldos | Completado y probado |
| Dataset sintético | 500 clientes, 800 cuentas, 49.582 movimientos, 341 sospechosos etiquetados | Reproducible con semilla fija |
| Consultas SQL | 23 controles con CTE y window functions | Ejecutadas sin errores |
| API | FastAPI `/v1`, idempotencia, correlación y auditoría | Completado |
| Contrato | OpenAPI 3.1 exportado | Completado |
| Pruebas | 69 tests de constraints, libro mayor, API, concurrencia, seed y SQL | 69 aprobadas |

Documentos de Fase 3:

- [Core y middleware (conceptual)](docs/core-y-middleware.md)
- [README de la fase](05-core-middleware/README.md)
- [Índice de consultas SQL](05-core-middleware/sql/README.md)
- [Contrato OpenAPI](05-core-middleware/openapi.yaml)

## Herramientas demostradas

> Estado actual del repositorio. No se declara el uso de una herramienta que no se haya operado.

| Capacidad | Herramienta | Artefacto en el repositorio | Estado |
|---|---|---|---|
| Análisis de negocio | BRD / RACI / riesgos / KPIs | Documentos de `01-negocio/` | Completado |
| Modelado de procesos | Bizagi / Camunda / Signavio | 6 `.bpmn` BPMN 2.0 | Validado estructuralmente; evidencia manual pendiente |
| Modelado de decisiones | DMN (Camunda / Signavio) | 4 `.dmn` | Validado estructuralmente; evidencia manual pendiente |
| Diagramación | Lucidchart / Visio / Miro | Mermaid, C4, ER y guía de recreación | Artefactos listos; evidencia manual pendiente |
| Gestión de backlog | Jira | `jira_import.csv` + guía | Artefactos listos; evidencia manual pendiente |
| Documentación | Confluence | Páginas en Markdown + kit de espacio | Artefactos listos; evidencia manual pendiente |
| Gestión de trabajo y CI | Azure DevOps | CSV de work items + pipeline YAML | Artefactos de Fase 2 listos; pipeline en Fase 7 |
| Datos y consultas | SQL (SQLite) | Esquema, 23 consultas y reglas | Implementado y probado |
| Modelado de requisitos | Historias de usuario / Gherkin | 40 historias, NFR, DoR/DoD y trazabilidad | Completado |
| Diseño de pantallas | Balsamiq / Figma | Especificaciones + prototipo | Pendiente |
| Excel avanzado | Microsoft Excel | Workbook `.xlsx` con fórmulas y dashboard | Pendiente |
| BI — modelado | Power BI | Medidas DAX + modelo | Pendiente |
| BI — visualización | Tableau | Especificación + dataset | Pendiente |
| Mensajería internacional | SWIFT MT / ISO 20022 | Catálogo, mapeo y validador | Pendiente |
| Pagos instantáneos | SPI-like (simulador) | Máquina de estados + API | Pendiente |
| Core bancario y middleware | SQLite + FastAPI | Modelo, libro mayor, API y OpenAPI | Implementado y probado |
| AML / compliance | KYC, screening, reglas SQL | Reglas, alertas, ROS | Pendiente (Fase 5; dataset etiquetado listo) |
| Automatización de pruebas | pytest | 69 pruebas de Fase 3 | Implementado |
| Integración continua | GitHub Actions | Workflow YAML | Pendiente |

## Estructura del repositorio

```text
nova-payments-aml/
├─ 01-negocio/           # BRD, stakeholders, riesgos, glosario, KPIs
├─ 02-procesos/          # BPMN, DMN, AS-IS/TO-BE, diagramas
├─ 03-requerimientos/    # épicas, historias, CSV Jira/ADO, Confluence, trazabilidad
├─ 04-diseno-ux/         # wireframes, especificaciones de pantalla, prototipo
├─ 05-core-middleware/   # modelo SQLite, libro mayor, API, datos sintéticos, tests
├─ 06-mensajeria/        # ISO 20022, MT103, validador, simulador instantáneo
├─ 07-aml-compliance/    # KYC, reglas SQL, screening, alertas, ROS, normativa
├─ 08-qa-uat/            # estrategia, casos UAT, pipelines, evidencias
├─ 09-analitica/         # datasets, Excel, Power BI (DAX), Tableau
├─ docs/                 # gobernanza: supuestos, pendientes, fuentes, evidencias
├─ AGENTS.md             # reglas operativas para agentes y colaboradores
├─ PLAN.md               # hoja de ruta por fases
├─ requirements.txt      # dependencias de Python
├─ .env.example          # variables de entorno (sin secretos)
└─ .gitignore
```

Cada carpeta contiene un `README.md` corto con su propósito, contenidos esperados y estado.

## Gobierno del proyecto

| Documento | Uso |
|---|---|
| [PLAN.md](PLAN.md) | Fases, tareas y criterios de cierre |
| [AGENTS.md](AGENTS.md) | Reglas de trabajo, contexto y convenciones |
| [docs/SUPUESTOS.md](docs/SUPUESTOS.md) | Decisiones y supuestos registrados |
| [docs/PENDIENTES.md](docs/PENDIENTES.md) | Bloqueos y tareas que requieren acción manual |
| [docs/FUENTES.md](docs/FUENTES.md) | Fuentes oficiales verificadas y su uso |
| [docs/EVIDENCIAS.md](docs/EVIDENCIAS.md) | Pasos manuales, capturas y enlaces de herramientas |

## Estado del proyecto

| Fase | Estado |
|---|---|
| 0 — Preparación del repositorio | Completada |
| 1 — Negocio y procesos | Completada en artefactos; evidencias manuales pendientes |
| 2 — Requerimientos | Completada en artefactos; evidencias manuales pendientes |
| 3 — Core bancario y middleware | Completada |
| 4 — Mensajería | Pendiente |
| 5 — AML y compliance | Pendiente |
| 6 — UX y analítica | Pendiente |
| 7 — QA/UAT y cierre | Pendiente |

## Aviso de ficción

NovaBank, sus clientes, cuentas, BIC e IBAN son inventados. Los formatos son válidos a título ilustrativo, pero no corresponden a entidades reales. Las referencias a BCP, SWIFT, GAFI, SEPRELAD e ISO 20022 son públicas y se citan como contexto normativo/técnico; el repositorio no representa a ninguna de esas entidades ni utiliza información confidencial.

## Autor

**Franco Tillería Centurión** — Analista Funcional / Business Analyst
LinkedIn: _pendiente de enlace público_.
