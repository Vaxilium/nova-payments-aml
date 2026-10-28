# Acta 2026-10-27 — Refinamiento y cierre de Fase 2

**Página:** Acta de reunión (simulada)  
**Fecha:** 2026-10-27  
**Hora:** 10:00–12:00 (America/Asuncion)  
**Modalidad:** Remota (ficticia)  
**Facilitador:** BA  
**Estado:** Cerrada

> Acta simulada del caso ficticio. Solo se usan roles, no nombres de personas reales. Las aprobaciones son parte del ejercicio y no constituyen aprobación formal de ninguna entidad.

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
| Auditor Interno | Auditoría | Sí |

---

## 2. Agenda

1. Revisión del backlog y de la Definition of Ready.
2. Planificación de Sprint 1 y Sprint 2.
3. Revisión de NFR y trazabilidad.
4. RAID log y pendientes de evidencia.
5. Cierre de Fase 2 y próximos pasos.

---

## 3. Resumen de la discusión

- Producto confirmó que el MVP de dos sprints debe demostrar pago local, cross-border, monitoreo/alertas y contabilidad base.
- El equipo revisó las 40 historias y confirmó que 26 son `Must`, 12 `Should` y 2 `Could`.
- Se acordó que Sprint 1 (47 SP) cubra alta, identidad, screening, pago local, estado, límites, evaluación de riesgo, autenticación y eventos.
- Se acordó que Sprint 2 (52 SP) cubra validación ISO 20022, pacs.008/pacs.002, monitoreo, alertas, partida doble e idempotencia.
- Cumplimiento advirtió que los umbrales y listas siguen siendo parámetros ficticios y deben validarse antes de producción.
- Auditoría pidió que la bitácora sea append-only y que la evidencia de prueba quede vinculada a la matriz de trazabilidad.
- Se revisó el RAID log y se mantuvieron abiertos los pendientes de fuentes normativas y evidencias de herramientas.
- Se acordó cerrar Fase 2 con los artefactos del repositorio y dejar EV-001, EV-002 y EV-003 para acción manual del autor.

---

## 4. Decisiones

| ID | Decisión | Referencia |
|---|---|---|
| D-14 | Aprobar el backlog de 40 historias / 198 SP como base del producto. | `historias-usuario.md` |
| D-15 | Comprometer Sprint 1 con 10 historias / 47 SP y Sprint 2 con 9 historias / 52 SP. | `planificacion-sprints.md` |
| D-16 | Adoptar la bitácora append-only con correlación. | ADR-005 |
| D-17 | Adoptar datos sintéticos con semilla fija y simuladores de rieles. | ADR-006 |
| D-18 | Mantener los IDs `TC-001` a `TC-040` reservados para Fase 7. | `matriz-trazabilidad.csv` |
| D-19 | No publicar enlaces de Jira, Confluence o Azure DevOps hasta que existan y el autor los cree. | S-008, `docs/EVIDENCIAS.md` |
| D-20 | Cerrar Fase 2 con evidencia manual pendiente y registrar el estado en `PLAN.md`. | `PLAN.md` |

---

## 5. Acciones

| ID | Acción | Dueño | Fecha | Estado |
|---|---|---|---|---|
| A-13 | Importar CSV a Jira y capturar backlog/tablero. | Autor | Fase 2 | Pendiente (EV-001) |
| A-14 | Crear espacio Confluence y pegar páginas. | Autor | Fase 2 | Pendiente (EV-002) |
| A-15 | Importar work items a Azure DevOps. | Autor | Fase 2 | Pendiente (EV-003) |
| A-16 | Validar umbrales AML con Riesgos/Cumplimiento. | Cumplimiento | Antes de Fase 5 | Pendiente (P-011) |
| A-17 | Verificar fuentes normativas primarias de SIPAP/SEPRELAD. | Cumplimiento / BA | Fase 4/5 | Pendiente (P-003, P-009) |
| A-18 | Preparar dataset sintético y seed. | TI — Datos / BA | Fase 3 | Pendiente |
| A-19 | Implementar API y libro mayor. | TI | Fase 3 | Pendiente |

---

## 6. RAID y pendientes

- **Riesgos abiertos:** R-01, R-02, R-04, R-09, R-10, R-12, R-16, R-17.
- **Supuestos no verificados:** SNV-01 a SNV-08.
- **Issues:** listas ficticias incompletas, umbrales sin aprobación, corresponsal simulado, dataset pendiente.
- **Dependencias:** SPI, SWIFT, core, screening, datos sintéticos, aprobación de umbrales.
- **Evidencias manuales:** EV-001, EV-002, EV-003.

---

## 7. Próxima reunión

**Fecha:** 2026-11-02  
**Tema:** Sprint 1 planning y validación del dataset sintético.

---

## 8. Referencias

- `../../epicas.md`
- `../../historias-usuario.md`
- `../../planificacion-sprints.md`
- `../../matriz-trazabilidad.csv`
- `../02-decisiones/adr-005-auditoria-correlacion.md`
- `../02-decisiones/adr-006-datos-sinteticos-simulacion.md`
- `../05-raid-log.md`
- `../../../docs/EVIDENCIAS.md`
- `../../../docs/PENDIENTES.md`

**Fin del acta.**
