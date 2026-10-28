# Glosario bilingüe

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub
**Documento:** GLO-NB-001
**Versión:** 1.0
**Fecha:** 2026-10-27
**Autor:** Franco Tillería Centurión — Business Analyst

> Glosario funcional del caso. Las definiciones son operativas y no sustituyen textos legales o estándares. Cuando un término depende de una fuente oficial, se indica en `docs/FUENTES.md`.

---

## 1. Cómo usar el glosario

- **Término (ES):** denominación usada en la documentación.
- **English:** equivalente usado en mensajes, APIs o documentación técnica.
- **Categoría:** dominio al que pertenece.
- **Definición:** explicación breve y aplicable al caso.
- **Nota:** aclaración, alcance o advertencia.

Los identificadores de código, campos de API y nombres de mensajes se mantienen en inglés; la documentación funcional se mantiene en español.

---

## 2. Gobernanza y análisis

| # | Término (ES) | English | Categoría | Definición | Nota |
|---|---|---|---|---|---|
| 1 | AS-IS | As-is | Procesos | Situación actual de un proceso, con sus pasos, sistemas y problemas. | Base para el análisis de brechas. |
| 2 | TO-BE | To-be | Procesos | Situación futura deseada de un proceso, rediseñada para cumplir objetivos. | Se modela en BPMN y se valida con negocio. |
| 3 | BPMN | Business Process Model and Notation | Procesos | Notación estándar para modelar procesos de negocio con eventos, tareas y gateways. | El caso usa BPMN 2.0. |
| 4 | DMN | Decision Model and Notation | Decisiones | Notación estándar para modelar decisiones y tablas de decisión. | El caso usa DMN 1.3. |
| 5 | BRD | Business Requirements Document | Análisis | Documento que define problema, objetivos, alcance y requerimientos de negocio. | Documento principal de Fase 1. |
| 6 | RACI | Responsible, Accountable, Consulted, Informed | Gobernanza | Matriz que asigna responsabilidad, rendición de cuentas, consulta e información. | Un solo `A` por actividad. |
| 7 | MoSCoW | Must, Should, Could, Won't | Priorización | Técnica de priorización de requerimientos por obligatoriedad y valor. | Usada en el BRD. |
| 8 | KPI | Key Performance Indicator | Medición | Indicador clave para medir el desempeño de un objetivo. | Fichas en `kpis.md`. |
| 9 | Línea base | Baseline | Medición | Valor de referencia medido antes de comparar resultados contra una meta. | No se inventa: se mide en el piloto. |
| 10 | UAT | User Acceptance Testing | Pruebas | Pruebas de aceptación ejecutadas por usuarios para validar que el proceso cumple el negocio. | Fase 4. |
| 11 | Trazabilidad | Traceability | Gobernanza | Capacidad de vincular requisito, proceso, regla, prueba y evidencia. | Se exige de extremo a extremo. |
| 12 | Evidencia | Evidence | Auditoría | Registro verificable de una decisión, control o resultado. | Logs, casos, actas y capturas. |
| 13 | Supuesto no verificado | Unverified assumption | Gobernanza | Afirmación usada para avanzar pero no confirmada con fuente oficial. | Se marca `SUPUESTO NO VERIFICADO`. |
| 14 | Riesgo residual | Residual risk | Riesgos | Riesgo que permanece después de aplicar controles. | Requiere aceptación formal. |
| 15 | Apetito de riesgo | Risk appetite | Riesgos | Nivel de riesgo que la organización está dispuesta a aceptar. | Define umbrales de escalamiento. |
| 16 | Control preventivo | Preventive control | Riesgos | Control que actúa antes de que ocurra el evento de riesgo. | Ejemplo: límite o validación. |
| 17 | Control detectivo | Detective control | Riesgos | Control que identifica un evento después de ocurrido. | Ejemplo: monitoreo o conciliación. |

---

## 3. Pagos y sistema financiero

