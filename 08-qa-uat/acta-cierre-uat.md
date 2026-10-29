# Acta de cierre de UAT — NovaBank

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub (caso ficticio)
**Fecha de ejecución:** 2026-10-29
**Responsable:** Franco Tillería Centurión (BA / QA lead del caso)
**Ambiente:** Windows local, Python 3.15, SQLite, pytest 9.2.0
**Documento relacionado:** `08-qa-uat/plan-uat.md`

## 1. Resumen de la ejecución

| Concepto | Resultado |
|---|---|
| Pruebas pytest ejecutadas | 204 |
| Pruebas pytest aprobadas | 204 |
| Pruebas pytest fallidas | 0 |
| Casos de prueba definidos | 65 |
| Casos automatizados | 51 |
| Casos automatizados aprobados | 51 (100 %) |
| Casos manuales pendientes | 6 |
| Casos no implementados | 8 |
| Consultas SQL de control | 23/23 OK |
| `PRAGMA integrity_check` | `ok` |
| Violaciones de clave foránea | 0 |
| Defectos abiertos | 5 (1 crítica, 2 altas, 2 medias) |

## 2. Evidencia generada

- `08-qa-uat/resultados/junit-uat.xml`: resultados JUnit de pytest.
- `08-qa-uat/resultados/pytest-output.txt`: salida de la ejecución.
- `08-qa-uat/resultados/resultados-uat.json`: consolidado de casos y métricas.
- `08-qa-uat/resultados/resultados-uat.csv`: resultados por caso.
- `08-qa-uat/resultados/sql-controls.json`: resultado de las 23 consultas.
- `08-qa-uat/matriz-ejecucion.xlsx`: workbook con resumen, casos, matriz,
  cobertura, defectos, resultados pytest y controles SQL.

## 3. Casos manuales pendientes

Los siguientes casos requieren una pantalla o herramienta que el agente no
puede operar. No se declaran ejecutados:

| Caso | Motivo |
|---|---|
| TC-022 | Formulario y persistencia de ROS no implementados |
| TC-023 | Flujo de aprobación de ROS no implementado |
| TC-027 | No hay endpoint de consulta de bitácora |
| TC-031 | Canal de autoservicio es un wireframe |
| TC-035 | Flujo de doble aprobación de reglas no implementado |
| TC-036 | Simulador de impacto de reglas no implementado |

## 4. Casos no implementados en el prototipo

| Caso | Funcionalidad ausente |
|---|---|
| TC-002 | Resolución de alias y titular enmascarado |
| TC-004 | Devolución de pago local |
| TC-011 | Alta digital de cliente |
| TC-012 | Verificación documental |
| TC-015 | Revisión periódica y bloqueo |
| TC-032 | Registro de reclamos |
| TC-033 | Notificaciones al cliente |
| TC-037 | Autenticación y autorización por rol |

## 5. Defectos

Se registraron cinco defectos de ejemplo con severidad, pasos, esperado,
obtenido y evidencia. El más relevante es **DEF-003** (API sin autenticación ni
autorización), que impide considerar el prototipo apto para un piloto productivo.

El detalle está en `08-qa-uat/defectos.md` y en la hoja `Defectos` del workbook.

## 6. Decisión de cierre

- **UAT del prototipo (nivel artefacto):** cerrada con resultado satisfactorio.
  Todos los casos automatizables aprobaron y no hay fallos de regresión.
- **Piloto productivo:** no aprobado. Existen brechas críticas y altas
  (autenticación, devoluciones, límite diario) y la conectividad real con
  SPI/SWIFT está fuera de alcance.
- **Evidencia de herramientas externas:** pendiente del autor. Los pasos están
  en `docs/EVIDENCIAS.md` (EV-001 a EV-011).

## 7. Acciones siguientes

1. El autor importa el backlog en Jira y Azure DevOps (EV-001, EV-003).
2. El autor crea el espacio de Confluence y publica el kit (EV-002).
3. El autor importa BPMN/DMN y recrea diagramas (EV-004, EV-005).
4. El autor recrea wireframes y prototipo (EV-006).
5. El autor construye y publica los tableros Power BI/Tableau (EV-007, EV-008).
6. El autor ejecuta los pipelines en Azure DevOps y GitHub Actions (EV-009, EV-010).
7. El autor revisa y publica el post de LinkedIn (EV-011).
8. El equipo ficticio prioriza DEF-003, DEF-002 y DEF-001 antes de un piloto.

## 8. Aprobaciones

| Rol | Nombre | Fecha | Firma |
|---|---|---|---|
| BA / QA lead | Franco Tillería Centurión (caso ficticio) | 2026-10-29 | _pendiente de firma_ |
| Product Owner | _ficticio_ | _pendiente_ | _pendiente_ |
| Cumplimiento | _ficticio_ | _pendiente_ | _pendiente_ |
| Operaciones | _ficticio_ | _pendiente_ | _pendiente_ |

> Este acta documenta una ejecución real de la suite local. No representa una
> aceptación formal de un banco, de un regulador ni de un cliente real.
