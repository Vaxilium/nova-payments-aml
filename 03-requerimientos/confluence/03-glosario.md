# Glosario — pagos, mensajería y AML

**Página:** Glosario  
**Documento fuente:** `01-negocio/glosario.md` (GLO-NB-001)  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Dueño:** BA / Producto  
**Estado:** Borrador para revisión ficticia

> Definiciones operativas del caso NovaBank. No sustituyen textos legales ni estándares. Las referencias normativas están en `docs/FUENTES.md`.

---

## 1. Gobernanza y análisis

| Término | English | Definición |
|---|---|---|
| AS-IS | As-is | Situación actual de un proceso, con pasos, sistemas y problemas. |
| TO-BE | To-be | Situación futura deseada, rediseñada para cumplir objetivos. |
| BPMN | Business Process Model and Notation | Notación estándar para modelar procesos con eventos, tareas y compuertas. |
| DMN | Decision Model and Notation | Notación estándar para modelar decisiones y tablas de decisión. |
| BRD | Business Requirements Document | Documento de problema, objetivos, alcance y requerimientos de negocio. |
| RACI | Responsible, Accountable, Consulted, Informed | Matriz de responsabilidades; un solo `A` por actividad. |
| MoSCoW | Must, Should, Could, Won't | Técnica de priorización por obligatoriedad y valor. |
| KPI | Key Performance Indicator | Indicador clave para medir un objetivo. |
| Línea base | Baseline | Valor de referencia medido antes de comparar contra una meta. |
| UAT | User Acceptance Testing | Pruebas de aceptación ejecutadas por usuarios. |
| Trazabilidad | Traceability | Capacidad de vincular requisito, proceso, regla, prueba y evidencia. |
| Evidencia | Evidence | Registro verificable de una decisión, control o resultado. |
| Supuesto no verificado | Unverified assumption | Afirmación usada para avanzar sin confirmación oficial. |
| Riesgo residual | Residual risk | Riesgo que permanece después de aplicar controles. |
| Apetito de riesgo | Risk appetite | Nivel de riesgo que la organización acepta. |
| Control preventivo | Preventive control | Control que actúa antes del evento de riesgo. |
| Control detectivo | Detective control | Control que identifica un evento después de ocurrido. |

---

## 2. Pagos y sistema financiero

| Término | English | Definición |
|---|---|---|
| SPI | Instant Payment System | Sistema de pagos instantáneos de Paraguay para bajo valor en guaraníes. |
| SIPAP | Paraguayan Payment System | Sistema de Pagos del Paraguay; integra LBTR, ACH, DEPO y SPI. |
| LBTR | Real-Time Gross Settlement | Liquidación bruta en tiempo real para operaciones de alto valor. |
| ACH | Automated Clearing House | Cámara de compensación para pagos por lote. |
| BCP | Banco Central del Paraguay | Autoridad monetaria y regulador del sistema de pagos. |
| SIB | Superintendencia de Bancos | Área del BCP que supervisa entidades financieras. |
| Alias / CAS | Alias | Identificador simple para dirigir un pago sin la cuenta completa. |
| P2P | Person to Person | Transferencia entre personas físicas. |
| P2B | Person to Business | Transferencia de una persona a una empresa. |
| Cross-border | Cross-border payment | Pago entre países distintos; el caso cubre salida USD/EUR. |
| Corresponsal | Correspondent bank | Banco que presta servicios de compensación o liquidación a otro. |
| Nostro | Nostro account | Cuenta del banco en un corresponsal. |
| Vostro | Vostro account | Cuenta de un corresponsal en nuestro banco. |
| FX | Foreign exchange | Conversión de moneda; fuera de alcance en el caso. |
| Devolución | Refund / return | Reversión o devolución de un pago al ordenante. |
| Irrevocabilidad | Irrevocability | Condición por la cual una orden no se cancela una vez aceptada. |
| STP | Straight-Through Processing | Procesamiento automático sin intervención manual. |
| p95 | 95th percentile | Valor por debajo del cual está el 95 % de las observaciones. |
| SLA | Service Level Agreement | Acuerdo de nivel de servicio con métricas y responsabilidades. |
| RTO | Recovery Time Objective | Tiempo máximo objetivo para restablecer un servicio. |
| RPO | Recovery Point Objective | Pérdida máxima de datos aceptada en una recuperación. |
| Idempotencia | Idempotency | Propiedad por la cual repetir una operación no duplica efectos. |
| Conciliación | Reconciliation | Comparación entre registros internos y fuentes externas. |
| Partida doble | Double-entry bookkeeping | Todo asiento tiene débito y crédito de igual importe. |
| Libro mayor | General ledger | Registro central de cuentas y movimientos contables. |