| # | Término (ES) | English | Categoría | Definición | Nota |
|---|---|---|---|---|---|
| 18 | SPI | Instant Payment System | Pagos | Sistema de pagos instantáneos del Paraguay, orientado a transferencias de bajo valor en guaraníes. | Referencia pública del BCP [F-01]. |
| 19 | SIPAP | Paraguayan Payment System | Pagos | Sistema de Pagos del Paraguay, que integra los módulos de pagos del país. | Incluye LBTR, ACH, DEPO y SPI [F-02]. |
| 20 | LBTR | Real-Time Gross Settlement | Pagos | Sistema de liquidación bruta en tiempo real para operaciones de alto valor. | Operación normalmente en horario acotado. |
| 21 | ACH | Automated Clearing House | Pagos | Cámara de compensación para pagos por lote. | Usada para volúmenes y pagos no urgentes. |
| 22 | BCP | Banco Central del Paraguay | Regulación | Autoridad monetaria y regulador del sistema de pagos. | Opera el SIPAP. |
| 23 | SIB | Superintendencia de Bancos | Regulación | Área del BCP que supervisa a las entidades financieras. | Supervisión prudencial. |
| 24 | Alias / CAS | Alias | Pagos | Identificador simple que permite dirigir un pago sin ingresar la cuenta completa. | En el caso se usa “alias” y “CAS” como sinónimos. |
| 25 | P2P | Person to Person | Pagos | Transferencia entre personas físicas. | Caso de uso principal local. |
| 26 | P2B | Person to Business | Pagos | Transferencia de una persona a una empresa. | Incluye pago de servicios. |
| 27 | Cross-border | Cross-border payment | Pagos | Pago en el que originador y beneficiario están en países distintos. | El caso cubre salida USD/EUR. |
| 28 | Corresponsal | Correspondent bank | Pagos | Banco que presta servicios de compensación o liquidación a otro banco. | Contraparte ficticia. |
| 29 | Nostro | Nostro account | Pagos | Cuenta que el banco mantiene en un banco corresponsal. | “Nuestra cuenta en el exterior”. |
| 30 | Vostro | Vostro account | Pagos | Cuenta que un banco corresponsal mantiene en nuestro banco. | “Su cuenta en nuestro banco”. |
| 31 | FX | Foreign exchange | Pagos | Conversión de una moneda a otra. | Fuera de alcance en Fase 1. |
| 32 | Devolución | Refund / return | Pagos | Proceso por el cual se revierte o devuelve un pago al ordenante. | El SPI contempla solicitud de devolución [F-01]. |
| 33 | Irrevocabilidad | Irrevocability | Pagos | Condición por la cual una orden no puede cancelarse una vez aceptada. | Exige confirmación previa clara. |
| 34 | STP | Straight-Through Processing | Operación | Procesamiento automático sin intervención manual. | Métrica clave de eficiencia. |
| 35 | p95 | 95th percentile | Medición | Valor por debajo del cual se encuentra el 95 % de las observaciones. | Usado para SLA de latencia. |
| 36 | SLA | Service Level Agreement | Operación | Acuerdo de nivel de servicio con métricas, objetivos y responsabilidades. | Debe ser medible. |
| 37 | RTO | Recovery Time Objective | Continuidad | Tiempo máximo objetivo para restablecer un servicio. | Se define con negocio y TI. |
| 38 | RPO | Recovery Point Objective | Continuidad | Cantidad máxima de datos que se acepta perder en una recuperación. | Se define con negocio y TI. |
| 39 | Idempotencia | Idempotency | Tecnología | Propiedad por la cual repetir una operación no produce efectos duplicados. | Crítica para reintentos. |
| 40 | Conciliación | Reconciliation | Contabilidad | Comparación entre registros internos y fuentes externas para detectar diferencias. | Cierre diario. |
| 41 | Partida doble | Double-entry bookkeeping | Contabilidad | Principio contable por el cual todo asiento tiene débito y crédito de igual importe. | Invariante verificada por tests. |
| 42 | Libro mayor | General ledger | Contabilidad | Registro central de cuentas y movimientos contables. | Fuente de verdad contable. |

---

## 4. Mensajería y estándares

