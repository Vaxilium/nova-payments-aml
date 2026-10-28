# Guía de importación a Jira

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub  
**Documento:** GUI-JIRA-001  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Autor:** Franco Tillería Centurión — Business Analyst  
**Artefacto:** `jira_import.csv`

> El agente no opera Jira. Esta guía describe los pasos que debe ejecutar el autor y deja el espacio de evidencia en `docs/EVIDENCIAS.md` (EV-001). No se declara que la importación fue realizada.

---

## 1. Contenido del CSV

`jira_import.csv` contiene **50 filas de datos**:

- 10 épicas (`EP-01` a `EP-10`).
- 40 historias (`US-001` a `US-040`).

Columnas:

| Columna | Uso | Obligatoria |
|---|---|---|
| `External issue ID` | ID estable (`EP-01`, `US-001`) para reimportar o actualizar. | Recomendada |
| `Project Key` | Clave del proyecto; el CSV usa `NOVA`. | Sí |
| `Issue Type` | `Epic` o `Story`. | Sí |
| `Summary` | Título de la épica o historia. | Sí |
| `Description` | Descripción y criterios Gherkin. | Sí |
| `Priority` | `High`, `Medium` o `Low`. | Sí |
| `Labels` | Etiquetas separadas por espacio. | Opcional |
| `Story Points` | Número entero; vacío en épicas. | Para historias |
| `Epic Name` | Nombre de la épica; solo para `Issue Type=Epic`. | Para épicas (company-managed) |
| `Epic Link` | Nombre de la épica; solo para historias. | Para historias (company-managed) |
| `Status` | `To Do`. | Opcional |
| `Sprint` | `Sprint 1`, `Sprint 2` o vacío. | Opcional |
| `Assignee` | Vacío para asignar después. | Opcional |
| `Reporter` | Vacío. | Opcional |

**Codificación:** UTF-8, separador coma, primera fila como encabezado. No se usa BOM.

---

## 2. Preparación del proyecto

1. Crear un proyecto Scrum en Jira Cloud con clave `NOVA` (o cambiar `Project Key` en el CSV).
2. Verificar que existan los tipos de issue `Epic` y `Story`.
3. Verificar que existan los estados `To Do`, `In Progress` y `Done`.
4. Verificar los campos:
   - `Story Points` (numérico).
   - `Epic Name` y `Epic Link` en proyectos **company-managed**.
   - `Parent` en proyectos **team-managed** (en ese caso, mapear `Epic Link` a `Parent`).
   - `Sprint` si se desea asignar sprints en la importación.
5. Crear los sprints `Sprint 1` y `Sprint 2` **antes** de importar si se va a mapear la columna `Sprint`. Si no existen, dejar la columna sin mapear y asignar los sprints manualmente en el backlog.

> En proyectos team-managed, el campo de épica puede llamarse `Parent` y no `Epic Link`. La importación permite mapear la columna del CSV al campo disponible; no es necesario editar el CSV.

---

## 3. Importación paso a paso

1. Ir a **Issues → Import issues from CSV** (o **Settings → System → Import and Export → External System Import → CSV**).
2. Seleccionar `03-requerimientos/jira_import.csv`.
3. Configurar:
   - Delimitador: coma.
   - Codificación: UTF-8.
   - Primera fila: encabezado.
4. En el mapeo de campos, asignar:
   - `External issue ID` → **External issue ID**.
   - `Project Key` → **Project**.
   - `Issue Type` → **Issue Type**.
   - `Summary` → **Summary**.
   - `Description` → **Description**.
   - `Priority` → **Priority**.
   - `Labels` → **Labels**.
   - `Story Points` → **Story Points**.
   - `Epic Name` → **Epic Name** (solo épicas).
   - `Epic Link` → **Epic Link** (historias; o **Parent** en team-managed).
   - `Status` → **Status**.
   - `Sprint` → **Sprint** (si los sprints existen).
5. Validar la vista previa: 50 filas, 10 épicas y 40 historias.
6. Ejecutar la importación y revisar el resumen de errores.
7. Verificar en el backlog:
   - Las 10 épicas existen.
   - Cada historia está vinculada a su épica.
   - Los story points suman 198.
   - Las etiquetas y prioridades se ven correctamente.
8. Crear el tablero y asignar `Sprint 1` (10 historias / 47 SP) y `Sprint 2` (9 historias / 52 SP) si no se hizo en la importación.
9. Capturar el backlog, el tablero y una historia con criterios Gherkin.

---

## 4. Problemas frecuentes

| Problema | Causa probable | Solución |
|---|---|---|
| `Priority` no se importa | El nombre no existe en el proyecto. | Crear `High`, `Medium`, `Low` o mapear a las prioridades existentes. |
| `Epic Link` no se reconoce | Proyecto team-managed. | Mapear la columna a `Parent`. |
| `Sprint` vacío | El sprint no existe o no se mapeó. | Crear los sprints y reimportar, o asignar manualmente. |
| `Story Points` vacío | Campo no configurado o valor no numérico. | Verificar el campo y los valores del CSV. |
| Acentos incorrectos | Codificación distinta de UTF-8. | Importar con UTF-8; no abrir/guardar con ANSI. |
| Duplicados al reimportar | `External issue ID` no mapeado. | Mapear el ID externo para actualizar en lugar de crear. |

---

## 5. Verificación posterior

- [ ] 10 épicas y 40 historias creadas.
- [ ] 40 historias con `Epic Link`/`Parent` correcto.
- [ ] Story points: 198 en total; 47 en Sprint 1 y 52 en Sprint 2.
- [ ] Prioridades y etiquetas visibles.
- [ ] Criterios Gherkin legibles en la descripción.
- [ ] Tablero con columnas `To Do`, `In Progress`, `Done`.
- [ ] Enlace del proyecto y captura registrados en `docs/EVIDENCIAS.md` (EV-001).

---

## 6. Referencias

- `historias-usuario.md` — fuente funcional de las historias.
- `epicas.md` — fuente de las épicas.
- `planificacion-sprints.md` — asignación de sprints.
- `matriz-trazabilidad.csv` — IDs estables para pruebas.
- `docs/EVIDENCIAS.md` — EV-001.

**Fin de la guía.**
