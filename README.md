# NovaBank — Instant & Cross-Border Payments + AML Hub

> Portfolio case study by **Franco Tillería Centurión** · Business Analyst (banking) · Asunción, Paraguay
> Fictional case. No real customer, account or confidential data is used.

## Executive Summary (English)

NovaBank is a fictional Paraguayan bank launching instant domestic transfers (inspired by the BCP's SPI) and cross-border payments over SWIFT/ISO 20022, with AML monitoring and compliance embedded end to end. This repository documents the full Business Analysis lifecycle: discovery, process modeling, requirements, core/middleware design, messaging validation, AML rules, UAT and analytics. It is built as a public portfolio to demonstrate practical BA tools and banking-domain knowledge on a realistic but entirely synthetic scenario.

## Caso de negocio (5 líneas)

1. NovaBank, banco ficticio de Paraguay, quiere competir en pagos con una propuesta instantánea local e internacional.
2. El canal local se inspira en el SPI del BCP: transferencias 24/7, con confirmación en segundos y trazabilidad de estado.
3. El canal internacional usa SWIFT e ISO 20022 para pagos cross-border con validación de IBAN/BIC y control de cumplimiento.
4. El riesgo AML se gestiona de forma integrada: KYC, screening, monitoreo transaccional, alertas y reporte de operaciones sospechosas.
5. El BA lidera el ciclo completo —levantamiento, procesos, requerimientos, diseño funcional, UAT y analítica— con evidencia trazable en cada fase.

## Alcance del portafolio

El repositorio recorre siete fases: negocio y procesos; requerimientos; core y middleware; mensajería; AML y compliance; UX y analítica; QA/UAT y cierre. Cada fase produce artefactos listos para revisar o importar en herramientas reales, más un registro honesto de lo que requiere ejecución manual del autor.

## Herramientas demostradas

> Estado inicial: todas **pendientes**. Se actualizarán a medida que avance cada fase.

| Capacidad | Herramienta | Artefacto en el repositorio | Estado |
|---|---|---|---|
| Gestión de backlog | Jira | CSV de importación + guía | Pendiente |
| Documentación | Confluence | Páginas en Markdown | Pendiente |
| Gestión de trabajo y CI | Azure DevOps | CSV de work items + pipeline YAML | Pendiente |
| Modelado de procesos | Bizagi / Camunda / Signavio | `.bpmn` BPMN 2.0 | Pendiente |
| Modelado de decisiones | DMN (Camunda / Signavio) | `.dmn` | Pendiente |
| Diagramación | Lucidchart / Visio / Miro | Mermaid/PlantUML + guía | Pendiente |
| Datos y consultas | SQL (SQLite) | Esquema, consultas, reglas | Pendiente |
| Modelado de requisitos | Historias de usuario / Gherkin | Backlog y criterios de aceptación | Pendiente |
| Diseño de pantallas | Balsamiq / Figma | Especificaciones + prototipo | Pendiente |
| Excel avanzado | Microsoft Excel | Workbook `.xlsx` con fórmulas y dashboard | Pendiente |
| BI — modelado | Power BI | Medidas DAX + modelo | Pendiente |
| BI — visualización | Tableau | Especificación + dataset | Pendiente |
| Mensajería internacional | SWIFT MT / ISO 20022 | Catálogo, mapeo y validador | Pendiente |
| Pagos instantáneos | SPI-like (simulador) | Máquina de estados + API | Pendiente |
| Core bancario y middleware | SQLite + FastAPI | Modelo, libro mayor, API | Pendiente |
| AML / compliance | KYC, screening, reglas SQL | Reglas, alertas, ROS | Pendiente |
| Automatización de pruebas | pytest | Suite de tests | Pendiente |
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
| 1 — Negocio y procesos | Pendiente |
| 2 — Requerimientos | Pendiente |
| 3 — Core bancario y middleware | Pendiente |
| 4 — Mensajería | Pendiente |
| 5 — AML y compliance | Pendiente |
| 6 — UX y analítica | Pendiente |
| 7 — QA/UAT y cierre | Pendiente |

## Aviso de ficción

NovaBank, sus clientes, cuentas, BIC e IBAN son inventados. Los formatos son válidos a título ilustrativo, pero no corresponden a entidades reales. Las referencias a BCP, SWIFT, GAFI, SEPRELAD e ISO 20022 son públicas y se citan como contexto normativo/técnico; el repositorio no representa a ninguna de esas entidades ni utiliza información confidencial.

## Autor

**Franco Tillería Centurión** — Analista Funcional / Business Analyst
LinkedIn: _pendiente de enlace público_.
