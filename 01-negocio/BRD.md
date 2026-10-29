# BRD — Business Requirements Document

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub
**Documento:** BRD-NB-001
**Versión:** 1.0
**Fecha:** 2026-10-27
**Autor:** Franco Tillería Centurión — Business Analyst
**Sponsor:** Gerencia de Banca Minorista (rol ficticio)
**Estado:** Aprobado para Fase 2 (validación funcional pendiente)

> Caso 100 % ficticio. NovaBank, sus clientes, cuentas, BIC e IBAN son inventados. Las referencias a BCP, SEPRELAD, GAFI, SWIFT e ISO 20022 son públicas y se usan solo como contexto normativo/técnico. Ver `docs/FUENTES.md`.

---

## 1. Resumen ejecutivo

NovaBank es un banco ficticio de Paraguay que compite en un mercado donde los clientes esperan pagos inmediatos, disponibilidad 24/7 y una experiencia digital comparable a la de las fintech. Hoy el banco no ofrece transferencias instantáneas locales de extremo a extremo ni un canal internacional integrado con ISO 20022; la operación depende de validaciones manuales, lotes y múltiples puntos de control, lo que eleva el costo, el tiempo de respuesta y el riesgo operativo.

El programa **NovaPay** tiene tres objetivos: (a) lanzar transferencias instantáneas locales inspiradas en el SPI del BCP; (b) habilitar pagos internacionales salientes sobre SWIFT/ISO 20022; y (c) integrar KYC, screening, monitoreo transaccional y gestión de alertas AML en el mismo flujo, sin frenar la experiencia del cliente.

Este BRD define el problema, los objetivos medibles, el alcance, los requerimientos de negocio, los beneficios y los KPIs. Los procesos, las reglas de decisión y los diagramas se detallan en `02-procesos/`. Los requerimientos funcionales y las historias se derivan en Fase 2.

---

## 2. Contexto y antecedentes

### 2.1 Contexto de mercado

- El BCP opera el Sistema de Pagos del Paraguay (SIPAP), con los módulos LBTR (alto valor), ACH (lotes), DEPO (valores) y SPI (pagos instantáneos de bajo valor) [F-02].
- El SPI permite transferencias interbancarias en guaraníes, 24 horas al día, 7 días a la semana, incluso feriados, con un tope de ₲10.000.000 por operación y un plazo máximo de acreditación de 5 segundos según la información pública del BCP [F-01].
- El SPI incorpora alias (CAS), devolución y solicitud de devolución; las transferencias son irreversibles, salvo procedimientos especiales por fraude [F-01].
- Los pagos transfronterizos migraron a ISO 20022: el período de coexistencia MT/ISO 20022 de SWIFT para CBPR+ finalizó el 22 de noviembre de 2025 [F-09]. La mensajería MT 103 sigue siendo relevante como referencia de negocio y para legados [F-10].
- La normativa paraguaya de prevención de LA/FT se apoya en la Ley N° 1015/1997 y sus modificatorias; SEPRELAD actúa como Unidad de Inteligencia Financiera (UIF) y recibe los Reportes de Operaciones Sospechosas (ROS) [F-03].
- El GAFI/FATF establece estándares de debida diligencia del cliente (Recomendación 10), transparencia de transferencias electrónicas (Recomendación 16) y reporte de operaciones sospechosas (Recomendación 20) [F-04].

### 2.2 Situación actual (AS-IS)

| Dimensión | Situación AS-IS | Consecuencia |
|---|---|---|
| Canal local | Solicitud por banca en línea o ventanilla; validación parcialmente manual; procesos por lote fuera del horario de LBTR/ACH. | Cliente sin confirmación inmediata; operación concentrada en horarios hábiles. |
| Disponibilidad | Ventanas de mantenimiento y cierres nocturnos. | Pagos urgentes quedan para el siguiente día hábil. |
| Datos | Formularios con validaciones básicas; correcciones manuales frecuentes. | Rechazos, reprocesos y costo operativo. |
| Internacional | Instrucción manual, armado de mensaje y seguimiento por correo o teléfono. | Baja trazabilidad, tiempos de respuesta altos y riesgo de error. |
| AML | Screening y monitoreo en herramientas separadas; alertas en hojas de cálculo y correo. | Priorización inconsistente, evidencia dispersa y SLA difíciles de auditar. |
| Contabilidad | Conciliación posterior y ajustes manuales. | Diferencias temporales y esfuerzo de cierre. |
| Cliente | Estado del pago consultado por contact center. | Mala experiencia y alto volumen de consultas. |

