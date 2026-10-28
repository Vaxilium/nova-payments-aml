# ADR-006 — Datos sintéticos reproducibles y simulación de rieles

**Estado:** Aceptada  
**Fecha:** 2026-10-27  
**Decisores:** BA, TI — Datos, Cumplimiento, Seguridad  
**Impacto:** Medio  
**Relacionado:** NFR-14, S-010, S-018, R-06

---

## 1. Contexto

El portafolio es público y el caso es ficticio. No se pueden usar datos reales de clientes, cuentas, documentos, listas de sanciones ni información de empleadores. Al mismo tiempo, se necesitan datos coherentes para probar pagos, alertas, conciliación y dashboards.

La reproducibilidad es clave: cualquier persona debe poder regenerar el mismo dataset y obtener los mismos resultados de pruebas.

---

## 2. Decisión

Se adoptan **datos sintéticos reproducibles** y **simuladores de rieles**.

### 2.1 Datos

1. Semilla fija `NOVABANK_SEED=20261027`.
2. Nombres, documentos, cuentas, IBAN, BIC y alias inventados con formato válido.
3. Listas ficticias de sanciones, PEP y países de alto riesgo, claramente marcadas como sintéticas.
4. Sin PII real, sin datos de empleadores reales y sin secretos.
5. Integridad referencial y reglas de negocio aplicadas al generar.
6. Diccionario de datos y script de seed versionados.

### 2.2 Simulación de rieles

1. **SPI local simulado:** máquina de estados, confirmación, rechazo, timeout y devolución.
2. **SWIFT/ISO 20022 simulado:** generación de `pacs.008`, respuesta `pacs.002`, rechazo y timeout.
3. **Screening simulado:** listas ficticias y coincidencia difusa.
4. **Core simulado:** cuentas, saldos y movimientos con interfaz estable.
5. Los simuladores permiten reproducir escenarios positivos y negativos sin conectividad real.

---

## 3. Consecuencias

### Positivas

- Reproducibilidad y pruebas deterministas.
- Sin riesgo de exponer datos personales.
- Permite demostrar el caso en GitHub/LinkedIn sin infraestructura real.
- Facilita la calibración de reglas y la simulación de impacto.

### Negativas / deuda asumida

- Los datos sintéticos no capturan toda la complejidad real.
- Los simuladores pueden ocultar restricciones de un proveedor real.
- Hay que mantener el seed y el diccionario actualizados.
- Los resultados no son evidencia de comportamiento productivo.

### Riesgos asociados

- R-06 (brecha de datos), R-07 (dependencia de proveedor), R-10 (mensajería), R-13 (deriva de reglas).

---

## 4. Alternativas evaluadas

| Alternativa | Por qué no se eligió |
|---|---|
| Usar datos reales anonimizados | Riesgo de reidentificación y de confidencialidad. |
| Datos aleatorios sin semilla | Resultados no reproducibles y pruebas inestables. |
| Copiar listas reales de sanciones | Riesgo legal y de falsos positivos sobre personas reales. |
| Depender de un sandbox de proveedor | No disponible para el portafolio y con acceso restringido. |

---

## 5. Criterios de aceptación

- El mismo seed genera el mismo dataset.
- No hay PII real ni datos de empleadores reales.
- Las listas están marcadas como ficticias.
- Los simuladores cubren aceptación, rechazo, timeout y devolución.
- El diccionario de datos describe cada campo.
- Las pruebas usan el dataset sintético y son deterministas.

---

## 6. Referencias

- `../../requerimientos-no-funcionales.md` — NFR-14.
- `../../../docs/SUPUESTOS.md` — S-010, S-018.
- `../../../01-negocio/BRD.md` — límites del caso.
- `../../../02-procesos/diagramas-sistema.md` — arquitectura de simulación.
- `../../../05-core-middleware/` — seed y modelo (Fase 3).
- `../../../06-mensajeria/` — simulador (Fase 4).

**Fin de la ADR.**
