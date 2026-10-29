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
| EV-006 | 6 | Balsamiq / Figma | Wireframes y prototipo | _pendiente_ | _pendiente_ | _pendiente_ | Artefacto listo; captura pendiente |
| EV-007 | 6 | Power BI | Modelo y dashboard | _pendiente_ | _pendiente_ | _pendiente_ | Artefacto listo; captura pendiente |
| EV-008 | 6 | Tableau | Dashboard | _pendiente_ | _pendiente_ | _pendiente_ | Artefacto listo; captura pendiente |
| EV-009 | 7 | Azure DevOps | Pipeline ejecutado | _pendiente_ | _pendiente_ | _pendiente_ | Artefacto listo; ejecución pendiente |
| EV-010 | 7 | GitHub Actions | Workflow ejecutado | _pendiente_ | _pendiente_ | _pendiente_ | Artefacto listo; ejecución pendiente |
| EV-011 | 7 | LinkedIn | Post publicado | _pendiente_ | _pendiente_ | _pendiente_ | Borrador listo; publicación pendiente |

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
- [x] Matriz de trazabilidad actualizada en Fase 7 con IDs y estados de los 65 casos.
- [ ] EV-001 completada por el autor.
- [ ] EV-002 completada por el autor.
- [ ] EV-003 completada por el autor.

---

## Fase 3 — Core bancario y middleware

**Estado:** Completado con evidencia automática. Esta fase no requiere herramientas externas.

Los artefactos son código y datos reproducibles; la evidencia se obtiene ejecutando los comandos.

