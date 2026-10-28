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
| EV-001 | 2 | Jira | CSV de épicas e historias | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-002 | 2 | Confluence | Páginas Markdown | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-003 | 2 | Azure DevOps | CSV de work items | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-004 | 1 | Bizagi / Camunda / Signavio | Archivos `.bpmn` y `.dmn` | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-005 | 1 | Lucidchart / Visio / Miro | Diagramas C4 y journeys | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-006 | 6 | Balsamiq / Figma | Wireframes y prototipo | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-007 | 6 | Power BI | Modelo y dashboard | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-008 | 6 | Tableau | Dashboard | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-009 | 7 | Azure DevOps | Pipeline ejecutado | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-010 | 7 | GitHub Actions | Workflow ejecutado | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |
| EV-011 | 7 | LinkedIn | Post publicado | _pendiente_ | _pendiente_ | _pendiente_ | Pendiente |

## Fase 0 — Preparación

No requiere evidencias externas. Los artefactos son archivos del repositorio y commits en GitHub.

- [x] Repositorio creado y remoto configurado.
- [ ] Primer push verificado en GitHub: `_pendiente_` (se completa al cierre de la sesión).

---

## Plantillas por herramienta

### Jira (Fase 2)

- [ ] Crear proyecto (clave sugerida: `NOVA`).
- [ ] Importar CSV de épicas e historias desde `03-requerimientos/`.
- [ ] Verificar campos, labels y criterios de aceptación.
- [ ] Crear tablero y sprint de ejemplo.
- Enlace del proyecto: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

### Confluence (Fase 2)

- [ ] Crear espacio `NovaBank`.
- [ ] Crear páginas desde los Markdown de `03-requerimientos/confluence/`.
- [ ] Verificar índice, enlaces y jerarquía.
- Enlace del espacio: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

### Azure DevOps (Fases 2 y 7)

- [ ] Crear organización/proyecto (nombre sugerido: `NovaBank-Payments`).
- [ ] Importar CSV de work items.
- [ ] Configurar area paths e iterations.
- [ ] Ejecutar pipeline YAML y conservar el run.
- Enlace del proyecto: _pendiente_
- Enlace del pipeline run: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

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
