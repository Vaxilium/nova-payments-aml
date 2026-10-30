"""Capturas PNG de los wireframes SVG y galería UX."""

from __future__ import annotations

from pathlib import Path

from .assetlib import ASSETS, IMG_DIR, ROOT, render_svg, write_text

WIREFRAME_DIR = ROOT / "04-diseno-ux" / "wireframes"
UX_DIR = IMG_DIR / "ux"

CAPTURES = [
    ("APP-01-inicio.svg", "ux-app-home.png", "Inicio de la app", 390, 844, 2),
    ("APP-02-transferencia-local.svg", "ux-app-local.png", "Transferencia local", 390, 844, 2),
    ("APP-03-transferencia-internacional.svg", "ux-app-international.png", "Transferencia internacional", 390, 844, 2),
    ("APP-04-confirmacion.svg", "ux-app-confirmation.png", "Confirmación", 390, 844, 2),
    ("APP-05-comprobante.svg", "ux-app-receipt.png", "Comprobante", 390, 844, 2),
    ("APP-06-error.svg", "ux-app-error.png", "Error controlado", 390, 844, 2),
    ("AML-01-bandeja-alertas.svg", "ux-aml-inbox.png", "Bandeja de alertas", 1440, 900, 1),
    ("AML-02-detalle-caso.svg", "ux-aml-case.png", "Detalle de caso", 1440, 900, 1),
    ("AML-03-historial-cliente.svg", "ux-aml-history.png", "Historial del cliente", 1440, 900, 1),
    ("AML-04-cierre-caso.svg", "ux-aml-closure.png", "Cierre de caso", 1440, 900, 1),
]


def render_captures() -> list[Path]:
    UX_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for filename, png_name, _, width, height, scale in CAPTURES:
        svg = (WIREFRAME_DIR / filename).read_text(encoding="utf-8")
        out = UX_DIR / png_name
        render_svg(svg, out, width=width, height=height, scale=scale, max_kb=500)
        outputs.append(out)
    return outputs


def write_gallery() -> Path:
    cards = []
    for filename, png_name, label, width, height, _ in CAPTURES:
        cards.append(
            f"""<article class="card">
            <a href="../img/ux/{png_name}"><img src="../img/ux/{png_name}" alt="Wireframe: {label}" loading="lazy"></a>
            <div class="meta"><h2>{label}</h2><p>{width} × {height} · baja fidelidad</p>
            <a href="../../../04-diseno-ux/wireframes/{filename}">Abrir SVG</a></div></article>"""
        )
    app_cards = "".join(cards[:6])
    aml_cards = "".join(cards[6:])
    body = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wireframes · NovaBank</title>
<link rel="icon" href="../brand/favicon.svg" type="image/svg+xml">
<style>
* {{ box-sizing:border-box; }}
body {{ margin:0; background:#F8FAFC; color:#0F172A;
  font-family:"Segoe UI",Inter,system-ui,sans-serif; }}
header {{ background:#071A2F; color:#fff; padding:44px 48px; }}
header h1 {{ margin:0 0 10px; font-size:30px; }}
header p {{ color:#CBD5E1; max-width:820px; line-height:1.55; margin:0; }}
main {{ max-width:1400px; margin:0 auto; padding:28px; }}
section {{ margin-bottom:34px; }}
section > h2 {{ font-size:18px; margin:0 0 12px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:18px; }}
.card {{ background:#fff; border:1px solid #E2E8F0; border-radius:14px; overflow:hidden;
  display:flex; flex-direction:column; }}
.card img {{ width:100%; height:320px; object-fit:contain; background:#fff; border-bottom:1px solid #E2E8F0; }}
.meta {{ padding:14px 16px; }}
.meta h3 {{ font-size:15px; margin:0 0 3px; }}
.meta p {{ color:#64748B; font-size:12px; margin:0 0 9px; }}
a {{ color:#155E8A; font-size:12px; font-weight:700; text-decoration:none; }}
footer {{ max-width:1400px; margin:0 auto; padding:0 28px 40px; color:#64748B; font-size:12px; }}
</style></head>
<body><header><h1>Wireframes · NovaBank</h1>
<p>Bocetos de baja fidelidad de la app de transferencias y la consola AML.
Son especificaciones visuales del caso ficticio, no capturas de una herramienta operada.</p></header>
<main>
<section><h2>App de transferencias</h2><div class="grid">{app_cards}</div></section>
<section><h2>Consola AML</h2><div class="grid">{aml_cards}</div></section>
</main>
<footer>Datos ficticios · sin PII · SVG originales en <code>04-diseno-ux/wireframes/</code>.</footer>
</body></html>"""
    path = ASSETS / "ux" / "index.html"
    write_text(path, body)
    return path


def render_all() -> list[Path]:
    outputs = render_captures()
    outputs.append(write_gallery())
    return outputs
