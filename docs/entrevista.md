# Guion de entrevista — NovaBank Payments + AML

**Uso:** preparación para entrevistas de Business Analyst / Analista Funcional.
**Formato:** por fase, una explicación de 2 minutos, decisiones clave, 5 preguntas
probables con respuesta y límites honestos.
**Regla:** nunca afirmar que se operó una herramienta que solo se documentó como
artefacto. El estado real está en `docs/AUDITORIA.md`.

---

## Fase 0 — Preparación del repositorio

### Explicación de 2 minutos

Antes de escribir requerimientos, armé la gobernanza del proyecto: reglas de
trabajo, hoja de ruta por fases, convenciones de commit y un registro de
supuestos, pendientes y fuentes. La idea era que cualquier persona —o cualquier
agente de IA— pudiera retomar el trabajo sin adivinar el contexto. También definí
que todo dato sería ficticio y que ninguna herramienta externa se declararía
operada sin evidencia. Eso me obligó a separar desde el día uno lo que es un
artefacto listo para importar de lo que es una herramienta realmente usada.

### Decisiones clave

- Gobernanza antes de artefactos: `AGENTS.md`, `PLAN.md`, `SUPUESTOS.md`,
  `PENDIENTES.md`, `FUENTES.md`, `EVIDENCIAS.md`.
- Repositorio público con datos 100 % sintéticos.
- Commits convencionales y push al cierre de cada fase.
- Regla de honestidad: nada de enlaces, capturas o métricas inventadas.

### 5 preguntas probables

1. **¿Por qué tanto trabajo de gobernanza antes de los entregables?**
   Porque el proyecto simula un trabajo real de varios meses. Sin reglas de
   alcance, supuestos y evidencia, es fácil inflar resultados o perder
   trazabilidad. La gobernanza es barata al inicio y cara de reconstruir después.

2. **¿Cómo evitó inventar información?**
   Separé tres estados: verificado por ejecución, entregado como artefacto y
   pendiente de acción manual. Todo lo no verificable se marca como supuesto y se
   registra en `PENDIENTES.md`.

3. **¿Qué haría distinto en un proyecto real?**
   Sumaría desde el inicio al oficial de cumplimiento y a legal, porque varias
   decisiones normativas —resolución aplicable, retención, plazos de ROS— no se
   pueden cerrar solo con documentación pública.

4. **¿Cómo manejó el cambio de alcance?**
   Con el registro de supuestos y el plan por fases. Cada cambio se documenta con
   impacto y se refleja en `PLAN.md`; no se amplía alcance sin justificación.

5. **¿Qué demuestra esta fase?**
   Criterio de gobierno: saber que un portafolio creíble empieza por definir qué
   se va a probar y qué no se va a afirmar.

### Límites honestos

- La gobernanza es del caso ficticio, no de una organización real.
- El repositorio no tiene licencia corporativa ni revisión legal.

---

## Fase 1 — Negocio y procesos

### Explicación de 2 minutos

Traduje el problema del banco a un BRD con objetivos, alcance, KPIs, restricciones
y riesgos. Después modelé el negocio: mapa de stakeholders y RACI, glosario
bilingüe, procesos AS-IS y TO-BE, seis diagramas BPMN y cuatro tablas DMN. El
foco fue cubrir el ciclo completo: onboarding/KYC, pago local tipo SPI, pago
internacional, gestión de alertas e investigación/ROS. También documenté el
contexto regulatorio con fuentes oficiales y separé lo verificado de lo que
requiere validación con cumplimiento.

### Decisiones clave

- Un solo pool `NovaBank` con lanes por rol para facilitar la lectura e importación.
- DMN con `hitPolicy=FIRST` para que el orden de reglas sea determinista.
- Umbrales y SLA como parámetros de diseño, no como límites regulatorios.
- Procesos modelados como no ejecutables: son diseño funcional, no un motor.
- Fuentes oficiales citadas y supuestos no verificados marcados explícitamente.