### Comandos ejecutados

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe 05-core-middleware\scripts\seed.py --db 05-core-middleware\db\novabank.db
.\.venv\Scripts\python.exe 05-core-middleware\scripts\export_openapi.py
.\.venv\Scripts\python.exe -m pytest -q
```

### Resultados verificados (2026-10-28)

- [x] `pytest -q`: **69 pruebas aprobadas**.
- [x] Seed reproducible con semilla `20261027`: 500 clientes, 800 cuentas y 49.582 movimientos.
- [x] 104.966 líneas de libro mayor y 52.084 asientos.
- [x] 341 movimientos sospechosos etiquetados en `_aml_ground_truth` y 492 normales de muestra.
- [x] Conciliación de saldos contra libro mayor: 0 diferencias; desbalance global PYG/USD: 0.
- [x] 23 consultas SQL ejecutadas sin errores sobre la base completa.
- [x] `openapi.yaml` generado con OpenAPI 3.1.
- [x] `PRAGMA integrity_check`: `ok`; `PRAGMA foreign_key_check`: sin filas.

### Artefactos de evidencia

- Esquema y triggers: `05-core-middleware/db/schema.sql`.
- Dataset reproducible: `05-core-middleware/scripts/seed.py`.
- Consultas: `05-core-middleware/sql/` (índice en `README.md`).
- API y contrato: `05-core-middleware/app/` y `05-core-middleware/openapi.yaml`.
- Pruebas: `05-core-middleware/tests/`.
- Documento conceptual: [`docs/core-y-middleware.md`](core-y-middleware.md).

> La base `novabank.db` y `seed_report.json` son locales y están ignorados por git.
> Cualquier persona puede regenerarlos con el comando de seed.

---

## Fase 4 — Mensajería financiera

**Estado:** Completado con evidencia automática. Esta fase no requiere herramientas externas.

### Comandos ejecutados

```powershell
.\.venv\Scripts\python.exe -m pytest -q
cd 06-mensajeria
..\.venv\Scripts\python.exe -m validator --message examples\iso20022\pacs.008-customer-credit-transfer.xml --international-pacs008
..\.venv\Scripts\python.exe -m validator --message examples\iso20022\pacs.002-payment-status-report-acsc.xml
..\.venv\Scripts\python.exe -m validator --message examples\iso20022\pacs.002-payment-status-report-rjct.xml
..\.venv\Scripts\python.exe -m validator --message examples\iso20022\pain.001-customer-credit-transfer.xml
..\.venv\Scripts\python.exe -m validator --message examples\iso20022\camt.053-bank-to-customer-statement.xml
..\.venv\Scripts\python.exe -m validator --mt103 examples\mt\mt103-international-transfer.txt --map
```

### Resultados verificados (2026-10-28)

- [x] `pytest -q`: **158 pruebas aprobadas** (69 del core + 89 de mensajería), 0 fallos.
- [x] Los 5 ejemplos XML son válidos, incluido el perfil internacional de pacs.008.
- [x] El MT103 de ejemplo es válido y se mapea a pacs.008.
- [x] El CSV de mapeo tiene 14 filas y coincide con `MAPPING_ROWS`.
- [x] El simulador internacional debita importe + comisión y balancea el asiento (`2102` / `1102` / `4102`).
- [x] Los rechazos y timeouts generan `pacs.002` válido con el motivo correspondiente.

### Artefactos de evidencia

- Catálogo: `06-mensajeria/docs/catalogo-iso20022.md`.
- Mapeo: `06-mensajeria/docs/mapeo-mt103-pacs008.md` y `06-mensajeria/mapping/mt103-pacs008.csv`.
- Validador: `06-mensajeria/validator/` y `06-mensajeria/docs/validador.md`.
- Simuladores: `06-mensajeria/simulator/` y `06-mensajeria/docs/simuladores.md`.
- Ejemplos: `06-mensajeria/examples/`.
- Diagramas: `06-mensajeria/diagrams/`.
- Pruebas: `06-mensajeria/tests/`.

> La validación es estructural y de negocio, no contra XSD oficiales (S-056). El bloqueo de ISO 20022/SWIFT se registra en P-008.

---

## Fase 5 — AML y compliance

**Estado:** Completado con evidencia automática. Esta fase no requiere herramientas externas.

### Comandos ejecutados

```powershell
.\.venv\Scripts\python.exe 07-aml-compliance\scripts\setup_aml.py --db 05-core-middleware\db\novabank.db
.\.venv\Scripts\python.exe 07-aml-compliance\scripts\evaluate_rules.py --db 05-core-middleware\db\novabank.db
.\.venv\Scripts\python.exe -m pytest 07-aml-compliance/tests -q
.\.venv\Scripts\python.exe -m pytest -q
```

### Resultados verificados (2026-10-29)

- [x] `pytest -q`: **183 pruebas aprobadas** (69 core + 89 mensajería + 25 AML), 0 fallos.
- [x] `pytest 07-aml-compliance/tests -q`: **25 pruebas aprobadas**.
- [x] Esquema AML aplicado sobre la base del core: KYC, alertas, casos, transiciones, screening y ROS.
- [x] Scoring KYC determinístico para 500 clientes; hay clientes HIGH, MEDIUM y LOW.
- [x] 12 reglas SQL ejecutadas sobre 49.582 transacciones.
- [x] 494 transacciones alertadas: 341 TP, 3 FP etiquetados y 150 sin etiqueta.
- [x] Precisión sobre etiquetadas: 99,13 %; precisión conservadora: 69,03 %; recall: 100 %.
- [x] Cobertura completa de STRUCTURING, HIGH_VELOCITY, PASS_THROUGH, ROUND_MULE y DORMANT_ACTIVATION.
- [x] Alertas deduplicadas: 1.326 coincidencias → 775 alertas (P1 110, P2 665).
- [x] Flujo de alerta y caso probado: asignación, escalamiento, cierre y transición auditada.
- [x] Hook AML probado: pago normal ALLOW, nombre sancionado REJECT, alto valor HOLD y país de riesgo HOLD.
- [x] Dos ROS ficticios documentados; ninguno presentado ante una autoridad.

### Artefactos de evidencia

- Esquema: `07-aml-compliance/aml/schema_aml.sql`.
- KYC: `07-aml-compliance/aml/kyc.py`.
- Screening: `07-aml-compliance/aml/screening.py`.
- Reglas: `07-aml-compliance/sql/rules/` (R01–R12).
- Alertas: `07-aml-compliance/aml/alerts.py`.
- Workflow: `07-aml-compliance/aml/workflow.py`.
- Evaluación: `07-aml-compliance/aml/evaluation.py` y `07-aml-compliance/docs/evaluacion-verdad.md`.
- Hook: `07-aml-compliance/aml/hook.py`.
- ROS: `07-aml-compliance/docs/ros.md`.
- Normativa: `07-aml-compliance/docs/mapeo-normativo.md`.
- Pruebas: `07-aml-compliance/tests/`.

> Las listas de sanciones/PEP y los países de alto riesgo son ficticios. Los SLA y umbrales son parámetros internos (SNV-08, SNV-10 a SNV-12).

---

## Fase 6 — UX y analítica

**Estado:** Artefactos automáticos completos; EV-006, EV-007 y EV-008 requieren captura manual del autor.

**Commits y push:** `a869314`, `fb7e2de`, `32a5597`, `975c393` y `338b94c` publicados en `origin/main` el 2026-10-29.

### Comandos ejecutados

```powershell
.\.venv\Scripts\python.exe 04-diseno-ux\wireframes\generar_wireframes.py
.\.venv\Scripts\python.exe 09-analitica\scripts\export_analytics.py
.\.venv\Scripts\python.exe 09-analitica\scripts\build_excel.py
.\.venv\Scripts\python.exe -m pytest 09-analitica\tests -q
.\.venv\Scripts\python.exe -m pytest -q
```

### Resultados verificados

- [x] 10 wireframes SVG + galería HTML + especificación de pantallas y flujo.
- [x] Dataset de 12 CSV con 49.582 transacciones, 10.820 pagos locales, 377 alertas y 59 casos.
- [x] `export_report.json` con `integrity_check = ok` y 0 violaciones de clave foránea.
- [x] Workbook `NovaBank_analitica.xlsx` con 11 hojas, 14 rangos con nombre, 11 tablas, validaciones, formato condicional y fórmulas `XLOOKUP`, `INDEX/MATCH`, `SUMIFS`, `COUNTIFS` y `PERCENTILE`.
- [x] 36 medidas DAX y columnas calculadas documentadas en `powerbi/medidas.dax`.
- [x] 14 scripts M, tema de Power BI y guía de publicación.
- [x] Campos calculados equivalentes y guía de Tableau Public.
- [x] 16 pruebas del módulo de analítica aprobadas; suite completa al cierre de Fase 6: **199 pruebas aprobadas**, 0 fallos. Tras Fase 7: **204** (5 pruebas de borde UAT).

### Artefactos de evidencia

- UX: `04-diseno-ux/especificacion-pantallas.md`, `flujo-prototipo.md`, `guia-estilo.md`, `accesibilidad.md` y `wireframes/`.
- Datos: `09-analitica/data/` y `09-analitica/data/README.md`.
- Diccionario: `09-analitica/docs/diccionario-datos.md`.
- Excel: `09-analitica/excel/NovaBank_analitica.xlsx` y `09-analitica/docs/excel.md`.
- Power Query: `09-analitica/powerquery/`.
- Power BI: `09-analitica/powerbi/medidas.dax`, `tema-novabank.json`, `README.md` y `09-analitica/docs/tablero.md`.
- Tableau: `09-analitica/tableau/calculos.md`.
- Pruebas: `09-analitica/tests/test_analytics.py`.

### Evidencia manual pendiente

- **EV-006:** recrear wireframes en Balsamiq/Figma y conectar el prototipo; captura y enlace.
- **EV-007:** construir el `.pbix`, validar cifras, publicar o capturar y registrar URL.
- **EV-008:** construir el libro de Tableau, publicar en Tableau Public (opcional) y capturar.

> La latencia de pagos locales y el ciclo de vida de alertas/casos son sintéticos. No se declara haber abierto Power BI, Tableau ni Figma.

---

## Fase 7 — QA/UAT y cierre

**Estado:** Automatización y artefactos completos. EV-009, EV-010 y EV-011
requieren ejecución manual del autor.

**Commits y push:** pendientes al cierre de esta sesión. Los resultados se
generaron localmente antes del commit final.

### Comandos ejecutados

```powershell
.\.venv\Scripts\python.exe 08-qa-uat\scripts\build_cases.py
.\.venv\Scripts\python.exe 08-qa-uat\scripts\run_uat.py
.\.venv\Scripts\python.exe 08-qa-uat\scripts\run_sql_controls.py
.\.venv\Scripts\python.exe 08-qa-uat\scripts\update_traceability.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -c "import yaml; yaml.safe_load(open('08-qa-uat/azure-pipelines.yml', encoding='utf-8')); yaml.safe_load(open('.github/workflows/ci.yml', encoding='utf-8')); print('YAML OK')"
```

### Resultados verificados (2026-10-29)

- [x] 65 casos de prueba definidos: 25 positivos, 32 negativos y 8 de límite.
- [x] 40/40 historias cubiertas por al menos un caso.
- [x] 51/51 casos automatizados aprobados (100 %).
- [x] 6 casos manuales pendientes de ejecución.
- [x] 8 casos no implementados declarados explícitamente.
- [x] `pytest -q`: **204 pruebas aprobadas**, 0 fallos.
- [x] 23/23 consultas SQL de control OK.
- [x] `PRAGMA integrity_check`: `ok`; 0 violaciones de clave foránea.
- [x] 5 defectos documentados: 1 crítica, 2 altas y 2 medias.
- [x] Matriz de trazabilidad actualizada con IDs y estados reales.
- [x] `matriz-ejecucion.xlsx` generado con 7 hojas.
- [x] `azure-pipelines.yml` y `.github/workflows/ci.yml` validados como YAML.
- [ ] Pipelines ejecutados en Azure DevOps y GitHub Actions (EV-009, EV-010).
- [ ] Post de LinkedIn publicado (EV-011).

### Artefactos de evidencia

- Estrategia: `08-qa-uat/estrategia-pruebas.md`.
- Plan UAT: `08-qa-uat/plan-uat.md`.
- Acta de cierre: `08-qa-uat/acta-cierre-uat.md`.
- Catálogo: `08-qa-uat/casos-prueba.csv` y `08-qa-uat/casos-prueba.md`.
- Importación Azure Test Plans: `08-qa-uat/casos-prueba-ado-testplans.csv`.
- Cobertura: `08-qa-uat/matriz-cobertura.csv`.
- Ejecución: `08-qa-uat/matriz-ejecucion.xlsx`.
- Resultados: `08-qa-uat/resultados/`.
- Defectos: `08-qa-uat/defectos.md`.
- Pipeline Azure DevOps: `08-qa-uat/azure-pipelines.yml`.
- Workflow GitHub Actions: `.github/workflows/ci.yml`.
- Textos LinkedIn: `docs/linkedin.md`.

### EV-009 — Ejecutar el pipeline en Azure DevOps

**Estado:** Artefacto listo; ejecución pendiente.

Pasos:

1. Crear la organización/proyecto `NovaBank-Payments` o reutilizar uno existente.
2. Conectar el repositorio `Vaxilium/nova-payments-aml` (GitHub) o subir el
   código a Azure Repos.
3. Ir a **Pipelines → New pipeline → Azure Repos Git / GitHub → Existing YAML**.
4. Seleccionar `08-qa-uat/azure-pipelines.yml`.
5. Ejecutar sobre `main` y aprobar los permisos que solicite.
6. Verificar que el stage `Quality` termina en verde.
7. Revisar la pestaña **Tests** y descargar el artefacto `qa-uat-results`.
8. Capturar el run, la pestaña de tests y el resumen de artefactos.

**Verificación mínima:**
- [ ] El pipeline instala dependencias sin error.
- [ ] `compileall` termina sin error.
- [ ] El seed genera la base sintética.
- [ ] `run_uat.py` termina con 51/51 automatizados aprobados.
- [ ] Los 204 tests aparecen en la pestaña Tests.
- [ ] El artefacto `qa-uat-results` se descarga y contiene `resultados-uat.json`.
- [ ] No hay secretos en el YAML ni en los logs.

- Enlace del run: _pendiente_
- Enlace del proyecto: _pendiente_
- Captura del run verde: _pendiente_
- Captura de la pestaña Tests: _pendiente_
- Fecha: _pendiente_

> El pipeline usa Python 3.12. Si alguna dependencia falla en esa versión, se
> registra el error y se ajusta `requirements.txt`; no se declara verde sin
> evidencia del run.

### EV-010 — Ejecutar el workflow de GitHub Actions

**Estado:** Artefacto listo; ejecución pendiente.

Pasos:

1. Hacer push de `.github/workflows/ci.yml` a `main`.
2. Abrir **Actions → CI** en `https://github.com/Vaxilium/nova-payments-aml`.
3. Esperar el run disparado por el push o usar **Run workflow**.
4. Verificar que el job `pytest, SQL y UAT` termina en verde.
5. Descargar los artefactos `qa-uat-results` y `junit-results`.
6. Capturar el resumen del run y la lista de artefactos.

