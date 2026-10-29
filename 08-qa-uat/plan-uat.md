# Plan UAT — NovaBank

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub (caso ficticio)
**Versión del plan:** 1.0
**Fecha:** 2026-10-29
**Responsable:** Franco Tillería Centurión (BA / QA lead del caso)
**Estado:** Ejecución automatizada completada; UAT manual de herramientas pendiente del autor.

## 1. Objetivo

Validar que el prototipo de NovaBank cumple los criterios de aceptación de las
40 historias de usuario y los controles técnicos de las fases 3 a 6, y dejar
preparada la evidencia que el autor debe completar en Jira, Azure DevOps,
Confluence, Figma/Balsamiq, Power BI, Tableau, Camunda y LinkedIn.

## 2. Alcance

### Dentro del alcance

- Transferencias locales PYG y su posteo contable.
- Transferencias internacionales USD con mensajería ISO 20022/MT103 simulada.
- Validación de identificadores, importes, monedas y mensajes.
- KYC, screening, reglas AML, alertas, casos, SLA y hook de pago.
- Conciliación, partida doble e inmutabilidad contable.
- Integridad del dataset analítico y KPIs.
- API `/v1`, idempotencia, correlación y salud.
- Casos de borde y negativos de los flujos anteriores.

### Fuera del alcance

- Conectividad real con SPI del BCP, SWIFT, corresponsales o cámaras.
- Certificación ISO 20022 contra XSD oficiales.
- Autenticación, autorización, cifrado, WAF y pruebas de penetración.
- Rendimiento, carga, alta disponibilidad, RTO/RPO y recuperación ante desastres.
- Front-end productivo, accesibilidad real y pruebas con usuarios reales.
- Presentación efectiva de un ROS ante una autoridad.
- Operación en producción o con datos reales.

## 3. Criterios de entrada

| ID | Criterio | Verificación | Estado |
|---|---|---|---|
| EN-01 | Código de fases 3 a 6 disponible | Carpetas `05` a `09` presentes | Cumplido |
| EN-02 | Suite de pruebas ejecutable | `pytest` colecta y ejecuta | Cumplido (204 pruebas) |
| EN-03 | Dataset sintético reproducible | Seed con semilla fija | Cumplido |
| EN-04 | Base con esquema AML inicializado | `setup_aml.py` y tests AML | Cumplido |
| EN-05 | Casos de prueba con trazabilidad | 40/40 historias con caso | Cumplido |
| EN-06 | Criterios de aceptación definidos | Gherkin en historias | Cumplido |
| EN-07 | Ambiente local operativo | Windows + Python 3.15 + `.venv` | Cumplido |
| EN-08 | Pipeline CI definido | Azure YAML + GitHub Actions | Cumplido a nivel artefacto; run pendiente (EV-009/EV-010) |
| EN-09 | Herramientas externas disponibles | Jira, ADO, Figma, Power BI, Tableau | Pendiente del autor |
| EN-10 | Datos sin PII real | Revisión de dataset y listas ficticias | Cumplido |

## 4. Criterios de salida

### 4.1 Salida de UAT del prototipo (nivel artefacto)

| ID | Criterio | Resultado real | Estado |
|---|---|---|---|
| EX-01 | 100 % de casos automatizables aprobados | 51/51 (100 %) | Cumplido |
| EX-02 | 0 fallos en la suite de regresión | 204/204 pytest | Cumplido |
| EX-03 | 100 % de consultas SQL de control ejecutadas | 23/23 | Cumplido |
| EX-04 | Integridad de base de datos | `integrity_check=ok`; 0 FK | Cumplido |
| EX-05 | 40/40 historias con al menos un caso | 65 casos para 40 historias | Cumplido |
| EX-06 | Defectos críticos del prototipo documentados | DEF-003 documentado | Cumplido |
| EX-07 | Casos manuales declarados como pendientes | 6 casos | Cumplido |
| EX-08 | Casos no implementados declarados | 8 casos | Cumplido |
| EX-09 | Workbook de ejecución generado | `matriz-ejecucion.xlsx` | Cumplido |
| EX-10 | Evidencia manual de herramientas externas | EV-001 a EV-011 | **Pendiente del autor** |

### 4.2 Salida para piloto productivo

| ID | Criterio | Resultado | Estado |
|---|---|---|---|
| PR-01 | Autenticación y autorización por rol | No implementado (DEF-003) | **No cumplido** |
| PR-02 | Devoluciones y reclamos operativos | No implementado (DEF-002) | **No cumplido** |
| PR-03 | Límite diario agregado | No implementado (DEF-005) | **No cumplido** |
| PR-04 | Conectividad real SPI/SWIFT | Fuera de alcance | **No aplica** |
| PR-05 | Pruebas de seguridad y carga | Fuera de alcance | **No aplica** |
| PR-06 | Aprobación de Cumplimiento y Riesgos | No realizada | **Pendiente** |

**Conclusión:** el prototipo cumple los criterios de salida de UAT a nivel
artefacto, pero **no está listo para un piloto productivo**. Las brechas están
documentadas como defectos y no se ocultan en el informe.

## 5. Ambiente y datos

| Elemento | Valor |
|---|---|
| Sistema operativo de ejecución | Windows 10/11 local |
| Python | 3.15 local; 3.12 en CI |
| Base de datos | SQLite `05-core-middleware/db/novabank.db` (ignorada por git) |
| Semilla | `20261027` |
| Dataset principal | 500 clientes, 800 cuentas, 49.582 movimientos |
| Operaciones sospechosas etiquetadas | 341 |
| Corte analítico | 49.582 transacciones, 10.820 pagos locales, 377 alertas, 59 casos |
| Listas AML | Ficticias, de uso interno del caso |
| Credenciales | No se usan credenciales reales ni secretos |

