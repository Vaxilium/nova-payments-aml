# Guía de recreación en Lucidchart, Visio y Miro

**Proyecto:** NovaBank Instant & Cross-Border Payments + AML Hub
**Documento:** GUI-NB-001
**Versión:** 1.0
**Fecha:** 2026-10-27

> Guía manual. El agente no opera Lucidchart, Visio ni Miro. Los diagramas fuente están en `bpmn/`, `dmn/`, `procesos-mermaid.md` y `diagramas-sistema.md`; esta guía indica cómo recrearlos y qué capturar como evidencia.

---

## 1. Objetivo

Permitir que el autor reproduzca los diagramas en herramientas visuales, mantenga consistencia entre artefactos y genere evidencias para el portafolio sin alterar el contenido funcional.

---

## 2. Mapa de artefactos y herramienta sugerida

| Artefacto | Fuente | Lucidchart | Visio | Miro | Formato de salida |
|---|---|---|---|---|---|
| Procesos BPMN | `bpmn/*.bpmn` | Importar BPMN o recrear | Importar BPMN | Recrear con frames | PNG/SVG + enlace |
| Decisiones DMN | `dmn/*.dmn` | Recrear tabla | Recrear tabla | Tabla/frame | PNG + enlace |
| Contexto C4 | `diagramas-sistema.md` | Plantilla C4 | Formas básicas | Frame | PNG/SVG |
| Contenedores | `diagramas-sistema.md` | Plantilla C4 | Formas básicas | Frame | PNG/SVG |
| ER | `diagramas-sistema.md` | Plantilla ER | Formas básicas | Frame | PNG |
| Event storming | `diagramas-sistema.md` | Post-its | Formas | Post-its | PNG |
| Journeys | `diagramas-sistema.md` | Plantilla journey | Formas | Frame | PNG |
| Procesos Mermaid | `procesos-mermaid.md` | Copiar como referencia | Copiar como referencia | Copiar como referencia | PNG |

---

## 3. Configuración común del lienzo

### 3.1 Formato

- **Orientación:** horizontal para BPMN y arquitectura; vertical para journeys.
- **Tamaño:** 1920 × 1080 px para capturas; lienzo amplio para edición.
- **Grid:** 10 px; snapping activo.
- **Márgenes:** 40 px.
- **Fuente:** Inter, Arial o Calibri; 12–14 pt para nodos; 10–11 pt para etiquetas.
- **Títulos:** 24–28 pt; subtítulos 16–18 pt.

### 3.2 Paleta

| Uso | Color | Hex |
|---|---|---|
| Fondo | Blanco | `#FFFFFF` |
| Texto principal | Gris azulado | `#1F2937` |
| Acento NovaBank | Azul | `#1D4ED8` |
| Éxito | Verde | `#047857` |
| Advertencia | Ámbar | `#B45309` |
| Riesgo / rechazo | Rojo | `#B91C1C` |
| AML / cumplimiento | Violeta | `#6D28D9` |
| Externo | Gris | `#6B7280` |
| Borde | Gris claro | `#D1D5DB` |

**Regla de accesibilidad:** no usar color como único canal; acompañar con texto, ícono o forma.

### 3.3 Convenciones de etiquetas

- Actividad: verbo en infinitivo (“Validar datos”, “Enviar orden”).
- Evento: sustantivo y estado (“Pago recibido”, “Alerta creada”).
- Gateway: pregunta cerrada (“¿Datos válidos?”).
- Lane: rol o sistema, no persona.
- IDs visibles solo en la vista técnica, no en la ejecutiva.

---

## 4. Recreación de BPMN

### 4.1 Lucidchart