**Verificación mínima:**
- [ ] El workflow se dispara en `push` o `pull_request` a `main`.
- [ ] Python 3.12 se configura correctamente.
- [ ] El seed y `run_uat.py` terminan sin error.
- [ ] Los artefactos se publican aunque el job falle (`if: always()`).
- [ ] El run queda verde y el enlace es público.
- [ ] No hay secretos ni tokens en el workflow.

- Enlace del run: _pendiente_
- Captura del run verde: _pendiente_
- Captura de artefactos: _pendiente_
- Fecha: _pendiente_

### EV-011 — Publicar el caso en LinkedIn

**Estado:** Borrador listo; publicación pendiente.

Pasos:

1. Revisar `docs/linkedin.md` y elegir uno de los tres borradores.
2. Reemplazar los placeholders de enlaces por URLs reales y verificadas.
3. Confirmar que no se afirma haber operado herramientas sin evidencia.
4. Publicar el post y agregar el repositorio a **Destacados**.
5. Capturar el post publicado y guardar la URL.

**Verificación mínima:**
- [ ] El texto no exagera resultados ni inventa métricas.
- [ ] El enlace al repositorio funciona sin autenticación.
- [ ] El enlace de LinkedIn es público o visible para la red objetivo.
- [ ] Las capturas no exponen datos personales ni credenciales.
- [ ] El post distingue claramente el caso ficticio.

