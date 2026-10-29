# Changelog

Todos los cambios relevantes de este repositorio se documentan aquí.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y versionado [SemVer](https://semver.org/lang/es/).

## [1.0.0] — 2026-10-29

### Agregado

- Fase 8 de auditoría y refuerzo del portafolio.
- `docs/AUDITORIA.md`: auditoría de verdad afirmación por afirmación.
- `README.en.md`: versión completa en inglés enlazada desde `README.md`.
- `docs/case-study.md`: caso de estudio de dos páginas.
- `docs/entrevista.md`: guion por fase con preguntas, respuestas y límites.
- `docs/github-metadata.md`: descripción corta y topics sugeridos.
- `docs/evidencias/README.md`: lista de capturas que debe subir el autor.
- `LICENSE` (MIT) y `CHANGELOG.md`.
- Comandos de Windows PowerShell probados en un clon limpio.

### Cambiado

- README: se separó lo verificado de lo que requiere ejecución manual.
- README: se aclaró que el corte reproducible de alertas es 377; el 775 es un
  snapshot histórico.
- README: “validado estructuralmente” se reemplazó por “XML bien formado” cuando
  no hubo ejecución en herramienta.
- `AGENTS.md`, `docs/SUPUESTOS.md` y `09-analitica/docs/excel.md`: rutas
  absolutas reemplazadas por rutas relativas.
- `08-qa-uat/scripts/run_uat.py`: sanea rutas absolutas en resultados y publica
  la ruta de base relativa al repositorio.

### Corregido

- `SNV-01` / `P-006`: verificado el SPI en la FAQ oficial del BCP (24/7,
  ₲10.000.000, acreditación máxima de 5 segundos).
- `F-01`, `F-03` y `F-04` de `docs/FUENTES.md`: reverificadas y actualizadas al
  2026-10-29.
- `P-005`: licencia MIT agregada.

### Verificado

- Clon limpio con entorno virtual nuevo.
- `204/204` pruebas pytest, `51/51` casos UAT automatizados, `23/23` controles SQL.
- `PRAGMA integrity_check = ok` y 0 violaciones de clave foránea.
- Seed: 500 clientes, 800 cuentas, 49.582 movimientos, 341 sospechosas.
- Evaluación AML: 494 alertadas, 341 TP, 3 FP, 150 sin etiqueta.

### Pendiente

- Evidencias manuales EV-001 a EV-011 (Jira, Confluence, Azure DevOps,
  Bizagi/Camunda/Signavio, Lucidchart/Visio/Miro, Balsamiq/Figma, Power BI,
  Tableau, GitHub Actions, LinkedIn).
- Validación de la resolución SEPRELAD aplicable a bancos de la SIB (P-009).
- Defectos DEF-001 a DEF-005, incluido DEF-003 (API sin autenticación).

## [0.7.0] — 2026-10-29

### Agregado

- Fase 7: estrategia de pruebas, plan UAT, 65 casos, matriz de cobertura,
  pipelines de GitHub Actions y Azure DevOps, README final y borradores LinkedIn.
- Defectos DEF-001 a DEF-005 y acta de cierre UAT.
- Suite final de 204 pruebas.

## [0.6.0] — 2026-10-29

### Agregado

- Fase 6: 10 wireframes, 12 CSV analíticos, workbook Excel de 11 hojas,
  36 medidas DAX, Power Query y guía Tableau.
- 16 pruebas de analítica.

## [0.5.0] — 2026-10-29

### Agregado

- Fase 5: scoring KYC, 12 reglas SQL, screening difuso, alertas y casos con SLA,
  dos ROS ficticios y mapeo normativo SEPRELAD/GAFI.
- Evaluación contra verdad: 494 alertadas, 341 TP, 3 FP, 150 sin etiqueta.

## [0.4.0] — 2026-10-28

### Agregado

- Fase 4: catálogo ISO 20022, mapeo MT103↔pacs.008, validador, simuladores local
  e internacional, ejemplos y pruebas.

## [0.3.0] — 2026-10-28

### Agregado

- Fase 3: esquema SQLite con 15 triggers, libro mayor de partida doble, seed
  reproducible, 23 consultas SQL, API FastAPI `/v1` y OpenAPI.

## [0.2.0] — 2026-10-28

### Agregado

- Fase 2: 10 épicas, 40 historias con Gherkin, 16 NFR, CSV Jira/ADO, kit
  Confluence con 6 ADR y matriz de trazabilidad.

## [0.1.0] — 2026-10-27

### Agregado

- Fase 1: BRD, stakeholders, riesgos, glosario, KPIs, 6 BPMN, 4 DMN, diagramas y
  contexto regulatorio.
- Fase 0: gobernanza del repositorio, `AGENTS.md`, `PLAN.md` y estructura inicial.
