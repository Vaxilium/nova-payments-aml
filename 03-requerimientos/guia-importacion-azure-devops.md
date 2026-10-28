# Guía de importación a Azure DevOps

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub  
**Documento:** GUI-ADO-001  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Autor:** Franco Tillería Centurión — Business Analyst  
**Artefactos:** `ado_workitems.csv` (maestro) y `ado_import/01_epics.csv`, `02_features.csv`, `03_stories.csv` (por pasada)

> El agente no opera Azure DevOps. Esta guía describe los pasos que debe ejecutar el autor y deja el espacio de evidencia en `docs/EVIDENCIAS.md` (EV-003). No se declara que la importación fue realizada.

---

## 1. Contenido de los artefactos

| Archivo | Contenido | Uso |
|---|---|---|
| `ado_workitems.csv` | 10 épicas, 15 features y 40 historias con IDs lógicos y `Parent Logical ID`. | Vista maestra y auditoría del backlog. |
| `ado_import/01_epics.csv` | 10 épicas. | Primera pasada de importación. |
| `ado_import/02_features.csv` | 15 features con `Parent Logical ID` de la épica. | Segunda pasada; completar `Parent` con el ID numérico de la épica. |
| `ado_import/03_stories.csv` | 40 historias con `Parent Logical ID` de la feature. | Tercera pasada; completar `Parent` con el ID numérico de la feature. |

**Total:** 10 épicas + 15 features + 40 historias = **65 work items**.

> Azure DevOps exige que `Parent` contenga el **ID numérico** de un work item ya existente. Por eso la importación se hace en tres pasadas. El CSV maestro conserva los IDs lógicos (`EP-01`, `FE-01-01`, `US-001`) para trazabilidad.

---

## 2. Preparación del proyecto

1. Crear un proyecto en Azure DevOps Services con proceso **Agile** (nombre sugerido: `NovaBank-Payments`).
2. Verificar que existan los work item types `Epic`, `Feature` y `User Story`.
3. Crear los **Area Paths**:
   - `NovaBank-Payments\Pagos`
   - `NovaBank-Payments\AML`
   - `NovaBank-Payments\Contabilidad`
   - `NovaBank-Payments\Analitica`
   - `NovaBank-Payments\Plataforma`
4. Crear las **Iterations**:
   - `NovaBank-Payments\Sprint 1`
   - `NovaBank-Payments\Sprint 2`
   - `NovaBank-Payments\Backlog`
5. Verificar los campos `Priority` (1–4), `Story Points` (numérico), `Tags` y `Acceptance Criteria`.
6. Si el proyecto tiene otro nombre, reemplazar `NovaBank-Payments` en los CSV antes de importar.

**Codificación:** UTF-8, separador coma, primera fila como encabezado.

---

## 3. Importación en tres pasadas

### Pasada 1 — Épicas

1. Ir a **Boards → Work items → Import work items**.
2. Subir `ado_import/01_epics.csv`.
3. Verificar el mapeo:
   - `Work Item Type` → **Work Item Type**
   - `Title` → **Title**
   - `Description` → **Description**
   - `Priority` → **Priority**
   - `Tags` → **Tags**
   - `Area Path` → **Area Path**
   - `Iteration Path` → **Iteration Path**
   - `State` → **State**
4. Importar y verificar que se crearon 10 épicas.
5. Anotar el **ID numérico** de cada épica y su `Logical ID` (`EP-01` a `EP-10`). Se puede exportar la consulta a CSV para obtener la relación.

### Pasada 2 — Features

1. Abrir `ado_import/02_features.csv` en Excel o en un editor CSV.
2. En la columna `Parent`, escribir el ID numérico de la épica correspondiente a `Parent Logical ID`.
   - Ejemplo: si `EP-01` quedó con ID `101`, todas las features con `Parent Logical ID=EP-01` llevan `Parent=101`.
3. Importar el archivo con **Import work items**.
4. Verificar 15 features y su vínculo con la épica.
5. Anotar el ID numérico de cada feature (`FE-01-01` a `FE-10-01`).

### Pasada 3 — Historias

1. Abrir `ado_import/03_stories.csv`.
2. En la columna `Parent`, escribir el ID numérico de la feature correspondiente a `Parent Logical ID`.
3. Importar el archivo.
4. Verificar 40 historias con su feature padre.
5. Revisar que los story points sumen 198 y que las iteraciones estén correctas:
   - Sprint 1: 10 historias / 47 SP.
   - Sprint 2: 9 historias / 52 SP.
   - Backlog: 21 historias / 99 SP.

> Si el proyecto usa otro proceso (Scrum o CMMI), los nombres de work item types pueden cambiar. En ese caso, mapear `User Story` al tipo equivalente (`Product Backlog Item` en Scrum) y ajustar la jerarquía.

---

## 4. Mapeo de campos

| Columna CSV | Campo Azure DevOps | Nota |
|---|---|---|
| `Work Item Type` | Work Item Type | `Epic`, `Feature`, `User Story`. |
| `Title` | Title | Obligatorio. |
| `Description` | Description | Texto o HTML. |
| `Acceptance Criteria` | Acceptance Criteria | HTML con escenarios Gherkin. |
| `Priority` | Priority | 1 = más alta; `Must=1`, `Should=2`, `Could=3`. |
| `Story Points` | Story Points | Entero; vacío en épicas y features. |
| `Tags` | Tags | Separados por `;`. |
| `Area Path` | Area Path | Ajustar al nombre real del proyecto. |
| `Iteration Path` | Iteration Path | Sprint 1, Sprint 2 o Backlog. |
| `State` | State | `New`. |
| `Parent` | Parent | ID numérico del work item padre. |
| `Parent Logical ID` | No importar | Referencia para armar la jerarquía. |
| `Logical ID` | No importar | Referencia para trazabilidad. |

---

## 5. Problemas frecuentes

| Problema | Causa probable | Solución |
|---|---|---|
| `Parent` no se reconoce | Se usó un ID lógico (`EP-01`) en lugar del numérico. | Reemplazar por el ID numérico asignado por Azure DevOps. |
| `Area Path` inválido | El área no existe o el proyecto tiene otro nombre. | Crear el área y ajustar el prefijo del proyecto. |
| `Iteration Path` inválido | La iteración no existe. | Crear `Sprint 1`, `Sprint 2` y `Backlog`. |
| `User Story` no existe | El proyecto usa proceso Scrum/CMMI. | Mapear a `Product Backlog Item` o al tipo equivalente. |
| Story Points vacío | Campo no configurado. | Verificar el campo en el proceso del proyecto. |
| Acentos incorrectos | Codificación distinta de UTF-8. | Importar con UTF-8. |

---

## 6. Verificación posterior

- [ ] 10 épicas, 15 features y 40 historias creadas.
- [ ] Jerarquía Epic → Feature → User Story correcta.
- [ ] Story points: 198 en total; 47 en Sprint 1 y 52 en Sprint 2.
- [ ] Area Paths e Iterations correctos.
- [ ] Acceptance Criteria visibles en las historias.
- [ ] Consulta de backlog y tablero de sprint funcionando.
- [ ] Enlace del proyecto y captura registrados en `docs/EVIDENCIAS.md` (EV-003).

---

## 7. Referencias

- `historias-usuario.md` — fuente funcional.
- `epicas.md` — fuente de épicas.
- `planificacion-sprints.md` — sprints y capacidad.
- `matriz-trazabilidad.csv` — IDs y casos reservados.
- `docs/EVIDENCIAS.md` — EV-003.

**Fin de la guía.**
