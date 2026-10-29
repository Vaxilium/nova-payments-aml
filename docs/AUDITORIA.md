# AUDITORÍA DE VERDAD

**Fecha:** 2026-10-29
**Alcance:** README, `docs/FUENTES.md`, documentos con `SUPUESTO NO VERIFICADO`,
pipelines, artefactos publicados y revisión de seguridad del repositorio.
**Método:** clon limpio en directorio temporal, entorno virtual nuevo,
`pip install -r requirements.txt`, ejecución de seed, `pytest`, UAT, controles SQL
y revisión directa de archivos. No se declara operada ninguna herramienta externa
(Jira, Confluence, Azure DevOps, Figma, Power BI, Tableau, Camunda, etc.).

**Regla aplicada:** una afirmación es **verificada** solo si se reprodujo con un
comando o se contrastó con un archivo del repositorio. Si depende de una
herramienta o de una captura manual, queda como **requiere ejecución manual**. Si
no se pudo reproducir, se marca **no verificada**. Si contradice los hechos, se
marca **falsa** y se corrige.

## 1. Resultado global

| Categoría | Cantidad |
|---|---|
| Afirmaciones auditadas | 34 |
| Verificadas por ejecución o archivo | 28 |
| Parciales (XML verificado, validación en herramienta no reproducida) | 1 |
| Requieren ejecución manual | 4 |
| No verificadas | 1 |
| Falsas | 0 |

No se encontraron claves, tokens, credenciales ni datos de empleadores reales.
Sí se encontraron rutas absolutas de la máquina local en artefactos generados y
en documentación; fueron sanitizadas (ver sección 5).

## 2. Afirmaciones del README

| # | Afirmación | Dónde | Verificación | Resultado |
|---|---|---|---|---|
| 1 | 204 pruebas pytest aprobadas | README, resultados | `python -m pytest -q` en clon limpio → `204 passed` | Verificada |
| 2 | 51/51 casos UAT automatizados aprobados | README, `resultados-uat.json` | `run_uat.py` → `51/51` | Verificada |
| 3 | 23/23 consultas SQL de control OK | README, `sql-controls.json` | `run_uat.py` → `23/23`, `integrity_check=ok`, 0 FK | Verificada |
| 4 | 5 defectos abiertos (1 crítica, 2 altas, 2 medias) | README, `08-qa-uat/defectos.md` | 5 registros `DEF-001`…`DEF-005` | Verificada |
| 5 | 40/40 historias trazadas | README, `matriz-trazabilidad.csv` | 40 filas, 40 `historia_id` únicos | Verificada |
| 6 | 10 épicas y 40 historias | README | `jira_import.csv`: 10 `Epic`, 40 `Story` | Verificada |
| 7 | 198 story points | README, PLAN | Suma de `Story Points` = 198 | Verificada |
| 8 | 6 BPMN y 4 DMN | README | `02-procesos/bpmn` = 6; `02-procesos/dmn` = 4 | Verificada |
| 9 | BPMN/DMN “validado estructuralmente” | README | XML bien formado comprobado; la validación con `bpmn-moddle`/`dmn-moddle` no dejó log reproducible | Parcial: XML verificado, validación semántica no reproducida |
| 10 | Importación en Bizagi/Camunda/Signavio pendiente | README, EVIDENCIAS | EV-004 sin enlace ni captura | Requiere ejecución manual |
| 11 | 23 consultas SQL | README | 23 archivos `.sql` en `05-core-middleware/sql/` | Verificada |
| 12 | 15 triggers de esquema | PLAN | `grep -c "CREATE TRIGGER" schema.sql` = 15 | Verificada |
| 13 | 500 clientes, 800 cuentas, 49.582 movimientos | README | `seed.py` imprime esos valores | Verificada |
| 14 | 104.966 líneas de libro mayor y 52.084 asientos | README | `seed.py` imprime esos valores | Verificada |
| 15 | 341 operaciones sospechosas etiquetadas | README | `seed.py` imprime 341 | Verificada |
| 16 | 0 diferencias de conciliación y 0 desbalance | README | Consultas SQL de control y `sql-controls.json` | Verificada |
| 17 | 4 tipos de mensaje ISO 20022 | README | Catálogo y ejemplos: `pacs.008`, `pacs.002`, `pain.001`, `camt.053` | Verificada |
| 18 | 14 filas de mapeo MT103↔pacs.008 | README | Tabla del documento con 14 filas de datos (+ encabezado y separador) | Verificada |
| 19 | 5 XML + 1 MT103 de ejemplo | README | 5 XML y 1 `.txt` en `06-mensajeria/examples/` | Verificada |
| 20 | 12 reglas AML (R01–R12) | README | 12 archivos en `07-aml-compliance/sql/rules/` | Verificada |
| 21 | 494 transacciones alertadas, 341 TP, 3 FP, 150 sin etiqueta | README | `evaluate_rules.py` en clon limpio reproduce exactamente | Verificada |
| 22 | Recall 100 %, precisión 99,13 %, precisión conservadora 69,03 % | README | Salida de `evaluate_rules.py` | Verificada |
| 23 | 12 CSV analíticos, 10.820 pagos locales, 59 casos, 377 alertas | README | `export_analytics.py` en clon limpio reproduce los conteos | Verificada |
| 24 | 36 medidas DAX | README | `medidas.dax`: 40 encabezados menos 4 columnas calculadas y 1 `VAR` | Verificada |
| 25 | 14 scripts Power Query | README, EVIDENCIAS | 14 archivos `.pq` en `09-analitica/powerquery/` | Verificada |
| 26 | Workbook Excel de 11 hojas | README | `openpyxl` informa 11 hojas | Verificada |
| 27 | 10 wireframes SVG | README | 10 archivos `.svg` | Verificada |
| 28 | 65 casos UAT: 25 positivos, 32 negativos, 8 límite | README | `resultados-uat.csv` | Verificada |
| 29 | 6 manuales pendientes y 8 no implementados | README | `resultados-uat.csv` | Verificada |
| 30 | 775 alertas deduplicadas (snapshot Fase 5) | README, EVIDENCIAS | El corte actual reproducible es 377; el 775 es un snapshot histórico sin comando de reproducción exacto | No verificada (documentada como `DEF-004` / `P-018`) |
| 31 | Pipelines de GitHub Actions y Azure DevOps “listos” | README | YAML parsea correctamente; no hay run ejecutado | Requiere ejecución manual |
| 32 | Jira, Confluence, Azure DevOps, Figma, Power BI, Tableau, Camunda, Bizagi, Signavio, Lucidchart, Visio, Miro | README | Solo hay artefactos de importación; no hay enlaces ni capturas | Requiere ejecución manual |
| 33 | LinkedIn publicado | README, EVIDENCIAS | Solo borradores; sin URL | Requiere ejecución manual |
| 34 | “Ninguna información real de empleadores” | Repositorio | Búsqueda de bancos/empleadores reales y credenciales sin coincidencias | Verificada |

