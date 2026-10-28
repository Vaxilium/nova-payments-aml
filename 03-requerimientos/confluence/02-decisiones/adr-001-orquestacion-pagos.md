# ADR-001 — Orquestación central de pagos con adaptadores

**Estado:** Aceptada  
**Fecha:** 2026-10-20  
**Decisores:** TI — Arquitectura, Producto Pagos, Operaciones  
**Impacto:** Alto  
**Relacionado:** BR-01, BR-05, BR-07, NFR-01, NFR-02

---

## 1. Contexto

NovaBank ya cuenta con core bancario, libro mayor y canal digital. El programa NovaPay debe habilitar pagos locales e internacionales y control de riesgo sin reemplazar el core. Los rieles (SPI local, SWIFT/ISO 20022) y los proveedores de screening tienen interfaces distintas, cambian con el tiempo y no deben acoplar el dominio de pagos a un proveedor.

La operación AS-IS está fragmentada: el canal, el back office, el core y cumplimiento ejecutan validaciones separadas. Esto produce reprocesos, estados inconsistentes y poca trazabilidad.

---

## 2. Decisión

Se adopta un **orquestador central de pagos** que:

1. Recibe la intención de pago del canal a través de una API versionada (`/v1`).
2. Ejecuta las validaciones de negocio, límites, screening y scoring en un flujo único.
3. Invoca adaptadores para el core, el riel local y el riel internacional.
4. Persiste el estado del pago y publica eventos de dominio.
5. Expone consultas de estado y evidencia a los canales y a operaciones.

El core sigue siendo la fuente de verdad de saldos y cuentas; el orquestador es la fuente de verdad del **estado del pago** y de la **decisión de riesgo**. No se reemplaza el core ni se duplica su contabilidad.

---

## 3. Consecuencias

### Positivas

- Un solo flujo para pago y riesgo; el screening ocurre antes de liberar.
- Adaptadores sustituibles para SPI, SWIFT y screening.
- Estados consistentes y trazables para canal, atención y auditoría.
- Menor acoplamiento entre dominio y proveedores.

### Negativas / deuda asumida

- El orquestador se vuelve un componente crítico; requiere alta disponibilidad y observabilidad.
- Hay que definir contratos estables y manejar versionado.
- La consistencia entre core y orquestador requiere conciliación y compensación.
- Aumenta la complejidad operativa si los adaptadores no están bien aislados.

### Riesgos asociados

- R-04 (indisponibilidad), R-05 (duplicidad), R-07 (dependencia de proveedor), R-10 (rechazo ISO 20022).
- Mitigaciones: idempotencia (ADR-002), adaptadores simulados (ADR-003), monitoreo y conciliación (ADR-005).

---

## 4. Alternativas evaluadas

| Alternativa | Por qué no se eligió |
|---|---|
| Implementar todo dentro del core | Acopla el core a rieles y proveedores; dificulta evolución y pruebas. |
| Dejar la orquestación al canal | Duplica reglas en cada canal y pierde una fuente única de estado. |
| Usar solo un ESB tradicional | Puede resolver integración, pero no el estado de negocio ni la decisión de riesgo. |
| Microservicios sin orquestador | Aumenta la coordinación distribuida y la complejidad de consistencia para el MVP. |

---

## 5. Criterios de aceptación de la decisión

- El orquestador expone un contrato `/v1` documentado con OpenAPI.
- El 100 % de los pagos pasa por el mismo flujo de validación y riesgo.
- El estado del pago es consultable por identificador y por `correlation_id`.
- El core no se modifica para lógica de riesgo ni de mensajería.
- Un adaptador puede sustituirse sin cambiar el dominio.

---

## 6. Referencias

- `../../historias-usuario.md` — US-001, US-016, US-024, US-039.
- `../../requerimientos-no-funcionales.md` — NFR-01, NFR-02, NFR-08.
- `../../../02-procesos/mapa-procesos.md` — PR-02, PR-03, PR-04.
- `../../../01-negocio/BRD.md` — alcance y restricciones.
- `../../../docs/FUENTES.md` — SPI y estándares.

**Fin de la ADR.**