> El AS-IS es una reconstrucción funcional del caso ficticio. No representa procesos, métricas ni sistemas reales de ninguna entidad.

### 2.3 Problema central

NovaBank no puede competir en pagos instantáneos ni en cross-border con la velocidad, disponibilidad y trazabilidad que el mercado exige, porque su operación está fragmentada entre canales, core, mensajería y cumplimiento. La fragmentación impide: confirmar en segundos, operar 24/7, detectar riesgo en tiempo real y demostrar control ante el regulador.

### 2.4 Oportunidad

Unificar el flujo de pago y el control AML en una sola plataforma de orquestación permite:

- Acreditar pagos locales en segundos y con confirmación al cliente.
- Procesar pagos internacionales con mensajería ISO 20022 y seguimiento de estado.
- Evaluar riesgo antes de liberar el pago, no después.
- Reducir reprocesos, consultas y costo por transacción.
- Generar evidencia auditable y trazable para cumplimiento.

---

## 3. Objetivos medibles (SMART)

| ID | Objetivo | Métrica | Meta | Fecha objetivo |
|---|---|---|---|---|
| O-01 | Lanzar transferencias instantáneas locales para personas y empresas. | p95 de acreditación; disponibilidad mensual | ≤ 5 s; ≥ 99,9 % | 2027-06-30 |
| O-02 | Habilitar transferencias internacionales salientes en USD/EUR con ISO 20022. | % de mensajes validados; tasa STP | 100 % validados; ≥ 90 % STP | 2027-09-30 |
| O-03 | Integrar screening y scoring de riesgo en el flujo de pago. | % de pagos evaluados antes de liberar; tiempo de evaluación | 100 %; ≤ 2 s p95 | 2027-06-30 |
| O-04 | Reducir la gestión manual de pagos y alertas. | % de reducción de intervención manual; alertas P1 asignadas a tiempo | −40 %; ≥ 95 % en ≤ 15 min | 2027-12-31 |
| O-05 | Mejorar la experiencia y la transparencia del estado del pago. | Satisfacción del cliente; reclamos por pago | ≥ 4,3/5; < 0,5 % | 2027-12-31 |
| O-06 | Asegurar trazabilidad y evidencia para auditoría. | % de operaciones con traza completa extremo a extremo | ≥ 99,5 % | 2027-12-31 |

> Las metas son objetivos de planificación del caso ficticio, no resultados medidos. La línea base se establecerá durante el piloto (ver `kpis.md`).

---

## 4. Alcance

### 4.1 Dentro del alcance

| ID | Incluido | Descripción |
|---|---|---|
| A-01 | Transferencia instantánea local | P2P y P2B en PYG, 24/7, hasta ₲10.000.000, con alias o cuenta, confirmación y estado. |
| A-02 | Devoluciones y reclamos | Solicitud de devolución, consulta de estado y gestión de reclamos de pago. |
| A-03 | Transferencia internacional saliente | USD/EUR, validación de IBAN/BIC, mensajería ISO 20022 (pacs.008/pacs.002), seguimiento y reintentos controlados. |
| A-04 | Onboarding y KYC | Alta de cliente, debida diligencia, beneficiario final, PEP, revisión periódica y bloqueo por riesgo. |
| A-05 | Screening | Evaluación de listas ficticias de sanciones/PEP en onboarding y en pagos. |
| A-06 | Monitoreo transaccional | Reglas de umbral, velocidad, geografía, contraparte y estructuración; generación de alertas. |
| A-07 | Gestión de alertas | Bandeja, priorización, asignación, investigación, escalamiento y cierre con evidencia. |
| A-08 | ROS ficticio | Preparación, revisión y registro de un Reporte de Operación Sospechosa en el caso de prueba. |
| A-09 | Contabilidad | Asientos de partida doble, conciliación y reporte de diferencias. |
| A-10 | Reporting operativo | KPIs de pagos, alertas, SLA, rechazos y fraude. |
| A-11 | Auditoría | Bitácora de eventos, cambios de reglas y decisiones, con retención configurable. |

### 4.2 Fuera del alcance