---

## 3. Mensajería y estándares

| Término | English | Definición |
|---|---|---|
| ISO 20022 | ISO 20022 | Estándar internacional de mensajes financieros con modelo de datos común. |
| pacs.008 | FIToFICustomerCreditTransfer | Mensaje ISO 20022 de transferencia de crédito de cliente entre instituciones. |
| pacs.002 | FIToFIPaymentStatusReport | Mensaje ISO 20022 que informa el estado de un pago. |
| UETR | Unique End-to-End Transaction Reference | Identificador único para seguir una transacción de extremo a extremo. |
| MT103 | MT 103 Single Customer Credit Transfer | Mensaje SWIFT de transferencia de crédito de cliente; referencia de legado. |
| CBPR+ | Cross-Border Payments and Reporting Plus | Guías de uso de ISO 20022 de SWIFT para pagos transfronterizos. |
| ISO 4217 | ISO 4217 | Estándar de códigos de moneda de tres letras y tres dígitos. |
| ISO 13616 | ISO 13616 | Estándar que define la estructura del IBAN. |
| IBAN | International Bank Account Number | Identificador internacional de cuenta con país, control y BBAN. |
| BIC | Bank Identifier Code | Código de 8 u 11 caracteres que identifica una institución financiera. |
| API | Application Programming Interface | Interfaz para intercambiar datos y ejecutar operaciones. |
| Webhook | Webhook | Notificación HTTP enviada cuando ocurre un evento. |
| Evento | Event | Hecho relevante con estado y momento determinado. |

---

## 4. AML/CFT y cumplimiento

| Término | English | Definición |
|---|---|---|
| SEPRELAD | Secretaría de Prevención de Lavado de Dinero o Bienes | Unidad de Inteligencia Financiera de Paraguay. |
| UIF | Financial Intelligence Unit | Autoridad que recibe, analiza y disemina información financiera sospechosa. |
| ROS | Suspicious Transaction Report | Reporte de operación sospechosa enviado a la UIF; en el caso es ficticio. |
| KYC | Know Your Customer | Proceso de identificar y verificar al cliente y su actividad. |
| CDD | Customer Due Diligence | Debida diligencia: identificación, verificación, propósito y monitoreo. |
| EDD | Enhanced Due Diligence | Debida diligencia reforzada para mayor riesgo. |
| PEP | Politically Exposed Person | Persona con función pública relevante o vínculo cercano. |
| Beneficiario final | Beneficial owner | Persona física que controla o se beneficia de una cuenta o entidad. |
| LA/FT | AML/CFT | Prevención de lavado de activos y financiamiento del terrorismo. |
| GAFI / FATF | Financial Action Task Force | Organismo intergubernamental que emite estándares AML/CFT. |
| Screening | Screening | Comparación contra listas de sanciones, PEP u otras. |
| Sanción | Sanction | Restricción legal o regulatoria sobre una persona, entidad o país. |
| Monitoreo transaccional | Transaction monitoring | Análisis continuo para detectar patrones inusuales. |
| Alerta | Alert | Señal generada por una regla o modelo que requiere revisión. |
| Caso AML | AML case | Expediente con alertas, evidencia, análisis y decisión. |
| Tipología | Typology | Patrón conocido de comportamiento delictivo o de riesgo. |
| Umbral | Threshold | Valor límite que activa una validación, alerta o revisión. |
| Estructuración | Structuring | Fragmentación de operaciones para evitar umbrales. |
| Falso positivo | False positive | Coincidencia o alerta que resulta no sospechosa. |
| Falso negativo | False negative | Caso sospechoso no detectado por el control. |
| Reserva | Tipping off | Prohibición de revelar al cliente que se reportó una sospecha. |
| Onboarding | Onboarding | Proceso de alta y aceptación de un cliente. |
| Motor de reglas | Rules engine | Componente que evalúa reglas y produce decisiones. |
| Riesgo operacional | Operational risk | Riesgo de pérdida por fallas de procesos, personas o sistemas. |

---

## 5. Siglas

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
| CAS | Clave de Alias Simple |
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

## 6. Referencias

- `01-negocio/glosario.md` — glosario completo.
- `docs/FUENTES.md` — fuentes oficiales.
- `docs/SUPUESTOS.md` — supuestos y términos no verificados.
- `01-negocio/BRD.md` — uso de conceptos en requerimientos.

**Fin de la página.**
