# DMN — Índice de decisiones

Tablas de decisión del caso NovaBank. Son artefactos de diseño; no se ejecutan en un motor en esta fase.

| Archivo | Decisión | Hit policy | Entradas | Salidas | Reglas |
|---|---|---|---|---|---|
| `ruteo-riesgo-transferencia.dmn` | Ruteo de riesgo de transferencia | FIRST | 7 | 5 | 9 |
| `scoring-riesgo-cliente.dmn` | Puntaje y clasificación de cliente | SUM + FIRST | 6 + 1 | 1 + 4 | 7 + 3 |
| `prioridad-alertas.dmn` | Prioridad de alerta AML | FIRST | 7 | 4 | 8 |
| `limites-aprobaciones.dmn` | Límites y aprobaciones de pago | FIRST | 5 | 5 | 9 |

## Variables principales

- `monto_gy`: monto en guaraníes.
- `pais_destino`: país de la contraparte.
- `perfil_cliente`: BAJO / MEDIO / ALTO.
- `canal`: WEB / APP / API / SUCURSAL.
- `tipo_transferencia`: LOCAL / INTERNACIONAL.
- `es_pep`: booleano.
- `en_lista_sanciones`: booleano.
- `puntos`: puntaje agregado del cliente.
- `prioridad`: P1 / P2 / P3.

## Convenciones

- `FIRST` para que el orden de las reglas exprese prioridad.
- `SUM` para acumular factores de riesgo; luego una tabla `FIRST` clasifica.
- Valores de país y actividad son **ficticios**.
- Los umbrales son parámetros del caso, no límites regulatorios.

## Validación

- Parseo con `dmn-moddle`: sin advertencias ni referencias sin resolver.
- Verificación de que cada regla tenga tantas entradas y salidas como la tabla.
- **No** se declara haber ejecutado las decisiones en Camunda o Signavio.

## Importación

1. Abrir Camunda Modeler o Signavio.
2. Importar el `.dmn`.
3. Revisar tabla, tipos y orden de reglas.
4. Ejecutar una regla con datos ficticios.
5. Capturar evidencia en `docs/EVIDENCIAS.md` (EV-004).

## Advertencia

Los umbrales, listas y resultados son de un caso ficticio. No usar estas decisiones para operar pagos reales sin validación de Cumplimiento, Riesgos y Legal.