| ID | Excluido | Motivo |
|---|---|---|
| E-01 | Transferencias internacionales entrantes (inbound) | Se evalúan en una segunda ola; el caso se enfoca en salida. |
| E-02 | Compra/venta de divisas y mesa de cambios | Requiere productos, precios y riesgos de mercado fuera del caso. |
| E-03 | QR Hub, pagos con tarjeta y adquirencia | Otros rieles y reglas; no son necesarios para demostrar el flujo principal. |
| E-04 | Construcción de la app móvil o del home banking | Se especifican pantallas y contratos, no se desarrolla el canal. |
| E-05 | Conectividad SWIFT real y certificación CBPR+ | Se simula el adaptador y se modelan los mensajes; la conexión real es responsabilidad de TI/Proveedor. |
| E-06 | Envío real de ROS a SEPRELAD | El ROS es ficticio y se documenta como artefacto de diseño. |
| E-07 | Uso de listas reales de sanciones/PEP | Riesgo de datos personales y de falsos positivos; se usan listas sintéticas. |
| E-08 | Crédito, leasing, seguros e inversiones | Fuera del dominio de pagos. |
| E-09 | Sustitución del core bancario | El proyecto integra el core existente. |
| E-10 | Cumplimiento fiscal o reportes regulatorios distintos de AML | Requiere alcance legal específico. |

### 4.3 Límites del caso

- Todo dato es sintético y reproducible con semilla fija.
- No se usan cuentas, documentos, direcciones ni identificadores de personas reales.
- Las reglas y umbrales son configurables y requieren aprobación formal antes de un uso real.
- La validación legal definitiva corresponde a las áreas de Cumplimiento y Legal; este documento no certifica cumplimiento regulatorio.

---

## 5. Stakeholders

El mapa completo, la matriz de poder/interés, el plan de involucramiento y la matriz RACI están en `stakeholders.md`.

| Grupo | Rol principal | Interés |
|---|---|---|
| Negocio / Producto | Dueño del producto y del resultado comercial | Time to market, adopción, ingresos |
| Operaciones | Operación diaria de pagos y conciliación | Eficiencia, excepciones, SLA |
| TI | Arquitectura, integración, seguridad y soporte | Estabilidad, escalabilidad, mantenibilidad |
| Riesgos | Riesgo operacional, crédito y fraude | Pérdidas, controles, apetito de riesgo |
| Cumplimiento / AML | KYC, screening, monitoreo, ROS | Cumplimiento normativo y evidencia |
| Contabilidad | Registro, conciliación y reporte | Exactitud, partida doble, cierres |
| Atención al cliente | Soporte y reclamos | Resolución, experiencia, información |
| Auditoría interna | Aseguramiento independiente | Diseño y efectividad de controles |

---

## 6. Procesos afectados

| Proceso | Estado actual | Estado objetivo | Referencia |
|---|---|---|---|
| Onboarding y KYC | Presencial y parcialmente digital | Alta digital con KYC remoto y debida diligencia por riesgo | `02-procesos/mapa-procesos.md` |
| Transferencia local | Lote/manual | Instantánea 24/7 con confirmación | BPMN AS-IS y TO-BE |
| Transferencia internacional | Manual | ISO 20022 con validación y seguimiento | BPMN internacional TO-BE |
| Gestión de alertas AML | Correo/hoja de cálculo | Bandeja, priorización y caso auditable | BPMN alerta AML |
| Investigación y ROS | Ad hoc | Flujo con evidencia y aprobación | BPMN investigación/ROS |
| Conciliación contable | Posterior/manual | Automatizada con excepciones controladas | Fase 3 |
| Reclamos | Contact center | Autoservicio y trazabilidad de estado | Fase 2/6 |

---

## 7. Requerimientos de negocio

Prioridad MoSCoW: **M** = Must, **S** = Should, **C** = Could, **W** = Won't (en esta fase).

