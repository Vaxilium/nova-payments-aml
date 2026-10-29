# Guía de estilo mínima — NovaBank Payments & AML Hub

**Documento:** UX-NB-003
**Versión:** 1.0
**Fecha:** 2026-10-29
**Uso:** referencia para wireframes, prototipos Figma/Balsamiq y futura implementación.

> La paleta y las tipografías son propuestas del caso ficticio. No se declara conformidad con un sistema de diseño corporativo real.

---

## 1. Paleta

| Token | Hex | Uso | Contraste sobre blanco |
|---|---|---|---|
| `color-primary-900` | `#0B3B60` | Encabezados, navegación, texto de marca | 12,6:1 |
| `color-primary-700` | `#155E8A` | Acciones primarias, enlaces | 6,6:1 |
| `color-primary-100` | `#DCEBF5` | Fondos de selección y hover suave | — |
| `color-accent-700` | `#0F766E` | Éxito, confirmaciones | 5,9:1 |
| `color-accent-100` | `#CCFBF1` | Fondo de éxito | — |
| `color-neutral-900` | `#111827` | Texto principal | 17,7:1 |
| `color-neutral-600` | `#4B5563` | Texto secundario | 7,6:1 |
| `color-neutral-300` | `#D1D5DB` | Bordes y divisores | — |
| `color-neutral-100` | `#F3F4F6` | Fondo de página | — |
| `color-surface` | `#FFFFFF` | Tarjetas y tablas | — |
| `color-warning-700` | `#B45309` | Advertencia | 5,0:1 |
| `color-warning-100` | `#FEF3C7` | Fondo de advertencia | — |
| `color-danger-700` | `#B91C1C` | Error, P1, SLA vencido | 6,5:1 |
| `color-danger-100` | `#FEE2E2` | Fondo de error | — |
| `color-info-700` | `#1D4ED8` | Información y enlaces secundarios | 6,3:1 |

**Regla:** el color nunca es el único portador de significado. Toda etiqueta de estado incluye texto y, cuando aplica, ícono.

## 2. Tipografía

| Rol | Familia propuesta | Tamaño | Peso | Altura de línea |
|---|---|---|---|---|
| Display | Inter | 32 px | 700 | 40 px |
| H1 | Inter | 24 px | 700 | 32 px |
| H2 | Inter | 20 px | 600 | 28 px |
| H3 | Inter | 16 px | 600 | 24 px |
| Cuerpo | Inter | 16 px | 400 | 24 px |
| Cuerpo pequeño | Inter | 14 px | 400 | 20 px |
| Etiqueta | Inter | 12 px | 600 | 16 px |
| Dato numérico | Inter tabular | 16–32 px | 600 | según contexto |

- Alternativa local: `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`.
- No usar más de tres tamaños en una misma tarjeta.
- Importes y fechas con cifras tabulares para alinear columnas.
- Evitar texto en mayúsculas sostenidas en párrafos; reservarlo para etiquetas cortas.

## 3. Espaciado y grilla

- Escala base de 4 px: `4, 8, 12, 16, 24, 32, 48, 64`.
- Contenedor máximo: 1.280 px en desktop; 16 px de margen lateral en mobile.
- Grilla desktop: 12 columnas con 24 px de gutter.
- Grilla mobile: 4 columnas con 16 px de gutter.
- Radios: 8 px en tarjetas, 6 px en inputs y botones, 999 px en badges.
- Sombras: una sola elevación (`0 1px 2px rgba(17,24,39,.08), 0 4px 12px rgba(17,24,39,.06)`).
- Bordes: 1 px `color-neutral-300`; foco con 2 px `color-primary-700` y offset de 2 px.

## 4. Componentes base

### Botones

| Variante | Fondo | Texto | Borde | Uso |
|---|---|---|---|---|
| Primario | `color-primary-700` | Blanco | Ninguno | Acción principal única por pantalla |
| Secundario | Blanco | `color-primary-700` | 1 px `color-primary-700` | Acción alternativa |
| Terciario | Transparente | `color-primary-700` | Ninguno | Enlaces y acciones menores |
| Destructivo | `color-danger-700` | Blanco | Ninguno | Cierre, cancelación irreversible |
| Deshabilitado | `color-neutral-100` | `color-neutral-600` | 1 px `color-neutral-300` | Solo con explicación visible |

Altura mínima 44 px; padding horizontal 16 px; texto 14–16 px.

### Campos

- Etiqueta persistente arriba del campo, nunca solo placeholder.
- Altura mínima 44 px.
- Ayuda debajo, 12–14 px, asociada con `aria-describedby`.
- Error debajo del campo, ícono + texto, borde `color-danger-700`.
- Estados: normal, hover, foco, error, deshabilitado, solo lectura, cargando.

### Tarjetas

- Fondo `color-surface`, borde `color-neutral-300`, radio 8 px, padding 16–24 px.
- Título con `h2`/`h3` semántico.
- No anidar más de dos niveles de tarjetas.

### Tablas

- Encabezado sticky en tablas largas.
- Fila con hover `color-neutral-100`; selección `color-primary-100`.
- Primera columna de identificación y última de acciones.
- En mobile, transformar en lista de tarjetas o permitir scroll horizontal con aviso.
- Nunca truncar importes ni fechas sin tooltip accesible.

### Badges de estado

| Estado | Fondo | Texto |
|---|---|---|
| NUEVA | `color-primary-100` | `color-primary-900` |
| EN_ANALISIS | `color-warning-100` | `color-warning-700` |
| ESCALADA | `#FFEDD5` | `#9A3412` |
| CERRADA_FALSO_POSITIVO | `color-neutral-100` | `color-neutral-600` |
| REPORTADA | `color-accent-100` | `color-accent-700` |
| P1 | `color-danger-100` | `color-danger-700` |
| P2 | `color-warning-100` | `color-warning-700` |
| P3 | `color-neutral-100` | `color-neutral-600` |

## 5. Iconografía

- Estilo lineal, 20–24 px, trazo 1,5–2 px.
- No usar emojis como íconos de estado.
- Todo ícono interactivo necesita nombre accesible; todo ícono decorativo usa `aria-hidden="true"`.
- Íconos de estado: check (éxito), alerta (advertencia), equis (error), reloj (SLA), info (ayuda).

## 6. Movimiento

- Duración 150–250 ms para microinteracciones; 300 ms para transiciones de pantalla.
- Respetar `prefers-reduced-motion`; desactivar desplazamientos y reducir transiciones a opacidad.
- No usar animaciones para comunicar un estado crítico sin alternativa textual.
- Spinner solo si la espera supera 300 ms; skeleton para cargas de contenido.

## 7. Contenido y tono

- Voz activa, frases cortas, sin jerga técnica en la app del cliente.
- En la consola AML se permite terminología de cumplimiento, pero se explica en ayuda contextual.
- Errores: qué pasó, por qué y qué hacer; nunca culpar al usuario.
- Evitar “OK” genérico; usar verbos concretos (“Confirmar transferencia”, “Cerrar caso”).
- Fechas relativas (“hace 2 horas”) con fecha absoluta en tooltip o texto secundario.

## 8. Uso en Figma/Balsamiq

1. Crear estilos de color y texto con los tokens de esta guía.
2. Crear componentes maestros para botones, campos, badges y tarjetas.
3. Usar auto-layout con la escala de espaciado.
4. Nombrar frames y capas con los IDs de pantalla (`APP-01`, `AML-01`).
5. Revisar contraste y foco antes de compartir.
6. Documentar cualquier excepción en la página “Decisiones” del archivo.
