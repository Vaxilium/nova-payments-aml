"""Utilidades compartidas para generar los activos visuales de NovaBank.

Todo el arte se produce con código: SVG, HTML/CSS y renderizado con Chromium
(Playwright). No se descargan imágenes de terceros ni se usan fotos reales.
"""

from __future__ import annotations

import base64
import html
import os
import re
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
BRAND_DIR = ASSETS / "brand"
IMG_DIR = ASSETS / "img"
DASHBOARD_DIR = ASSETS / "dashboard"
LINKEDIN_DIR = ASSETS / "linkedin"
SRC_DIR = ASSETS / "src"

DEFAULT_NODE_MODULES = Path(
    os.environ.get(
        "NOVA_ASSET_NODE_MODULES",
        str(Path(os.environ.get("TEMP", "/tmp")) / "opencode" / "assets-npm" / "node_modules"),
    )
)

PALETTE = {
    "navy_950": "#04121F",
    "navy_900": "#071A2F",
    "navy_800": "#0A2540",
    "navy_700": "#103B5C",
    "navy_600": "#155E8A",
    "cyan_400": "#22D3EE",
    "cyan_300": "#67E8F9",
    "turquoise_500": "#14B8A6",
    "turquoise_400": "#2DD4BF",
    "mint_300": "#5EEAD4",
    "slate_500": "#64748B",
    "slate_400": "#94A3B8",
    "slate_300": "#CBD5E1",
    "slate_200": "#E2E8F0",
    "slate_100": "#F1F5F9",
    "slate_50": "#F8FAFC",
    "white": "#FFFFFF",
    "ink": "#0F172A",
    "amber_400": "#FBBF24",
    "amber_500": "#F59E0B",
    "red_400": "#F87171",
    "red_500": "#EF4444",
    "green_400": "#34D399",
    "green_500": "#10B981",
}

FONT_UI = '"Segoe UI", Inter, system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif'
FONT_MONO = '"Cascadia Mono", Consolas, "Courier New", monospace'

TAGLINE_ES = "Pagos que fluyen. Riesgo bajo control."
TAGLINE_EN = "Payments that flow. Risk under control."

AUTHOR = {
    "name": "Franco Tillería Centurión",
    "role_es": "Business Analyst",
    "linkedin": "https://www.linkedin.com/in/franco-tilleria-centurion/",
    "github": "https://github.com/Vaxilium",
    "repo": "https://github.com/Vaxilium/nova-payments-aml",
    "site": "https://vaxilium.github.io/nova-payments-aml/",
}


def ensure_dirs() -> None:
    for path in (BRAND_DIR, IMG_DIR, DASHBOARD_DIR, LINKEDIN_DIR, SRC_DIR, IMG_DIR / "bpmn"):
        path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def format_int(value: int | float) -> str:
    return f"{int(round(value)):,}".replace(",", ".")


def format_pct(value: float, digits: int = 1) -> str:
    formatted = f"{value:.{digits}f}".replace(".", ",")
    return f"{formatted} %"


def svg_data_uri(svg: str) -> str:
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def optimize_png(path: Path, max_kb: int = 500) -> None:
    """Comprime un PNG sin cambiar sus dimensiones y avisa si supera el límite."""
    limit = max_kb * 1024
    if not path.exists() or path.stat().st_size <= limit:
        return
    with Image.open(path) as image:
        image = image.convert("RGBA")
        alpha = image.getchannel("A")
        has_alpha = alpha.getextrema()[0] < 255
        method = Image.Quantize.FASTOCTREE if has_alpha else Image.Quantize.MEDIANCUT
        target = image if has_alpha else image.convert("RGB")
        for colors in (256, 192, 128, 96, 64):
            quantized = target.quantize(colors=colors, method=method)
            quantized.save(path, format="PNG", optimize=True)
            if path.stat().st_size <= limit:
                return
        target.save(path, format="PNG", optimize=True)


@contextmanager
def browser_page(
    width: int,
    height: int,
    *,
    scale: int = 1,
    dark: bool = False,
) -> Iterator[object]:
    """Abre una página de Chromium y la cierra al salir del contexto."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=scale,
            color_scheme="dark" if dark else "light",
        )
        page = context.new_page()
        try:
            yield page
        finally:
            context.close()
            browser.close()


def _shoot(
    page: object,
    out: Path,
    *,
    selector: str | None = None,
    full_page: bool = False,
    omit_background: bool = False,
    max_kb: int = 500,
) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    if selector:
        page.locator(selector).screenshot(  # type: ignore[attr-defined]
            path=str(out), omit_background=omit_background
        )
    else:
        page.screenshot(  # type: ignore[attr-defined]
            path=str(out), full_page=full_page, omit_background=omit_background
        )
    optimize_png(out, max_kb=max_kb)


def render_html(
    body: str,
    out: Path,
    *,
    width: int,
    height: int,
    scale: int = 1,
    full_page: bool = False,
    selector: str | None = None,
    wait_ms: int = 300,
    dark: bool = False,
    max_kb: int = 500,
    css: str = "",
    title: str = "NovaBank asset",
) -> None:
    html_doc = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{css}</style>
</head>
<body>{body}</body>
</html>"""
    with browser_page(width, height, scale=scale, dark=dark) as page:
        page.set_content(html_doc, wait_until="load")  # type: ignore[attr-defined]
        page.wait_for_timeout(wait_ms)  # type: ignore[attr-defined]
        _shoot(
            page,
            out,
            selector=selector,
            full_page=full_page,
            max_kb=max_kb,
        )


def render_svg(
    svg: str,
    out: Path,
    *,
    width: int,
    height: int,
    scale: int = 1,
    transparent: bool = True,
    max_kb: int = 500,
) -> None:
    body = (
        f'<div style="width:{width}px;height:{height}px;overflow:hidden">'
        f'<div style="width:{width}px;height:{height}px">{svg}</div></div>'
    )
    css = (
        "html,body{margin:0;padding:0;background:transparent;}"
        f"svg{{display:block;width:{width}px;height:{height}px;}}"
    )
    html_doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body>{body}</body></html>"""
    with browser_page(width, height, scale=scale) as page:
        page.set_content(html_doc, wait_until="load")  # type: ignore[attr-defined]
        _shoot(page, out, omit_background=transparent, max_kb=max_kb)


def render_png_cover(
    source: Path,
    out: Path,
    *,
    width: int,
    height: int,
    background: str = PALETTE["navy_900"],
    padding: int = 40,
    max_kb: int = 500,
) -> None:
    """Compone un PNG de un solo color con una imagen centrada y su escala."""
    with Image.open(source) as image:
        image = image.convert("RGBA")
        image.thumbnail((width - padding * 2, height - padding * 2), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (width, height), background)
        x = (width - image.width) // 2
        y = (height - image.height) // 2
        canvas.alpha_composite(image, (x, y))
        canvas.convert("RGB").save(out, format="PNG", optimize=True)
    optimize_png(out, max_kb=max_kb)


def images_under(path: Path) -> Iterable[Path]:
    return sorted(
        item
        for item in path.rglob("*")
        if item.suffix.lower() in {".png", ".gif", ".jpg", ".jpeg", ".webp", ".svg"}
    )


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")
