# Registro de riesgos

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub
**Documento:** RSK-NB-001
**Versión:** 1.0
**Fecha:** 2026-10-27
**Autor:** Franco Tillería Centurión — Business Analyst

> Evaluación cualitativa de un caso ficticio. Las probabilidades e impactos son estimaciones de diseño, no mediciones históricas. No se declaran riesgos materializados ni pérdidas reales.

---

## 1. Metodología

- **Probabilidad (P):** 1 = raro, 2 = improbable, 3 = posible, 4 = probable, 5 = casi seguro.
- **Impacto (I):** 1 = insignificante, 2 = menor, 3 = moderado, 4 = mayor, 5 = severo.
- **Score:** `P × I` (1–25).
- **Nivel:** Bajo 1–4; Medio 5–9; Alto 10–16; Crítico 17–25.
- **Respuesta:** evitar, mitigar, transferir o aceptar.
- **Riesgo residual:** nivel esperado después de la mitigación, sujeto a evidencia.
- **Dueño:** rol accountable por el seguimiento.

### 1.1 Escala de impacto

| Nivel | Cliente | Operación | Regulatorio | Económico | Reputación |
|---|---|---|---|---|---|
| 1 | Molestia menor | Sin interrupción | Sin hallazgo | < USD 1.000 | Interno |
| 2 | Reclamo simple | Retraso < 1 h | Observación menor | USD 1.000–10.000 | Local |
| 3 | Reclamo formal | Retraso < 1 día | Hallazgo corregible | USD 10.000–100.000 | Regional |
| 4 | Pérdida de fondos | Interrupción > 1 día | Sanción/requerimiento | USD 100.000–1 M | Nacional |
| 5 | Daño sistémico | Interrupción crítica | Sanción grave | > USD 1 M | Nacional/internacional |

> Los rangos económicos son parámetros del caso, no valores reales.

### 1.2 Apetito de riesgo

NovaBank acepta riesgos **bajos** sin escalamiento; los **medios** requieren plan de tratamiento; los **altos** requieren aprobación de Riesgos; los **críticos** requieren aprobación del Sponsor y un plan con fecha. Ningún riesgo crítico puede quedar sin dueño ni sin evidencia de avance.

---

## 2. Mapa de calor

| P \ I | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **5** | 5 | 10 | 15 | 20 | 25 |
| **4** | 4 | 8 | 12 | 16 | 20 |
| **3** | 3 | 6 | 9 | 12 | 15 |
| **2** | 2 | 4 | 6 | 8 | 10 |
| **1** | 1 | 2 | 3 | 4 | 5 |

**Leyenda:** Bajo (1–4), Medio (5–9), Alto (10–16), Crítico (17–25).

---

## 3. Registro principal

