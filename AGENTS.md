# AGENTS.md — Guía operativa del repositorio

> Fuente de verdad para agentes de IA y colaboradores. Leer completo antes de actuar.
> Última actualización: 2026-10-27 (Fase 0).

## 1. Contexto del proyecto

- **Repositorio:** `nova-payments-aml` — portafolio público para GitHub y LinkedIn.
- **Autor:** Franco Tillería Centurión — Analista Funcional / Business Analyst con experiencia bancaria (Asunción, Paraguay).
- **Ruta local de trabajo:** `C:\Users\User\Documents\nova-payments-aml` (Windows + PowerShell 5.1). No trabajar en `C:\Users\User` aunque sea el cwd por defecto.
- **Remoto:** `origin` → `https://github.com/Vaxilium/nova-payments-aml.git`, rama `main`.

### Caso de negocio (100 % ficticio)

**NovaBank Instant & Cross-Border Payments + AML Hub.** NovaBank, banco ficticio de Paraguay, lanza:

1. Transferencias instantáneas locales inspiradas en el SPI del BCP.
2. Transferencias internacionales SWIFT / ISO 20022.
3. Monitoreo AML y cumplimiento integrado (KYC, screening, alertas, ROS).

El autor actúa como BA end-to-end: levantamiento, procesos, requerimientos, diseño funcional, mensajería, AML, analítica y UAT.

### Competencias que el portafolio debe demostrar

Jira, Confluence, Azure DevOps, BPMN/DMN (Bizagi/Signavio/Camunda), diagramación (Lucidchart/Visio/Miro), SQL, Excel avanzado, Power BI/Tableau, Balsamiq/Figma, mensajería financiera (SWIFT, ISO 20022, pagos instantáneos), core bancario y middleware, AML/compliance, Python/FastAPI/SQLite/pytest.

## 2. Reglas de autonomía

