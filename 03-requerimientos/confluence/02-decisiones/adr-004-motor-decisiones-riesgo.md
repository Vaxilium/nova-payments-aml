# ADR-004 — Motor de decisiones DMN para riesgo y priorización

**Estado:** Aceptada  
**Fecha:** 2026-10-22  
**Decisores:** Riesgos, Cumplimiento, TI, BA  
**Impacto:** Alto  
**Relacionado:** BR-07, BR-08, BR-09, BR-14, SNV-04

---

## 1. Contexto

Las decisiones de riesgo no pueden quedar dispersas en código, hojas de cálculo o criterios individuales. NovaBank necesita:

- evaluar screening y scoring antes de liberar un pago;
- priorizar alertas de forma consistente;
- aplicar límites y aprobaciones según el riesgo;
- permitir que Riesgos y Cumplimiento ajusten reglas con control.

La lógica cambia con frecuencia y debe ser auditable. Los umbrales concretos son parámetros del caso y están marcados `SUPUESTO NO VERIFICADO` (SNV-04) hasta su validación.

---

## 2. Decisión

Se adopta **DMN (Decision Model and Notation)** como notación para las decisiones de riesgo y priorización, con las siguientes reglas:

1. **Scoring de cliente:** tabla de suma de factores + tabla de clasificación.
2. **Ruteo de riesgo de transferencia:** evalúa cliente, importe, país, contraparte y canal.
3. **Prioridad de alertas:** asigna P1/P2/P3 según criticidad, monto y coincidencia.
4. **Límites y aprobaciones:** decide si la operación se libera, requiere aprobación o se rechaza.
5. **Hit policy:** `FIRST` para reglas ordenadas por prioridad; `SUM` para acumular puntos cuando aplique.
6. **Versionado:** cada cambio de regla genera una versión con autor, fecha, aprobador y vigencia.
7. **Simulación:** toda regla nueva se prueba contra el dataset sintético antes de activarse.

La decisión se registra con la versión de la regla, las entradas evaluadas y la salida. El motor de reglas es un componente del orquestador; no reemplaza la revisión humana en casos que requieren EDD.

---

## 3. Consecuencias

### Positivas

- Reglas legibles por negocio y auditables.
- Cambios parametrizados sin desplegar código.
- Consistencia entre canales y procesos.
- Trazabilidad de la decisión y de la versión aplicada.

### Negativas / deuda asumida

- Requiere gobierno de cambios y capacidad de simulación.
- Las tablas pueden volverse complejas si no se documentan.
- Un cambio mal aprobado impacta producción; se necesita control.
- La calidad de la decisión depende de datos y umbrales validados.

### Riesgos asociados

- R-03 (falsos positivos), R-09 (falla de screening), R-13 (deriva de reglas), R-16 (scope creep).

---

## 4. Alternativas evaluadas

| Alternativa | Por qué no se eligió |
|---|---|
| Reglas hardcodeadas | Difíciles de cambiar y auditar; requieren despliegue. |
| Hojas de cálculo operadas manualmente | Sin control de versión ni trazabilidad. |
| Modelo de machine learning propietario | Sin datos históricos suficientes y con baja explicabilidad para el MVP. |
| Reglas solo en SQL | Válidas para monitoreo, pero menos legibles para negocio y para simulación. |

---

## 5. Criterios de aceptación

- Cada decisión registra la versión de la regla y las entradas.
- Un cambio de regla requiere aprobación de Riesgos y Cumplimiento.
- La simulación muestra impacto antes de activar.
- La prioridad P1 se asigna de forma consistente.
- La decisión es explicable para auditoría y para el analista.
- Los umbrales no verificados están marcados y no se presentan como regulatorios.

---

## 6. Referencias

- `../../../02-procesos/dmn/scoring-riesgo-cliente.dmn`
- `../../../02-procesos/dmn/ruteo-riesgo-transferencia.dmn`
- `../../../02-procesos/dmn/prioridad-alertas.dmn`
- `../../../02-procesos/dmn/limites-aprobaciones.dmn`
- `../../historias-usuario.md` — US-014, US-016, US-017, US-018, US-034, US-035, US-036.
- `../../../docs/SUPUESTOS.md` — SNV-04.
- `../../../docs/PENDIENTES.md` — P-011.

**Fin de la ADR.**