## 3. Afirmaciones que se corrigieron en el README

1. Se separó “verificado por ejecución” de “requiere ejecución manual” en la
   matriz de herramientas.
2. Se reemplazó “validado estructuralmente” por “XML bien formado; validación en
   herramienta pendiente”.
3. Se aclaró que el corte de 775 alertas es histórico y no reproducible hoy, y
   que el corte reproducible actual es 377.
4. Se agregó una sección de comandos probados en un clon limpio, con resultados
   esperados.
5. Se agregó el enlace a `README.en.md`, `docs/case-study.md`,
   `docs/entrevista.md` y `docs/AUDITORIA.md`.

## 4. Fuentes y supuestos no verificados

| ID | Tema | Intento de verificación 2026-10-29 | Estado final |
|---|---|---|---|
| SNV-01 / P-006 | SPI 24/7, PYG, tope ₲10.000.000, acreditación 5 s | `webfetch` a `https://www.bcp.gov.py/sistemas-de-pago-y-tesoreria` devolvió el texto: “Todos los días, las 24 horas (incluso feriados)… hasta ₲10.000.000… 5 segundos” | **Verificado** en la FAQ oficial del BCP. Se cierra P-006 manteniendo la discrepancia con la tabla resumen de F-02 |
| SNV-02 / P-009 | Norma SEPRELAD aplicable a bancos | `webfetch` a la FAQ de SEPRELAD confirmó que los bancos son sujetos obligados (Ley N° 1015/1997 y Ley N° 6960), el concepto de ROS y PEP (Res. N° 50/19). El texto completo de la resolución específica para la SIB sigue sin descargarse | Parcial: obligación general verificada; resolución específica sigue marcada |
| SNV-03 / P-010 | Lista de países de alto riesgo | Es ficticia por diseño | Se mantiene como supuesto interno ficticio; no requiere fuente real |
| SNV-04 / P-011 | Umbrales DMN y SLA | Parámetros de diseño, no normativa | Se mantiene marcado |
| SNV-05 / P-009 | Plazos de ROS | No se verificó un plazo concreto | Se mantiene marcado |
| SNV-06 / P-008 | ISO 20022 obligatorio tras el fin de coexistencia | `webfetch` a SWIFT devolvió HTTP 403 | Se mantiene marcado; no se afirma obligación legal |
| SNV-07 / P-012 | Retención de auditoría 5 años | Sin fuente interna o normativa | Se mantiene marcado |
| SNV-08 / P-011 | SLA de alertas | Parámetros internos | Se mantiene marcado |
| SNV-09 / P-008 | Mapeo MT103↔pacs.008 | Propuesta funcional; sin guía SWIFT completa | Se mantiene marcado |
| SNV-10 / P-009, P-011 | Pesos y umbrales KYC | Diseño del caso | Se mantiene marcado |
| SNV-11 / P-015 | Proxy de dormancia R06 | Limitación de datos | Se mantiene marcado |
| SNV-12 / P-011, P-017 | Umbrales R01–R12 | Calibrados sobre datos sintéticos | Se mantiene marcado |

