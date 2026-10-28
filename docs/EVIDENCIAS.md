# EVIDENCIAS

Registro de pasos manuales, capturas y enlaces de herramientas que el agente **no puede operar**.

> **Regla de honestidad:** aquí solo se documenta lo que el autor ejecutó realmente. Los placeholders `_pendiente_` no son evidencia. Nunca completar con enlaces inventados.

## Cómo usar este documento

1. Al cerrar cada fase, el agente agrega una sección con los pasos a ejecutar y los espacios para captura/enlace.
2. El autor importa los artefactos, verifica el resultado y completa los campos.
3. Solo entonces el estado pasa de `Pendiente` a `Completado`.
4. Si algo no se puede reproducir, se anota el motivo (no se omite).

## Índice de evidencias

| ID | Fase | Herramienta | Artefacto a importar | Enlace | Captura | Fecha | Estado |
|---|---|---|---|---|---|---|---|
| EV-001 | 2 | Jira | `03-requerimientos/jira_import.csv` | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-002 | 2 | Confluence | `03-requerimientos/confluence/*.md` | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-003 | 2 | Azure DevOps | `ado_workitems.csv` + `ado_import/*.csv` | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-004 | 1 | Bizagi / Camunda / Signavio | Archivos `.bpmn` y `.dmn` | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-005 | 1 | Lucidchart / Visio / Miro | Diagramas C4, procesos y journeys | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-006 | 6 | Balsamiq / Figma | Wireframes y prototipo | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-007 | 6 | Power BI | Modelo y dashboard | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-008 | 6 | Tableau | Dashboard | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-009 | 7 | Azure DevOps | Pipeline ejecutado | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-010 | 7 | GitHub Actions | Workflow ejecutado | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-011 | 7 | LinkedIn | Post publicado | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |

## Fase 0 — Preparación

No requiere evidencias externas. Los artefactos son archivos del repositorio y commits en GitHub.

- [x] Repositorio creado y remoto configurado.
- [x] Primer push verificado en GitHub: https://github.com/Vaxilium/nova-payments-aml (2026-10-27, rama `main`).

---

## Fase 1 — Negocio y procesos

### EV-004 — Importar BPMN/DMN en Bizagi, Camunda o Signavio

**Estado:** Pendiente de acción manual.

Pasos:

1. Abrir Camunda Modeler, Bizagi Modeler o Signavio Process Manager.
2. Importar `02-procesos/bpmn/transferencia-instantanea-to-be.bpmn`.
3. Verificar pool, lanes, eventos, gateways, flujos y etiquetas.
4. Importar los cinco BPMN restantes:
   - `transferencia-instantanea-as-is.bpmn`
   - `transferencia-internacional-to-be.bpmn`
   - `onboarding-kyc.bpmn`
   - `alerta-aml.bpmn`
   - `investigacion-ros.bpmn`
5. Importar los cuatro DMN:
   - `ruteo-riesgo-transferencia.dmn`
   - `scoring-riesgo-cliente.dmn`
   - `prioridad-alertas.dmn`
   - `limites-aprobaciones.dmn`
6. Ejecutar al menos una regla de cada DMN con datos ficticios.
7. Capturar el diagrama y el resultado de la decisión.

**Verificación mínima:**
- [ ] Los seis BPMN abren sin errores.
- [ ] Los cuatro DMN abren sin errores.
- [ ] Las lanes y etiquetas se ven completas.
- [ ] Una regla de ruteo devuelve un resultado coherente.
- [ ] Una regla de scoring devuelve un puntaje y una clasificación.
- [ ] Una regla de prioridad asigna P1/P2/P3.
- [ ] Una regla de límites devuelve aprobación o rechazo.

- Enlace al proyecto/modelo: _pendiente_
- Captura BPMN local TO-BE: _pendiente_
- Captura DMN ruteo: _pendiente_
- Fecha: _pendiente_
- Herramienta usada: _pendiente_

### EV-005 — Recrear diagramas en Lucidchart, Visio o Miro

**Estado:** Pendiente de acción manual.

Pasos:

1. Seguir `02-procesos/guia-lucidchart-visio-miro.md`.
2. Crear el contexto C4 y el diagrama de contenedores.
3. Recrear el proceso local TO-BE y el proceso internacional.
4. Recrear el journey de cliente persona y el de empresa.
5. Compartir con permiso de solo lectura.
6. Capturar cada frame/diagrama.

