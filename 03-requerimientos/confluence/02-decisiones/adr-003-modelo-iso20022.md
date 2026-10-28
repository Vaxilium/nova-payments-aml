# ADR-003 — Modelo canónico ISO 20022 y adaptador SWIFT simulado

**Estado:** Aceptada  
**Fecha:** 2026-10-22  
**Decisores:** TI — Integración de Pagos, Operaciones Internacionales, BA  
**Impacto:** Alto  
**Relacionado:** BR-05, BR-06, NFR-11, R-10

---

## 1. Contexto

Los pagos transfronterizos migraron a ISO 20022. El período de coexistencia MT/ISO 20022 de SWIFT para CBPR+ finalizó el 22 de noviembre de 2025 según la referencia pública registrada en `docs/FUENTES.md` (F-09). El caso necesita modelar un pago saliente en USD/EUR con mensajería ISO 20022, validación de campos y seguimiento de estado, sin conectividad SWIFT real.

MT103 sigue siendo una referencia de negocio y de legado, pero no es el formato objetivo del nuevo flujo.

---

## 2. Decisión

Se adopta un **modelo canónico de pago internacional** y dos adaptadores:

1. **Generador ISO 20022:** transforma el modelo canónico en `pacs.008` (transferencia de crédito de cliente) y valida el esquema antes de enviar.
2. **Procesador de estados:** interpreta `pacs.002` (reporte de estado) y correlaciona por `UETR`.
3. **Adaptador SWIFT simulado:** sustituye la conectividad real; registra el mensaje, simula la respuesta del corresponsal y permite probar aceptación, rechazo y timeout.
4. **Mapeo MT103 ↔ ISO 20022:** se documenta como referencia de legado en Fase 4; no se usa para el flujo nuevo.

El modelo canónico contiene, como mínimo:

- `payment_id`, `uetr`, `end_to_end_id`.
- ordenante y beneficiario (nombre, cuenta/IBAN, BIC, país).
- importe, moneda ISO 4217, fecha de ejecución.
- propósito, referencia, gastos e instrucciones.
- estado, motivo de rechazo y trazas.

---

## 3. Consecuencias

### Positivas

- Un solo modelo interno para validación, riesgo y mensajería.
- El adaptador simulado permite probar sin certificación real.
- El `UETR` da trazabilidad extremo a extremo.
- El mapeo a MT103 queda documentado para legados.

### Negativas / deuda asumida

- El esquema ISO 20022 es amplio; hay que acotar los campos usados.
- La simulación no garantiza compatibilidad real con un corresponsal.
- Los cambios de versión del esquema requieren mantenimiento.
- El mapeo MT103 puede perder semántica si no se documenta.

### Riesgos asociados

- R-10 (rechazo o reparación de mensajes), R-07 (dependencia de proveedor), R-09 (screening internacional).

---

## 4. Alternativas evaluadas

| Alternativa | Por qué no se eligió |
|---|---|
| Mantener MT103 como formato principal | El estándar objetivo es ISO 20022; MT queda como legado. |
| Generar XML directamente desde el canal | Acopla el canal al esquema y duplica validaciones. |
| Usar un proveedor SaaS sin modelo canónico | Dificulta pruebas, auditoría y sustitución. |
| Simular solo el XML sin estados | No permite probar rechazos, devoluciones ni conciliación. |

---

## 5. Criterios de aceptación

- Todo pago internacional se valida contra el modelo canónico antes de generar el mensaje.
- El `pacs.008` incluye `UETR` y los campos obligatorios definidos en Fase 4.
- El `pacs.002` se correlaciona con el pago por `UETR`.
- El adaptador simulado permite reproducir aceptación, rechazo y timeout.
- Un mensaje inválido se rechaza antes de la red y queda con evidencia.
- El mapeo MT103 ↔ ISO 20022 está documentado y probado.

---

## 6. Referencias

- `../../historias-usuario.md` — US-006, US-007, US-008, US-009, US-010.
- `../../requerimientos-no-funcionales.md` — NFR-11.
- `../../../docs/FUENTES.md` — F-08, F-09, F-10.
- `../../../02-procesos/bpmn/transferencia-internacional-to-be.bpmn`
- `../../../02-procesos/mapa-procesos.md` — PR-03.

**Fin de la ADR.**
