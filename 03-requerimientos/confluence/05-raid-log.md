# RAID log — NovaPay

**Página:** RAID log  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Dueño:** BA / Producto  
**Estado:** Activo

> Registro consolidado de **R**iesgos, **A**ssumptions (supuestos), **I**ssues y **D**ependencias del caso ficticio. No reemplaza el registro detallado de riesgos (`01-negocio/riesgos.md`) ni el registro de supuestos (`docs/SUPUESTOS.md`).

---

## 1. Resumen

| Categoría | Abiertos | En seguimiento / vigentes | Cerrados |
|---|---:|---:|---:|
| Riesgos | 8 | 12 | 0 |
| Supuestos | 6 | 6 | 0 |
| Issues | 4 | 1 | 0 |
| Dependencias | 10 | 0 | 0 |

---

## 2. Riesgos (R)

| ID | Riesgo | P | I | Nivel | Respuesta | Dueño | Estado | Próximo paso |
|---|---|---|---|---|---|---|---|---|
| R-01 | Interpretación errónea de SPI/SEPRELAD. | 4 | 5 | Crítico | Mitigar | Cumplimiento | Abierto | Validar fuentes y dictamen (P-003, P-009). |
| R-02 | Fraude o suplantación en pagos instantáneos. | 4 | 5 | Crítico | Mitigar | Riesgos | Abierto | Confirmación de beneficiario, límites y monitoreo. |
| R-03 | Falsos positivos bloquean clientes legítimos. | 4 | 3 | Alto | Mitigar | Cumplimiento | En seguimiento | Calibrar reglas y medir K-11. |
| R-04 | Indisponibilidad de SPI, SWIFT, core o proveedor. | 3 | 5 | Alto | Mitigar/Transferir | TI | Abierto | Plan de continuidad y monitoreo. |
| R-05 | Duplicidad por reintentos sin idempotencia. | 3 | 5 | Alto | Evitar/Mitigar | TI/Operaciones | En seguimiento | Implementar y probar NFR-05. |
| R-06 | Brecha de datos personales o información AML. | 2 | 5 | Alto | Mitigar | Seguridad | En seguimiento | Revisión de accesos y enmascaramiento. |
| R-07 | Dependencia crítica de proveedor de mensajería/screening. | 3 | 4 | Alto | Mitigar/Transferir | TI/Cumplimiento | En seguimiento | SLA y plan de contingencia. |
| R-08 | Baja adopción por clientes y sucursales. | 3 | 3 | Medio | Mitigar | Producto | En seguimiento | Campaña y piloto. |
| R-09 | Falla de screening en pagos internacionales. | 2 | 5 | Alto | Mitigar | Cumplimiento | Abierto | Validación obligatoria y doble control. |
| R-10 | Rechazo o reparación de mensajes ISO 20022. | 4 | 3 | Alto | Mitigar | TI | Abierto | Validador y catálogo de campos (Fase 4). |
| R-11 | Diferencias de conciliación. | 3 | 4 | Alto | Mitigar | Contabilidad | En seguimiento | Partida doble y conciliación diaria. |
| R-12 | Acumulación de alertas sin investigar. | 4 | 4 | Alto | Mitigar | Monitoreo AML | Abierto | Priorización, capacidad y SLA. |
| R-13 | Deriva de reglas/scoring. | 4 | 3 | Alto | Mitigar | Riesgos | En seguimiento | Revisión periódica y pruebas de regresión. |
| R-14 | Uso indebido de acceso a información o pagos. | 2 | 5 | Alto | Mitigar | Seguridad/Auditoría | En seguimiento | Segregación y revisión de accesos. |
| R-15 | Falta de capacitación en nuevos procesos. | 3 | 3 | Medio | Mitigar | Operaciones | En seguimiento | Plan de capacitación. |
| R-16 | Scope creep. | 4 | 3 | Alto | Mitigar | Producto | Abierto | MoSCoW y control de cambios. |
| R-17 | Evidencia incompleta. | 3 | 4 | Alto | Mitigar | BA/Auditoría | Abierto | Trazabilidad y pruebas de evidencia. |
| R-18 | Información incorrecta al cliente sobre estado/plazo. | 3 | 3 | Medio | Mitigar | Atención | En seguimiento | Fuente única de estado y guion. |
| R-19 | Devolución fuera de plazo. | 3 | 3 | Medio | Mitigar | Operaciones | En seguimiento | Cronómetro y responsable. |
| R-20 | Incumplimiento de SLA de screening. | 2 | 4 | Medio | Transferir/Mitigar | Cumplimiento | En seguimiento | SLA y contingencia. |

**Top 5:** R-01, R-02, R-04, R-05, R-12. Ver `01-negocio/riesgos.md` para el detalle y los planes de respuesta.

---

## 3. Supuestos (A)