| ID | Requerimiento | Prioridad | Criterio de éxito | Proceso |
|---|---|---|---|---|
| BR-01 | Permitir transferencias instantáneas locales en PYG, 24/7, hasta ₲10.000.000. | M | Pago aceptado y acreditado en ≤ 5 s p95; disponible en feriados. | Local TO-BE |
| BR-02 | Permitir identificar al beneficiario por alias o por cuenta. | M | Alias válido resuelve cuenta y titular sin ambigüedad. | Local TO-BE |
| BR-03 | Informar el estado del pago en tiempo real al cliente. | M | Estados consistentes: recibido, validado, enviado, acreditado, rechazado, devuelto. | Local/internacional |
| BR-04 | Gestionar devoluciones y reclamos de pago. | S | Solicitud registrada, trazable y con plazo visible. | Local TO-BE |
| BR-05 | Procesar transferencias internacionales salientes en USD/EUR con ISO 20022. | M | Mensaje validado y enviado; estado reconciliado. | Internacional TO-BE |
| BR-06 | Validar IBAN, BIC, moneda ISO 4217, importe y campos obligatorios antes de enviar. | M | 100 % de mensajes inválidos se rechazan antes de la red. | Internacional |
| BR-07 | Evaluar screening y riesgo del pago antes de liberar fondos. | M | 100 % de pagos evaluados; decisión registrada. | Local/internacional |
| BR-08 | Monitorear transacciones con reglas de umbral, velocidad, geografía, contraparte y estructuración. | M | Alerta generada con evidencia y regla aplicada. | AML |
| BR-09 | Gestionar alertas con prioridad, asignación, investigación, escalamiento y cierre. | M | Caso con historial completo y SLA medible. | Alerta AML |
| BR-10 | Aplicar KYC/CDD, identificar beneficiario final y tratar PEP. | M | Cliente con perfil de riesgo y debida diligencia documentada. | Onboarding |
| BR-11 | Registrar cada movimiento con partida doble y conciliar contra el riel. | M | Asientos balanceados; diferencias explicadas. | Contabilidad |
| BR-12 | Mantener traza de auditoría de eventos, decisiones y cambios de reglas. | M | Consulta por operación y por usuario; retención definida. | Transversal |
| BR-13 | Proveer KPIs operativos y de cumplimiento. | S | Tablero con métricas de pago, alertas, rechazos y SLA. | Reporting |
| BR-14 | Permitir configuración de límites y reglas sin despliegue de código. | S | Cambio parametrizado, versionado y aprobado. | Transversal |
| BR-15 | Gestionar excepciones y reintentos sin duplicar pagos. | M | Idempotencia por identificador único; estado consistente. | Local/internacional |
| BR-16 | Atender consultas y reclamos con información del estado del pago. | S | Agente ve traza y puede explicar la situación. | Atención al cliente |

### 7.1 Requerimientos no funcionales de alto nivel

| ID | Categoría | Requerimiento |
|---|---|---|
| NFR-01 | Disponibilidad | Canal de pagos ≥ 99,9 % mensual; operación 24/7. |
| NFR-02 | Rendimiento | p95 de evaluación de riesgo ≤ 2 s; p95 de acreditación local ≤ 5 s. |
| NFR-03 | Seguridad | Autenticación fuerte, cifrado en tránsito y en reposo, mínimo privilegio. |
| NFR-04 | Auditabilidad | Eventos inmutables y retención según política de cumplimiento. |
| NFR-05 | Escalabilidad | Soportar picos de campañas y cierres sin degradación. |
| NFR-06 | Observabilidad | Métricas, trazas y alertas operativas por componente. |
| NFR-07 | Recuperación | RTO/RPO definidos con el negocio; pruebas de recuperación. |
| NFR-08 | Usabilidad | Flujo de pago ≤ 4 pasos; errores comprensibles y accionables. |
| NFR-09 | Interoperabilidad | Contratos versionados (`/v1`) y mensajería ISO 20022. |
| NFR-10 | Privacidad | Minimización de datos, enmascaramiento y control de acceso. |

---

## 8. Beneficios esperados

### 8.1 Beneficios para el cliente

- Confirmación en segundos y disponibilidad 24/7.
- Visibilidad del estado y del motivo de rechazo.
- Menos pasos y menos datos repetidos gracias al alias.
- Atención más rápida y con información consistente.

### 8.2 Beneficios para NovaBank

| ID | Beneficio | Métrica | Meta | Horizonte |
|---|---|---|---|---|
| B-01 | Mayor adopción de pagos digitales | Transacciones digitales / total | +25 % | 12 meses post-lanzamiento |
| B-02 | Menor costo operativo por pago | Costo por transacción | −20 % | 12 meses |
| B-03 | Menos reprocesos | % de pagos con intervención manual | −40 % | 12 meses |
| B-04 | Mejor detección de riesgo | % de alertas priorizadas correctamente | ≥ 90 % | 6 meses |
| B-05 | Menor tiempo de investigación | Días hábiles promedio por caso | −30 % | 12 meses |
| B-06 | Menos pérdidas por fraude | Pérdida por fraude / volumen | −15 % | 12 meses |
| B-07 | Mayor capacidad de evidencia | % de casos con evidencia completa | ≥ 99 % | 6 meses |
| B-08 | Mejor posición competitiva | NPS de pagos | +10 puntos | 12 meses |

