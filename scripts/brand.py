"""Marca NovaBank: isotipo, logo horizontal, favicon y guía de uso."""

from __future__ import annotations

from .assetlib import (
    BRAND_DIR,
    FONT_UI,
    PALETTE,
    TAGLINE_EN,
    TAGLINE_ES,
    write_text,
)

STAR_PATH = (
    "M32 2.5 L39.6 24.4 L61.5 32 L39.6 39.6 L32 61.5 "
    "L24.4 39.6 L2.5 32 L24.4 24.4 Z"
)


def _gradient(prefix: str, start: str, end: str) -> str:
    return (
        f'<linearGradient id="{prefix}-nova" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{start}"/>'
        f'<stop offset="100%" stop-color="{end}"/>'
        "</linearGradient>"
    )


def isotipo_svg(
    *,
    prefix: str = "nb",
    variant: str = "gradient",
    size: int = 64,
    title: str = "Isotipo NovaBank",
) -> str:
    """Devuelve el isotipo como SVG. Variantes: gradient, dark, light, mono."""
    if variant == "dark":
        start, end = PALETTE["cyan_400"], PALETTE["mint_300"]
        node = PALETTE["white"]
        fill = "url(#%s-nova)" % prefix
    elif variant == "light":
        start, end = PALETTE["navy_600"], PALETTE["turquoise_500"]
        node = PALETTE["white"]
        fill = "url(#%s-nova)" % prefix
    elif variant == "mono":
        start = end = "currentColor"
        node = "currentColor"
        fill = "currentColor"
    else:
        start, end = PALETTE["cyan_400"], PALETTE["turquoise_500"]
        node = PALETTE["white"]
        fill = "url(#%s-nova)" % prefix

    gradients = "" if variant == "mono" else _gradient(prefix, start, end)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 64 64" role="img" aria-label="{title}">
<defs>{gradients}
<mask id="{prefix}-hole"><rect width="64" height="64" fill="#fff"/><circle cx="32" cy="32" r="5.4" fill="#000"/></mask>
</defs>
<path d="{STAR_PATH}" fill="{fill}" mask="url(#{prefix}-hole)"/>
<circle cx="32" cy="32" r="1.9" fill="{node}"/>
</svg>"""


def horizontal_svg(
    *,
    prefix: str = "nbh",
    variant: str = "light",
    width: int = 400,
) -> str:
    """Logo horizontal con wordmark y bajada. Variantes light, dark y mono."""
    if variant == "dark":
        nova, bank, sub = PALETTE["white"], PALETTE["cyan_300"], PALETTE["slate_400"]
        mark = isotipo_svg(prefix=f"{prefix}-mark", variant="dark", size=64, title="Isotipo NovaBank")
    elif variant == "mono":
        nova = bank = sub = "currentColor"
        mark = isotipo_svg(prefix=f"{prefix}-mark", variant="mono", size=64, title="Isotipo NovaBank")
    else:
        nova, bank, sub = PALETTE["navy_800"], PALETTE["turquoise_500"], PALETTE["slate_500"]
        mark = isotipo_svg(prefix=f"{prefix}-mark", variant="light", size=64, title="Isotipo NovaBank")

    mark = mark.replace("<svg ", '<svg x="8" y="8" ')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="80" viewBox="0 0 400 80" role="img" aria-label="NovaBank — Payments &amp; AML Hub">
{mark}
<text x="88" y="41" font-family='{FONT_UI}' font-size="38" font-weight="700" letter-spacing="-1.4">
<tspan fill="{nova}">Nova</tspan><tspan fill="{bank}">Bank</tspan>
</text>
<text x="90" y="62" font-family='{FONT_UI}' font-size="10.5" font-weight="600" letter-spacing="3.1" fill="{sub}">PAYMENTS &amp; AML HUB</text>
</svg>"""


def favicon_svg() -> str:
    """Favicon cuadrado con fondo navy y estrella nova."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64" role="img" aria-label="Favicon NovaBank">
<rect width="64" height="64" rx="14" fill="{PALETTE['navy_900']}"/>
<g transform="translate(8 8) scale(0.75)">
{isotipo_svg(prefix="nb-fav", variant="dark", size=64, title="Estrella nova")}
</g>
</svg>"""


def brand_markdown() -> str:
    return f"""# Marca NovaBank — identidad visual

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
| Base profunda | Navy 950 | `{PALETTE['navy_950']}` | Fondos oscuros, texto sobre claro |
| Base principal | Navy 900 | `{PALETTE['navy_900']}` | Banner, dashboard oscuro, portadas |
| Superficie | Navy 800 | `{PALETTE['navy_800']}` | Tarjetas, paneles |
| Superficie elevada | Navy 700 | `{PALETTE['navy_700']}` | Gráficos, tablas |
| Azul de apoyo | Navy 600 | `{PALETTE['navy_600']}` | Enlaces y series secundarias |
| Acento cian | Cyan 400 | `{PALETTE['cyan_400']}` | Dato principal, foco, CTA |
| Acento turquesa | Turquoise 500 | `{PALETTE['turquoise_500']}` | Dato secundario, éxito |
| Neutro claro | Slate 50 | `{PALETTE['slate_50']}` | Fondo claro |
| Neutro medio | Slate 500 | `{PALETTE['slate_500']}` | Texto secundario en claro |
| Neutro oscuro | Ink | `{PALETTE['ink']}` | Texto principal en claro |
| Alerta alta | Amber 500 | `{PALETTE['amber_500']}` | Prioridad P1, advertencias |
| Crítico | Red 400 | `{PALETTE['red_400']}` | Severidad crítica, errores |

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

- Español: **«{TAGLINE_ES}»**
- Inglés: **«{TAGLINE_EN}»**

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
python scripts\\make_assets.py --only brand
```
"""


def write_brand_sources() -> None:
    write_text(BRAND_DIR / "logo-horizontal.svg", horizontal_svg(prefix="nbh-light", variant="light"))
    write_text(
        BRAND_DIR / "logo-horizontal-dark.svg",
        horizontal_svg(prefix="nbh-dark", variant="dark"),
    )
    write_text(
        BRAND_DIR / "logo-horizontal-mono.svg",
        horizontal_svg(prefix="nbh-mono", variant="mono"),
    )
    write_text(BRAND_DIR / "isotipo.svg", isotipo_svg(prefix="nbi-light", variant="light", size=512))
    write_text(
        BRAND_DIR / "isotipo-dark.svg",
        isotipo_svg(prefix="nbi-dark", variant="dark", size=512),
    )
    write_text(
        BRAND_DIR / "isotipo-mono.svg",
        isotipo_svg(prefix="nbi-mono", variant="mono", size=512),
    )
    write_text(BRAND_DIR / "favicon.svg", favicon_svg())
    write_text(BRAND_DIR / "brand.md", brand_markdown())