## 6. Calendario de referencia (ficticio)

| Actividad | Fecha planificada | Estado |
|---|---|---|
| Preparación de ambiente y datos | 2026-10-27 | Completado |
| Revisión de criterios de entrada | 2026-10-28 | Completado |
| Ejecución automatizada | 2026-10-29 | Completado |
| Registro de defectos | 2026-10-29 | Completado |
| UAT manual de herramientas | A definir por el autor | Pendiente |
| Aceptación y cierre formal | A definir por el autor | Pendiente |

Las fechas son parte del caso ficticio y no representan un proyecto real.

## 7. Casos y cobertura

| Concepto | Cantidad | Artefacto |
|---|---|---|
| Casos totales | 65 | `casos-prueba.csv` |
| Positivos | 25 | `casos-prueba.md` |
| Negativos | 32 | `casos-prueba.md` |
| Límites | 8 | `casos-prueba.md` |
| Automatizados | 51 | `resultados/resultados-uat.json` |
| Manuales pendientes | 6 | `casos-prueba.csv` |
| No implementados | 8 | `casos-prueba.csv` |
| Historias cubiertas | 40/40 | `matriz-cobertura.csv` |
| Defectos de ejemplo | 5 | `defectos.md` |

Casos manuales pendientes: TC-022, TC-023, TC-027, TC-031, TC-035 y TC-036.
Casos no implementados: TC-002, TC-004, TC-011, TC-012, TC-015, TC-032, TC-033 y TC-037.

## 8. Ejecución

### 8.1 Comandos

```powershell
# 1. Activar entorno
.\.venv\Scripts\Activate.ps1

# 2. Generar la base sintética (si no existe)
python 05-core-middleware\scripts\seed.py --db 05-core-middleware\db\novabank.db

# 3. Ejecutar la UAT consolidada (pytest + SQL + Excel)
python 08-qa-uat\scripts\run_uat.py

# 4. Alternativa: solo pytest
python -m pytest -q
```

### 8.2 Resultado de la ejecución del 2026-10-29

- `pytest -q`: **204 pruebas aprobadas**, 0 fallos.
- UAT: **51/51 casos automatizados aprobados**.
- SQL: **23/23 consultas OK**; `integrity_check=ok`; 0 violaciones de clave foránea.
- Casos manuales: **6 pendientes de ejecución manual**.
- Casos no implementados: **8 declarados**.
- Defectos: **5 abiertos** (1 crítica, 2 altas, 2 medias).

La evidencia está en `08-qa-uat/resultados/` y en `08-qa-uat/matriz-ejecucion.xlsx`.

### 8.3 UAT manual de herramientas

| Actividad | Evidencia | Estado |
|---|---|---|
| Importar backlog en Jira | EV-001 | Pendiente del autor |
| Crear espacio en Confluence | EV-002 | Pendiente del autor |
| Importar work items en Azure DevOps | EV-003 | Pendiente del autor |
| Importar BPMN/DMN en Camunda/Bizagi | EV-004 | Pendiente del autor |
| Recrear diagramas en Lucidchart/Visio/Miro | EV-005 | Pendiente del autor |
| Recrear wireframes en Figma/Balsamiq | EV-006 | Pendiente del autor |
| Construir y publicar dashboard Power BI | EV-007 | Pendiente del autor |
| Construir y publicar dashboard Tableau | EV-008 | Pendiente del autor |
| Ejecutar pipeline Azure DevOps | EV-009 | Pendiente del autor |
| Ejecutar workflow GitHub Actions | EV-010 | Pendiente del autor |
| Publicar post de LinkedIn | EV-011 | Pendiente del autor |

## 9. Defectos

| ID | Título | Severidad | Estado |
|---|---|---|---|
| DEF-001 | Alias de beneficiario no resuelto | Alta | Abierto |
| DEF-002 | Sin flujo de devolución local/internacional | Alta | Abierto |
| DEF-003 | Sin autenticación ni autorización por rol | Crítica | Abierto |
| DEF-004 | Discrepancia de cortes de alertas 775 vs 377 | Media | Abierto |
| DEF-005 | Límite diario agregado no validado | Media | Abierto |

El detalle con pasos, esperado, obtenido y evidencia está en `defectos.md`.

## 10. Roles y responsabilidades

| Rol | Responsabilidad en UAT |
|---|---|
| BA / QA lead | Diseñar casos, ejecutar automatización, consolidar resultados |
| Product Owner | Aceptar alcance y limitaciones |
| Desarrollo | Corregir defectos y mantener la suite |
| Cumplimiento | Validar reglas AML, SLA y ROS |
| Operaciones | Validar conciliación y límites |
| Autor del portafolio | Ejecutar UAT de herramientas y capturar evidencia |

## 11. Gestión de bloqueos

- Un caso que no puede ejecutarse se marca como **manual pendiente** o **no
  implementado**; no se cuenta como aprobado.
- Un defecto se registra con evidencia y no se cierra sin corrección verificada.
- Si una herramienta externa no está disponible, se mantiene el placeholder en
  `docs/EVIDENCIAS.md` y se anota el motivo.
- Los pendientes de alcance se registran en `docs/PENDIENTES.md`.

## 12. Aprobación

| Rol | Nombre | Fecha | Firma |
|---|---|---|---|
| BA / QA lead | Franco Tillería Centurión (caso ficticio) | 2026-10-29 | _pendiente de firma_ |
| Product Owner | _ficticio_ | _pendiente_ | _pendiente_ |
| Cumplimiento | _ficticio_ | _pendiente_ | _pendiente_ |

La aprobación formal del autor y de las áreas ficticias no se declara ejecutada.
