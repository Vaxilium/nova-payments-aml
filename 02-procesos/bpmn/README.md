# BPMN 2.0 — Índice

Modelos de proceso del caso NovaBank. Son artefactos de diseño (`isExecutable="false"`), no despliegues.

| Archivo | Proceso | Lanes | Nodos | Flujos |
|---|---|---|---|---|
| `transferencia-instantanea-as-is.bpmn` | Transferencia local AS-IS | 4 | 12 | 12 |
| `transferencia-instantanea-to-be.bpmn` | Transferencia local TO-BE | 5 | 21 | 21 |
| `transferencia-internacional-to-be.bpmn` | Pago internacional saliente TO-BE | 5 | 21 | 22 |
| `onboarding-kyc.bpmn` | Onboarding y KYC TO-BE | 5 | 17 | 18 |
| `alerta-aml.bpmn` | Gestión de alerta AML TO-BE | 4 | 16 | 16 |
| `investigacion-ros.bpmn` | Investigación y ROS TO-BE | 4 | 14 | 14 |

## Convenciones

- Un pool `NovaBank`; lanes por rol o sistema.
- Eventos, tareas, gateways y flujos con DI para visualización.
- Mensajes de confirmación con `messageEventDefinition` y `messageRef`.
- Etiquetas de negocio en español; IDs en inglés.

## Validación

- Parseo con `bpmn-moddle`: sin advertencias ni referencias sin resolver.
- Verificación de que cada nodo tenga forma DI y cada flujo tenga borde DI.
- Verificación de que no haya dos nodos en la misma lane y columna.
- **No** se declara haber abierto los archivos en Camunda, Bizagi o Signavio.

## Importación

1. Abrir Camunda Modeler, Bizagi Modeler o Signavio.
2. Importar el `.bpmn`.
3. Revisar lanes, gateways y etiquetas.
4. Capturar evidencia en `docs/EVIDENCIAS.md` (EV-004).

## Advertencia

Los umbrales, nombres y carriles son ficticios. No usar estos modelos para operar pagos reales sin validación de negocio, riesgo, cumplimiento y tecnología.