> Las metas son objetivos del caso. No se declaran resultados obtenidos.

### 8.3 Beneficios de cumplimiento

- Screening y monitoreo integrados al flujo, con decisión y evidencia.
- Alertas priorizadas por riesgo, con SLA y trazabilidad.
- ROS preparado con campos y narrativa consistentes.
- Reporte de auditoría listo para revisión interna y regulatoria.

---

## 9. KPIs

La ficha completa de cada KPI (definición, fórmula, fuente, frecuencia, dueño y umbral) está en `kpis.md`. Resumen:

| ID | KPI | Fórmula | Meta |
|---|---|---|---|
| K-01 | Tiempo de acreditación local p95 | Percentil 95 de (acreditación − aceptación) | ≤ 5 s |
| K-02 | Disponibilidad del canal | Minutos disponibles / minutos del mes | ≥ 99,9 % |
| K-03 | Tasa STP local | Pagos sin intervención / pagos totales | ≥ 95 % |
| K-04 | Rechazos por datos inválidos | Rechazos por validación / intentos | ≤ 2 % |
| K-05 | Cobertura de screening | Pagos evaluados / pagos liberados | 100 % |
| K-06 | Asignación de alertas P1 | Alertas P1 asignadas ≤ 15 min / total P1 | ≥ 95 % |
| K-07 | Cierre de investigación | Casos cerrados ≤ 10 días hábiles / total | ≥ 90 % |
| K-08 | ROS dentro de plazo | ROS presentados en plazo / ROS totales | 100 % |
| K-09 | Falsos positivos | Alertas descartadas / alertas generadas | ≤ 30 % |
| K-10 | Conciliación contable | Asientos conciliados / asientos totales | ≥ 99,5 % |

---

## 10. Supuestos

| ID | Supuesto | Impacto si no se cumple | Estado |
|---|---|---|---|
| SU-01 | El SPI opera 24/7, en PYG, con tope de ₲10.000.000 y acreditación ≤ 5 s. | Cambia el diseño del canal y los SLA. | Verificado con F-01 (2026-10-29); P-006 cerrado |
| SU-02 | NovaBank ya tiene core bancario, libro mayor y canal digital. | El alcance de TI y el cronograma cambian. | Activo |
| SU-03 | El banco será participante o subparticipante del SPI. | Sin participación no hay canal local directo. | Activo |
| SU-04 | La conexión SWIFT se simula mediante un adaptador; no hay certificación real en el caso. | El esfuerzo de integración real es mayor. | Activo |
| SU-05 | Las listas de sanciones/PEP y la lista de países de alto riesgo son ficticias. | Si se usan listas reales, cambian el screening y la privacidad. | Activo |
| SU-06 | El banco cuenta con oficial de cumplimiento y analistas AML. | El flujo de alertas no tendría responsables. | Activo |
| SU-07 | Los umbrales de los DMN son parámetros de diseño. | Sin validación, pueden generar falsos positivos o exposiciones. | `SUPUESTO NO VERIFICADO` (SNV-04) |
| SU-08 | Los pagos internacionales salen en USD/EUR; el cliente asume el FX. | Si el banco ofrece FX, se requiere otro alcance. | Activo |
| SU-09 | Los datos sintéticos se generan con semilla fija. | Se pierde reproducibilidad. | Activo |
| SU-10 | La validación legal es responsabilidad de Cumplimiento y Legal. | El BRD no debe tratarse como certificación regulatoria. | Activo |

---

## 11. Restricciones