| ID | Categoría | Riesgo | Causa | Efecto | P | I | Score | Nivel | Respuesta | Mitigación | Dueño | Residual |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R-01 | Cumplimiento | Interpretación errónea de las reglas del SPI y de SEPRELAD. | Lectura parcial de normativa, fuentes contradictorias o desactualizadas. | Diseño no conforme, sanciones, reprocesos. | 4 | 5 | 20 | Crítico | Mitigar | Validar con Cumplimiento/Legal, registrar fuentes y supuestos, revisión por especialista. | Cumplimiento | 8 (Medio) |
| R-02 | Fraude | Suplantación o ingeniería social en pagos instantáneos. | Irreversibilidad del SPI y velocidad de la operación. | Pérdida de fondos del cliente, reclamos, daño reputacional. | 4 | 5 | 20 | Crítico | Mitigar | Confirmación de beneficiario, límites, scoring, fricción selectiva, educación y monitoreo. | Riesgos | 10 (Alto) |
| R-03 | Cumplimiento | Falsos positivos bloquean clientes legítimos. | Reglas y listas mal calibradas. | Mala experiencia, abandono, carga operativa. | 4 | 3 | 12 | Alto | Mitigar | Calibración, revisión humana, métricas de falsos positivos, feedback loop. | Cumplimiento | 6 (Medio) |
| R-04 | Tecnología | Indisponibilidad de SPI, SWIFT, core o proveedor. | Falla de infraestructura, red o tercero. | Pagos detenidos, SLA incumplido, pérdida de confianza. | 3 | 5 | 15 | Alto | Mitigar/Transferir | Alta disponibilidad, reintentos, colas, monitoreo, plan de continuidad y SLA con proveedor. | TI | 8 (Medio) |
| R-05 | Operación | Pago duplicado por reintentos sin idempotencia. | Timeout con respuesta desconocida. | Doble débito, pérdida económica, reclamos. | 3 | 5 | 15 | Alto | Evitar/Mitigar | Clave de idempotencia, máquina de estados, conciliación y reversa controlada. | TI/Operaciones | 6 (Medio) |
| R-06 | Seguridad | Brecha de datos personales o información AML. | Acceso indebido, error de configuración o proveedor. | Sanción, daño reputacional, riesgo para clientes. | 2 | 5 | 10 | Alto | Mitigar | Mínimo privilegio, cifrado, enmascaramiento, auditoría, pruebas de seguridad. | Seguridad | 5 (Medio) |
| R-07 | Terceros | Dependencia crítica de un proveedor de mensajería/screening. | Concentración y baja sustituibilidad. | Interrupción o costo elevado. | 3 | 4 | 12 | Alto | Mitigar/Transferir | SLA, plan de contingencia, cláusulas de salida, monitoreo. | TI/Cumplimiento | 8 (Medio) |
| R-08 | Adopción | Baja adopción por clientes y sucursales. | Poca comunicación, usabilidad deficiente o hábitos. | No se alcanzan beneficios. | 3 | 3 | 9 | Medio | Mitigar | Campaña, capacitación, piloto, métricas de adopción. | Producto | 4 (Bajo) |
| R-09 | Cumplimiento | Falla de screening en pagos internacionales. | Campos incompletos, listas desactualizadas o reglas mal aplicadas. | Operación con contraparte sancionada, sanción regulatoria. | 2 | 5 | 10 | Alto | Mitigar | Validación obligatoria, listas versionadas, doble control y evidencia. | Cumplimiento | 5 (Medio) |
| R-10 | Tecnología | Rechazo o reparación de mensajes ISO 20022. | Mapeo incorrecto, campos faltantes o versión de esquema. | Retraso, costo operativo, pérdida de STP. | 4 | 3 | 12 | Alto | Mitigar | Validador, catálogo de campos, pruebas de contrato, monitoreo de rechazos. | TI | 6 (Medio) |
| R-11 | Contabilidad | Diferencias de conciliación. | Desfase entre riel, core y libro mayor. | Ajustes manuales, reportes inexactos. | 3 | 4 | 12 | Alto | Mitigar | Partida doble, conciliación automática, cola de diferencias y cierre diario. | Contabilidad | 6 (Medio) |
| R-12 | Cumplimiento | Acumulación de alertas sin investigar. | Volumen, reglas ruidosas o falta de analistas. | Riesgo no atendido, SLA incumplido, sanción. | 4 | 4 | 16 | Alto | Mitigar | Priorización, capacidad, SLA, tablero y escalamiento. | Monitoreo AML | 8 (Medio) |
| R-13 | Modelo | Deriva de reglas/scoring. | Cambios de comportamiento o falta de recalibración. | Detección ineficaz o falsos positivos. | 4 | 3 | 12 | Alto | Mitigar | Revisión periódica, métricas, pruebas de regresión y gobierno de cambios. | Riesgos | 6 (Medio) |
| R-14 | Fraude interno | Uso indebido de acceso a información o pagos. | Privilegios excesivos o falta de segregación. | Pérdida, fuga de datos, sanción. | 2 | 5 | 10 | Alto | Mitigar | Segregación de funciones, revisión de accesos, logs y monitoreo. | Seguridad/Auditoría | 4 (Bajo) |
| R-15 | Personas | Falta de capacitación en nuevos procesos. | Cambio de herramientas y roles. | Errores, excepciones, mala atención. | 3 | 3 | 9 | Medio | Mitigar | Plan de capacitación, manuales, acompañamiento y evaluación. | Operaciones | 4 (Bajo) |
| R-16 | Proyecto | Scope creep. | Nuevos pedidos sin control de cambios. | Retraso, sobrecosto, baja calidad. | 4 | 3 | 12 | Alto | Mitigar | Alcance explícito, comité, control de cambios y MoSCoW. | Producto | 6 (Medio) |
| R-17 | Auditoría | Evidencia incompleta. | Logs dispersos o decisiones no registradas. | Hallazgo, imposibilidad de demostrar control. | 3 | 4 | 12 | Alto | Mitigar | Trazabilidad por diseño, retención, pruebas de evidencia y revisión. | BA/Auditoría | 5 (Medio) |
| R-18 | Comunicación | Información incorrecta al cliente sobre estado o plazo. | Estados inconsistentes o guiones desactualizados. | Reclamos, desconfianza, contacto repetido. | 3 | 3 | 9 | Medio | Mitigar | Fuente única de estado, guion, notificaciones y monitoreo de reclamos. | Atención al Cliente | 4 (Bajo) |
| R-19 | Operación | Devolución fuera de plazo. | Proceso manual o falta de seguimiento. | Incumplimiento, reclamo, pérdida. | 3 | 3 | 9 | Medio | Mitigar | Cronómetro, alertas, responsable y reporte. | Operaciones | 4 (Bajo) |
| R-20 | Proveedor | Incumplimiento de SLA de screening. | Capacidad o disponibilidad del proveedor. | Bloqueo de pagos o evaluación tardía. | 2 | 4 | 8 | Medio | Transferir/Mitigar | SLA, monitoreo, contingencia y revisión contractual. | Cumplimiento | 4 (Bajo) |

