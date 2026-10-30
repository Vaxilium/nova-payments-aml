"""Orquestador reproducible de los activos visuales de NovaBank.

Uso:
    python -m scripts.make_assets --only brand
    python -m scripts.make_assets --only charts
    python -m scripts.make_assets --only diagrams
    python -m scripts.make_assets --only ux
    python -m scripts.make_assets --only demo
    python -m scripts.make_assets --all

Las dependencias de generación están en requirements-assets.txt.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

from .assetlib import (
    BRAND_DIR,
    IMG_DIR,
    PALETTE,
    ROOT,
    ensure_dirs,
    render_svg,
    write_text,
)
from .brand import write_brand_sources
from .covers import render_all as render_covers
from .dashboard import render_all as render_dashboard
from .diagrams import render_all as render_diagrams
from .carousel import render_all as render_carousel
from .charts import render_all as render_charts
from .data import dataset
from .demo import render_all as render_demo
from .ux import render_all as render_ux


def render_brand_pngs() -> list[Path]:
    outputs: list[Path] = []

    def capture(svg_name: str, png_name: str, width: int, height: int, scale: int = 1) -> Path:
        out = BRAND_DIR / png_name
        render_svg(
            (BRAND_DIR / svg_name).read_text(encoding="utf-8"),
            out,
            width=width,
            height=height,
            scale=scale,
            max_kb=500,
        )
        outputs.append(out)
        return out

    capture("logo-horizontal.svg", "logo-horizontal-512.png", 400, 80, 1)
    capture("logo-horizontal.svg", "logo-horizontal-1024.png", 400, 80, 2)
    capture("logo-horizontal.svg", "logo-horizontal-1600.png", 400, 80, 4)
    capture("logo-horizontal-dark.svg", "logo-horizontal-dark-1024.png", 400, 80, 2)
    capture("isotipo.svg", "isotipo-32.png", 32, 32)
    capture("isotipo.svg", "isotipo-128.png", 128, 128)
    capture("isotipo.svg", "isotipo-512.png", 512, 512)
    capture("isotipo-dark.svg", "isotipo-dark-512.png", 512, 512)
    capture("favicon.svg", "favicon-32.png", 32, 32)
    capture("favicon.svg", "favicon-64.png", 64, 64)
    capture("favicon.svg", "apple-touch-icon.png", 180, 180)

    icon_path = BRAND_DIR / "favicon.ico"
    with Image.open(BRAND_DIR / "favicon-64.png") as icon:
        icon.save(icon_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    outputs.append(icon_path)
    return outputs


def run_brand() -> None:
    write_brand_sources()
    render_brand_pngs()


def run_charts() -> None:
    render_charts(dataset())


def run_diagrams() -> None:
    render_diagrams()


def run_covers() -> None:
    render_covers()


def run_dashboard() -> None:
    render_dashboard()


def run_ux() -> None:
    render_ux()


def run_demo() -> None:
    render_demo()


def run_linkedin() -> None:
    render_carousel()


STEPS = {
    "brand": run_brand,
    "charts": run_charts,
    "diagrams": run_diagrams,
    "covers": run_covers,
    "dashboard": run_dashboard,
    "ux": run_ux,
    "demo": run_demo,
    "linkedin": run_linkedin,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Genera los activos visuales de NovaBank.")
    parser.add_argument(
        "--only",
        choices=sorted(STEPS),
        action="append",
        help="Genera solo el paso indicado. Se puede repetir.",
    )
    parser.add_argument("--all", action="store_true", help="Genera todos los pasos disponibles.")
    args = parser.parse_args(argv)

    if not args.all and not args.only:
        parser.print_help()
        return 2

    ensure_dirs()
    selected = list(STEPS) if args.all else list(dict.fromkeys(args.only or []))
    for name in selected:
        print(f"[assets] {name}...")
        STEPS[name]()
    print(f"[assets] listo · {len(selected)} paso(s) · salida en {ROOT / 'docs' / 'assets'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
