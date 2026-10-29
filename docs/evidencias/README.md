# Evidencias — capturas que debe subir el autor

Esta carpeta está pensada para almacenar capturas de pantalla de herramientas que
el agente **no puede operar**. Mientras una captura no exista, la evidencia sigue
siendo **pendiente** y no debe declararse como completada.

**Regla:** cada captura debe ser propia, sin datos personales, sin credenciales y
sin información de empleadores reales. Los nombres, cuentas y montos del caso son
ficticios.

## Convención de nombres

```text
capitalización: EV-XXX_descripcion-corta.png
ejemplo:        EV-001_jira-backlog.png
```

Formatos aceptados: `.png`, `.jpg` o `.webp`. Tamaño recomendado: 1400–1920 px de
ancho. Para enlaces, usar una lista en el `docs/EVIDENCIAS.md` con fecha de acceso.

## Lista de capturas

### Fase 1 — Procesos

- [ ] `EV-004_bpmn-local-to-be.png` — BPMN de transferencia instantánea TO-BE en
      Camunda, Bizagi o Signavio.
- [ ] `EV-004_bpmn-internacional-to-be.png` — BPMN de transferencia internacional.
- [ ] `EV-004_dmn-scoring.png` — DMN de scoring con un resultado de ejemplo.
- [ ] `EV-004_dmn-prioridad.png` — DMN de prioridad de alertas con P1/P2/P3.
- [ ] `EV-005_c4-contexto.png` — diagrama C4 de contexto en Lucidchart, Visio o Miro.
- [ ] `EV-005_journey-cliente.png` — journey de cliente persona o empresa.

### Fase 2 — Requerimientos

- [ ] `EV-001_jira-backlog.png` — backlog con 10 épicas y 40 historias.
- [ ] `EV-001_jira-historia-gherkin.png` — una historia con criterios Gherkin completos.
- [ ] `EV-002_confluence-arbol.png` — árbol de páginas del espacio NovaBank.
- [ ] `EV-002_confluence-adr.png` — una página de ADR publicada.
- [ ] `EV-003_ado-jerarquia.png` — jerarquía Epic → Feature → User Story en Azure DevOps.
- [ ] `EV-003_ado-sprint.png` — sprint board con los work items importados.

### Fase 6 — UX y analítica

- [ ] `EV-006_figma-flujo.png` — flujo de prototipo en Balsamiq o Figma.
- [ ] `EV-006_figma-pantalla-transferencia.png` — pantalla de transferencia.
- [ ] `EV-007_powerbi-modelo.png` — modelo de datos en Power BI Desktop.
- [ ] `EV-007_powerbi-dashboard.png` — tablero con cifras conciliadas.
- [ ] `EV-008_tableau-dashboard.png` — tablero en Tableau o Tableau Public.

### Fase 7 — CI y difusión

- [ ] `EV-009_ado-pipeline-verde.png` — run verde del pipeline de Azure DevOps.
- [ ] `EV-009_ado-tests.png` — pestaña Tests con los 204 tests.
- [ ] `EV-010_github-actions-verde.png` — run verde de GitHub Actions.
- [ ] `EV-010_github-artefactos.png` — artefactos `qa-uat-results` y `junit-results`.
- [ ] `EV-011_linkedin-post.png` — post publicado y repositorio en Destacados.

## Enlaces que deben registrarse

| ID | Enlace esperado | Dónde registrarlo |
|---|---|---|
| EV-001 | Proyecto y tablero de Jira | `docs/EVIDENCIAS.md` |
| EV-002 | Espacio e índice de Confluence | `docs/EVIDENCIAS.md` |
| EV-003 | Proyecto y consulta de jerarquía de ADO | `docs/EVIDENCIAS.md` |
| EV-004 | Proyecto/modelo BPMN-DMN | `docs/EVIDENCIAS.md` |
| EV-005 | Diagramas de solo lectura | `docs/EVIDENCIAS.md` |
| EV-006 | Prototipo de solo lectura | `docs/EVIDENCIAS.md` |
| EV-007 | `.pbix` o dashboard publicado | `docs/EVIDENCIAS.md` |
| EV-008 | Dashboard de Tableau Public | `docs/EVIDENCIAS.md` |
| EV-009 | Run del pipeline de ADO | `docs/EVIDENCIAS.md` |
| EV-010 | Run de GitHub Actions | `docs/EVIDENCIAS.md` |
| EV-011 | Post de LinkedIn | `docs/EVIDENCIAS.md` |

## Después de subir una captura

1. Agregar el archivo a esta carpeta.
2. Editar `docs/EVIDENCIAS.md` y completar enlace, captura, fecha y estado.
3. Verificar que no haya datos personales ni credenciales visibles.
4. Actualizar `PLAN.md` si la evidencia cierra una tarea.