### 5 preguntas probables

1. **¿Por qué BPMN y DMN en lugar de solo un flowchart?**
   Porque BPMN permite separar roles, eventos y gateways con una notación
   estándar, y DMN hace explícita la lógica de decisión. Un flowchart no alcanza
   para auditar reglas ni para importar en un motor.

2. **¿Cómo definió los umbrales de riesgo?**
   Como parámetros de diseño calibrados sobre el caso, no como normativa. Están
   marcados como supuestos y deberían validarse con Riesgos y Cumplimiento.

3. **¿Qué proceso fue el más difícil?**
   El de alertas e investigación/ROS, porque cruza negocio, cumplimiento,
   tecnología y plazos. Ahí se ve si el modelo resiste un caso real.

4. **¿Cómo validó los BPMN/DMN?**
   Verifiqué que el XML esté bien formado y que la estructura sea coherente. La
   importación y ejecución en Camunda, Bizagi o Signavio quedó como evidencia
   manual pendiente; no afirmo haberla hecho.

5. **¿Qué pasa con la discrepancia del horario del SPI?**
   La FAQ del BCP dice 24/7 y la tabla resumen del SIPAP dice días hábiles. El
   2026-10-29 reverifiqué la FAQ y confirmé 24/7, ₲10.000.000 y 5 segundos.
   Adopté F-01 y dejé la discrepancia documentada.

### Límites honestos

- Los BPMN/DMN no se ejecutaron en un motor real.
- Los umbrales, SLA y listas de riesgo son ficticios.
- La resolución SEPRELAD específica para bancos de la SIB no se verificó en texto
  completo.

---

## Fase 2 — Requerimientos

### Explicación de 2 minutos

Convertí el negocio en un backlog trazable: 10 épicas, 40 historias con criterios
de aceptación en Gherkin, priorización MoSCoW, estimación relativa y 198 story
points. Agregué 16 requerimientos no funcionales, Definition of Ready/Done, dos
sprints y dos artefactos de importación: CSV para Jira y CSV para Azure DevOps.
También armé un kit de Confluence con índice, BRD resumido, seis ADR, actas y RAID
log. La matriz de trazabilidad conecta objetivo, requerimiento, épica, historia,
proceso y caso de prueba.

### Decisiones clave

- Historias con Gherkin, no solo descripciones narrativas.
- IDs de casos `TC-001` a `TC-040` reservados desde el inicio para evitar inventar
  ejecuciones posteriores.
- Tres pasadas para Azure DevOps por la jerarquía Epic → Feature → Story.
- Confluence en Markdown listo para pegar, sin macros ni enlaces inventados.

### 5 preguntas probables

1. **¿Cómo priorizó 40 historias?**
   Con MoSCoW y valor de negocio/riesgo. Los dos primeros sprints comprometen 19
   historias y 99 SP; el resto queda priorizado, no ejecutado.

2. **¿Qué hace que una historia esté “lista”?**
   Que tenga valor, criterios de aceptación verificables, dependencias claras,
   estimación y un caso de prueba asociado. Eso está en el DoR.

3. **¿Cómo aseguró la trazabilidad?**
   Con una matriz que conecta objetivo → requerimiento → historia → proceso →
   caso. Al llenarla aparecieron ocho funcionalidades especificadas pero no
   implementadas; eso es información útil, no un fracaso.

4. **¿Por qué no importó realmente a Jira?**
   Porque el agente no opera Jira. El CSV y la guía están listos, pero la
   importación, captura y enlace son evidencia manual del autor.

5. **¿Qué métrica de backlog usaría?**
   Cobertura trazable (40/40), porcentaje de historias con criterios completos y
   distribución de SP por épica. No usaría “velocidad” como si fuera un dato real,
   porque el equipo es ficticio.

### Límites honestos

