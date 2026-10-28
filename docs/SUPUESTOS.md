# SUPUESTOS Y DECISIONES

Registro de toda decisión o supuesto tomado sin consulta al autor, según las reglas de autonomía de `AGENTS.md`.

**Convenciones**
- **Decisión:** elección operativa tomada por el agente.
- **Supuesto:** condición asumida como verdadera a falta de información.
- **`SUPUESTO NO VERIFICADO`:** afirmación que depende de normativa o estándar real y aún no fue contrastada con fuente oficial. Debe aparecer marcada también en el documento donde se use.
- Fechas en formato `YYYY-MM-DD`. Estado: `activo`, `reemplazado`, `cerrado`.

| ID | Fecha | Tipo | Decisión / supuesto | Motivo | Impacto | Estado |
|---|---|---|---|---|---|---|
| S-001 | 2026-10-27 | Decisión | El repositorio de trabajo es `C:\Users\User\Documents\nova-payments-aml`, no el cwd por defecto `C:\Users\User`. | Es el clon con el remoto `origin` correcto. | Bajo | Activo |
| S-002 | 2026-10-27 | Supuesto | Todo nombre, cuenta, BIC, IBAN, cliente y transacción es ficticio, aunque con formato válido. | Regla de honestidad y privacidad del portafolio. | Alto | Activo |
| S-003 | 2026-10-27 | Decisión | El stack objetivo es Python 3.12, pero el equipo solo tiene Python 3.15. Se crea `.venv` con 3.15 y el código se mantiene compatible con 3.12+. | Único intérprete disponible. | Medio | Activo |
| S-004 | 2026-10-27 | Decisión | Se ignoran `*.db`, `*.sqlite` y `*.sqlite3`; la base se regenera con el script de seed (semilla fija). | Evitar binarios y datos volátiles en git; garantizar reproducibilidad. | Bajo | Activo |
| S-005 | 2026-10-27 | Decisión | Carpetas en español con prefijo numérico; código e identificadores en inglés. | Orden narrativo del portafolio y convención de código. | Bajo | Activo |
| S-006 | 2026-10-27 | Decisión | Documentación en español; `README.md` con resumen ejecutivo en inglés al inicio. | Requisito del autor y alcance internacional del portafolio. | Bajo | Activo |
| S-007 | 2026-10-27 | Decisión | En Fase 0 no se escribe contenido normativo; las fuentes oficiales se verificarán al inicio de las fases 1, 4 y 5. | Evitar citas inventadas. | Medio | Activo |
| S-008 | 2026-10-27 | Decisión | No se publican enlaces a Jira, Confluence, Azure DevOps, Figma, Power BI ni similares hasta que existan y el autor los cree. `EVIDENCIAS.md` solo contiene placeholders. | No inventar enlaces ni afirmar uso de herramientas. | Alto | Activo |
| S-009 | 2026-10-27 | Decisión | Una sola rama `main`; commits convencionales; push al cierre de cada fase; prohibido `--force`. | Simplicidad y trazabilidad del portafolio. | Bajo | Activo |
| S-010 | 2026-10-27 | Decisión | Los datos sintéticos se generan con semilla fija (`NOVABANK_SEED=20261027`) y se documentan en el diccionario de datos. | Reproducibilidad y pruebas deterministas. | Medio | Activo |
| S-011 | 2026-10-27 | Decisión | Lo no verificable se marca `SUPUESTO NO VERIFICADO` inline y se lista en `PENDIENTES.md`. | Transparencia. | Alto | Activo |
| S-012 | 2026-10-27 | Decisión | Se incluye `opencode.json` en el repositorio como configuración de la sesión de trabajo. | Facilitar futuras sesiones del agente. | Bajo | Activo |
| S-013 | 2026-10-27 | Decisión | No se crea `LICENSE` en Fase 0; la licencia se decide antes de difundir el repositorio (Fase 7). | Evitar otorgar licencia sin decisión explícita del autor. | Medio | Activo |
| S-014 | 2026-10-27 | Decisión | El remoto `Vaxilium/nova-payments-aml` no existía; se creó como repositorio público con `gh repo create` y se hizo el push inicial. | El push falló con "Repository not found" y la cuenta `Vaxilium` ya estaba autenticada. El proyecto es un portafolio público. | Bajo | Activo |
| S-015 | 2026-10-27 | Supuesto | El canal local opera 24/7, en guaraníes, con tope de ₲10.000.000 por operación y acreditación objetivo ≤ 5 segundos. | F-01 del BCP describe esas condiciones; F-02 tiene una contradicción de horario registrada en P-006. | Alto | Activo |
| S-016 | 2026-10-27 | Decisión | El alcance internacional de Fase 1 es solo saliente (outbound), en USD y EUR, con corresponsalía simulada. | Acota el caso y permite modelar el flujo completo sin depender de conectividad SWIFT real. | Medio | Activo |
| S-017 | 2026-10-27 | Supuesto | NovaBank ya cuenta con core bancario, libro mayor y canal digital; el proyecto integra, no reemplaza, esos sistemas. | El caso se centra en pagos y AML, no en la construcción de un core completo. | Alto | Activo |
| S-018 | 2026-10-27 | Supuesto | Las listas de sanciones, PEP y países de alto riesgo son ficticias y de uso interno del caso. | Evita usar datos reales y permite demostrar screening sin riesgo de falsos positivos sobre personas reales. | Alto | Activo |
| S-019 | 2026-10-27 | Supuesto | El onboarding AS-IS es presencial y por banca en línea; el TO-BE incorpora alta digital con KYC remoto y validación documental. | Coherente con la trasformación del caso y con el alcance de Fase 1. | Medio | Activo |
| S-020 | 2026-10-27 | Supuesto | Los umbrales de los DMN (montos, plazos, SLA y prioridades) son parámetros de diseño, no límites regulatorios. | No se encontró una tabla oficial de umbrales aplicable al caso; se marcan como configurables. | Alto | Activo |
| S-021 | 2026-10-27 | Decisión | Los procesos BPMN se modelan con `isExecutable="false"` y se validan estructuralmente con `bpmn-moddle`; no se despliegan en un motor. | Fase 1 es diseño funcional; la ejecución corresponde a fases posteriores. | Medio | Activo |
| S-022 | 2026-10-27 | Decisión | Los DMN usan `hitPolicy="FIRST"` para que el orden de las reglas exprese prioridad y sea determinista. | Evita ambigüedad cuando varias reglas podrían aplicar. | Bajo | Activo |
| S-023 | 2026-10-27 | Decisión | Se usa el namespace Camunda (`http://camunda.org/schema/1.0/bpmn`) solo como metadatos de modelo; no se usan extensiones propietarias. | Mantener portabilidad entre Camunda, Bizagi y Signavio. | Bajo | Activo |
| S-024 | 2026-10-27 | Supuesto | Las fechas, metas y líneas base de los KPIs son objetivos de planificación del caso ficticio; no son resultados medidos. | Honestidad: no se inventan métricas históricas. | Alto | Activo |
| S-025 | 2026-10-27 | Decisión | El modelo entidad-relación de Fase 1 es preliminar y conceptual; el DDL definitivo se construye en Fase 3. | Evitar sobre-especificar antes de los requerimientos. | Medio | Activo |
| S-026 | 2026-10-27 | Supuesto | La validación de IBAN/BIC se hará con formato y checksum; la pertenencia a un país o entidad real no se valida en Fase 1. | El caso es ficticio y no consulta directorios reales. | Medio | Activo |
| S-027 | 2026-10-27 | Decisión | No se afirma que los archivos `.bpmn`/`.dmn` hayan sido abiertos en Camunda Modeler; la evidencia manual queda en EV-004. | No declarar uso de herramientas no operadas. | Alto | Activo |
| S-028 | 2026-10-27 | Supuesto | El banco opera con un oficial de cumplimiento y un equipo de analistas AML; los roles y SLA son ficticios. | Permite modelar el flujo de alertas y escalamiento. | Medio | Activo |
| S-029 | 2026-10-27 | Decisión | Los BPMN usan un solo pool `NovaBank` con lanes por rol/sistema; los sistemas externos se representan como carriles o tareas, no como pools separados con message flows. | Simplifica la importación y la lectura; el foco es la orquestación interna. | Bajo | Activo |
| S-030 | 2026-10-27 | Decisión | El scoring de cliente usa una tabla DMN `SUM` para puntos y una segunda tabla `FIRST` para clasificar. | Permite sumar factores sin perder una salida legible. | Bajo | Activo |
| S-031 | 2026-10-27 | Decisión | Mermaid, C4 y los journeys son vistas de comunicación; la fuente de verdad de procesos y decisiones son los BPMN/DMN. | Evita divergencia entre artefactos. | Medio | Activo |
| S-032 | 2026-10-27 | Decisión | Los mensajes BPMN de confirmación se modelan con `messageEventDefinition` y `messageRef`; no implican integración real. | Documenta la semántica sin afirmar conectividad. | Bajo | Activo |

