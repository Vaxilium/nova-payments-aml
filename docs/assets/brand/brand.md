# Marca NovaBank — identidad visual

> Marca **ficticia** creada para el portafolio. No representa a ninguna entidad
> financiera real. Todo el arte se genera con código en `scripts/make_assets.py`.

## Concepto

El isotipo es una **estrella nova de cuatro puntas** construida con geometría
simple. El centro hueco y el nodo interior sugieren una red de pagos: un punto
de origen que se conecta con cuatro direcciones. La forma se reconoce a 32 px y
no depende de degradados para conservar su silueta. Las variantes monocromas
eliminan el degradado y conservan el nodo central.

## Paleta

| Rol | Nombre | Hex | Uso |
|---|---|---|---|
| Base profunda | Navy 950 | `#04121F` | Fondos oscuros, texto sobre claro |
| Base principal | Navy 900 | `#071A2F` | Banner, dashboard oscuro, portadas |
| Superficie | Navy 800 | `#0A2540` | Tarjetas, paneles |
| Superficie elevada | Navy 700 | `#103B5C` | Gráficos, tablas |
| Azul de apoyo | Navy 600 | `#155E8A` | Enlaces y series secundarias |
| Acento cian | Cyan 400 | `#22D3EE` | Dato principal, foco, CTA |
| Acento turquesa | Turquoise 500 | `#14B8A6` | Dato secundario, éxito |
| Neutro claro | Slate 50 | `#F8FAFC` | Fondo claro |
| Neutro medio | Slate 500 | `#64748B` | Texto secundario en claro |
| Neutro oscuro | Ink | `#0F172A` | Texto principal en claro |
| Alerta alta | Amber 500 | `#F59E0B` | Prioridad P1, advertencias |
| Crítico | Red 400 | `#F87171` | Severidad crítica, errores |

Regla de proporción: **60 % navy, 25 % neutros, 10 % cian/turquesa y 5 % alertas**.
El cian se reserva para el dato más importante de cada pieza; no se usa como
color decorativo masivo.

## Tipografía

- **UI y títulos:** `Segoe UI`, con fallback a `Inter`, `system-ui`, `-apple-system`,
  `Helvetica Neue`, `Arial`, `sans-serif`.
- **Datos y código:** `Cascadia Mono`, con fallback a `Consolas`, `Courier New`,
  `monospace`.
- **Wordmark:** `Segoe UI` 700, tracking negativo (−1,4). En contextos donde la
  fuente no esté disponible, el SVG usa la pila del sistema; no se convierte el
  texto a curvas para mantenerlo editable.

## Variantes

| Archivo | Fondo recomendado | Uso |
|---|---|---|
| `logo-horizontal.svg` | Claro | README, documentos, presentaciones |
| `logo-horizontal-dark.svg` | Oscuro | Banner, GitHub dark, portadas |
| `logo-horizontal-mono.svg` | Cualquiera | Impresión, sellos, una tinta |
| `isotipo.svg` | Claro | Avatar, marca de agua |
| `isotipo-dark.svg` | Oscuro | Avatar en fondos navy |
| `isotipo-mono.svg` | Cualquiera | Favicon impreso, bordado |
| `favicon.svg` | — | Navegador, GitHub Pages |

PNG disponibles: `logo-horizontal-512.png`, `logo-horizontal-1024.png`,
`logo-horizontal-1600.png`, `isotipo-32.png`, `isotipo-128.png`,
`isotipo-512.png`, `favicon-32.png` y `favicon.ico`.

## Espacio de respeto y tamaño mínimo

- Dejar libre el equivalente a la altura de la estrella (64 px en el SVG base)
  alrededor del logo.
- Tamaño mínimo horizontal: **160 px** de ancho.
- Tamaño mínimo del isotipo: **24 px**; se probó a 32 px.
- No estirar, rotar, cambiar la proporción de la estrella ni recolorear el
  wordmark fuera de la paleta.

## Tagline

- Español: **«Pagos que fluyen. Riesgo bajo control.»**
- Inglés: **«Payments that flow. Risk under control.»**

La tagline es ficticia y se usa solo en piezas del portafolio.

## Usos incorrectos

- No usar logos, marcas o nombres de bancos, redes de pago o entidades reales.
- No usar fotografías de personas ni imágenes con derechos de terceros.
- No presentar la marca como un banco operativo ni como una certificación.
- No alterar el degradado para simular otra marca.

## Créditos y reproducibilidad

El arte se genera con SVG propio y se rasteriza con Chromium (Playwright). La
guía de créditos está en [`../CREDITOS.md`](../CREDITOS.md). Para regenerar:

```powershell
python -m scripts.make_assets --only brand
```