- Enlace del post: _pendiente_
- Enlace del repositorio en Destacados: _pendiente_
- Captura del post: _pendiente_
- Fecha: _pendiente_

### Checklist de cierre de Fase 7

- [x] Estrategia y plan UAT creados.
- [x] 65 casos con cobertura 40/40 historias.
- [x] Ejecución automatizada real y reproducible.
- [x] Controles SQL e integridad verificados.
- [x] Defectos documentados con severidad y evidencia.
- [x] Matriz de trazabilidad actualizada.
- [x] Pipelines de Azure DevOps y GitHub Actions creados y validados como YAML.
- [x] Acta de cierre UAT creada.
- [x] README final y borradores de LinkedIn creados.
- [ ] EV-009 completada por el autor.
- [ ] EV-010 completada por el autor.
- [ ] EV-011 completada por el autor.

> La UAT automatizada está cerrada. La UAT manual y la evidencia de herramientas
> externas no se declaran completadas hasta que el autor las ejecute.

---

## Plantillas por herramienta

### Jira (Fase 2)

Ver **EV-001** en la sección Fase 2. Artefacto: `03-requerimientos/jira_import.csv`.

### Confluence (Fase 2)

Ver **EV-002** en la sección Fase 2. Artefacto: `03-requerimientos/confluence/`.

