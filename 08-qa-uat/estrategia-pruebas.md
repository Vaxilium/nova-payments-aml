# Estrategia de pruebas — NovaBank

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub (caso ficticio)
**Fase:** 7 — QA/UAT y cierre
**Autor del caso:** Franco Tillería Centurión
**Fecha:** 2026-10-29
**Estado:** Estrategia aplicada sobre el prototipo local; no representa un plan de certificación productiva.

## 1. Propósito

Definir cómo se verifica que los artefactos de las fases 3 a 6 cumplen los
requerimientos funcionales y no funcionales del caso, qué se automatiza, qué
requiere ejecución manual y qué queda explícitamente fuera de alcance.

La estrategia prioriza la **evidencia reproducible** sobre la cantidad de
pruebas: cada caso automatizado se ejecuta con `pytest`, cada control SQL se
ejecuta contra la base sintética y cada caso manual queda marcado como pendiente
hasta que el autor aporte la captura correspondiente.

## 2. Objetivos de calidad

| ID | Objetivo | Métrica | Resultado real (2026-10-29) |
|---|---|---|---|
| QO-01 | Verificar los flujos críticos de pagos locales e internacionales | Casos automatizados aprobados | 51/51 (100 %) |
| QO-02 | Verificar la contabilidad por partida doble | Asientos desbalanceados persistidos | 0 |
| QO-03 | Verificar la mensajería ISO 20022/MT103 | Ejemplos y validadores aprobados | 204/204 pruebas pytest |
| QO-04 | Verificar reglas AML y screening | Reglas ejecutadas sin error | 12/12 |
| QO-05 | Verificar la integridad de los datos analíticos | `integrity_check` y claves foráneas | `ok`; 0 violaciones |
| QO-06 | Mantener trazabilidad historia → caso → evidencia | Historias con al menos un caso | 40/40 |
| QO-07 | Ser honestos sobre lo no ejecutado | Casos manuales/no implementados declarados | 6 manuales + 8 no implementados |

## 3. Referencias

- `01-negocio/BRD.md` y `01-negocio/kpis.md`.
- `03-requerimientos/historias-usuario.md` y `matriz-trazabilidad.csv`.
- `03-requerimientos/requerimientos-no-funcionales.md`.
- `05-core-middleware/`, `06-mensajeria/`, `07-aml-compliance/` y `09-analitica/`.
- `08-qa-uat/casos-prueba.csv` y `08-qa-uat/matriz-cobertura.csv`.
- `docs/EVIDENCIAS.md` para la evidencia manual de herramientas externas.

## 4. Enfoque por niveles

| Nivel | Qué verifica | Herramienta | Automatización |
|---|---|---|---|
| Unitario | Cálculos, validadores, scoring, reglas, triggers | pytest | Sí |
| Integración | API `/v1`, libro mayor, simuladores, hook AML | pytest + SQLite | Sí |
| Sistema | Flujos completos de pago local e internacional | pytest + simuladores | Sí, en proceso |
| Regresión | Suite completa de fases 3 a 7 | pytest | Sí |
| Controles SQL | Conciliación, duplicados, estructuración, cobertura AML | SQLite + 23 consultas | Sí |
| UAT funcional | Recorridos de negocio y pantallas | Guion UAT + evidencia manual | Parcial |
| UAT de herramientas | Jira, ADO, Figma, Power BI, Tableau, Camunda | Herramientas externas | No; requiere autor |

La base es la pirámide clásica: muchas pruebas automatizadas de bajo nivel y
pocas pruebas UAT de extremo a extremo, porque el prototipo no tiene front-end
productivo ni conectividad real con SPI/SWIFT.

## 5. Tipos de prueba cubiertos

| Tipo | Cobertura | Ejemplos |
|---|---|---|
| Funcional positivo | Flujos válidos de pago, mensaje, alerta y asiento | TC-001, TC-007, TC-017, TC-024 |
| Funcional negativo | Rechazos, validaciones, conflictos | TC-006, TC-043, TC-052, TC-059 |
| Límites | Topes, precisión, umbrales y bordes | TC-041, TC-042, TC-046, TC-065 |
| Integración | API + core + simulador + contabilidad | TC-001, TC-009, TC-025 |
| Contable | Partida doble, inmutabilidad, sobregiro | TC-024, TC-063, TC-064, TC-065 |
| Mensajería | IBAN, BIC, ISO 4217, pacs.008, pacs.002, MT103 | TC-006 a TC-010, TC-045 a TC-056 |
| AML | KYC, screening, reglas, alertas, casos, hook | TC-013, TC-014, TC-016 a TC-021 |
| Analítica | Integridad del dataset, KPIs y exportación | TC-028, TC-029, TC-030 |
| Regresión | Suite completa en cada cambio | 204 pruebas pytest |
| Seguridad | Fuera de alcance del prototipo; brecha declarada | TC-037 y DEF-003 |
| Performance y carga | Fuera de alcance; solo se observa tiempo de suite | No aplica |
| Accesibilidad | Especificada en Fase 6; no hay front-end que probar | EV-006 |

## 6. Ambientes