- La capacidad del equipo y la velocidad son supuestos de planificación.
- No hay un Jira/Confluence/ADO real con enlaces públicos.
- Las 40 historias no están todas implementadas: 8 funcionalidades quedaron fuera
  del prototipo.

---

## Fase 3 — Core bancario y middleware

### Explicación de 2 minutos

Construí un core simulado en SQLite con clientes, cuentas, movimientos, libro
mayor y asientos. La regla central es partida doble: cada asiento debe balancear y
los triggers impiden modificar o borrar movimientos contables. Generé un dataset
sintético reproducible con semilla fija —500 clientes, 800 cuentas y 49.582
movimientos— y una API FastAPI `/v1` con idempotencia, estados y auditoría.
También escribí 23 consultas SQL de control y una suite de pruebas que verifica
invariantes contables, no solo respuestas de API.

### Decisiones clave

- Importes como enteros en la unidad menor para evitar errores de redondeo.
- Libro mayor como fuente de verdad contable; el saldo operativo se concilia.
- Idempotency-key obligatoria y respuestas persistidas.
- SQLite en modo WAL para el prototipo, con límites documentados.
- 15 triggers para inmutabilidad y control de partida doble.

### 5 preguntas probables

1. **¿Por qué SQLite y no PostgreSQL?**
   Porque el objetivo es reproducibilidad y cero infraestructura. SQLite permite
   que cualquier persona clone y ejecute todo. El límite es un solo escritor y
   falta de réplicas; está documentado.

2. **¿Cómo garantiza que la contabilidad esté balanceada?**
   Con triggers y pruebas que suman débitos y créditos por asiento y por moneda.
   El resultado medido es 0 descuadres y 0 diferencias de conciliación.

3. **¿Qué pasa si se reintenta una transferencia?**
   La API exige idempotency-key y devuelve la misma respuesta sin duplicar el
   asiento. Hay pruebas de idempotencia y de concurrencia básica.

4. **¿Cómo manejó errores y estados?**
   Con estados explícitos y códigos de error consistentes. La transferencia no se
   considera exitosa hasta que el asiento y el estado están persistidos.

5. **¿Qué no demuestra este core?**
   No demuestra alta concurrencia, réplicas, recuperación ante desastres,
   seguridad de producción ni rendimiento. Es un prototipo funcional.

### Límites honestos

- Un solo escritor y prueba de concurrencia básica con dos hilos.
- Sin autenticación ni autorización (DEF-003, crítico).
- Sin conexión a un core bancario real.

---

## Fase 4 — Mensajería financiera

### Explicación de 2 minutos

Modelé la mensajería local e internacional. Armé un catálogo de cuatro mensajes
ISO 20022 —`pacs.008`, `pacs.002`, `pain.001` y `camt.053`—, un mapeo campo a
campo entre MT103 y `pacs.008`, y un validador de IBAN, BIC, ISO 4217, importes y
campos obligatorios. Después construí dos simuladores: uno instantáneo tipo SPI
con tope en guaraníes y máquina de estados, y uno internacional en USD con
comisión e idempotencia. Los ejemplos y las pruebas cubren aceptación, rechazo,
timeout y reintento.

### Decisiones clave

- Validación estructural y de negocio, sin declarar conformidad con XSD oficiales.
- El tramo local usa cuenta/alias; el internacional usa IBAN/BIC.
- El simulador internacional liquida en USD; EUR se valida pero no se contabiliza.
- Rechazos con códigos estándar cuando están identificados y `TIMEOUT` como motivo
  propietario del simulador.
- Mapeo MT103↔pacs.008 como propuesta funcional, no como traducción certificada.

### 5 preguntas probables

1. **¿Validó los mensajes contra los XSD oficiales?**
   No. Los portales de ISO 20022 y SWIFT bloquearon la descarga automatizada. La
   validación es estructural y de negocio; no afirmo certificación.

