# Acta 2026-10-20 — Kickoff del programa NovaPay

**Página:** Acta de reunión (simulada)  
**Fecha:** 2026-10-20  
**Hora:** 09:00–10:30 (America/Asuncion)  
**Modalidad:** Remota (ficticia)  
**Facilitador:** BA  
**Estado:** Cerrada

> Acta simulada del caso ficticio. Solo se usan roles, no nombres de personas reales. Las decisiones son de diseño y no constituyen aprobación formal de ninguna entidad.

---

## 1. Asistentes

| Rol | Área | Asistencia |
|---|---|---|
| Sponsor | Gerencia de Banca Minorista | Sí |
| Product Owner | Producto — Pagos | Sí |
| Business Analyst | Análisis funcional | Sí |
| Gerente de Operaciones | Operaciones | Sí |
| Arquitecto de Soluciones | TI — Arquitectura | Sí |
| Oficial de Cumplimiento | Cumplimiento / AML | Sí |
| Gerente de Riesgos | Riesgos | Sí |
| Contralor | Contabilidad | Sí |
| Auditor Interno | Auditoría | Ausente con aviso |

---

## 2. Agenda

1. Contexto del programa y problema de negocio.
2. Alcance, exclusiones y objetivos medibles.
3. Principios de arquitectura y gobierno.
4. Riesgos iniciales y dependencias.
5. Próximos pasos y responsables.

---

## 3. Resumen de la discusión

- El Sponsor confirmó que el programa busca pagos instantáneos locales, cross-border saliente y control AML integrado, sin reemplazar el core.
- Operaciones describió el AS-IS: validaciones manuales, procesos por lote y estados inconsistentes.
- Cumplimiento enfatizó que el screening debe ocurrir antes de liberar el pago y que toda decisión debe quedar auditada.
- TI advirtió que los rieles y proveedores cambian; se necesita un orquestador con adaptadores y contratos estables.
- Riesgos pidió idempotencia y control de duplicados desde el primer diseño.
- Se acordó priorizar un MVP demostrable en dos sprints, con historias `Must` y dependencias resueltas.

---

## 4. Decisiones

| ID | Decisión | Referencia |
|---|---|---|
| D-01 | Adoptar un orquestador central de pagos con adaptadores al core y a los rieles. | ADR-001 |
| D-02 | Adoptar idempotencia y máquina de estados para pagos reintentables. | ADR-002 |
| D-03 | Priorizar el backlog con MoSCoW y planificar dos sprints de 2 semanas. | `planificacion-sprints.md` |
| D-04 | El screening y el scoring se ejecutan antes de liberar fondos. | BR-07, US-016 |
| D-05 | Los umbrales y reglas AML son parámetros sujetos a aprobación de Riesgos y Cumplimiento. | SNV-04 |
| D-06 | No se usan datos reales ni listas reales de sanciones/PEP. | S-018, ADR-006 |

---

## 5. Acciones

| ID | Acción | Dueño | Fecha | Estado |
|---|---|---|---|---|
| A-01 | Documentar contexto, alcance y objetivos en el BRD. | BA | 2026-10-21 | Cerrada |
| A-02 | Modelar procesos AS-IS/TO-BE y decisiones DMN. | BA / TI | 2026-10-24 | Cerrada |
| A-03 | Definir principios de arquitectura e idempotencia. | TI — Arquitectura | 2026-10-22 | Cerrada |
| A-04 | Revisar requisitos de screening y ROS. | Cumplimiento | 2026-10-24 | En curso |
| A-05 | Identificar riesgos y dependencias iniciales. | Riesgos / BA | 2026-10-23 | Cerrada |
| A-06 | Preparar backlog de épicas e historias. | BA / Producto | 2026-10-27 | Cerrada |

---

## 6. Riesgos y dependencias destacados

- R-01: interpretación normativa de SPI/SEPRELAD.
- R-02: fraude o suplantación en pagos instantáneos.
- R-04: indisponibilidad de SPI/SWIFT/core.
- R-05: duplicidad por reintentos.
- D-01: participación/certificación en SPI.
- D-02: conectividad SWIFT y corresponsalía.
- D-03: API del core para cuentas y saldos.

---

## 7. Próxima reunión

**Fecha:** 2026-10-22  
**Tema:** taller de requerimientos, mensajería ISO 20022 y reglas de decisión.

---

## 8. Referencias

- `../../../01-negocio/BRD.md`
- `../../../02-procesos/mapa-procesos.md`
- `../02-decisiones/adr-001-orquestacion-pagos.md`
- `../02-decisiones/adr-002-idempotencia-estados.md`
- `../05-raid-log.md`

**Fin del acta.**