1. **No hacer preguntas ni pedir confirmación.** Decidir, ejecutar y registrar cada decisión o supuesto en `docs/SUPUESTOS.md`.
2. **Trabajar por fases según `PLAN.md`.** Al terminar cada tarea: marcar `[x]` en `PLAN.md` y hacer commit con mensaje convencional (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`).
3. **Al terminar cada fase:** `git push origin main`.
4. **Fallos:** diagnosticar y corregir. Máximo **3 intentos por problema**; si persiste, registrarlo en `docs/PENDIENTES.md` y continuar con lo siguiente.
5. **No ampliar alcance** fuera de la fase activa salvo que sea necesario para desbloquearla.

## 3. Calidad y honestidad

- **Todo es ficción.** Nombres, cuentas, BIC e IBAN inventados pero con formato válido. Prohibido usar información confidencial o interna de empleadores reales. Entidades reales (BCP, SWIFT, GAFI) solo como referencia pública.
- **Normativa y estándares reales** (SPI del BCP, SEPRELAD, resoluciones del BCP, GAFI, ISO 20022, SWIFT): buscar primero en fuentes oficiales con `webfetch`/búsqueda. Citar nombre y URL en `docs/FUENTES.md`. Lo no verificable se marca **`SUPUESTO NO VERIFICADO`** en el documento donde aparezca y se anota en `docs/PENDIENTES.md`.
- **Nunca inventar** números de resolución, citas textuales, enlaces, capturas, métricas ni resultados de herramientas.
- **Nunca afirmar** que se usó una herramienta que no se operó.

## 4. Herramientas que el agente no puede operar

Jira, Confluence, Azure DevOps, Figma, Balsamiq, Miro, Lucidchart, Visio, Power BI, Tableau, Bizagi/Signavio/Camunda.

Para cada una se generan **artefactos listos para importar o copiar** y se documentan los pasos manuales en `docs/EVIDENCIAS.md` con espacios para capturas y enlaces:

| Herramienta | Artefacto esperado | Formato |
|---|---|---|
| Jira | Épicas, historias, criterios de aceptación | CSV de importación + Markdown |
| Confluence | BRD, decisiones, runbook, índice | Markdown listo para pegar |
| Azure DevOps | Work items, áreas, iteraciones, pipeline | CSV + YAML |
| Bizagi / Camunda / Signavio | Procesos y decisiones | `.bpmn` (BPMN 2.0 XML), `.dmn` |
| Lucidchart / Visio / Miro | Arquitectura, flujos, journeys | Mermaid/PlantUML + guía de recreación |
| Balsamiq / Figma | Wireframes y prototipo | Especificaciones de pantalla + JSON/CSV de componentes |
| Power BI | Modelo, medidas, dashboard | Especificación + medidas DAX + CSV |
| Tableau | Dashboard | Especificación + CSV + pasos |
| Excel | Workbook avanzado | `.xlsx` + descripción de fórmulas y validaciones |

## 5. Seguridad

- Nunca escribir claves, tokens ni credenciales en el repo.
- Usar `.env` (ignorado por git) y `.env.example` con placeholders.
- Nunca `git push --force`.
- No borrar ni modificar nada fuera de esta carpeta.
- Dependencias mínimas y auditadas; preferir librerías estándar cuando sea razonable.

## 6. Idioma y estilo

- Documentación en **español**.
- `README.md` con **resumen ejecutivo en inglés al inicio**.
- Nombres de carpetas en español (prefijo numérico por orden narrativo).
- Código e identificadores en inglés; docstrings en español; evitar comentarios inline innecesarios.
- Tablas y checklists para información estructurada; encabezados con jerarquía clara.
- Fechas en formato `YYYY-MM-DD`.

## 7. Stack y comandos

- **Stack:** Python 3.12 (objetivo), SQLite, FastAPI, pytest, openpyxl.
- **Entorno actual:** Python 3.15 disponible; se usa 3.15 y el código se mantiene compatible con 3.12+. Registrado en `docs/SUPUESTOS.md` (S-003).
- **Entorno virtual:** `.venv` en la raíz (ignorado por git).

```powershell
# Crear y activar entorno
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# Si PowerShell bloquea scripts: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Dependencias
pip install -r requirements.txt

# Calidad y pruebas
pytest -q
python -m compileall .

# API (fases posteriores)
uvicorn app.main:app --reload
```

## 8. Estructura del repositorio

```text
nova-payments-aml/
├─ 01-negocio/           # BRD, stakeholders, riesgos, glosario, KPIs
├─ 02-procesos/          # BPMN, DMN, AS-IS/TO-BE, diagramas
├─ 03-requerimientos/    # épicas, historias, CSV Jira/ADO, Confluence, trazabilidad
├─ 04-diseno-ux/         # wireframes, especificaciones de pantalla, prototipo
├─ 05-core-middleware/   # modelo SQLite, libro mayor, API, datos sintéticos, tests
├─ 06-mensajeria/        # ISO 20022, MT103, validador, simulador instantáneo
├─ 07-aml-compliance/    # KYC, reglas SQL, screening, alertas, ROS, normativa
├─ 08-qa-uat/            # estrategia, casos UAT, pipelines, evidencias
├─ 09-analitica/         # datasets, Excel, Power BI (DAX), Tableau
├─ docs/                 # gobernanza: supuestos, pendientes, fuentes, evidencias
├─ AGENTS.md
├─ PLAN.md
├─ README.md
├─ requirements.txt
└─ .gitignore
```

## 9. Flujo de trabajo por sesión

1. Leer `AGENTS.md`, `PLAN.md`, `docs/SUPUESTOS.md` y `docs/PENDIENTES.md`.
2. Identificar la **fase activa** y la primera tarea sin `[x]`.
3. Antes de escribir contenido normativo, verificar fuentes oficiales y registrarlas en `docs/FUENTES.md`.
4. Implementar la tarea y verificar (tests, `compileall`, validación de artefactos).
5. Marcar `[x]` en `PLAN.md`.
6. Registrar supuestos/decisiones nuevas en `docs/SUPUESTOS.md` y fallos en `docs/PENDIENTES.md`.
7. Commit convencional. Al cerrar la fase: `git push origin main`.
8. Actualizar `docs/EVIDENCIAS.md` con pasos manuales pendientes para el autor.

### Definition of Done (por tarea)

- Artefacto creado en la carpeta correcta.
- Contenido coherente con el caso y trazable cuando aplique.
- Sin secretos ni datos reales.
- Verificado (tests o revisión explícita).
- Registrado en `PLAN.md` y, si corresponde, en `EVIDENCIAS.md`.
- Commit realizado con mensaje convencional.

## 10. Convenciones de commits

```text
feat(scope): nueva funcionalidad o artefacto
fix(scope): corrección
docs(scope): documentación
test(scope): pruebas
chore(scope): mantenimiento, configuración
refactor(scope): reestructuración sin cambio funcional
```

- Un commit por tarea o grupo lógico pequeño.
- Mensajes en español o inglés, descriptivos y en imperativo.
- Prohibido commitear `.venv`, `.env`, `__pycache__`, bases SQLite generadas y credenciales.

## 11. Criterios de calidad técnicos

- Datos sintéticos **reproducibles** con semilla fija; sin PII real.
- SQL **parametrizado**; nunca concatenar entrada de usuario.
- Contabilidad por **partida doble** con invariantes verificadas por tests.
- Mensajería con validación de formato (IBAN, BIC, ISO 4217, ISO 20022) y casos negativos.
- Reglas AML cubiertas por tests con escenarios positivos y negativos.
- Contratos de API versionados (`/v1`) y OpenAPI exportado.
- Trazabilidad requisito → historia → caso de prueba → evidencia.

## 12. Checklist de cierre de sesión

- [ ] `PLAN.md` actualizado.
- [ ] `docs/SUPUESTOS.md` y `docs/PENDIENTES.md` al día.
- [ ] `docs/EVIDENCIAS.md` con pasos manuales nuevos.
- [ ] Tests/verificaciones ejecutados.
- [ ] Commit(s) creados.
- [ ] Push realizado si se cerró una fase.
