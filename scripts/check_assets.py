"""Valida existencia, peso, dimensiones y referencias de los activos visuales."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from urllib.parse import unquote

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
MAX_PNG = 500 * 1024
MAX_GIF = 5 * 1024 * 1024
MAX_PDF = 10 * 1024 * 1024

REQUIRED = [
    "brand/logo-horizontal.svg",
    "brand/logo-horizontal-dark.svg",
    "brand/isotipo.svg",
    "brand/isotipo-dark.svg",
    "brand/favicon.svg",
    "brand/favicon.ico",
    "img/banner-light.png",
    "img/banner-dark.png",
    "img/social-preview.png",
    "img/demo.gif",
    "img/demo-poster.png",
    "img/dashboard-light.png",
    "img/dashboard-dark.png",
    "img/architecture.png",
    "img/sequence-instant.png",
    "img/sequence-international.png",
    "img/chart-daily-volume.png",
    "img/chart-currency-mix.png",
    "img/chart-instant-latency.png",
    "img/chart-alerts-by-rule.png",
    "img/chart-rule-quality.png",
    "img/chart-confusion-matrix.png",
    "dashboard/index.html",
    "ux/index.html",
    "linkedin/portada-linkedin.png",
    "linkedin/carousel-novabank.pdf",
]

REFERENCE_FILES = [
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "docs" / "linkedin.md",
    ROOT / "docs" / "case-study.md",
    ROOT / "docs" / "assets" / "brand" / "brand.md",
    ROOT / "docs" / "assets" / "ux" / "index.html",
    ROOT / "docs" / "assets" / "dashboard" / "index.html",
    ROOT / "docs" / "site" / "index.html",
]

MD_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
HTML_IMAGE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
HTML_SRC = re.compile(r'\bsrc\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
HTML_ALT = re.compile(r'\balt\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)
HTML_PICTURE_SOURCE = re.compile(r'<source\b[^>]*>', re.IGNORECASE)
SOURCE_SRCSET = re.compile(r'\bsrcset\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)


def _is_local(reference: str) -> bool:
    value = reference.strip()
    return bool(value) and not value.startswith(
        ("#", "http://", "https://", "data:", "mailto:", "tel:", "javascript:")
    )


def _resolve(base_file: Path, reference: str) -> Path | None:
    value = unquote(html.unescape(reference.strip())).split("#", 1)[0].split("?", 1)[0]
    if not _is_local(value):
        return None
    # GitHub Pages site: docs/site/index.html references assets/... which map to docs/assets/ at deploy time
    if base_file.parent == ROOT / "docs" / "site" and value.startswith("assets/"):
        return (ROOT / "docs" / value).resolve()
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    return (base_file.parent / candidate).resolve()


def _check_references(errors: list[str]) -> int:
    checked = 0
    for path in REFERENCE_FILES:
        if not path.exists():
            errors.append(f"Falta el archivo de referencia: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        references: list[tuple[str, str, str]] = []
        for alt, reference in MD_IMAGE.findall(text):
            references.append((reference, alt, "markdown"))
        for tag in HTML_IMAGE.findall(text):
            src = HTML_SRC.search(tag)
            alt = HTML_ALT.search(tag)
            if src:
                references.append((src.group(1), alt.group(1) if alt else None, "html"))
        for tag in HTML_PICTURE_SOURCE.findall(text):
            srcset = SOURCE_SRCSET.search(tag)
            if srcset:
                for item in srcset.group(1).split(","):
                    references.append((item.strip().split(" ")[0], "", "picture"))

        for reference, alt, kind in references:
            target = _resolve(path, reference)
            if target is None:
                continue
            checked += 1
            if not target.exists():
                errors.append(
                    f"Referencia rota en {path.relative_to(ROOT)}: {reference}"
                )
            if kind == "markdown" and not (alt or "").strip():
                errors.append(
                    f"Imagen sin texto alternativo en {path.relative_to(ROOT)}: {reference}"
                )
            if kind == "html" and alt is None:
                errors.append(
                    f"Imagen sin atributo alt en {path.relative_to(ROOT)}: {reference}"
                )
    return checked


def _check_required(errors: list[str]) -> int:
    for relative in REQUIRED:
        path = ASSETS / relative
        if not path.exists():
            errors.append(f"Falta el activo requerido: docs/assets/{relative}")
    return len(REQUIRED)


def _check_sizes(errors: list[str]) -> int:
    checked = 0
    for path in sorted(ASSETS.rglob("*")):
        if not path.is_file():
            continue
        size = path.stat().st_size
        suffix = path.suffix.lower()
        if suffix == ".png":
            checked += 1
            if size > MAX_PNG:
                errors.append(f"PNG supera 500 KB: {path.relative_to(ROOT)} ({size // 1024} KB)")
        elif suffix == ".gif":
            checked += 1
            if size > MAX_GIF:
                errors.append(f"GIF supera 5 MB: {path.relative_to(ROOT)} ({size // 1024} KB)")
        elif suffix == ".pdf":
            checked += 1
            if size > MAX_PDF:
                errors.append(f"PDF supera 10 MB: {path.relative_to(ROOT)} ({size // 1024} KB)")
            elif path.read_bytes()[:4] != b"%PDF":
                errors.append(f"PDF inválido: {path.relative_to(ROOT)}")
    return checked


def _check_images(errors: list[str]) -> int:
    checked = 0
    for path in sorted(ASSETS.rglob("*.png")):
        checked += 1
        try:
            with Image.open(path) as image:
                width, height = image.size
                if width < 16 or height < 16:
                    errors.append(f"PNG demasiado pequeño: {path.relative_to(ROOT)} ({width}x{height})")
                if "carousel" in path.parts and (width, height) != (1080, 1350):
                    errors.append(f"Carrusel fuera de 1080x1350: {path.relative_to(ROOT)} ({width}x{height})")
                if path.name == "demo-poster.png" and (width, height) != (1280, 800):
                    errors.append(f"Póster de demo fuera de 1280x800: {width}x{height}")
        except Exception as exc:
            errors.append(f"No se pudo leer {path.relative_to(ROOT)}: {exc}")
    return checked


def _check_gif(errors: list[str]) -> int:
    path = ASSETS / "img" / "demo.gif"
    if not path.exists():
        return 0
    try:
        with Image.open(path) as image:
            frames = getattr(image, "n_frames", 1)
            if frames < 5:
                errors.append(f"El GIF tiene muy pocos frames: {frames}")
            return frames
    except Exception as exc:
        errors.append(f"No se pudo leer demo.gif: {exc}")
        return 0


def main() -> int:
    errors: list[str] = []
    required = _check_required(errors)
    references = _check_references(errors)
    sizes = _check_sizes(errors)
    images = _check_images(errors)
    frames = _check_gif(errors)

    if errors:
        print("check_assets: FALLÓ")
        for error in errors:
            print(f" - {error}")
        return 1

    print("check_assets: OK")
    print(f" - activos requeridos: {required}")
    print(f" - referencias locales: {references}")
    print(f" - archivos con límite de peso: {sizes}")
    print(f" - PNG validados: {images}")
    print(f" - frames del GIF: {frames}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
