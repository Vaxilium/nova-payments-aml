# 03 — Requerimientos

Propósito: transformar el negocio en un backlog claro, priorizado y trazable, listo para Jira, Azure DevOps y Confluence.

**Estado:** Fase 2 completada en artefactos; evidencias manuales EV-001, EV-002 y EV-003 pendientes de acción del autor.

---

## 1. Contenido

| Archivo / carpeta | Qué contiene |
|---|---|
| `epicas.md` | 10 épicas con objetivo, alcance, KPIs, historias y story points. |
| `historias-usuario.md` | 40 historias «Como… quiero… para…» con Gherkin, MoSCoW, story points y dependencias. |
| `requerimientos-no-funcionales.md` | 16 NFR: disponibilidad 24/7, rendimiento, seguridad, auditoría, idempotencia, conciliación, observabilidad, recuperación, privacidad e interoperabilidad. |
| `planificacion-sprints.md` | Dos sprints con objetivo, historias comprometidas, riesgos y criterios de salida. |
| `definition-of-ready-done.md` | DoR, DoD por tipo de historia, DoD de sprint y de fase. |
| `jira_import.csv` | 10 épicas + 40 historias para importar a Jira. |
| `guia-importacion-jira.md` | Pasos, mapeo de campos y verificación en Jira. |
| `ado_workitems.csv` | 10 épicas + 15 features + 40 historias con IDs lógicos. |
| `ado_import/` | Tres CSV por pasada para Azure DevOps y guía de jerarquía. |
| `guia-importacion-azure-devops.md` | Pasos, mapeo de campos y verificación en Azure DevOps. |
| `confluence/` | Kit de páginas Markdown: inicio, BRD resumido, 6 ADR, glosario, 3 actas y RAID log. |
| `matriz-trazabilidad.csv` | Objetivo → requerimiento → historia → proceso BPMN → caso de prueba reservado. |

---

## 2. Resumen del backlog

| Dimensión | Valor |
|---|---|
| Épicas | 10 |
| Historias | 40 |
| Story points | 198 |
| Must | 26 historias / 135 SP |
| Should | 12 historias / 52 SP |
| Could | 2 historias / 11 SP |
| Sprint 1 | 10 historias / 47 SP |
| Sprint 2 | 9 historias / 52 SP |
| Backlog restante | 21 historias / 99 SP |
| Casos de prueba reservados | `TC-001` a `TC-040` (Fase 7) |

---

## 3. Cómo usar los artefactos

1. **Revisar negocio:** leer `epicas.md`, `confluence/01-brd-resumido.md` y `confluence/03-glosario.md`.
2. **Refinar backlog:** validar `historias-usuario.md` contra `definition-of-ready-done.md`.
3. **Importar a Jira:** seguir `guia-importacion-jira.md` con `jira_import.csv`.
4. **Importar a Azure DevOps:** seguir `guia-importacion-azure-devops.md` con `ado_import/`.
5. **Crear Confluence:** seguir `confluence/README.md` y pegar las páginas.
6. **Verificar trazabilidad:** abrir `matriz-trazabilidad.csv` y comprobar que cada historia tiene objetivo, requerimiento, proceso y `TC-###`.
7. **Registrar evidencia:** completar EV-001, EV-002 y EV-003 en `docs/EVIDENCIAS.md`.

---

## 4. Convenciones

- IDs estables: `EP-###`, `US-###`, `TC-###`.
- Prioridad MoSCoW: `Must`, `Should`, `Could`; `Won't` se documenta en el BRD como exclusión.
- Story points: Fibonacci (1, 2, 3, 5, 8, 13); no son horas.
- Gherkin en español: `Dado`, `Cuando`, `Entonces`, `Y`.
- Fechas `YYYY-MM-DD`.
- Sin datos reales, secretos ni enlaces inventados.

---

## 5. Trazabilidad y pruebas

La matriz `matriz-trazabilidad.csv` vincula:

```text
objetivo de negocio → requerimiento BRD → historia → proceso BPMN → caso de prueba
```

Los casos `TC-001` a `TC-040` están **reservados** y se completarán en la Fase 7 (UAT). No se declaran ejecutados.

---

## 6. Referencias

- `../01-negocio/BRD.md` — requerimientos y objetivos.
- `../01-negocio/kpis.md` — KPIs.
- `../01-negocio/riesgos.md` — riesgos.
- `../02-procesos/mapa-procesos.md` — procesos PR-01 a PR-14.
- `../docs/SUPUESTOS.md` — supuestos y decisiones.
- `../docs/PENDIENTES.md` — pendientes.
- `../docs/EVIDENCIAS.md` — EV-001, EV-002, EV-003.

**Fin del README.**