| ID | Restricción | Tipo | Efecto |
|---|---|---|---|
| RE-01 | El caso es ficticio y no puede usar datos reales. | Legal/ética | Datos sintéticos y listas ficticias. |
| RE-02 | No se dispone de conectividad SWIFT/SPI real en el portafolio. | Técnica | Adaptadores y simuladores. |
| RE-03 | El equipo es reducido y el cronograma es acotado. | Proyecto | Priorización MoSCoW y entregas por fase. |
| RE-04 | La normativa aplicable debe verificarse con fuentes oficiales. | Legal | Citas, supuestos marcados y revisión de Cumplimiento. |
| RE-05 | El presupuesto de infraestructura es limitado. | Económica | Arquitectura modular y servicios gestionados. |
| RE-06 | El banco no reemplaza su core en este programa. | Técnica | Integración por API/adaptador. |
| RE-07 | El canal móvil no se desarrolla en este alcance. | Alcance | Especificaciones y contratos, no app. |
| RE-08 | La información de cumplimiento es reservada. | Legal | Control de acceso y enmascaramiento. |
| RE-09 | El repositorio es público. | Seguridad | Sin secretos, credenciales ni datos personales. |
| RE-10 | La documentación debe ser comprensible para audiencia no técnica. | Comunicación | Diagramas, glosario y lenguaje claro. |

---

## 12. Dependencias

| ID | Dependencia | Dueño | Riesgo asociado |
|---|---|---|---|
| D-01 | Participación/certificación en SPI | Operaciones / BCP | Sin canal local. |
| D-02 | Conectividad SWIFT y acuerdo de corresponsalía | TI / Tesorería | Sin canal internacional. |
| D-03 | Core bancario y API de cuentas | TI / Core | Sin débito/consulta de saldo. |
| D-04 | Herramienta de screening y listas | Cumplimiento | Sin control de sanciones/PEP. |
| D-05 | Motor de reglas y monitoreo | Riesgos / TI | Sin detección oportuna. |
| D-06 | Disponibilidad de datos sintéticos | BA / Datos | Sin pruebas reproducibles. |
| D-07 | Aprobación de umbrales y apetito de riesgo | Riesgos / Cumplimiento | Reglas sin legitimidad. |
| D-08 | Validación legal de normativa | Legal / Cumplimiento | Diseño no conforme. |
| D-09 | Infraestructura de observabilidad | TI | Sin evidencia de SLA. |
| D-10 | Plan de comunicación y capacitación | Negocio / RRHH | Baja adopción y errores operativos. |

---

## 13. Riesgos

El registro completo, con probabilidad, impacto, score, respuesta, dueño y riesgo residual, está en `riesgos.md`. Los riesgos prioritarios son:

- **R-01** Incumplimiento normativo por interpretación errónea de SPI/SEPRELAD.
- **R-02** Fraude o suplantación en pagos instantáneos.
- **R-03** Falsos positivos que bloquean clientes legítimos.
- **R-04** Indisponibilidad del SPI, SWIFT o core.
- **R-05** Duplicidad de pagos por reintentos sin idempotencia.
- **R-06** Brecha de datos personales o de información AML.
- **R-07** Dependencia de un proveedor crítico.
- **R-08** Baja adopción por parte de clientes y sucursales.

---

## 14. Marco regulatorio y estándares

| Tema | Referencia | Uso en el caso | Estado |
|---|---|---|---|
| Pagos instantáneos | BCP — SPI / SIPAP [F-01, F-02] | Límite, horario, acreditación, alias, devoluciones. | Verificado con discrepancia de horario (P-006). |
| Prevención LA/FT | SEPRELAD — Ley N° 1015/1997 y modificatorias, ROS, PEP [F-03] | KYC, beneficiario final, PEP, alertas, ROS. | Verificado; resolución específica para bancos pendiente (P-009). |
| Estándar internacional AML | GAFI/FATF — R.10, R.16, R.20 [F-04] | Debida diligencia, transparencia de pagos, reporte. | Verificado con acceso parcial (P-007). |
| Mensajería ISO 20022 | ISO 20022 / SWIFT CBPR+ [F-08, F-09] | pacs.008, pacs.002 y estados. | Verificado con acceso parcial (P-008). |
| Mensajería MT | SWIFT MT 103 [F-10] | Referencia de legado y mapeo futuro. | Verificado. |
| IBAN | ISO 13616-1:2020 / SWIFT [F-06, F-07] | Validación de cuenta internacional. | Verificado. |
| Monedas | ISO 4217:2015 [F-05] | Códigos de moneda y unidades menores. | Verificado. |

> `SUPUESTO NO VERIFICADO`: la aplicación concreta de cada norma al perímetro de NovaBank debe ser validada por Cumplimiento y Legal. Este BRD no constituye asesoría legal ni certificación de cumplimiento.