**Verificación mínima:**
- [ ] Contexto C4 con actores y sistemas externos.
- [ ] Contenedores con orquestador, riesgo, mensajería, core y datos.
- [ ] Proceso local TO-BE con lanes y gateways.
- [ ] Journey persona y empresa.
- [ ] Sin datos reales.
- [ ] Enlace de lectura probado.

- Enlace Lucidchart: _pendiente_
- Enlace Visio (OneDrive/SharePoint): _pendiente_
- Enlace Miro: _pendiente_
- Captura contexto C4: _pendiente_
- Captura proceso local TO-BE: _pendiente_
- Captura journey: _pendiente_
- Fecha: _pendiente_

### Checklist de cierre de Fase 1

- [x] BRD, stakeholders, riesgos, glosario, KPIs y contexto regulatorio creados.
- [x] Seis BPMN y cuatro DMN creados.
- [x] BPMN validados con `bpmn-moddle`.
- [x] DMN validados con `dmn-moddle`.
- [x] Mermaid, C4, ER, event storming y journeys creados.
- [x] Guía de recreación visual creada.
- [ ] EV-004 completada por el autor.
- [ ] EV-005 completada por el autor.

> **Nota:** la validación estructural con `bpmn-moddle`/`dmn-moddle` no equivale a una prueba en Camunda, Bizagi o Signavio. La evidencia de herramienta sigue pendiente.

---

## Fase 2 — Requerimientos

### EV-001 — Importar backlog en Jira

**Estado:** Pendiente de acción manual.

Artefacto: `03-requerimientos/jira_import.csv` (50 filas: 10 épicas + 40 historias).
Guía: `03-requerimientos/guia-importacion-jira.md`.

Pasos:

1. Crear un proyecto Jira Cloud con clave `NOVA` (company-managed o team-managed).
2. Crear los campos personalizados `Story Points` (número) y `Sprint` (si el proyecto no los trae).
3. Importar `jira_import.csv` desde **Issues → Import issues from CSV**.
4. Mapear columnas:
   - `External issue ID` → clave externa.
   - `Issue Type` → tipo (`Epic`/`Story`).
   - `Summary`, `Description`, `Priority`, `Labels`, `Story Points` → campos homónimos.
   - `Epic Name` + `Epic Link` (company-managed) o `Parent` (team-managed).
   - `Sprint` → sprint correspondiente.
5. Crear el tablero Scrum y los sprints `Sprint 1` y `Sprint 2`.
6. Verificar que las descripciones conserven los escenarios Gherkin.

**Verificación mínima:**
- [ ] 10 épicas creadas.
- [ ] 40 historias creadas y vinculadas a su épica.
- [ ] 198 story points en total.
- [ ] Sprint 1: 10 historias / 47 SP.
- [ ] Sprint 2: 9 historias / 52 SP.
- [ ] Backlog restante: 21 historias / 99 SP.
- [ ] Una historia de ejemplo muestra criterios Gherkin completos.

- Enlace del proyecto: _pendiente_
- Enlace del tablero: _pendiente_
- Captura del backlog: _pendiente_
- Captura de una historia con Gherkin: _pendiente_
- Fecha: _pendiente_

### EV-002 — Crear espacio en Confluence

**Estado:** Pendiente de acción manual.

Artefacto: `03-requerimientos/confluence/`.
Guía: `03-requerimientos/confluence/README.md`.

Pasos:

1. Crear el espacio `NovaBank` (clave sugerida: `NOVA`).
2. Crear la página de inicio desde `00-inicio.md`.
3. Crear las páginas hijas en este orden:
   - `01-brd-resumido.md`
   - `02-decisiones/README.md` y los seis ADR (`adr-001` a `adr-006`)
   - `03-glosario.md`
   - `04-actas/acta-2026-10-20-kickoff.md`, `acta-2026-10-22-requerimientos.md`, `acta-2026-10-27-refinamiento.md`
   - `05-raid-log.md`
4. Pegar el Markdown y revisar tablas, encabezados y enlaces.
5. Etiquetar las páginas con `novabank`, `requerimientos`, `aml` y `pagos`.
6. Verificar que el índice de `00-inicio.md` apunte a las páginas creadas.

**Verificación mínima:**
- [ ] Espacio y página de inicio creados.
- [ ] BRD resumido publicado.
- [ ] Seis ADR publicados.
- [ ] Glosario publicado.
- [ ] Tres actas publicadas.
- [ ] RAID log publicado.
- [ ] Enlaces del índice funcionan.
- [ ] Sin datos reales ni enlaces inventados.

