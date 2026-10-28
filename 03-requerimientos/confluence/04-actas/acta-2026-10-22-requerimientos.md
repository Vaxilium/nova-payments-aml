# Acta 2026-10-22 — Taller de requerimientos y mensajería

**Página:** Acta de reunión (simulada)  
**Fecha:** 2026-10-22  
**Hora:** 14:00–16:00 (America/Asuncion)  
**Modalidad:** Remota (ficticia)  
**Facilitador:** BA  
**Estado:** Cerrada

> Acta simulada del caso ficticio. Solo se usan roles, no nombres de personas reales.

---

## 1. Asistentes

| Rol | Área | Asistencia |
|---|---|---|
| Product Owner | Producto — Pagos | Sí |
| Business Analyst | Análisis funcional | Sí |
| Gerente de Operaciones Internacionales | Operaciones Intl. | Sí |
| Arquitecto de Integración | TI — Integración de Pagos | Sí |
| Oficial de Cumplimiento | Cumplimiento / AML | Sí |
| Gerente de Riesgos | Riesgos | Sí |
| Analista de Datos | TI — Datos | Sí |

---

## 2. Agenda

1. Requerimientos de pagos locales e internacionales.
2. Modelo ISO 20022 y seguimiento de estados.
3. Reglas de decisión para riesgo y priorización.
4. NFR críticos: rendimiento, idempotencia, auditoría y conciliación.
5. Estimación inicial y dependencias.

---

## 3. Resumen de la discusión

- Operaciones Internacionales confirmó que el flujo saliente debe validar IBAN/BIC, moneda e importe antes de generar el mensaje.
- TI propuso un modelo canónico y un adaptador SWIFT simulado; el `UETR` será la clave de seguimiento.
- Cumplimiento pidió que la decisión de screening registre la versión de la lista y el motivo.
- Riesgos pidió que la priorización de alertas sea determinista y que los umbrales sean configurables.
- Se acordó que la idempotencia cubra creación de pago, envío internacional, devolución y reclamo.
- Se discutió el p95 de acreditación local (≤ 5 s) y el p95 de scoring (≤ 2 s) como objetivos de diseño.
- El equipo estimó el backlog en 40 historias / 198 SP; el MVP de dos sprints cubre 19 historias / 99 SP.

---

## 4. Decisiones

| ID | Decisión | Referencia |
|---|---|---|
| D-07 | Adoptar un modelo canónico ISO 20022 con `pacs.008`/`pacs.002` y adaptador simulado. | ADR-003 |
| D-08 | Usar DMN para scoring, ruteo, prioridad de alertas y límites. | ADR-004 |
| D-09 | Validar IBAN/BIC con formato y checksum; no consultar directorios reales. | S-026 |
| D-10 | Adoptar NFR de disponibilidad 99,9 %, p95 local ≤ 5 s y p95 scoring ≤ 2 s. | `requerimientos-no-funcionales.md` |
| D-11 | La idempotencia se aplica a toda API que crea o modifica recursos. | NFR-05 |
| D-12 | La prioridad P1 tiene SLA de asignación de 15 minutos. | US-018, K-09 |
| D-13 | El ROS es ficticio y no se envía a SEPRELAD. | E-06, US-023 |

---

## 5. Acciones

| ID | Acción | Dueño | Fecha | Estado |
|---|---|---|---|---|
| A-07 | Documentar catálogo de campos ISO 20022 y mapeo MT103. | TI — Integración / BA | Fase 4 | Pendiente |
| A-08 | Ajustar DMN de prioridad y límites con Riesgos/Cumplimiento. | BA / Riesgos | 2026-10-27 | Cerrada |
| A-09 | Definir umbrales iniciales y marcarlos como parámetros. | Riesgos / Cumplimiento | 2026-10-27 | En curso |
| A-10 | Especificar NFR y criterios de verificación. | BA / TI | 2026-10-28 | Cerrada |
| A-11 | Preparar CSV de Jira y Azure DevOps. | BA | 2026-10-28 | Cerrada |
| A-12 | Definir dataset sintético mínimo para los sprints. | TI — Datos / BA | 2026-11-02 | Pendiente |

---

## 6. Riesgos y dependencias destacados

- R-10: rechazo o reparación de mensajes ISO 20022.
- R-09: falla de screening en pagos internacionales.
- R-13: deriva de reglas/scoring.
- D-02: conectividad SWIFT y corresponsalía.
- D-04: herramienta de screening y listas.
- D-06: disponibilidad de datos sintéticos.

---

## 7. Próxima reunión

**Fecha:** 2026-10-27  
**Tema:** refinamiento del backlog, planificación de sprints y RAID log.

---

## 8. Referencias

- `../../historias-usuario.md`
- `../../requerimientos-no-funcionales.md`
- `../02-decisiones/adr-003-modelo-iso20022.md`
- `../02-decisiones/adr-004-motor-decisiones-riesgo.md`
- `../05-raid-log.md`

**Fin del acta.**