1. Crear documento `NB — Procesos de pagos y AML`.
2. Insertar `Swimlane` horizontal; nombrar el pool `NovaBank`.
3. Crear lanes: `Canal`, `Motor de Pagos`, `Riesgo / AML`, `Core / Contabilidad`, `Operaciones`.
4. Copiar los nodos del BPMN fuente respetando carriles y orden.
5. Usar rombos para gateways y óvalos para eventos.
6. Conectar con flechas ortogonales; etiquetar `Sí`/`No`.
7. Agregar notas con reglas (`DMN`, límites y SLA).
8. Exportar `PNG` a 2x y `SVG`; guardar enlace.

**Atajo:** si Lucidchart permite importar BPMN, usar `bpmn/transferencia-instantanea-to-be.bpmn` y ajustar estilos. Verificar que no se pierdan lanes ni etiquetas.

### 4.2 Visio

1. Abrir plantilla `Business Process Model and Notation (BPMN) 2.0` o `Cross-Functional Flowchart`.
2. Crear pool y lanes con las mismas etiquetas.
3. Importar BPMN si la versión lo permite; si no, recrear.
4. Ajustar conexiones y etiquetas.
5. Guardar como `.vsdx` y exportar `PDF`/`PNG`.
6. Verificar que los gateways tengan salidas etiquetadas.

### 4.3 Miro

1. Crear board `NB — Pagos y AML`.
2. Usar frames por proceso: `Local AS-IS`, `Local TO-BE`, `Internacional`, `Onboarding`, `Alerta`, `ROS`.
3. Usar swimlanes nativos o frames por lane.
4. Pegar post-its con las actividades; conectar con flechas.
5. Agregar un frame `Decisiones DMN` con tablas resumidas.
6. Compartir en modo lectura y capturar.

### 4.4 Verificación BPMN

- [ ] Un pool y lanes coherentes.
- [ ] Evento de inicio y fin por camino.
- [ ] Gateways con salidas etiquetadas.
- [ ] Sin actividades huérfanas.
- [ ] Sin flujos que crucen indebidamente lanes.
- [ ] Nombres de actividades en verbo infinitivo.
- [ ] Sin datos reales ni PII.

---

## 5. Recreación de DMN

1. Crear una tabla por decisión: `Ruteo`, `Scoring`, `Prioridad`, `Límites`.
2. Columnas de entrada con el nombre de la variable y el tipo.
3. Columnas de salida con el nombre y el tipo.
4. Respetar `hitPolicy`:
   - `FIRST` para ruteo, prioridad y límites.
   - `SUM` para puntaje; luego una tabla de clasificación.
5. Ordenar las reglas por prioridad y documentar el motivo.
6. Agregar una nota con la versión y el dueño de la regla.

**Advertencia:** no cambiar el orden de las reglas `FIRST` sin revisar el efecto. Un cambio de orden puede alterar la decisión.

---

## 6. Recreación de arquitectura C4

### 6.1 Contexto

1. Dibujar un rectángulo central `NovaBank`.
2. Ubicar actores a la izquierda (cliente, canal) y sistemas externos a la derecha (SPI, SWIFT, SEPRELAD, screening).
3. Usar flechas con verbo: “envía”, “consulta”, “reporta”.
4. Agregar leyenda de externos vs. internos.

### 6.2 Contenedores

1. Agrupar por zonas: canales, aplicaciones, datos, externos.
2. Dibujar contenedores con nombre y responsabilidad.
3. Conectar según `diagramas-sistema.md`.
4. Resaltar el orquestador como componente central.
5. No mostrar detalles de clases ni tablas.

### 6.3 Componentes

1. Abrir el orquestador.
2. Mostrar validador, límites, router, máquina de estados, clientes y outbox.
3. Etiquetar patrones: idempotencia, saga, outbox.
4. Mantener máximo 12 componentes para legibilidad.

---

## 7. ER, event storming y journeys

### 7.1 ER

1. Usar notación crow’s foot.
2. Dibujar entidades principales: Cliente, Cuenta, Perfil de Riesgo, Transferencia, Evento, Alerta, Caso, ROS, Asiento.
3. Marcar claves primarias y foráneas.
4. No incluir todos los atributos; los definitivos van en Fase 3.
5. Agregar nota: “modelo conceptual”.

