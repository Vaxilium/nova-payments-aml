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