- Enlace del espacio: _pendiente_
- Enlace del índice: _pendiente_
- Captura del árbol de páginas: _pendiente_
- Captura de un ADR: _pendiente_
- Fecha: _pendiente_

### EV-003 — Importar work items en Azure DevOps

**Estado:** Pendiente de acción manual.

Artefactos: `03-requerimientos/ado_import/01_epics.csv`, `02_features.csv`, `03_stories.csv`.
Maestro de auditoría: `03-requerimientos/ado_workitems.csv`.
Guía: `03-requerimientos/guia-importacion-azure-devops.md`.

Pasos:

1. Crear organización y proyecto `NovaBank-Payments` (o ajustar el prefijo en los CSV).
2. Crear los Area Paths `NovaBank-Payments\Pagos`, `\AML`, `\Contabilidad`, `\Analitica` y `\Plataforma`.
3. Crear las Iterations `Sprint 1` (2026-11-02 a 2026-11-13) y `Sprint 2` (2026-11-16 a 2026-11-27).
4. **Pasada 1:** importar `01_epics.csv` y anotar los IDs numéricos asignados.
5. **Pasada 2:** completar `Parent` de `02_features.csv` con el ID de cada épica e importar.
6. **Pasada 3:** completar `Parent` de `03_stories.csv` con el ID de cada feature e importar.
7. Verificar la jerarquía Epic → Feature → User Story y los story points.

**Verificación mínima:**
- [ ] 10 épicas creadas.
- [ ] 15 features creadas y vinculadas.
- [ ] 40 historias creadas y vinculadas.
- [ ] 198 story points en total.
- [ ] Sprint 1 y Sprint 2 configurados.
- [ ] Una consulta de jerarquía muestra padre e hijos correctos.

- Enlace del proyecto: _pendiente_
- Enlace de la consulta de jerarquía: _pendiente_
- Captura del tablero: _pendiente_
- Captura de una historia con su feature: _pendiente_
- Fecha: _pendiente_

### Checklist de cierre de Fase 2

- [x] 10 épicas y 40 historias creadas con Gherkin, MoSCoW y story points.
- [x] 16 NFR y Definition of Ready/Done creados.
- [x] Dos sprints planificados (47 SP + 52 SP).
- [x] CSV de Jira y de Azure DevOps generados y verificados.
- [x] Kit Confluence con 6 ADR, glosario, actas y RAID log creado.
- [x] Matriz de trazabilidad con `TC-001` a `TC-040` reservados.
- [ ] EV-001 completada por el autor.
- [ ] EV-002 completada por el autor.
- [ ] EV-003 completada por el autor.

---

## Plantillas por herramienta

### Jira (Fase 2)

Ver **EV-001** en la sección Fase 2. Artefacto: `03-requerimientos/jira_import.csv`.

### Confluence (Fase 2)

Ver **EV-002** en la sección Fase 2. Artefacto: `03-requerimientos/confluence/`.

### Azure DevOps (Fases 2 y 7)

Ver **EV-003** en la sección Fase 2 para la importación de work items. El pipeline YAML se ejecuta en Fase 7 (EV-009).

### Bizagi / Camunda / Signavio (Fase 1)

- [ ] Importar cada `.bpmn` y verificar que abre sin errores.
- [ ] Importar cada `.dmn` y probar al menos una regla.
- [ ] Exportar captura del diagrama y del resultado de la decisión.
- Enlace: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

### Lucidchart / Visio / Miro (Fase 1)

- [ ] Recrear el diagrama de contexto C4 y el journey principal siguiendo la guía.
- [ ] Compartir con permiso de solo lectura.
- Enlace: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

### Balsamiq / Figma (Fase 6)

- [ ] Recrear los wireframes según la especificación de pantalla.
- [ ] Conectar el flujo del prototipo.
- [ ] Compartir enlace de solo lectura.
- Enlace: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

### Power BI (Fase 6)

- [ ] Importar el CSV del dataset analítico.
- [ ] Crear el modelo y las medidas DAX especificadas.
- [ ] Construir el dashboard y publicar captura.
- Enlace: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

### Tableau (Fase 6)

- [ ] Conectar el dataset.
- [ ] Construir las vistas especificadas.
- [ ] Publicar en Tableau Public (opcional) y capturar.
- Enlace: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

### GitHub Actions (Fase 7)

- [ ] Verificar que el workflow corre en `main`.
- [ ] Conservar enlace al run verde.
- Enlace del run: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

### LinkedIn (Fase 7)

- [ ] Revisar el borrador del post.
- [ ] Publicar solo con enlaces reales y verificados.
- Enlace del post: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_