### 7.2 Event storming

1. Usar post-its naranjas para eventos, azules para comandos, lilas para políticas.
2. Ordenar en línea de tiempo.
3. Agrupar por agregado: Pago, Riesgo, Alerta, Caso.
4. Marcar puntos de dolor con rojo.
5. Identificar políticas: “si riesgo alto, retener”, “si confirmado, contabilizar”.

### 7.3 Journey

1. Definir etapas: iniciar, confirmar, esperar, resolver.
2. Puntuar 1–5 por etapa.
3. Marcar emoción con color.
4. Anotar puntos de dolor y oportunidades.
5. Mantener un journey por segmento (persona y empresa).

---

## 8. Estructura recomendada de Miro

```text
Board: NB — Pagos y AML
├─ Frame 00 — Portada y leyenda
├─ Frame 01 — Contexto C4
├─ Frame 02 — Contenedores
├─ Frame 03 — Local AS-IS
├─ Frame 04 — Local TO-BE
├─ Frame 05 — Internacional TO-BE
├─ Frame 06 — Onboarding y KYC
├─ Frame 07 — Alerta AML
├─ Frame 08 — Investigación y ROS
├─ Frame 09 — DMN (4 tablas)
├─ Frame 10 — ER preliminar
├─ Frame 11 — Event storming
├─ Frame 12 — Journeys
└─ Frame 13 — Decisiones y pendientes
```

---

## 9. Exportación y evidencias

### 9.1 Formatos

| Uso | Formato | Configuración |
|---|---|---|
| Repositorio | PNG | 2x, fondo blanco, sin bordes de selección |
| Presentación | SVG/PDF | Vectorial, texto seleccionable |
| Enlace | URL de la herramienta | Permiso de lectura |
| Portafolio | PNG + enlace | 1920 px de ancho |

### 9.2 Evidencias para `docs/EVIDENCIAS.md`

- `EV-004`: captura de Camunda Modeler o visor BPMN con el proceso local TO-BE abierto.
- `EV-005`: captura de Lucidchart/Visio/Miro con el contexto C4 y el proceso local TO-BE.
- `EV-006`: captura de la tabla DMN de ruteo.
- `EV-007`: captura del tablero de KPIs (Fase 6).

Cada captura debe incluir:

- Nombre del artefacto.
- Fecha.
- Herramienta.
- Enlace de lectura (si aplica).
- Breve descripción de lo que se ve.

**No se debe afirmar** que la captura fue generada por el agente ni que la herramienta fue operada por el agente.

---

## 10. Accesibilidad y calidad visual

- Contraste mínimo 4,5:1 para texto.
- No usar solo color para indicar estado.
- Fuente mínima 10 pt en capturas.
- Etiquetas completas, sin abreviaturas no explicadas.
- Evitar cruces de flechas; usar codos ortogonales.
- Dejar espacio en blanco entre lanes.
- Incluir leyenda y título.
- Revisar ortografía y consistencia de nombres.

---

## 11. Checklist de aceptación visual

- [ ] Título y versión visibles.
- [ ] Leyenda de colores y formas.
- [ ] Todos los nodos del BPMN están representados.
- [ ] Gateways y etiquetas `Sí`/`No` visibles.
- [ ] Lanes correctos.
- [ ] DMN con entradas, salidas y reglas completas.
- [ ] C4 con actores y externos diferenciados.
- [ ] ER con claves y cardinalidades.
- [ ] Journey con etapas y puntos de dolor.
- [ ] Sin datos reales.
- [ ] Exportación legible.
- [ ] Enlace de lectura probado.

---

## 12. Referencias

- `bpmn/` — modelos BPMN 2.0.
- `dmn/` — tablas DMN.
- `procesos-mermaid.md` — vistas rápidas.
- `diagramas-sistema.md` — C4, ER, event storming y journeys.
- `../docs/EVIDENCIAS.md` — registro de capturas y enlaces.