2. **¿Cómo evita duplicar un pago internacional al reintentar?**
   Con idempotencia y una máquina de estados. El reintento no genera un segundo
   `pacs.008` ni un segundo asiento.

3. **¿Qué diferencia hay entre `pacs.008` y `pacs.002`?**
   `pacs.008` es la transferencia de crédito; `pacs.002` es el reporte de estado
   de ese pago, con aceptación o rechazo y motivo.

4. **¿Por qué no usa IBAN para el pago local?**
   Porque el registro IBAN consultado no incluye a Paraguay. El caso usa alias o
   cuenta local y reserva IBAN/BIC para el tramo internacional.

5. **¿Qué pasa si el mensaje es válido pero AML lo retiene?**
   El hook AML devuelve `ALLOW`, `HOLD` o `REJECT`. Es una interfaz simulada; las
   reglas reales se implementan en la fase AML.

### Límites honestos

- Sin conectividad real con SPI, SWIFT ni corresponsales.
- Sin certificación ISO 20022.
- El mapeo MT103↔pacs.008 no se contrastó con la guía SWIFT completa.

---

## Fase 5 — AML y compliance

### Explicación de 2 minutos

Implementé el ciclo AML: scoring KYC de 0 a 100, perfiles determinísticos sin PII,
screening difuso con listas ficticias, doce reglas SQL de monitoreo, generación y
deduplicación de alertas, priorización P1/P2/P3, casos con SLA, workflow auditado
y dos ROS ficticios. Para evaluar las reglas usé las 341 operaciones sospechosas
etiquetadas del dataset: las 12 reglas detectaron las 341 (recall 100 %) y
generaron 494 transacciones alertadas, con 3 falsos positivos etiquetados y 150
sin etiqueta. La precisión sobre etiquetadas es 99,13 %; la conservadora, 69,03 %.

### Decisiones clave

- Reglas en SQL parametrizado, no en código opaco.
- Deduplicación por regla + cliente + cuenta + día.
- Screening con Jaro-Winkler y umbrales explícitos.
- Distinguir precisión sobre etiquetadas de precisión conservadora.
- Listas y umbrales ficticios, marcados como supuestos.

### 5 preguntas probables

1. **¿Por qué el recall es 100 % y la precisión no?**
   Porque el dataset tiene etiquetadas las 341 operaciones sospechosas y las
   reglas se calibraron para cubrirlas. La precisión baja cuando se cuentan las
   150 alertas sin etiqueta como falsos positivos.

2. **¿Qué es la precisión conservadora?**
   Es la métrica que trata toda alerta sin etiqueta como falso positivo. Es más
   dura y más honesta cuando la muestra normal es solo ~1 % del dataset.

3. **¿Cómo evita falsos positivos por nombres?**
   Con screening difuso, umbrales de similitud y revisión humana. No uso listas
   reales; las listas son ficticias para no afectar personas reales.

4. **¿R06 mide dormancia real?**
   No. El core no tiene un campo de dormancia; uso un proxy y lo documento como
   limitación (P-015).

5. **¿Los ROS se presentaron ante SEPRELAD?**
   No. Son borradores ficticios. No se presentó nada ante ninguna autoridad y no
   se afirma cumplimiento legal.

### Límites honestos

- Umbrales calibrados sobre datos sintéticos, no de producción.
- La resolución SEPRELAD específica para bancos de la SIB no está verificada en
  texto completo.
- Dos ROS ficticios, sin presentación real.
- El proxy de dormancia no mide dormancia real.

---

## Fase 6 — UX y analítica

### Explicación de 2 minutos

Diseñé diez wireframes para los flujos clave —transferencia, bandeja de alertas,
detalle de caso— con especificaciones de pantalla, estados, mensajes de error y
criterios de accesibilidad. En analítica exporté doce CSV, construí un workbook
Excel de once hojas con tablas, validaciones, Power Query y fórmulas, documenté
36 medidas DAX para Power BI y una guía de campos calculados para Tableau. El
objetivo era mostrar que el BA puede pasar del requerimiento al tablero sin
inventar datos.