---

## 15. Criterios de éxito y aprobación

### 15.1 Criterios de éxito del BRD

- [x] Problema, contexto y oportunidad definidos.
- [x] Objetivos medibles con métrica, meta y fecha.
- [x] Alcance dentro/fuera explícito.
- [x] Supuestos y restricciones registrados.
- [x] Beneficios y KPIs trazables.
- [x] stakeholders, riesgos y procesos referenciados.
- [x] Fuentes oficiales registradas y brechas marcadas.

### 15.2 Aprobaciones requeridas

| Rol | Nombre / área | Criterio | Estado |
|---|---|---|---|
| Sponsor | Gerencia de Banca Minorista | Alineación estratégica y presupuesto | Pendiente de validación ficticia |
| Negocio | Producto Pagos | Alcance y beneficios | Pendiente de validación ficticia |
| Operaciones | Gerencia de Operaciones | Capacidad operativa y SLA | Pendiente de validación ficticia |
| TI | Arquitectura | Viabilidad técnica e integración | Pendiente de validación ficticia |
| Riesgos | Riesgo Operacional | Apetito y controles | Pendiente de validación ficticia |
| Cumplimiento | Oficial de Cumplimiento | KYC, screening, ROS | Pendiente de validación ficticia |
| Contabilidad | Contraloría | Partida doble y conciliación | Pendiente de validación ficticia |

> Las aprobaciones son parte del caso ficticio; no se declaran obtenidas.

### 15.3 Criterios de salida de Fase 1

- BRD, stakeholders, riesgos, glosario y KPIs revisados.
- Procesos AS-IS/TO-BE y BPMN/DMN validados estructuralmente.
- Fuentes registradas y pendientes documentados.
- Evidencias manuales de Camunda/Lucidchart preparadas en `docs/EVIDENCIAS.md`.

---

## 16. Trazabilidad hacia Fase 2

| Requerimiento | Épica propuesta | Historias (Fase 2) | Proceso |
|---|---|---|---|
| BR-01, BR-02, BR-03 | Pagos locales instantáneos | Crear transferencia, resolver alias, consultar estado | Local TO-BE |
| BR-04 | Devoluciones y reclamos | Solicitar devolución, responder devolución | Local TO-BE |
| BR-05, BR-06 | Cross-border ISO 20022 | Validar IBAN/BIC, enviar pacs.008, procesar pacs.002 | Internacional TO-BE |
| BR-07, BR-08 | Riesgo en tiempo real | Screening, scoring, reglas de monitoreo | Local/internacional |
| BR-09 | Gestión de alertas | Bandeja, asignación, investigación, escalamiento | Alerta AML |
| BR-10 | Onboarding y KYC | Alta, CDD, PEP, beneficiario final, revisión | Onboarding |
| BR-11 | Contabilidad y conciliación | Asientos, conciliación, diferencias | Fase 3 |
| BR-12 | Auditoría | Bitácora, consulta, retención | Transversal |
| BR-13 | Reporting | Tablero operativo y de cumplimiento | Fase 6 |
| BR-14 | Parametrización | Administrar límites y reglas | Transversal |
| BR-15 | Idempotencia y excepciones | Reintentos, timeout, reversa | Local/internacional |
| BR-16 | Atención al cliente | Consulta de estado y reclamo | Fase 2/6 |

---

## 17. Anexos

| Anexo | Documento |
|---|---|
| Mapa de stakeholders y RACI | `01-negocio/stakeholders.md` |
| Registro de riesgos | `01-negocio/riesgos.md` |
| Glosario bilingüe | `01-negocio/glosario.md` |
| Ficha de KPIs | `01-negocio/kpis.md` |
| Contexto regulatorio | `01-negocio/contexto-regulatorio.md` |
| Mapa de procesos | `02-procesos/mapa-procesos.md` |
| Procesos Mermaid | `02-procesos/procesos-mermaid.md` |
| Diagramas de sistema | `02-procesos/diagramas-sistema.md` |
| Guía de diagramación | `02-procesos/guia-lucidchart-visio-miro.md` |
| Fuentes | `docs/FUENTES.md` |
| Supuestos y pendientes | `docs/SUPUESTOS.md`, `docs/PENDIENTES.md` |

---

**Fin del documento.**