Fuentes oficiales consultadas en esta auditoría:

- BCP — Sistemas de Pago y Tesorería:
  <https://www.bcp.gov.py/sistemas-de-pago-y-tesoreria> (consulta directa correcta,
  2026-10-29).
- SEPRELAD — Preguntas Frecuentes:
  <https://www.seprelad.gov.py/?page_id=1810> (consulta directa correcta,
  2026-10-29).
- FATF — The FATF Recommendations:
  <https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Fatf-recommendations.html>
  (página oficial accesible; el PDF se descargó como binario y no se parseó,
  2026-10-29).
- SWIFT — ISO 20022 implementation: HTTP 403 (2026-10-29).
- SEPRELAD — Resolución N° 70/2019: respuesta mayor a 5 MB, no parseada
  (2026-10-29).

## 5. Revisión de seguridad

| Hallazgo | Ubicación | Acción |
|---|---|---|
| Ruta absoluta de la máquina local | `AGENTS.md` (sección 1) | Reemplazada por ruta relativa al repositorio |
| Ruta absoluta en supuesto | `docs/SUPUESTOS.md` S-001 | Generalizada a “carpeta local del repositorio” |
| Ruta absoluta en ejemplo de Excel | `09-analitica/docs/excel.md` | Reemplazada por ruta relativa |
| Ruta absoluta en resultados UAT | `08-qa-uat/resultados/resultados-uat.json` | El generador ahora publica rutas relativas al repo |
| Ruta absoluta en salida de pytest | `08-qa-uat/resultados/pytest-output.txt` | El generador sanea rutas absolutas antes de escribir |
| Credenciales, tokens o claves | Repositorio completo | Sin coincidencias |
| Nombres de empleadores reales | Repositorio completo | Sin coincidencias |
| `opencode.json` con permisos amplios | Raíz | Se conserva como configuración local; no contiene secretos |
| `.env.example` | Raíz | Solo placeholders; `.env` está ignorado |

**Nota:** el usuario de Windows (`User`) visible en rutas no es un dato personal
sensible, pero se elimina igualmente para que los artefactos sean portables.

## 6. Prueba desde cero (clon limpio)

Comandos ejecutados en un directorio temporal (`<temp>\nova-clean`) sobre un
`git clone` del repositorio, con entorno virtual nuevo:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m compileall -q 05-core-middleware 06-mensajeria 07-aml-compliance 08-qa-uat 09-analitica
.\.venv\Scripts\python.exe 05-core-middleware\scripts\seed.py --db 05-core-middleware\db\novabank.db
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe 08-qa-uat\scripts\run_uat.py --db 05-core-middleware\db\novabank.db
.\.venv\Scripts\python.exe 07-aml-compliance\scripts\setup_aml.py --db 05-core-middleware\db\novabank.db
.\.venv\Scripts\python.exe 07-aml-compliance\scripts\evaluate_rules.py --db 05-core-middleware\db\novabank.db
.\.venv\Scripts\python.exe 09-analitica\scripts\export_analytics.py
.\.venv\Scripts\python.exe 09-analitica\scripts\build_excel.py
```

Resultados observados:

| Paso | Resultado |
|---|---|
| `compileall` | exit 0 |
| seed | 500 clientes, 800 cuentas, 49.582 movimientos, 341 sospechosas |
| `pytest -q` | `204 passed` en 14,62 s |
| UAT | `51/51` automatizados, 6 manuales, 8 no implementados |
| SQL | `23/23`, `integrity_check=ok`, 0 FK |
| Evaluación AML | 494 alertadas, 341 TP, 3 FP, 150 sin etiqueta |
| Export analítico | 12 CSV, 377 alertas, 59 casos |
| Workbook | 11 hojas |

No se requirieron correcciones de código para que la suite pasara. Las únicas
correcciones fueron de documentación, sanitización de rutas y aclaraciones de
alcance.

## 7. Pendientes que siguen siendo manuales

- EV-001 a EV-011: importar/publicar en Jira, Confluence, Azure DevOps,
  Bizagi/Camunda/Signavio, Lucidchart/Visio/Miro, Balsamiq/Figma, Power BI,
  Tableau, GitHub Actions y LinkedIn.
- Confirmar con Cumplimiento la resolución SEPRELAD aplicable a bancos de la SIB
  (P-009).
- Reproducir o retirar el snapshot histórico de 775 alertas (P-018), o conservarlo
  como referencia fechada.