## Supuestos no verificados vigentes

Los siguientes supuestos se marcan `SUPUESTO NO VERIFICADO` en los documentos donde se usan y quedan asociados a `PENDIENTES.md`:

| ID | Supuesto | Documento donde se usa | Pendiente |
|---|---|---|---|
| SNV-01 | El Reglamento General del SIPAP vigente mantiene el tope de ₲10.000.000, la operación 24/7 y el plazo de acreditación de 5 segundos. | BRD, contexto regulatorio, procesos | P-006 |
| SNV-02 | La Resolución SEPRELAD aplicable a bancos supervisados por la SIB es consistente con el enfoque de ROS, PEP y debida diligencia descrito en F-03. | Contexto regulatorio, procesos AML | P-009 |
| SNV-03 | La lista ficticia de países de alto riesgo se inspira en categorías públicas del GAFI, sin reproducir una lista oficial. | DMN de ruteo, reglas AML | P-010 |
| SNV-04 | Los umbrales de revisión manual y aprobación son adecuados para el apetito de riesgo del banco. | DMN de límites y aprobaciones | P-011 |
| SNV-05 | La obligación de reportar ROS se activa con independencia del monto y dentro de plazos que el caso fija como parámetro interno. | Proceso de alertas, ROS | P-009 |
| SNV-06 | El uso de ISO 20022 para pagos transfronterizos es obligatorio desde el fin de la coexistencia (22-11-2025). | BRD, proceso internacional | P-008 |

## Historial de cambios

| Fecha | Cambio |
|---|---|
| 2026-10-27 | Creación del registro con S-001 a S-013. |
| 2026-10-27 | Se agrega S-014 por la creación del repositorio remoto. |
| 2026-10-27 | Fase 1: se agregan S-015 a S-028 y los supuestos no verificados SNV-01 a SNV-06. |
| 2026-10-27 | Fase 1: se agregan S-029 a S-032 por decisiones de modelado BPMN/DMN y artefactos visuales. |