| # | Término (ES) | English | Categoría | Definición | Nota |
|---|---|---|---|---|---|
| 43 | ISO 20022 | ISO 20022 | Estándar | Estándar internacional para el intercambio de mensajes financieros con un modelo de datos común. | Base de la mensajería internacional del caso [F-08]. |
| 44 | pacs.008 | FIToFICustomerCreditTransfer | Mensajería | Mensaje ISO 20022 de transferencia de crédito de cliente entre instituciones financieras. | Equivalente funcional a MT 103. |
| 45 | pacs.002 | FIToFIPaymentStatusReport | Mensajería | Mensaje ISO 20022 que informa el estado de un pago. | Se correlaciona con pacs.008. |
| 46 | UETR | Unique End-to-End Transaction Reference | Mensajería | Identificador único que permite seguir una transacción de extremo a extremo. | Clave de trazabilidad. |
| 47 | MT103 | MT 103 Single Customer Credit Transfer | Mensajería | Mensaje SWIFT de transferencia de crédito de cliente. | Referencia de legado [F-10]. |
| 48 | CBPR+ | Cross-Border Payments and Reporting Plus | Mensajería | Guías de uso de ISO 20022 de SWIFT para pagos transfronterizos y reportes. | Coexistencia MT/ISO finalizó el 22-11-2025 [F-09]. |
| 49 | ISO 4217 | ISO 4217 | Estándar | Estándar de códigos de moneda de tres letras y tres dígitos. | Ejemplos: PYG, USD, EUR [F-05]. |
| 50 | ISO 13616 | ISO 13616 | Estándar | Estándar que define la estructura del IBAN. | SWIFT actúa como autoridad de registro [F-06, F-07]. |
| 51 | IBAN | International Bank Account Number | Estándar | Identificador internacional de cuenta con país, dígitos de control y BBAN. | Se valida estructura y checksum. |
| 52 | BIC | Bank Identifier Code | Estándar | Código de 8 u 11 caracteres que identifica a una institución financiera. | También llamado SWIFT code. |
| 53 | API | Application Programming Interface | Tecnología | Interfaz que permite a sistemas intercambiar datos y ejecutar operaciones. | Contratos versionados `/v1`. |
| 54 | Webhook | Webhook | Tecnología | Notificación HTTP enviada por un sistema a otro cuando ocurre un evento. | Requiere reintentos e idempotencia. |
| 55 | Evento | Event | Tecnología | Hecho relevante ocurrido en el proceso, con estado y momento determinado. | Base de la trazabilidad. |

---

## 5. AML/CFT y cumplimiento

| # | Término (ES) | English | Categoría | Definición | Nota |
|---|---|---|---|---|---|
| 56 | SEPRELAD | Secretaría de Prevención de Lavado de Dinero o Bienes | Regulación | Unidad de Inteligencia Financiera (UIF) de Paraguay. | Recibe ROS [F-03]. |
| 57 | UIF | Financial Intelligence Unit | Regulación | Autoridad nacional que recibe, analiza y disemina información financiera sospechosa. | En Paraguay, SEPRELAD. |
| 58 | ROS | Suspicious Transaction Report | Cumplimiento | Reporte de una operación sospechosa enviado a la UIF. | En el caso es ficticio. |
| 59 | KYC | Know Your Customer | Cumplimiento | Proceso de identificar y verificar al cliente y entender su actividad. | Parte de CDD. |
| 60 | CDD | Customer Due Diligence | Cumplimiento | Debida diligencia del cliente: identificación, verificación, propósito y monitoreo. | Basada en riesgo [F-04 R.10]. |
| 61 | EDD | Enhanced Due Diligence | Cumplimiento | Debida diligencia reforzada para clientes o operaciones de mayor riesgo. | Aplica a PEP y alto riesgo. |
| 62 | PEP | Politically Exposed Person | Cumplimiento | Persona con función pública relevante o vínculo cercano, sujeta a controles reforzados. | Res. SEPRELAD 50/19 citada en F-03. |
| 63 | Beneficiario final | Beneficial owner | Cumplimiento | Persona física que controla o se beneficia de una cuenta, entidad u operación. | Umbrales de F-03; validación pendiente. |
| 64 | LA/FT | AML/CFT | Cumplimiento | Prevención de lavado de activos y financiamiento del terrorismo. | Marco del caso. |
| 65 | GAFI / FATF | Financial Action Task Force | Regulación | Organismo intergubernamental que emite estándares AML/CFT. | R.10, R.16 y R.20 [F-04]. |
| 66 | Screening | Screening | Cumplimiento | Comparación de personas u operaciones contra listas de sanciones, PEP u otras. | Listas ficticias en el caso. |
| 67 | Sanción | Sanction | Cumplimiento | Restricción legal o regulatoria que impide operar con una persona, entidad o país. | Requiere bloqueo y reporte. |
| 68 | Lista de sanciones | Sanctions list | Cumplimiento | Catálogo de personas o entidades sujetas a restricciones. | No se usan listas reales. |
| 69 | Monitoreo transaccional | Transaction monitoring | Cumplimiento | Análisis continuo de operaciones para detectar patrones inusuales o sospechosos. | Reglas y scoring. |
| 70 | Alerta | Alert | Cumplimiento | Señal generada por una regla o modelo que requiere revisión. | Debe tener prioridad y dueño. |
| 71 | Caso AML | AML case | Cumplimiento | Expediente que agrupa alertas, evidencia, análisis y decisión. | Ciclo de vida auditable. |
| 72 | Tipología | Typology | Cumplimiento | Patrón conocido de comportamiento delictivo o de riesgo. | Guía el diseño de reglas. |
| 73 | Umbral | Threshold | Cumplimiento | Valor límite que activa una validación, alerta o revisión. | Parámetro configurable. |
| 74 | Estructuración | Structuring | Cumplimiento | Fragmentación de operaciones para evitar umbrales de reporte o control. | Regla de monitoreo. |
| 75 | Falso positivo | False positive | Cumplimiento | Coincidencia o alerta que resulta no sospechosa tras la revisión. | Se mide para calibrar. |
| 76 | Falso negativo | False negative | Cumplimiento | Caso sospechoso que no fue detectado por el control. | Riesgo crítico de modelo. |
| 77 | Reserva | Tipping off | Cumplimiento | Prohibición de revelar al cliente que se reportó una operación sospechosa. | Control de acceso y comunicación. |
| 78 | Onboarding | Onboarding | Cumplimiento | Proceso de alta y aceptación de un cliente. | Incluye KYC y riesgo. |
| 79 | Motor de reglas | Rules engine | Tecnología | Componente que evalúa reglas de negocio y produce decisiones. | Parametrizable y versionado. |
| 80 | Riesgo operacional | Operational risk | Riesgos | Riesgo de pérdida por fallas de procesos, personas, sistemas o eventos externos. | Incluye fraude y errores. |