### Decisiones clave

- Wireframes como SVG + especificación, no solo imágenes.
- Dataset analítico derivado del core, con diccionario de datos.
- Latencia de pagos y ciclo de vida de casos marcados como sintéticos.
- Modelo estrella con `fact_cases` independiente para evitar rutas ambiguas.
- XLOOKUP con alternativa INDEX/MATCH para compatibilidad.

### 5 preguntas probables

1. **¿Los dashboards existen en Power BI/Tableau?**
   No publicados. Existen el modelo, las medidas DAX y la especificación. La
   construcción y captura requieren ejecución manual del autor.

2. **¿Cómo asegura que las cifras del tablero coincidan con el core?**
   El export analítico parte de la misma base y los totales se contrastan contra
   las consultas SQL de control y los tests de analítica.

3. **¿Qué muestra el tablero de SLA si la latencia es sintética?**
   Muestra el diseño del indicador y el flujo de datos. La latencia no es una
   medición operativa real; está declarada como sintética.

4. **¿Por qué 36 medidas DAX y no más?**
   Porque cubren las preguntas de negocio del caso: volumen, SLA, alertas, casos,
   conciliación y clientes de riesgo. Más medidas sin preguntas sería ruido.

5. **¿Cómo Priorizó los wireframes?**
   Por los flujos de mayor riesgo y valor: pago local, alertas y caso. No hice un
   front-end productivo.

### Límites honestos

- No se operó Figma, Balsamiq, Power BI ni Tableau.
- El workbook Excel se generó y se validó por código; la revisión visual manual
  sigue pendiente.
- Sin pruebas con usuarios reales ni accesibilidad certificada.

---

## Fase 7 — QA/UAT y cierre

### Explicación de 2 minutos

Cerré el ciclo con una estrategia de pruebas, un plan UAT, 65 casos y una matriz
de cobertura. 51 casos son automatizables y se ejecutaron con resultado 51/51; 6
quedaron manuales y 8 corresponden a funcionalidades no implementadas. Documenté
cinco defectos, incluido uno crítico: la API no tiene autenticación ni
autorización. También dejé pipelines de GitHub Actions y Azure DevOps, el README
final y borradores de LinkedIn. La regla fue no declarar verde ningún pipeline ni
herramienta que no se hubiera ejecutado.

### Decisiones clave

- Separar “automatizado aprobado”, “manual pendiente” y “no implementado”.
- Registrar defectos reales, no solo resultados positivos.
- Pipelines como artefactos; ejecución marcada como pendiente.
- Acta de cierre que no aprueba un piloto productivo por DEF-003.

### 5 preguntas probables

1. **¿Por qué solo 51 de 65 casos están aprobados?**
   Porque 6 dependen de pantallas o aprobaciones manuales y 8 son funcionalidades
   que el prototipo no implementa. Declarar 65/65 sería falso.

2. **¿Cuál es el defecto más grave?**
   DEF-003: la API no tiene autenticación ni autorización por rol. Es crítico y
   bloquea cualquier piloto fuera de un entorno controlado.

3. **¿Los pipelines corren en GitHub/Azure?**
   Los YAML están creados y validados sintácticamente, pero no se ejecutaron en
   las plataformas. La ejecución y captura son evidencia manual pendiente.

4. **¿Cómo se que la UAT es reproducible?**
   Porque `run_uat.py` corre pytest, controles SQL y los casos automatizados sobre
   la base regenerada con semilla fija. El resultado se guarda en JSON, CSV y
   JUnit.

5. **¿Qué faltaría para un piloto?**
   Autenticación/autorización, devoluciones, resolución de alias, validación de
   límite diario, UAT manual y evidencia de herramientas. No alcanza con que los
   tests pasen.