---

## 4. Top 5 riesgos y señales tempranas

| ID | Riesgo | Señal temprana | Umbral | KPI relacionado |
|---|---|---|---|---|
| R-01 | Interpretación normativa | Cambio de norma, observación de Cumplimiento, discrepancia de fuentes. | Cualquier cambio no evaluado | — |
| R-02 | Fraude instantáneo | Aumento de reclamos por suplantación; patrones anómalos. | +20 % semanal | K-14 |
| R-04 | Indisponibilidad | Caída de disponibilidad o latencia. | < 99,95 % / > 8 s | K-01, K-02 |
| R-05 | Duplicidad | Aumento de reversas o diferencias. | > 0,1 % de pagos | K-17 |
| R-12 | Backlog de alertas | Cola creciente y SLA en riesgo. | > 50 casos o < 90 % a tiempo | K-09, K-10 |

---

## 5. Planes de respuesta

### 5.1 R-01 — Interpretación normativa

- **Acción inmediata:** congelar decisiones que dependan de la norma no verificada.
- **Validación:** revisión con Cumplimiento y Legal; registrar fuente, fecha y alcance.
- **Criterio de cierre:** dictamen documentado y requisitos actualizados.
- **Contingencia:** si no hay dictamen, mantener el flujo en modo piloto controlado y no exponer clientes reales.

### 5.2 R-02 — Fraude instantáneo

- **Prevención:** scoring, límites, confirmación de beneficiario y fricción selectiva.
- **Detección:** reglas de velocidad, dispositivo, geografía y contraparte.
- **Respuesta:** bloqueo preventivo, contacto con el cliente, investigación y reclamo.
- **Criterio de cierre:** caso resuelto, pérdida contenida y regla ajustada.

### 5.3 R-04 — Indisponibilidad

- **Prevención:** arquitectura redundante, monitoreo y pruebas de carga.
- **Respuesta:** activar plan de continuidad, comunicación y reintentos.
- **Criterio de cierre:** servicio restablecido, causa raíz identificada y acción correctiva.