---

## 6. Índice de siglas

| Sigla | Expansión |
|---|---|
| ACH | Automated Clearing House |
| AML/CFT | Anti-Money Laundering / Combating the Financing of Terrorism |
| API | Application Programming Interface |
| AS-IS | Situación actual |
| BCP | Banco Central del Paraguay |
| BIC | Bank Identifier Code |
| BPMN | Business Process Model and Notation |
| BRD | Business Requirements Document |
| CAS | Clave de Alias Simple (uso funcional en el SPI) |
| CBPR+ | Cross-Border Payments and Reporting Plus |
| CDD | Customer Due Diligence |
| DMN | Decision Model and Notation |
| EDD | Enhanced Due Diligence |
| FATF | Financial Action Task Force |
| FX | Foreign Exchange |
| GAFI | Grupo de Acción Financiera Internacional |
| IBAN | International Bank Account Number |
| ISO | International Organization for Standardization |
| KPI | Key Performance Indicator |
| KYC | Know Your Customer |
| LA/FT | Lavado de Activos / Financiamiento del Terrorismo |
| LBTR | Liquidación Bruta en Tiempo Real |
| MoSCoW | Must, Should, Could, Won't |
| P2P | Person to Person |
| P2B | Person to Business |
| PEP | Politically Exposed Person |
| RACI | Responsible, Accountable, Consulted, Informed |
| ROS | Reporte de Operación Sospechosa |
| RPO | Recovery Point Objective |
| RTO | Recovery Time Objective |
| SIB | Superintendencia de Bancos |
| SIPAP | Sistema de Pagos del Paraguay |
| SLA | Service Level Agreement |
| SPI | Sistema de Pagos Instantáneos |
| STP | Straight-Through Processing |
| TO-BE | Situación futura |
| UAT | User Acceptance Testing |
| UETR | Unique End-to-End Transaction Reference |
| UIF | Unidad de Inteligencia Financiera |

---

## 7. Términos deliberadamente excluidos

| Término | Motivo |
|---|---|
| CBDC | No forma parte del alcance del caso. |
| Open Banking | No se modela en Fase 1. |
| QR interoperable | Fuera del alcance (E-03). |
| Tarjetas de crédito/débito | Otro dominio de negocio. |
| Criptoactivos | Fuera del alcance y con marco regulatorio distinto. |
| SWIFT gpi completo | Solo se usa el concepto de UETR y seguimiento; no se implementa gpi. |

---

## 8. Referencias

- `docs/FUENTES.md` — definiciones respaldadas por fuentes.
- `docs/SUPUESTOS.md` — supuestos y términos no verificados.
- `BRD.md` — uso de los conceptos en requerimientos.
- `contexto-regulatorio.md` — marco normativo.