| ID | Supuesto | Impacto si no se cumple | Dueño | Estado | Referencia |
|---|---|---|---|---|---|
| SNV-01 | SPI 24/7, PYG, tope ₲10.000.000 y acreditación ≤ 5 s. | Cambia el diseño del canal y los SLA. | Cumplimiento | Abierto | P-006 |
| SNV-02 | Resolución SEPRELAD aplicable a bancos es consistente con el enfoque de ROS/PEP. | Diseño no conforme. | Cumplimiento | Abierto | P-009 |
| SNV-03 | La lista de países de alto riesgo es ficticia e inspirada en categorías GAFI. | Screening no representativo. | Cumplimiento | Abierto | P-010 |
| SNV-04 | Los umbrales de revisión y aprobación son adecuados al apetito. | Falsos positivos o exposición. | Riesgos | Abierto | P-011 |
| SNV-05 | El ROS se activa con independencia del monto y dentro de plazos internos. | Reporte tardío o incompleto. | Cumplimiento | Abierto | P-009 |
| SNV-06 | ISO 20022 es obligatorio para cross-border desde el fin de la coexistencia. | Mensajería no conforme. | TI | Abierto | P-008 |
| S-017 | NovaBank ya tiene core, libro mayor y canal digital. | Cambia el alcance de TI. | TI | Vigente | S-017 |
| S-045 | NovaBank será participante o subparticipante del SPI. | Sin canal local directo. | Operaciones | Vigente | D-01 |
| S-016 | La conexión SWIFT se simula con un adaptador. | Mayor esfuerzo de integración. | TI | Vigente | ADR-003 |
| S-018 | Listas de sanciones/PEP y países de alto riesgo son ficticias. | Cambia screening y privacidad. | Cumplimiento | Vigente | S-018 |
| S-028 | Existe oficial de cumplimiento y analistas AML. | Flujo de alertas sin responsables. | Cumplimiento | Vigente | S-028 |
| S-010 | Datos sintéticos con semilla fija. | Se pierde reproducibilidad. | BA/Datos | Vigente | S-010 |

---

## 4. Issues (I)

| ID | Issue | Impacto | Dueño | Estado | Próximo paso |
|---|---|---|---|---|---|
| I-01 | Las listas ficticias de sanciones/PEP aún no tienen dataset mínimo para los sprints. | Alto | Cumplimiento / Datos | Abierto | Definir dataset antes del 2026-11-02. |
| I-02 | Los umbrales de los DMN no están aprobados por Riesgos/Cumplimiento. | Alto | Riesgos | Abierto | Taller de validación (P-011). |
| I-03 | El corresponsal simulado no tiene contrato de respuesta pacs.002 definido. | Alto | TI — Integración | Abierto | Definir catálogo de estados en Fase 4. |
| I-04 | El dataset sintético de clientes/cuentas aún no existe. | Medio | TI — Datos | Abierto | Implementar seed en Fase 3. |
| I-05 | Las evidencias de Jira/Confluence/ADO dependen de acción manual del autor. | Medio | Autor | En seguimiento | Ejecutar EV-001, EV-002, EV-003. |

---

## 5. Dependencias (D)

| ID | Dependencia | Dueño | Impacto | Estado | Próximo paso |
|---|---|---|---|---|---|
| D-01 | Participación/certificación en SPI. | Operaciones / BCP | Sin canal local. | Abierto | Confirmar estatus ficticio. |
| D-02 | Conectividad SWIFT y acuerdo de corresponsalía. | TI / Tesorería | Sin canal internacional. | Abierto | Usar adaptador simulado. |
| D-03 | Core bancario y API de cuentas. | TI / Core | Sin débito/consulta de saldo. | Abierto | Definir contrato de adaptador. |
| D-04 | Herramienta de screening y listas. | Cumplimiento | Sin control de sanciones/PEP. | Abierto | Dataset ficticio y motor. |
| D-05 | Motor de reglas y monitoreo. | Riesgos / TI | Sin detección oportuna. | Abierto | DMN y reglas SQL. |
| D-06 | Disponibilidad de datos sintéticos. | BA / Datos | Sin pruebas reproducibles. | Abierto | Seed de Fase 3. |
| D-07 | Aprobación de umbrales y apetito de riesgo. | Riesgos / Cumplimiento | Reglas sin legitimidad. | Abierto | Taller y acta. |
| D-08 | Validación legal de normativa. | Legal / Cumplimiento | Diseño no conforme. | Abierto | Dictamen (P-003, P-009). |
| D-09 | Infraestructura de observabilidad. | TI | Sin evidencia de SLA. | Abierto | Definir en Fase 3/7. |
| D-10 | Plan de comunicación y capacitación. | Negocio / RRHH | Baja adopción y errores. | Abierto | Plan de Fase 7. |

---

## 6. Reglas de actualización

1. El RAID se revisa en cada comité quincenal y al cierre de cada sprint.
2. Un riesgo se cierra cuando la causa se elimina o el residual es aceptado con evidencia.
3. Un supuesto se cierra cuando se verifica con fuente oficial o se reemplaza por una decisión.
4. Un issue se cierra cuando existe una acción verificable, no solo una intención.
5. Una dependencia se cierra cuando el proveedor o área confirma la entrega.
6. Todo cambio se registra con fecha, dueño y evidencia.

---

## 7. Referencias

- `../../../01-negocio/riesgos.md` — registro completo de riesgos.
- `../../../docs/SUPUESTOS.md` — supuestos y decisiones.
- `../../../docs/PENDIENTES.md` — pendientes y bloqueos.
- `../../../docs/EVIDENCIAS.md` — evidencias manuales.
- `../../planificacion-sprints.md` — sprints y capacidad.
- `../02-decisiones/README.md` — ADR.

**Fin de la página.**