| Ambiente | Uso | Estado |
|---|---|---|
| Local Windows + Python 3.15 | Ejecución de la suite y generación de evidencia | Operativo |
| CI Linux + Python 3.12 | Reproducción en Azure Pipelines y GitHub Actions | Configurado; ejecución pendiente del autor |
| Herramientas SaaS | Jira, Confluence, ADO, Figma, Power BI, Tableau | No operadas por el agente |

La diferencia de versión de Python está registrada en `docs/SUPUESTOS.md`
(S-003) y en `docs/PENDIENTES.md` (P-001).

## 7. Datos de prueba

- Dataset sintético reproducible con semilla fija `20261027`.
- 500 clientes, 800 cuentas y 49.582 movimientos en el corte principal.
- 341 operaciones sospechosas etiquetadas para evaluar reglas AML.
- Listas de sanciones/PEP y países de alto riesgo **ficticias**.
- Sin PII real, sin credenciales y sin datos de empleadores.
- Las pruebas de integración usan bases temporales sembradas con semillas
  propias para aislar cada ejecución.

## 8. Automatización

| Componente | Comando | Resultado |
|---|---|---|
| Suite completa | `python -m pytest -q` | 204 aprobadas, 0 fallos |
| UAT consolidada | `python 08-qa-uat/scripts/run_uat.py` | 51/51 casos automatizados aprobados |
| Controles SQL | `python 08-qa-uat/scripts/run_sql_controls.py` | 23/23 consultas OK |
| Semilla | `python 05-core-middleware/scripts/seed.py` | Base reproducible |
| Compilación | `python -m compileall .` | Sin errores de sintaxis |

Los scripts de UAT escriben `08-qa-uat/resultados/resultados-uat.json`,
`resultados-uat.csv`, `sql-controls.json` y `matriz-ejecucion.xlsx`.

## 9. Gestión de defectos

- Severidad: Crítica, Alta, Media, Baja.
- Prioridad: P1 a P3.
- Estados: Abierto, En análisis, Resuelto, Cerrado, Aceptado como limitación.
- Todo defecto debe incluir caso, pasos, esperado, obtenido, evidencia e impacto.
- Los cinco defectos de ejemplo están en `08-qa-uat/defectos.md` y en la hoja
  `Defectos` del workbook.
- No se declara ningún defecto como resuelto sin una corrección verificada.

## 10. Métricas

| Métrica | Fórmula | Resultado |
|---|---|---|
| Cobertura de historias | Historias con al menos un caso / 40 | 40/40 (100 %) |
| Tasa de éxito automatizada | Casos automatizados aprobados / automatizados | 51/51 (100 %) |
| Casos manuales pendientes | Casos marcados Manual | 6 |
| Casos no implementados | Casos marcados No implementado | 8 |
| Pruebas pytest | Aprobadas / total | 204/204 |
| Controles SQL | OK / total | 23/23 |
| Defectos abiertos | Críticos + altos + medios + bajos | 5 (1 crítica, 2 altas, 2 medias) |
| Integridad de datos | `PRAGMA integrity_check` | `ok` |
| Claves foráneas | `PRAGMA foreign_key_check` | 0 violaciones |

## 11. Riesgos de la estrategia

| Riesgo | Impacto | Mitigación |
|---|---|---|
| El prototipo no tiene front-end productivo | UAT visual limitada | Wireframes y especificaciones; evidencia manual EV-006 |
| No hay conectividad SPI/SWIFT real | No se prueba interoperabilidad real | Simuladores deterministas; alcance declarado |
| La suite AML depende de la base local | CI puede fallar si no se siembra | Pipeline siembra antes de pytest |
| Muestra normal AML pequeña | Precisión conservadora subestimada | Registrado en P-017 |
| Dos cortes de alertas (775 vs 377) | Inconsistencia de reporte | Registrado en P-018 y DEF-004 |
| Casos manuales sin ejecutar | Cobertura UAT incompleta | Estado explícito y checklist en EVIDENCIAS |

## 12. Roles

| Rol | Responsabilidad |
|---|---|
| BA / QA lead (autor) | Diseño de casos, criterios, evidencia y cierre |
| Desarrollo | Corrección de defectos y mantenimiento de la suite |
| Cumplimiento | Validación de reglas, SLA y ROS |
| Operaciones | Validación de conciliación y límites |
| Product Owner | Aceptación de alcance y limitaciones |

## 13. Entregables

- `08-qa-uat/plan-uat.md`
- `08-qa-uat/casos-prueba.csv` y `casos-prueba-ado-testplans.csv`
- `08-qa-uat/matriz-cobertura.csv`
- `08-qa-uat/matriz-ejecucion.xlsx`
- `08-qa-uat/defectos.md`
- `08-qa-uat/acta-cierre-uat.md`
- `08-qa-uat/azure-pipelines.yml`
- `.github/workflows/ci.yml`
- `docs/EVIDENCIAS.md` con EV-009, EV-010 y EV-011

## 14. Límites y honestidad

- La suite demuestra comportamiento funcional y contable del prototipo, no
  rendimiento, seguridad, alta disponibilidad ni recuperación ante desastres.
- La validación ISO 20022 es estructural y de negocio, no contra XSD oficiales.
- Los resultados de UAT son locales y reproducibles; no son resultados de
  producción ni de un piloto con clientes reales.
- Las herramientas externas no fueron operadas por el agente. Su evidencia
  depende del autor y está marcada como pendiente en `docs/EVIDENCIAS.md`.
