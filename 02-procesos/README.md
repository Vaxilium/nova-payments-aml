# 02 — Procesos

Propósito: modelar cómo opera NovaBank hoy (AS-IS) y cómo debe operar (TO-BE), con procesos, decisiones, arquitectura y experiencia.

## Contenidos

| Artefacto | Descripción | Estado |
|---|---|---|
| `mapa-procesos.md` | Cadena de valor, inventario, SIPOC, brechas, controles y prioridades. | Completado |
| `bpmn/transferencia-instantanea-as-is.bpmn` | Proceso actual de transferencia local. | Validado estructuralmente |
| `bpmn/transferencia-instantanea-to-be.bpmn` | Proceso objetivo local 24/7. | Validado estructuralmente |
| `bpmn/transferencia-internacional-to-be.bpmn` | Pago saliente USD/EUR con ISO 20022. | Validado estructuralmente |
| `bpmn/onboarding-kyc.bpmn` | Alta digital, screening, riesgo y EDD. | Validado estructuralmente |
| `bpmn/alerta-aml.bpmn` | Generación, priorización, investigación y decisión de alertas. | Validado estructuralmente |
| `bpmn/investigacion-ros.bpmn` | Investigación, aprobación, registro y reporte simulado de ROS. | Validado estructuralmente |
| `dmn/ruteo-riesgo-transferencia.dmn` | Ruteo de riesgo por monto, país, perfil, canal y tipo. | Validado estructuralmente |
| `dmn/scoring-riesgo-cliente.dmn` | Puntaje y clasificación de riesgo de cliente. | Validado estructuralmente |
| `dmn/prioridad-alertas.dmn` | Prioridad, SLA y escalamiento de alertas. | Validado estructuralmente |
| `dmn/limites-aprobaciones.dmn` | Límites operativos y nivel de aprobación. | Validado estructuralmente |
| `procesos-mermaid.md` | Vistas Mermaid de procesos, estados y secuencias. | Completado |
| `diagramas-sistema.md` | C4, componentes, ER, event storming, journeys y despliegue. | Completado |
| `guia-lucidchart-visio-miro.md` | Pasos de recreación visual y evidencias. | Completado |

## Verificación técnica

- Los seis BPMN se parsearon con `bpmn-moddle` **sin advertencias ni referencias sin resolver**.
- Los cuatro DMN se parsearon con `dmn-moddle` **sin advertencias ni referencias sin resolver**.
- Los procesos tienen `isExecutable="false"`: son artefactos de diseño, no despliegues.
- No se afirma que los archivos se hayan abierto en Camunda Modeler, Bizagi ni Signavio. Esa verificación queda como evidencia manual `EV-004`.

## Índices

- `bpmn/README.md` — detalle de los seis procesos.
- `dmn/README.md` — detalle de las cuatro decisiones.

## Convenciones

- BPMN 2.0 con un pool `NovaBank`, lanes por rol/sistema y DI para visualización.
- DMN 1.3 con `hitPolicy="FIRST"` salvo el scoring, que usa `SUM` + clasificación.
- IDs y nombres de campos en inglés; etiquetas de negocio en español.
- Los umbrales son parámetros del caso y están marcados como supuestos.

## Pendientes

- Abrir los BPMN en Camunda Modeler/Bizagi y capturar evidencia.
- Recrear contexto C4 y proceso local en Lucidchart/Visio/Miro.
- Validar reglas con Riesgos y Cumplimiento (P-011).
