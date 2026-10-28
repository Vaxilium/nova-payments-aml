# NovaBank — Payments & AML

**Espacio:** NovaBank  
**Página:** Inicio  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Dueño:** Producto — Pagos  
**Estado:** Borrador para revisión ficticia

> Caso 100 % ficticio. NovaBank, sus clientes, cuentas, BIC e IBAN son inventados. Las referencias a BCP, SEPRELAD, GAFI, SWIFT e ISO 20022 son públicas y se usan solo como contexto normativo/técnico.

---

## 1. Propósito del espacio

Concentrar el conocimiento funcional del programa **NovaPay**: pagos instantáneos locales, pagos internacionales ISO 20022 y monitoreo AML. Es la fuente de consulta para Producto, Operaciones, TI, Riesgos, Cumplimiento, Contabilidad y Auditoría.

**Resultado esperado:** un equipo que entiende el alcance, las decisiones, los requerimientos y los riesgos sin depender de cadenas de correo.

---

## 2. Navegación

| Sección | Página | Qué encontrarás |
|---|---|---|
| Negocio | BRD resumido | Problema, objetivos, alcance, requerimientos y KPIs. |
| Negocio | Glosario | Términos de pagos, mensajería, AML y contabilidad. |
| Requerimientos | Épicas | 10 épicas con resultados esperados. |
| Requerimientos | Historias y criterios | 40 historias con Gherkin, MoSCoW, story points y dependencias. |
| Requerimientos | NFR | Disponibilidad, rendimiento, seguridad, auditoría, idempotencia y conciliación. |
| Requerimientos | Planificación de sprints | Dos sprints con objetivo, alcance y DoD. |
| Decisiones | Índice de ADR | Seis decisiones de arquitectura y sus consecuencias. |
| Operación y control | RAID log | Riesgos, supuestos, issues y dependencias. |
| Actas | Reuniones simuladas | Kickoff, taller de requerimientos y refinamiento. |

---

## 3. Estado del programa

| Dimensión | Estado | Nota |
|---|---|---|
| Negocio y procesos | Completado (Fase 1) | BRD, BPMN, DMN, riesgos y KPIs. |
| Requerimientos | Completado (Fase 2) | Backlog, NFR, sprints, CSV y trazabilidad. |
| Core y API | Pendiente (Fase 3) | Modelo SQLite, FastAPI y pruebas. |
| Mensajería | Pendiente (Fase 4) | ISO 20022, MT103 y simulador. |
| AML | Pendiente (Fase 5) | KYC, reglas, screening y ROS. |
| UX y analítica | Pendiente (Fase 6) | Wireframes, Excel, Power BI y Tableau. |
| QA/UAT y cierre | Pendiente (Fase 7) | UAT, CI y README final. |

---

## 4. Decisiones clave

1. El programa **integra** el core existente; no lo reemplaza.
2. El pago y el control de riesgo ocurren en un solo flujo; el screening no es un apéndice.
3. Toda operación que crea o modifica pagos es **idempotente**.
4. La mensajería internacional usa **ISO 20022** (pacs.008/pacs.002); MT103 queda como referencia de legado.
5. La auditoría es **append-only** y se correlaciona por operación.
6. Los datos son **sintéticos y reproducibles**; no se usan listas reales de sanciones ni PII.

---

## 5. Cómo usar este espacio

- **Producto:** prioriza con el BRD y las épicas; valida el alcance de cada sprint.
- **Operaciones:** revisa procesos, SLA, excepciones y runbook.
- **TI:** revisa NFR, ADR, contratos y dependencias.
- **Riesgos/Cumplimiento:** revisa RAID, reglas, umbrales y evidencia.
- **Contabilidad:** revisa partida doble y conciliación.
- **Auditoría:** revisa trazabilidad, retención y controles.

---

## 6. Reglas de gobernanza

1. Toda decisión relevante se registra como ADR.
2. Todo cambio de alcance se refleja en el RAID log y en el acta correspondiente.
3. Los documentos de requerimientos se versionan; no se sobrescriben sin historial.
4. Los enlaces a herramientas externas solo se publican cuando existen y fueron verificados.
5. No se incluyen datos reales, secretos ni información confidencial.

---

## 7. Contactos (roles ficticios)

| Rol | Responsabilidad |
|---|---|
| Sponsor — Gerencia de Banca Minorista | Visión, presupuesto y aprobación. |
| Product Owner — Producto Pagos | Prioridad del backlog y valor. |
| Business Analyst | Requerimientos, trazabilidad y documentación. |
| Gerencia de Operaciones | Procesos, SLA y excepciones. |
| TI — Arquitectura e Integración | Viabilidad técnica y seguridad. |
| Oficial de Cumplimiento | KYC, screening, alertas y ROS. |
| Contraloría | Partida doble y conciliación. |
| Auditoría Interna | Aseguramiento y evidencia. |

---

## 8. Referencias

- `01-brd-resumido.md`
- `03-glosario.md`
- `02-decisiones/README.md`
- `05-raid-log.md`
- `../epicas.md`
- `../historias-usuario.md`
- `../requerimientos-no-funcionales.md`
- `../planificacion-sprints.md`

**Fin de la página.**