### 5.4 R-05 — Duplicidad

- **Prevención:** idempotencia y máquina de estados.
- **Detección:** conciliación y alertas de reversa.
- **Respuesta:** identificar, reversar y notificar.
- **Criterio de cierre:** sin duplicados en 30 días y prueba de regresión.

### 5.5 R-12 — Backlog AML

- **Prevención:** calibración de reglas y capacidad.
- **Detección:** cola, edad y SLA.
- **Respuesta:** reasignación, priorización y escalamiento.
- **Criterio de cierre:** SLA ≥ 95 % durante 4 semanas.

---

## 6. Riesgo residual y aceptación

| ID | Residual | Aceptable | Aprobador | Condición |
|---|---|---|---|---|
| R-01 | Medio | Sí, con dictamen | Sponsor/Riesgos | Dictamen legal documentado. |
| R-02 | Alto | Sí, con controles | Sponsor/Riesgos | Controles implementados y monitoreados. |
| R-03 | Medio | Sí | Cumplimiento | Métricas de falsos positivos. |
| R-04 | Medio | Sí | TI | Plan de continuidad probado. |
| R-05 | Medio | Sí | TI/Operaciones | Idempotencia validada. |
| R-06 | Medio | Sí | Seguridad | Pruebas y revisión. |
| R-07 | Medio | Sí | TI | SLA y contingencia. |
| R-12 | Medio | Sí | Cumplimiento | Capacidad y SLA. |
| Otros | Bajo/Medio | Sí | Dueño | Plan vigente. |

> La aceptación es ficticia y forma parte del ejercicio. No constituye aprobación real de riesgo.

---

## 7. Gobernanza y revisión

- **Frecuencia:** revisión quincenal en comité de proyecto; mensual en comité de riesgos.
- **Disparadores:** incidente, cambio normativo, cambio de alcance, falla de proveedor o desvío de KPI.
- **Registro:** cada cambio de estado, score o dueño se documenta con fecha.
- **Evidencia:** planes, pruebas, actas y capturas en `docs/EVIDENCIAS.md`.
- **Cierre:** un riesgo se cierra cuando la causa se elimina o el residual es aceptado con evidencia.

---

## 8. Trazabilidad

| Riesgo | Requerimiento | Proceso | KPI |
|---|---|---|---|
| R-01 | BR-01, BR-05, BR-10 | Todos | K-07, K-12 |
| R-02 | BR-07, BR-08 | Local TO-BE, Alerta AML | K-09, K-14 |
| R-03 | BR-07, BR-08 | Alerta AML | K-11 |
| R-04 | NFR-01, NFR-07 | Local/internacional | K-02 |
| R-05 | BR-15 | Local/internacional | K-17 |
| R-06 | NFR-03, NFR-10 | Transversal | K-16 |
| R-07 | D-02, D-04 | Internacional/Alerta | K-05, K-09 |
| R-08 | O-05 | Canales | K-13 |
| R-09 | BR-07 | Internacional | K-07 |
| R-10 | BR-06 | Internacional | K-06 |
| R-11 | BR-11 | Contabilidad | K-17 |
| R-12 | BR-09 | Alerta AML | K-09, K-10 |
| R-13 | BR-08 | Monitoreo | K-11 |
| R-14 | BR-12 | Transversal | K-16 |
| R-15 | BR-14 | Operación | K-03 |
| R-16 | — | Proyecto | — |
| R-17 | BR-12 | Transversal | K-16 |
| R-18 | BR-03, BR-16 | Atención | K-14 |
| R-19 | BR-04 | Local TO-BE | K-14 |
| R-20 | BR-07 | Screening | K-07 |

---

## 9. Referencias

- `BRD.md` — objetivos y requerimientos.
- `stakeholders.md` — dueños y gobernanza.
- `kpis.md` — métricas de seguimiento.
- `contexto-regulatorio.md` — marco normativo.
- `docs/PENDIENTES.md` — brechas que afectan riesgos.
