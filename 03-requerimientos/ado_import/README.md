# Importación a Azure DevOps — archivos por pasada

Este directorio contiene los CSV separados para importar en Azure DevOps sin perder la jerarquía Epic → Feature → User Story.

| Archivo | Pasada | Contenido | Acción antes de importar |
|---|---|---|---|
| `01_epics.csv` | 1 | 10 épicas | Importar tal cual. |
| `02_features.csv` | 2 | 15 features | Completar `Parent` con el ID numérico de la épica; `Parent Logical ID` conserva el ID lógico para auditoría. |
| `03_stories.csv` | 3 | 40 historias | Completar `Parent` con el ID numérico de la feature; `Parent Logical ID` conserva el ID lógico para auditoría. |

**Por qué tres pasadas:** Azure DevOps exige que el campo `Parent` contenga el ID numérico de un work item existente. No se puede crear un hijo y su padre en la misma importación.

**Columnas de referencia:** `Logical ID` y `Parent Logical ID` no se importan; sirven para identificar cada work item y reconstruir la jerarquía con los IDs numéricos que asigna Azure DevOps.

**Guía completa:** `../guia-importacion-azure-devops.md`.

**Maestro:** `../ado_workitems.csv` contiene los 65 work items con IDs lógicos para auditoría y trazabilidad. No se importa directamente porque `Parent Logical ID` no es un campo de Azure DevOps.

**Verificación:** 10 épicas + 15 features + 40 historias = 65 work items; 198 story points.
