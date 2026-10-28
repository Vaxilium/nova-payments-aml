# ADR-005 — Bitácora de auditoría append-only con correlación extremo a extremo

**Estado:** Aceptada  
**Fecha:** 2026-10-27  
**Decisores:** TI, Auditoría Interna, Cumplimiento, Seguridad  
**Impacto:** Alto  
**Relacionado:** BR-12, NFR-04, R-17

---

## 1. Contexto

Auditoría y Cumplimiento necesitan reconstruir qué pasó con una operación: quién la inició, qué validaciones pasó, qué decidió el motor de riesgo, qué mensaje se envió, qué respondió el riel y quién cerró el caso. La evidencia está dispersa entre canal, core, mensajería, alertas y correo.

Sin una traza única y confiable, no se puede demostrar el control ni explicar una diferencia de conciliación. La evidencia debe resistir revisión interna y regulatoria, sin exponer datos personales innecesarios.

---

## 2. Decisión

Se adopta una **bitácora de auditoría append-only** con correlación por operación.

### 2.1 Atributos mínimos del evento

| Campo | Descripción |
|---|---|
| `event_id` | Identificador único e inmutable. |
| `correlation_id` | Identificador de la operación de extremo a extremo. |
| `occurred_at` | Fecha y hora en UTC. |
| `actor` | Usuario, servicio o sistema que ejecutó la acción. |
| `action` | Acción realizada (crear, validar, decidir, enviar, cerrar). |
| `entity_type` / `entity_id` | Tipo e identificador de la entidad afectada. |
| `result` | Resultado de la acción. |
| `reason` | Motivo o código cuando corresponde. |
| `rule_version` | Versión de la regla aplicada, si aplica. |
| `payload_hash` | Hash del payload relevante, sin datos sensibles. |

### 2.2 Reglas

1. Solo se agregan eventos; no se actualizan ni se eliminan.
2. Cada operación debe tener un `correlation_id` desde su creación.
3. Un evento sin `correlation_id` se rechaza.
4. Los datos personales se enmascaran o se referencian por ID; no se copian completos.
5. La consulta se controla por rol y se audita.
6. La retención inicial es un parámetro (5 años) sujeto a validación de Cumplimiento/Legal.
7. La evidencia exportable incluye la cadena de eventos y el sello de integridad.

---

## 3. Consecuencias

### Positivas

- Trazabilidad completa y explicable.
- Base para conciliación, investigación y auditoría.
- Detección de accesos indebidos y de intentos de alteración.
- Evidencia consistente para UAT y para el regulador.

### Negativas / deuda asumida

- Requiere almacenamiento y políticas de retención.
- Aumenta el volumen de datos y el costo de consulta.
- Exige disciplina para correlacionar todos los servicios.
- La inmutabilidad debe implementarse técnicamente, no solo declararse.

### Riesgos asociados

- R-06 (brecha de datos), R-14 (fraude interno), R-17 (evidencia incompleta).

---

## 4. Alternativas evaluadas

| Alternativa | Por qué no se eligió |
|---|---|
| Logs de aplicación sin estructura | Difíciles de correlacionar y de retener con integridad. |
| Base de datos editable | Permite alteración y no sirve como evidencia fuerte. |
| Correo o carpeta compartida | Sin control de acceso ni trazabilidad confiable. |
| Solo logs del proveedor | No cubre decisiones internas ni cambios de reglas. |

---

## 5. Criterios de aceptación

- Toda operación tiene una cadena de eventos completa.
- La consulta por `correlation_id` devuelve los eventos en orden.
- La modificación o borrado de un evento se rechaza y se registra.
- Los logs no contienen PII sin enmascarar.
- La exportación de evidencia incluye sello de integridad.
- La retención está aprobada por Cumplimiento/Legal antes de producción.

---

## 6. Referencias

- `../../historias-usuario.md` — US-027, US-038.
- `../../requerimientos-no-funcionales.md` — NFR-04, NFR-10.
- `../../../02-procesos/mapa-procesos.md` — PR-13.
- `../../../01-negocio/riesgos.md` — R-06, R-14, R-17.
- `../../../docs/SUPUESTOS.md` — retención como parámetro.

**Fin de la ADR.**
