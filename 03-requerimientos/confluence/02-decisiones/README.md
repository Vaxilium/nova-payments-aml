# Índice de decisiones de arquitectura (ADR)

**Página:** Decisiones de arquitectura  
**Versión:** 1.0  
**Fecha:** 2026-10-28  
**Dueño:** TI — Arquitectura  
**Estado:** Borrador para revisión ficticia

> Las ADR documentan decisiones de diseño del caso NovaBank. No describen una implementación real ni certifican productos de terceros. Las referencias a ISO 20022, SWIFT, BCP y SEPRELAD son públicas y se usan como contexto.

---

## 1. Registro de ADR

| ID | Título | Estado | Fecha | Decisor |
|---|---|---|---|---|
| ADR-001 | Orquestación central de pagos con adaptadores al core y a los rieles | Aceptada | 2026-10-20 | TI — Arquitectura |
| ADR-002 | Idempotencia y máquina de estados para pagos reintentables | Aceptada | 2026-10-20 | TI — Arquitectura / Operaciones |
| ADR-003 | Modelo canónico ISO 20022 y adaptador SWIFT simulado | Aceptada | 2026-10-22 | TI — Integración / Operaciones Intl. |
| ADR-004 | Motor de decisiones DMN para riesgo y priorización de alertas | Aceptada | 2026-10-22 | Riesgos / Cumplimiento / TI |
| ADR-005 | Bitácora de auditoría append-only con correlación extremo a extremo | Aceptada | 2026-10-27 | TI / Auditoría |
| ADR-006 | Datos sintéticos reproducibles y simulación de rieles | Aceptada | 2026-10-27 | BA / Datos / TI |

---

## 2. Convención de una ADR

Cada ADR contiene:

- **Contexto:** fuerza o problema que motiva la decisión.
- **Decisión:** qué se decidió y qué se descartó.
- **Consecuencias:** efectos positivos, negativos y deuda asumida.
- **Alternativas:** opciones evaluadas y por qué no se eligieron.
- **Estado:** propuesta, aceptada, reemplazada o rechazada.
- **Referencias:** documentos, procesos o fuentes.

---

## 3. Reglas de gobierno

1. Una ADR se crea cuando la decisión afecta arquitectura, integración, seguridad, datos o control.
2. No se modifica una ADR aceptada; se crea una nueva que la reemplaza.
3. Toda ADR debe tener un dueño y una fecha.
4. Las decisiones con impacto regulatorio requieren revisión de Cumplimiento/Legal.
5. Las ADR no sustituyen el análisis legal ni la aprobación formal del banco.

---

## 4. Relación con otros artefactos

- `../01-brd-resumido.md` — objetivos y alcance.
- `../05-raid-log.md` — riesgos y dependencias asociados.
- `../../requerimientos-no-funcionales.md` — atributos de calidad.
- `../../historias-usuario.md` — historias impactadas.
- `../../../02-procesos/` — BPMN y DMN.
- `../../../docs/FUENTES.md` — fuentes.

**Fin de la página.**