### Azure DevOps (Fases 2 y 7)

- **EV-003:** importar los work items de `03-requerimientos/ado_import/`.
- **EV-009:** crear el pipeline desde `08-qa-uat/azure-pipelines.yml`, ejecutarlo
  en `main` y capturar el run verde, la pestaña Tests y el artefacto
  `qa-uat-results`.
- Enlace del proyecto: _pendiente_
- Enlace del run: _pendiente_
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

- [ ] Recrear los wireframes de `04-diseno-ux/especificacion-pantallas.md` usando `04-diseno-ux/wireframes/index.html` como referencia.
- [ ] Conectar el flujo de `04-diseno-ux/flujo-prototipo.md`.
- [ ] Compartir enlace de solo lectura.
- Enlace: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

### Power BI (Fase 6)

- [ ] Importar los CSV de `09-analitica/data/` con `09-analitica/powerquery/`.
- [ ] Crear el modelo y las medidas de `09-analitica/powerbi/medidas.dax`.
- [ ] Construir las páginas de `09-analitica/docs/tablero.md`, validar cifras y publicar captura.
- Enlace: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

### Tableau (Fase 6)

- [ ] Conectar los CSV y crear las relaciones de `09-analitica/tableau/calculos.md`.
- [ ] Crear las hojas y dashboards especificados.
- [ ] Publicar en Tableau Public (opcional) y capturar.
- Enlace: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

### GitHub Actions (Fase 7)

Ver **EV-010** en la sección Fase 7. Workflow: `.github/workflows/ci.yml`.

- [ ] Verificar que el workflow corre en `main` con Python 3.12.
- [ ] Descargar `qa-uat-results` y `junit-results`.
- [ ] Conservar enlace al run verde.
- Enlace del run: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_

### LinkedIn (Fase 7)

Ver **EV-011** en la sección Fase 7. Borradores: `docs/linkedin.md`.

- [ ] Revisar el borrador del post y elegir uno de los tres.
- [ ] Reemplazar placeholders por enlaces reales y verificados.
- [ ] Publicar solo si el repositorio y las métricas son verificables.
- Enlace del post: _pendiente_
- Captura: _pendiente_
- Fecha: _pendiente_