### Límites honestos

- UAT manual no ejecutada.
- Pipelines no ejecutados en las plataformas.
- Sin post de LinkedIn publicado ni enlace de Jira/Confluence/ADO.
- El prototipo no es apto para producción.

---

## Fase 8 — Auditoría y refuerzo

### Explicación de 2 minutos

Hice una auditoría de verdad: recorrí cada afirmación del README y la clasifiqué
como verificada, no verificada o falsa. Ejecuté todo desde un clon limpio con un
entorno virtual nuevo, documenté los comandos exactos de Windows PowerShell y
corregí lo que no era reproducible. También revisé seguridad —claves, tokens,
rutas personales, nombres de empleadores— y reforcé el portafolio con README en
inglés, case study, guion de entrevista, licencia MIT, changelog y lista de
capturas pendientes. El resultado es un repositorio que dice exactamente lo que
puede probar.

### Decisiones clave

- Un solo valor reproducible para alertas: 377; el 775 queda como snapshot
  histórico fechado.
- “XML bien formado” en lugar de “validado en Camunda” cuando no hubo ejecución.
- Sanitizar rutas absolutas en artefactos generados.
- Cerrar P-006 al verificar el SPI en la FAQ oficial del BCP.
- No declarar falsa ninguna afirmación: las que no se pudieron reproducir se
  marcan como no verificadas o manuales.

### 5 preguntas probables

1. **¿Encontró afirmaciones falsas?**
   Ninguna falsa. Una no reproducible (el snapshot de 775 alertas) y cuatro filas
   que requieren ejecución manual y agrupan Jira, Confluence, ADO, Bizagi/Camunda,
   BI y LinkedIn.

2. **¿Cómo probó desde cero?**
   Con `git clone` a un directorio temporal, `.venv` nuevo, `pip install -r
   requirements.txt`, seed, pytest, UAT, controles SQL, evaluación AML y export
   analítico. Todo pasó sin cambios de código.

3. **¿Qué hizo con las rutas personales?**
   Las eliminé de AGENTS, SUPUESTOS, documentación de Excel y artefactos de
   resultados. El generador de UAT ahora publica rutas relativas y sanea la salida
   de pytest.

4. **¿Qué supuesto pudo verificar?**
   SNV-01: el SPI opera 24/7, en guaraníes, hasta ₲10.000.000 y con acreditación
   máxima de 5 segundos. La FAQ oficial del BCP lo dice textualmente.

5. **¿Qué queda para el autor?**
   Subir capturas y enlaces de las once evidencias manuales, validar la resolución
   SEPRELAD aplicable y decidir si corrige los defectos DEF-001 a DEF-005.

### Límites honestos

- La auditoría verifica lo que el repositorio puede probar; no certifica calidad
  profesional ni cumplimiento normativo.
- Las herramientas externas siguen sin evidencia operada.
- El caso es ficticio y no representa a ninguna entidad real.

---

## Límites transversales del proyecto

| Qué es real | Qué es simulado | Qué no existe |
|---|---|---|
| Código, SQL, tests, seed, export y métricas reproducibles | Banco, clientes, cuentas, BIC, IBAN, listas, umbrales, SLA y ROS | Conexión SPI/SWIFT, certificación ISO 20022, autenticación, alta disponibilidad, piloto productivo |
| Fuentes oficiales citadas (BCP, SEPRELAD, FATF, ISO) | Procesos, actas, comité, equipo y velocidad | Uso operado de Jira, Confluence, ADO, Figma, Power BI, Tableau, Camunda, Bizagi, Signavio, Lucidchart, Visio o Miro |
| Ejecución local verificada en clon limpio | Latencia de pagos y ciclo de vida de casos | Presentación real de un ROS ante una autoridad |

**Frase de cierre para entrevista:** “Puedo mostrar cada número ejecutándolo, y
puedo decir con la misma claridad qué no hice.”
