"""Genera los wireframes SVG de baja fidelidad y la galería HTML.

Uso:
    python 04-diseno-ux/wireframes/generar_wireframes.py

No depende de librerías externas. Los SVG son estáticos y se pueden abrir
directamente en el navegador o en GitHub.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent

PALETTE = {
    "navy": "#0B3B60",
    "blue": "#155E8A",
    "blue_soft": "#DCEBF5",
    "teal": "#0F766E",
    "teal_soft": "#CCFBF1",
    "ink": "#111827",
    "muted": "#4B5563",
    "line": "#D1D5DB",
    "surface": "#FFFFFF",
    "bg": "#F3F4F6",
    "warn": "#B45309",
    "warn_soft": "#FEF3C7",
    "danger": "#B91C1C",
    "danger_soft": "#FEE2E2",
    "info": "#1D4ED8",
    "info_soft": "#DBEAFE",
}

FONT = "Inter, Segoe UI, system-ui, sans-serif"


def esc(value: str) -> str:
    return escape(str(value), quote=True)


def text(
    x: float,
    y: float,
    value: str,
    *,
    size: int = 13,
    weight: int = 400,
    fill: str = PALETTE["ink"],
    anchor: str = "start",
    family: str = FONT,
) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(value)}</text>'
    )


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str = PALETTE["surface"],
    stroke: str | None = PALETTE["line"],
    rx: int = 8,
    sw: float = 1,
    dashed: bool = False,
) -> str:
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    stroke_attr = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{stroke_attr}{dash}/>'


def line(x1: float, y1: float, x2: float, y2: float, *, stroke: str = PALETTE["line"], sw: float = 1, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{dash}/>'


def circle(cx: float, cy: float, r: float, *, fill: str = "none", stroke: str | None = None, sw: float = 1) -> str:
    stroke_attr = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{stroke_attr}/>'


def button(
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    *,
    variant: str = "primary",
) -> str:
    if variant == "primary":
        fill, stroke, color = PALETTE["blue"], None, "#FFFFFF"
    elif variant == "danger":
        fill, stroke, color = PALETTE["danger"], None, "#FFFFFF"
    else:
        fill, stroke, color = PALETTE["surface"], PALETTE["blue"], PALETTE["blue"]
    return (
        rect(x, y, w, h, fill=fill, stroke=stroke, rx=8)
        + text(x + w / 2, y + h / 2 + 5, label, size=13, weight=600, fill=color, anchor="middle")
    )


def badge(x: float, y: float, label: str, *, kind: str = "info") -> str:
    fills = {
        "p1": (PALETTE["danger_soft"], PALETTE["danger"]),
        "p2": (PALETTE["warn_soft"], PALETTE["warn"]),
        "p3": (PALETTE["bg"], PALETTE["muted"]),
        "ok": (PALETTE["teal_soft"], PALETTE["teal"]),
        "info": (PALETTE["blue_soft"], PALETTE["blue"]),
        "warn": (PALETTE["warn_soft"], PALETTE["warn"]),
        "danger": (PALETTE["danger_soft"], PALETTE["danger"]),
    }
    bg, fg = fills.get(kind, fills["info"])
    width = max(54, len(label) * 7 + 16)
    return rect(x, y, width, 22, fill=bg, stroke=None, rx=11) + text(
        x + width / 2, y + 15, label, size=11, weight=600, fill=fg, anchor="middle"
    )


def input_field(
    x: float,
    y: float,
    w: float,
    label: str,
    placeholder: str,
    *,
    h: int = 44,
    value: str | None = None,
    error: str | None = None,
    hint: str | None = None,
    required: bool = True,
) -> str:
    parts = [text(x, y - 8, label + (" *" if required else ""), size=12, weight=600, fill=PALETTE["muted"])]
    border = PALETTE["danger"] if error else PALETTE["line"]
    parts.append(rect(x, y, w, h, fill=PALETTE["surface"], stroke=border, rx=6))
    shown = value if value is not None else placeholder
    color = PALETTE["ink"] if value is not None else "#9CA3AF"
    parts.append(text(x + 12, y + 27, shown, size=13, fill=color))
    if error:
        parts.append(text(x, y + h + 16, error, size=11, fill=PALETTE["danger"]))
    elif hint:
        parts.append(text(x, y + h + 16, hint, size=11, fill=PALETTE["muted"]))
    return "".join(parts)


def app_header(title: str, subtitle: str = "") -> str:
    parts = [
        rect(0, 0, 390, 64, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=0),
        circle(28, 32, 15, fill=PALETTE["blue_soft"], stroke=None),
        text(28, 37, "N", size=15, weight=700, fill=PALETTE["navy"], anchor="middle"),
        text(52, 28, title, size=15, weight=700),
        text(52, 45, subtitle, size=11, fill=PALETTE["muted"]),
        circle(360, 32, 14, fill=PALETTE["bg"], stroke=PALETTE["line"]),
        text(360, 36, "FT", size=10, weight=700, fill=PALETTE["muted"], anchor="middle"),
    ]
    return "".join(parts)


def app_back_header(title: str, subtitle: str = "") -> str:
    parts = [
        rect(0, 0, 390, 64, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=0),
        text(20, 38, "‹", size=26, weight=400, fill=PALETTE["blue"]),
        text(44, 28, title, size=15, weight=700),
        text(44, 45, subtitle, size=11, fill=PALETTE["muted"]),
    ]
    return "".join(parts)


def bottom_nav(active: str) -> str:
    labels = ["Inicio", "Transferir", "Movimientos", "Perfil"]
    parts = [rect(0, 796, 390, 48, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=0)]
    step = 390 / len(labels)
    for index, label in enumerate(labels):
        cx = step * index + step / 2
        color = PALETTE["blue"] if label == active else PALETTE["muted"]
        parts.append(circle(cx, 816, 7, fill=PALETTE["blue_soft"] if label == active else "none", stroke=color))
        parts.append(text(cx, 837, label, size=10, weight=600 if label == active else 400, fill=color, anchor="middle"))
    return "".join(parts)


def desktop_frame(title: str, subtitle: str, active_nav: str) -> tuple[list[str], str]:
    parts = [
        rect(0, 0, 1440, 900, fill=PALETTE["bg"], stroke=None, rx=0),
        rect(0, 0, 232, 900, fill=PALETTE["navy"], stroke=None, rx=0),
        text(24, 44, "NovaBank", size=20, weight=700, fill="#FFFFFF"),
        text(24, 64, "Payments & AML Hub", size=11, fill="#BFDBFE"),
        line(24, 84, 208, 84, stroke="#1E4E73"),
    ]
    nav_items = [
        ("▤", "Bandeja de alertas"),
        ("▦", "Casos"),
        ("◉", "Clientes"),
        ("⚙", "Reglas"),
        ("▥", "Reportes"),
    ]
    y = 118
    for icon, label in nav_items:
        selected = label == active_nav
        if selected:
            parts.append(rect(12, y - 20, 208, 36, fill="#155E8A", stroke=None, rx=6))
        parts.append(text(30, y + 3, icon, size=15, fill="#FFFFFF" if selected else "#93C5FD"))
        parts.append(text(56, y + 3, label, size=13, weight=600 if selected else 400, fill="#FFFFFF" if selected else "#DBEAFE"))
        y += 48
    parts.extend(
        [
            line(24, 760, 208, 760, stroke="#1E4E73"),
            circle(40, 798, 14, fill="#155E8A", stroke=None),
            text(40, 802, "AM", size=10, weight=700, fill="#FFFFFF", anchor="middle"),
            text(64, 796, "Ana Martínez", size=12, weight=600, fill="#FFFFFF"),
            text(64, 812, "Analista AML", size=10, fill="#BFDBFE"),
            rect(232, 0, 1208, 64, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=0),
            text(264, 28, title, size=20, weight=700),
            text(264, 47, subtitle, size=11, fill=PALETTE["muted"]),
            rect(940, 16, 300, 34, fill=PALETTE["bg"], stroke=PALETTE["line"], rx=6),
            text(956, 38, "Buscar alerta, caso o cliente…", size=12, fill="#9CA3AF"),
            circle(1280, 32, 14, fill=PALETTE["warn_soft"], stroke=None),
            text(1280, 36, "3", size=10, weight=700, fill=PALETTE["warn"], anchor="middle"),
            circle(1320, 32, 14, fill=PALETTE["blue_soft"], stroke=None),
            text(1320, 36, "AM", size=10, weight=700, fill=PALETTE["blue"], anchor="middle"),
            text(1348, 28, "Ana Martínez", size=12, weight=600),
            text(1348, 43, "Cumplimiento", size=10, fill=PALETTE["muted"]),
            text(1360, 72, "Boceto de baja fidelidad · 1440 × 900", size=9, fill="#9CA3AF", anchor="end"),
        ]
    )
    return parts, ""


def wrap(width: int, height: int, title: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
        f"<title id=\"title\">{esc(title)}</title>"
        f"<desc id=\"desc\">Wireframe de baja fidelidad de {esc(title)}. "
        f"Caso ficticio NovaBank.</desc>"
        f'<rect width="{width}" height="{height}" fill="{PALETTE["bg"]}"/>'
        f"{body}</svg>"
    )


def app_inicio() -> str:
    parts = [
        app_header("NovaBank", "Hola, Lucía"),
        text(20, 96, "Disponible", size=12, weight=600, fill=PALETTE["muted"]),
        text(20, 132, "₲ 12.450.000", size=28, weight=700, fill=PALETTE["navy"]),
        text(20, 156, "Cuenta •••• 5678 · PYG", size=12, fill=PALETTE["muted"]),
        button(270, 104, 100, 36, "Ver detalle", variant="secondary"),
        line(0, 180, 390, 180),
        button(20, 200, 108, 48, "Transferir"),
        button(141, 200, 108, 48, "Pagar", variant="secondary"),
        button(262, 200, 108, 48, "Movimientos", variant="secondary"),
        rect(20, 268, 350, 58, fill=PALETTE["warn_soft"], stroke=None, rx=8),
        text(36, 290, "Operación en revisión", size=12, weight=700, fill=PALETTE["warn"]),
        text(36, 308, "Tu transferencia internacional está siendo verificada.", size=11, fill=PALETTE["warn"]),
        text(20, 360, "Últimas operaciones", size=15, weight=700),
        text(348, 360, "Ver todas", size=11, weight=600, fill=PALETTE["blue"], anchor="end"),
    ]
    rows = [
        ("Transferencia a María G.", "Hoy · 10:24", "− ₲ 850.000", "Acreditada", "ok"),
        ("Depósito de sueldo", "Ayer · 08:02", "+ ₲ 6.200.000", "Acreditado", "ok"),
        ("Transferencia a Juan P.", "27/10 · 18:40", "− ₲ 1.300.000", "En revisión", "warn"),
    ]
    y = 384
    for name, date, amount, status, kind in rows:
        parts.append(rect(20, y, 350, 64, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8))
        parts.append(circle(46, y + 32, 16, fill=PALETTE["blue_soft"], stroke=None))
        parts.append(text(46, y + 36, "↔", size=14, weight=700, fill=PALETTE["blue"], anchor="middle"))
        parts.append(text(72, y + 26, name, size=13, weight=600))
        parts.append(text(72, y + 44, date, size=11, fill=PALETTE["muted"]))
        parts.append(text(354, y + 26, amount, size=13, weight=700, anchor="end"))
        parts.append(badge(274, y + 36, status, kind=kind))
        y += 76
    parts.append(bottom_nav("Inicio"))
    return wrap(390, 844, "APP-01 Inicio", "".join(parts))


def app_local() -> str:
    parts = [
        app_back_header("Nueva transferencia", "Paso 1 de 2"),
        rect(20, 80, 170, 40, fill=PALETTE["blue"], stroke=None, rx=6),
        text(105, 105, "Local (SPI)", size=12, weight=700, fill="#FFFFFF", anchor="middle"),
        rect(200, 80, 170, 40, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=6),
        text(285, 105, "Internacional", size=12, weight=600, fill=PALETTE["blue"], anchor="middle"),
        input_field(20, 156, 350, "Cuenta origen", "", value="Cuenta •••• 5678 · PYG"),
        input_field(20, 240, 350, "Alias o cuenta destino", "Ej.: maria.gomez o 00000000001234", value="maria.gomez"),
        input_field(20, 324, 350, "Nombre del destinatario", "", value="María Gómez", required=False, hint="Se completa al validar el alias."),
        input_field(20, 408, 350, "Importe", "0", value="₲ 850.000", hint="Máximo ₲ 10.000.000 por operación."),
        input_field(20, 492, 350, "Concepto", "Seleccioná un motivo", value="Pago personal", required=False),
        rect(20, 570, 350, 58, fill=PALETTE["info_soft"], stroke=None, rx=8),
        text(36, 592, "Transferencia instantánea", size=12, weight=700, fill=PALETTE["info"]),
        text(36, 610, "Disponible 24/7. Acreditación objetivo: hasta 5 segundos.", size=11, fill=PALETTE["info"]),
        rect(0, 760, 390, 84, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=0),
        text(20, 788, "Total a transferir", size=11, fill=PALETTE["muted"]),
        text(20, 810, "₲ 850.000", size=18, weight=700),
        button(180, 780, 190, 44, "Continuar"),
    ]
    return wrap(390, 844, "APP-02 Nueva transferencia local", "".join(parts))


def app_international() -> str:
    parts = [
        app_back_header("Transferencia internacional", "Paso 1 de 2"),
        rect(20, 80, 350, 52, fill=PALETTE["warn_soft"], stroke=None, rx=8),
        text(36, 101, "Puede demorar hasta 2 días hábiles", size=12, weight=700, fill=PALETTE["warn"]),
        text(36, 119, "La comisión se muestra antes de confirmar.", size=11, fill=PALETTE["warn"]),
        input_field(20, 156, 350, "Cuenta origen", "", value="Cuenta •••• 9012 · USD"),
        input_field(20, 232, 165, "País destino", "País", value="España"),
        input_field(205, 232, 165, "Moneda", "USD / EUR", value="EUR"),
        input_field(20, 308, 350, "BIC / SWIFT", "8 u 11 caracteres", value="NVBKESMM"),
        input_field(20, 384, 350, "IBAN / cuenta", "ES00 0000 0000 0000 0000", value="ES91 2100 0418 4502 0005 1332"),
        input_field(20, 460, 350, "Nombre del beneficiario", "", value="Carlos Ruiz"),
        input_field(20, 536, 350, "Importe", "0,00", value="EUR 1.250,00"),
        rect(20, 612, 350, 76, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
        text(36, 634, "Resumen de costos", size=12, weight=700),
        text(36, 654, "Comisión estimada", size=11, fill=PALETTE["muted"]),
        text(354, 654, "USD 25,00", size=11, weight=600, anchor="end"),
        text(36, 674, "Total a debitar", size=12, weight=700),
        text(354, 674, "USD 1.275,00", size=12, weight=700, anchor="end"),
        rect(0, 760, 390, 84, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=0),
        text(20, 788, "Total estimado", size=11, fill=PALETTE["muted"]),
        text(20, 810, "USD 1.275,00", size=18, weight=700),
        button(180, 780, 190, 44, "Continuar"),
    ]
    return wrap(390, 844, "APP-03 Nueva transferencia internacional", "".join(parts))


def app_confirm() -> str:
    parts = [
        app_back_header("Revisá y confirmá", "Paso 2 de 2"),
        rect(20, 88, 350, 250, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
        text(36, 116, "Transferencia local", size=15, weight=700),
        badge(280, 100, "SPI", kind="info"),
        line(36, 132, 354, 132),
        text(36, 160, "Destinatario", size=11, fill=PALETTE["muted"]),
        text(354, 160, "María Gómez", size=13, weight=600, anchor="end"),
        text(36, 190, "Alias", size=11, fill=PALETTE["muted"]),
        text(354, 190, "maria.gomez", size=13, anchor="end"),
        text(36, 220, "Cuenta origen", size=11, fill=PALETTE["muted"]),
        text(354, 220, "•••• 5678 · PYG", size=13, anchor="end"),
        text(36, 250, "Concepto", size=11, fill=PALETTE["muted"]),
        text(354, 250, "Pago personal", size=13, anchor="end"),
        line(36, 270, 354, 270),
        text(36, 298, "Total a transferir", size=12, weight=700),
        text(354, 298, "₲ 850.000", size=20, weight=700, fill=PALETTE["navy"], anchor="end"),
        rect(20, 354, 350, 54, fill=PALETTE["info_soft"], stroke=None, rx=8),
        text(36, 376, "Autorización requerida", size=12, weight=700, fill=PALETTE["info"]),
        text(36, 394, "Ingresá tu PIN de 6 dígitos para confirmar.", size=11, fill=PALETTE["info"]),
        input_field(20, 436, 350, "PIN de seguridad", "••••••", value="••••••", required=True),
        rect(20, 522, 350, 42, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=6),
        text(36, 548, "☐  Guardar este destinatario", size=12),
        text(20, 594, "Una vez confirmada, la operación no se puede cancelar.", size=11, fill=PALETTE["muted"]),
        button(20, 700, 350, 46, "Confirmar transferencia"),
        button(20, 756, 350, 40, "Editar datos", variant="secondary"),
    ]
    return wrap(390, 844, "APP-04 Confirmación", "".join(parts))


def app_receipt() -> str:
    parts = [
        app_header("Comprobante", "Transferencia realizada"),
        circle(195, 150, 42, fill=PALETTE["teal_soft"], stroke=None),
        text(195, 163, "✓", size=38, weight=700, fill=PALETTE["teal"], anchor="middle"),
        text(195, 222, "₲ 850.000", size=30, weight=700, fill=PALETTE["navy"], anchor="middle"),
        text(195, 248, "Acreditada a María Gómez", size=13, fill=PALETTE["muted"], anchor="middle"),
        rect(20, 278, 350, 238, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
        text(36, 306, "Comprobante N.º TX-000012345", size=13, weight=700),
        line(36, 320, 354, 320),
    ]
    rows = [
        ("Fecha y hora", "29/10/2026 · 10:24"),
        ("Cuenta origen", "•••• 5678 · PYG"),
        ("Destinatario", "María Gómez"),
        ("Alias", "maria.gomez"),
        ("Concepto", "Pago personal"),
        ("Comisión", "₲ 0"),
    ]
    y = 348
    for label, value in rows:
        parts.append(text(36, y, label, size=11, fill=PALETTE["muted"]))
        parts.append(text(354, y, value, size=12, weight=600, anchor="end"))
        y += 26
    parts.append(text(20, 554, "Estado de la operación", size=13, weight=700))
    steps = ["Recibida", "Validada", "Enviada", "Acreditada"]
    x = 42
    for index, step in enumerate(steps):
        parts.append(circle(x, 594, 11, fill=PALETTE["teal"], stroke=None))
        parts.append(text(x, 598, "✓", size=10, weight=700, fill="#FFFFFF", anchor="middle"))
        parts.append(text(x, 624, step, size=10, fill=PALETTE["teal"], anchor="middle"))
        if index < len(steps) - 1:
            parts.append(line(x + 14, 594, x + 80, 594, stroke=PALETTE["teal"], sw=2))
        x += 94
    button(20, 680, 170, 44, "Descargar PDF", variant="secondary"),
    button(200, 680, 170, 44, "Compartir", variant="secondary"),
    button(20, 740, 350, 44, "Volver al inicio"),
    return wrap(390, 844, "APP-05 Comprobante", "".join(parts))


def app_error() -> str:
    parts = [
        app_header("Resultado de la operación", "No se completó"),
        circle(195, 150, 42, fill=PALETTE["danger_soft"], stroke=None),
        text(195, 164, "!", size=36, weight=700, fill=PALETTE["danger"], anchor="middle"),
        text(195, 222, "El servicio no está disponible", size=20, weight=700, anchor="middle"),
        text(195, 250, "No pudimos enviar la transferencia.", size=13, fill=PALETTE["muted"], anchor="middle"),
        text(195, 270, "No se debitó tu cuenta.", size=13, weight=600, fill=PALETTE["teal"], anchor="middle"),
        rect(20, 306, 350, 94, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
        text(36, 334, "Referencia", size=11, fill=PALETTE["muted"]),
        text(354, 334, "ERR-RIEL-503", size=12, weight=600, anchor="end"),
        text(36, 362, "Operación", size=11, fill=PALETTE["muted"]),
        text(354, 362, "TX-000012346", size=12, weight=600, anchor="end"),
        text(36, 390, "Fecha y hora", size=11, fill=PALETTE["muted"]),
        text(354, 390, "29/10/2026 · 10:31", size=12, weight=600, anchor="end"),
        button(20, 428, 350, 44, "Reintentar"),
        button(20, 484, 350, 44, "Corregir datos", variant="secondary"),
        button(20, 540, 350, 44, "Volver al inicio", variant="secondary"),
        rect(20, 612, 350, 84, fill=PALETTE["info_soft"], stroke=None, rx=8),
        text(36, 636, "¿Necesitás ayuda?", size=12, weight=700, fill=PALETTE["info"]),
        text(36, 656, "Atención al cliente 24/7 desde la app.", size=11, fill=PALETTE["info"]),
        text(36, 676, "Tené a mano el número de referencia.", size=11, fill=PALETTE["info"]),
        text(195, 790, "Boceto de baja fidelidad · 390 × 844", size=9, fill="#9CA3AF", anchor="middle"),
    ]
    return wrap(390, 844, "APP-06 Error", "".join(parts))


def aml_inbox() -> str:
    parts, _ = desktop_frame("Bandeja de alertas", "Triage y priorización por riesgo y SLA", "Bandeja de alertas")
    counters = [
        ("Nuevas", "128", PALETTE["blue"]),
        ("P1 abiertas", "34", PALETTE["danger"]),
        ("Vencidas", "12", PALETTE["warn"]),
        ("En análisis", "61", PALETTE["teal"]),
    ]
    x = 264
    for label, value, color in counters:
        parts.append(rect(x, 84, 224, 72, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8))
        parts.append(text(x + 16, 108, label, size=11, fill=PALETTE["muted"]))
        parts.append(text(x + 16, 140, value, size=24, weight=700, fill=color))
        x += 240
    parts.append(rect(264, 172, 1144, 48, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8))
    filters = ["Prioridad: Todas", "Estado: Abiertas", "Regla: Todas", "Segmento: Todos", "Últimos 30 días"]
    x = 280
    for item in filters:
        parts.append(rect(x, 181, 170, 30, fill=PALETTE["bg"], stroke=PALETTE["line"], rx=6))
        parts.append(text(x + 10, 200, item, size=10, fill=PALETTE["muted"]))
        x += 182
    parts.append(button(1300, 181, 94, 30, "Filtros", variant="secondary"))
    parts.append(rect(264, 232, 1144, 38, fill=PALETTE["blue_soft"], stroke=None, rx=6))
    parts.append(text(280, 256, "12 alertas vencidas requieren atención", size=11, weight=600, fill=PALETTE["blue"]))
    headers = [("Prioridad", 280), ("Alerta", 370), ("Cliente", 500), ("Regla", 700), ("Score", 970), ("Estado", 1030), ("Asignada", 1160), ("Vence", 1270)]
    parts.append(rect(264, 280, 1144, 36, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=0))
    for label, x in headers:
        parts.append(text(x, 303, label, size=10, weight=700, fill=PALETTE["muted"]))
    rows = [
        ("P1", "ALT-000341", "CUS-000128 · RETAIL", "R07 · Alto riesgo", "94", "NUEVA", "Sin asignar", "Vencida"),
        ("P1", "ALT-000342", "CUS-000044 · CORPORATE", "R04 · Pass-through", "91", "EN_ANALISIS", "A. Martínez", "2 h 10 m"),
        ("P2", "ALT-000343", "CUS-000301 · SME", "R01 · Estructuración", "78", "NUEVA", "Sin asignar", "3 h 40 m"),
        ("P2", "ALT-000344", "CUS-000218 · PREMIUM", "R02 · Velocidad", "72", "ESCALADA", "L. Ferreira", "1 d 2 h"),
        ("P2", "ALT-000345", "CUS-000087 · RETAIL", "R05 · Redondos", "68", "EN_ANALISIS", "M. Benítez", "8 h"),
        ("P3", "ALT-000346", "CUS-000410 · SME", "R08 · Perfil", "55", "CERRADA_FP", "A. Martínez", "—"),
        ("P1", "ALT-000347", "CUS-000155 · CORPORATE", "R10 · Circulares", "88", "NUEVA", "Sin asignar", "45 min"),
    ]
    y = 316
    for priority, alert, customer, rule, score, status, assigned, due in rows:
        parts.append(rect(264, y, 1144, 54, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=0))
        parts.append(badge(280, y + 16, priority, kind=priority.lower()))
        parts.append(text(370, y + 22, alert, size=11, weight=600, fill=PALETTE["blue"]))
        parts.append(text(370, y + 39, "Hace 18 min", size=9, fill=PALETTE["muted"]))
        parts.append(text(500, y + 22, customer, size=11, weight=600))
        parts.append(text(500, y + 39, "Segmento y país", size=9, fill=PALETTE["muted"]))
        parts.append(text(700, y + 22, rule, size=11))
        parts.append(text(700, y + 39, "Score de riesgo", size=9, fill=PALETTE["muted"]))
        parts.append(text(970, y + 30, score, size=13, weight=700, fill=PALETTE["danger"] if int(score) >= 80 else PALETTE["ink"]))
        status_kind = "danger" if status == "NUEVA" else ("ok" if "CERRADA" in status else "warn")
        parts.append(badge(1030, y + 16, status, kind=status_kind))
        parts.append(text(1160, y + 30, assigned, size=11))
        parts.append(text(1270, y + 30, due, size=11, fill=PALETTE["danger"] if due == "Vencida" else PALETTE["muted"]))
        y += 54
    parts.append(text(280, 758, "Mostrando 1–7 de 128 alertas", size=11, fill=PALETTE["muted"]))
    for index in range(4):
        parts.append(rect(1210 + index * 38, 744, 30, 28, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=5))
        parts.append(text(1225 + index * 38, 763, str(index + 1), size=10, anchor="middle", fill=PALETTE["muted"]))
    return wrap(1440, 900, "AML-01 Bandeja de alertas", "".join(parts))


def aml_case() -> str:
    parts, _ = desktop_frame("Caso CASE-000087", "Detalle, evidencia y decisión", "Bandeja de alertas")
    parts.extend(
        [
            rect(264, 84, 1144, 92, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
            text(284, 112, "CASE-000087 · Estructuración y velocidad inusual", size=18, weight=700),
            text(284, 136, "Cliente CUS-000128 · RETAIL · Paraguay · KYC HIGH", size=12, fill=PALETTE["muted"]),
            badge(284, 148, "EN_ANALISIS", kind="warn"),
            badge(410, 148, "P1", kind="p1"),
            text(466, 164, "Score 94", size=11, weight=700, fill=PALETTE["danger"]),
            text(560, 164, "SLA vencido: 29/10/2026 09:15", size=11, fill=PALETTE["danger"]),
            text(1360, 112, "Asignado a", size=10, fill=PALETTE["muted"], anchor="end"),
            text(1360, 132, "Ana Martínez", size=12, weight=600, anchor="end"),
            button(1180, 142, 90, 30, "Escalar", variant="secondary"),
            button(1280, 142, 108, 30, "Cerrar caso", variant="danger"),
            rect(264, 188, 1144, 40, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=6),
            text(284, 213, "Alertas (3)", size=12, weight=700, fill=PALETTE["blue"]),
            text(392, 213, "Operaciones (18)", size=12, fill=PALETTE["muted"]),
            text(532, 213, "KYC y perfil", size=12, fill=PALETTE["muted"]),
            text(656, 213, "Historial", size=12, fill=PALETTE["muted"]),
            text(742, 213, "Notas", size=12, fill=PALETTE["muted"]),
            rect(264, 240, 748, 220, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
            text(284, 266, "Alertas vinculadas", size=14, weight=700),
            rect(264, 464, 748, 388, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
            text(284, 490, "Operaciones relacionadas", size=14, weight=700),
            text(996, 490, "18 movimientos en 30 días", size=10, fill=PALETTE["muted"], anchor="end"),
        ]
    )
    alerts = [
        ("R01 · Estructuración", "ALT-000341", "P1", "Hace 18 min"),
        ("R02 · Velocidad por cantidad", "ALT-000322", "P1", "Hace 2 días"),
        ("R08 · Importe atípico", "ALT-000298", "P2", "Hace 5 días"),
    ]
    y = 286
    for rule, alert, priority, when in alerts:
        parts.append(rect(284, y, 708, 44, fill=PALETTE["bg"], stroke=None, rx=6))
        parts.append(text(298, y + 18, rule, size=11, weight=600))
        parts.append(text(298, y + 34, f"{alert} · {when}", size=10, fill=PALETTE["muted"]))
        parts.append(badge(906, y + 11, priority, kind=priority.lower()))
        y += 54
    ops = [
        ("27/10 09:12", "Transferencia", "− ₲ 9.800.000", "ACC-000484 → ACC-000214", "API"),
        ("27/10 09:20", "Transferencia", "− ₲ 9.900.000", "ACC-000484 → ACC-000221", "API"),
        ("27/10 09:34", "Transferencia", "− ₲ 9.700.000", "ACC-000484 → ACC-000233", "API"),
        ("28/10 10:02", "Depósito", "+ ₲ 29.400.000", "Efectivo · sucursal centro", "BRANCH"),
        ("28/10 10:15", "Transferencia", "− ₲ 29.400.000", "ACC-000484 → ACC-000311", "API"),
    ]
    y = 510
    for when, kind, amount, counterpart, channel in ops:
        parts.append(line(284, y + 44, 992, y + 44))
        parts.append(text(284, y + 20, when, size=10, fill=PALETTE["muted"]))
        parts.append(text(390, y + 20, kind, size=11, weight=600))
        parts.append(text(540, y + 20, amount, size=11, weight=700, fill=PALETTE["danger"] if amount.startswith("−") else PALETTE["teal"]))
        parts.append(text(390, y + 36, counterpart, size=10, fill=PALETTE["muted"]))
        parts.append(text(920, y + 20, channel, size=10, fill=PALETTE["muted"], anchor="end"))
        y += 54
    parts.extend(
        [
            rect(1028, 240, 380, 212, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
            text(1048, 266, "Resumen del cliente", size=14, weight=700),
            text(1048, 294, "Nombre", size=10, fill=PALETTE["muted"]),
            text(1388, 294, "L. R. •••• 1234", size=11, weight=600, anchor="end"),
            text(1048, 322, "Segmento", size=10, fill=PALETTE["muted"]),
            text(1388, 322, "RETAIL", size=11, weight=600, anchor="end"),
            text(1048, 350, "Riesgo KYC", size=10, fill=PALETTE["muted"]),
            text(1388, 350, "HIGH · 88/100", size=11, weight=700, fill=PALETTE["danger"], anchor="end"),
            text(1048, 378, "PEP", size=10, fill=PALETTE["muted"]),
            text(1388, 378, "No", size=11, anchor="end"),
            text(1048, 406, "EDD", size=10, fill=PALETTE["muted"]),
            text(1388, 406, "Requerida", size=11, weight=600, fill=PALETTE["warn"], anchor="end"),
            text(1048, 434, "Ver historial completo ›", size=10, weight=600, fill=PALETTE["blue"]),
            rect(1028, 464, 380, 170, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
            text(1048, 490, "Línea de tiempo", size=14, weight=700),
            circle(1056, 516, 5, fill=PALETTE["blue"], stroke=None),
            text(1070, 520, "Alerta creada · 27/10 09:15", size=10),
            line(1056, 521, 1056, 556, stroke=PALETTE["line"]),
            circle(1056, 562, 5, fill=PALETTE["warn"], stroke=None),
            text(1070, 566, "Asignada a Ana · 27/10 09:22", size=10),
            line(1056, 567, 1056, 602, stroke=PALETTE["line"]),
            circle(1056, 608, 5, fill=PALETTE["danger"], stroke=None),
            text(1070, 612, "SLA vencido · 29/10 09:15", size=10, fill=PALETTE["danger"]),
            rect(1028, 646, 380, 206, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
            text(1048, 672, "Nota de investigación", size=14, weight=700),
            rect(1048, 686, 340, 88, fill=PALETTE["bg"], stroke=PALETTE["line"], rx=6),
            text(1060, 706, "Se observan depósitos fraccionados y salidas", size=10, fill=PALETTE["muted"]),
            text(1060, 724, "inmediatas hacia terceros. Solicitar SOF.", size=10, fill=PALETTE["muted"]),
            text(1060, 754, "0/2.000", size=9, fill=PALETTE["muted"]),
            button(1048, 786, 160, 34, "Guardar nota", variant="secondary"),
            button(1218, 786, 170, 34, "Abrir cierre", variant="danger"),
        ]
    )
    return wrap(1440, 900, "AML-02 Detalle de caso", "".join(parts))


def aml_history() -> str:
    parts, _ = desktop_frame("Historial del cliente", "CUS-000128 · RETAIL · Paraguay", "Clientes")
    parts.extend(
        [
            rect(264, 84, 1144, 84, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
            circle(306, 126, 26, fill=PALETTE["blue_soft"], stroke=None),
            text(306, 132, "LR", size=14, weight=700, fill=PALETTE["blue"], anchor="middle"),
            text(346, 114, "L. R. •••• 1234", size=18, weight=700),
            text(346, 136, "Cliente desde 2024 · Asunción · CI •••• 1234", size=11, fill=PALETTE["muted"]),
            badge(346, 144, "KYC HIGH", kind="danger"),
            badge(438, 144, "PEP: No", kind="info"),
            badge(516, 144, "EDD requerida", kind="warn"),
            button(1220, 108, 80, 32, "Abrir caso", variant="secondary"),
            button(1310, 108, 78, 32, "Exportar", variant="secondary"),
        ]
    )
    cards = [
        ("Score KYC", "88 / 100", PALETTE["danger"], "Alto"),
        ("Operaciones 90 d", "142", PALETTE["ink"], "₲ 214,8 M"),
        ("Alertas abiertas", "3", PALETTE["warn"], "1 vencida"),
        ("Casos cerrados", "2", PALETTE["teal"], "Último: falso positivo"),
        ("Antigüedad", "2 a 5 meses", PALETTE["ink"], "Alta"),
    ]
    x = 264
    for label, value, color, detail in cards:
        parts.append(rect(x, 184, 220, 82, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8))
        parts.append(text(x + 16, 208, label, size=10, fill=PALETTE["muted"]))
        parts.append(text(x + 16, 236, value, size=20, weight=700, fill=color))
        parts.append(text(x + 16, 254, detail, size=10, fill=PALETTE["muted"]))
        x += 236
    parts.extend(
        [
            rect(264, 282, 556, 280, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
            text(284, 308, "Volumen mensual", size=14, weight=700),
            text(800, 308, "PYG · últimos 6 meses", size=10, fill=PALETTE["muted"], anchor="end"),
        ]
    )
    bar_heights = [56, 84, 66, 120, 98, 142]
    for index, height in enumerate(bar_heights):
        x = 306 + index * 80
        parts.append(rect(x, 510 - height, 44, height, fill=PALETTE["blue_soft"], stroke=None, rx=4))
        parts.append(text(x + 22, 528, ["May", "Jun", "Jul", "Ago", "Sep", "Oct"][index], size=9, fill=PALETTE["muted"], anchor="middle"))
    parts.extend(
        [
            rect(840, 282, 568, 280, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
            text(860, 308, "Alertas por regla", size=14, weight=700),
            text(1388, 308, "12 meses", size=10, fill=PALETTE["muted"], anchor="end"),
        ]
    )
    rules = [("R01 Estructuración", 74), ("R02 Velocidad", 58), ("R05 Redondos", 42), ("R08 Perfil", 28), ("R04 Pass-through", 18)]
    y = 340
    for label, width in rules:
        parts.append(text(860, y + 10, label, size=10))
        parts.append(rect(1080, y, width * 3, 14, fill=PALETTE["warn_soft"], stroke=None, rx=7))
        parts.append(text(1088 + width * 3, y + 11, str(width), size=9, weight=600, fill=PALETTE["warn"]))
        y += 38
    parts.extend(
        [
            rect(264, 578, 1144, 274, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
            text(284, 604, "Operaciones recientes", size=14, weight=700),
            text(1388, 604, "Ver todas", size=10, weight=600, fill=PALETTE["blue"], anchor="end"),
        ]
    )
    headers = [("Fecha", 284), ("Tipo", 390), ("Importe", 520), ("Contraparte", 680), ("Canal", 980), ("Estado", 1100), ("Alerta", 1220)]
    for label, x in headers:
        parts.append(text(x, 634, label, size=10, weight=700, fill=PALETTE["muted"]))
    rows = [
        ("27/10 09:12", "Transferencia", "− ₲ 9.800.000", "ACC-000214", "API", "POSTED", "R01"),
        ("27/10 09:20", "Transferencia", "− ₲ 9.900.000", "ACC-000221", "API", "POSTED", "R02"),
        ("27/10 09:34", "Transferencia", "− ₲ 9.700.000", "ACC-000233", "API", "POSTED", "R01"),
        ("28/10 10:02", "Depósito", "+ ₲ 29.400.000", "Sucursal centro", "BRANCH", "POSTED", "—"),
        ("28/10 10:15", "Transferencia", "− ₲ 29.400.000", "ACC-000311", "API", "POSTED", "R04"),
    ]
    y = 650
    for when, kind, amount, counterpart, channel, status, alert in rows:
        parts.append(line(284, y + 30, 1388, y + 30))
        parts.append(text(284, y + 12, when, size=10))
        parts.append(text(390, y + 12, kind, size=10, weight=600))
        parts.append(text(520, y + 12, amount, size=10, weight=700, fill=PALETTE["danger"] if amount.startswith("−") else PALETTE["teal"]))
        parts.append(text(680, y + 12, counterpart, size=10))
        parts.append(text(980, y + 12, channel, size=10))
        parts.append(badge(1100, y, status, kind="ok"))
        parts.append(badge(1220, y, alert, kind="warn" if alert != "—" else "p3"))
        y += 36
    return wrap(1440, 900, "AML-03 Historial del cliente", "".join(parts))


def aml_close() -> str:
    parts, _ = desktop_frame("Caso CASE-000087", "Cierre del caso", "Bandeja de alertas")
    parts.extend(
        [
            rect(264, 84, 1144, 92, fill=PALETTE["surface"], stroke=PALETTE["line"], rx=8),
            text(284, 112, "CASE-000087 · Estructuración y velocidad inusual", size=18, weight=700),
            text(284, 136, "Cliente CUS-000128 · RETAIL · KYC HIGH · 3 alertas vinculadas", size=12, fill=PALETTE["muted"]),
            badge(284, 148, "EN_ANALISIS", kind="warn"),
            badge(410, 148, "P1", kind="p1"),
            text(480, 164, "Score 94 · SLA vencido", size=11, weight=600, fill=PALETTE["danger"]),
            rect(0, 0, 1440, 900, fill="#111827", stroke=None, rx=0, sw=0),
        ]
    )
    parts[-1] = '<rect x="0" y="0" width="1440" height="900" fill="#111827" opacity="0.45"/>'
    parts.extend(
        [
            rect(330, 92, 780, 716, fill=PALETTE["surface"], stroke=None, rx=12),
            text(362, 132, "Cerrar caso CASE-000087", size=20, weight=700),
            text(362, 154, "El cierre es definitivo y queda registrado en la auditoría.", size=11, fill=PALETTE["muted"]),
            line(362, 170, 1078, 170),
            text(362, 198, "Resumen", size=12, weight=700),
            text(362, 218, "Cliente CUS-000128 · 3 alertas · 18 operaciones · score 94", size=11, fill=PALETTE["muted"]),
            text(362, 236, "Analista: Ana Martínez · Caso abierto: 27/10/2026 09:15", size=11, fill=PALETTE["muted"]),
            text(362, 270, "Decisión *", size=12, weight=700),
        ]
    )
    options = [
        ("Falso positivo", "La actividad es consistente con el perfil y la documentación.", True),
        ("Escalar a caso", "Requiere investigación ampliada o aprobación de otro nivel.", False),
        ("Reportar ROS", "Existe sospecha fundamentada que debe reportarse.", False),
    ]
    y = 286
    for label, detail, selected in options:
        border = PALETTE["blue"] if selected else PALETTE["line"]
        fill = PALETTE["blue_soft"] if selected else PALETTE["surface"]
        parts.append(rect(362, y, 716, 48, fill=fill, stroke=border, rx=6))
        parts.append(circle(382, y + 24, 8, fill=PALETTE["blue"] if selected else PALETTE["surface"], stroke=PALETTE["blue"]))
        if selected:
            parts.append(circle(382, y + 24, 3, fill="#FFFFFF", stroke=None))
        parts.append(text(400, y + 20, label, size=12, weight=700))
        parts.append(text(400, y + 36, detail, size=10, fill=PALETTE["muted"]))
        y += 58
    parts.extend(
        [
            text(362, 472, "Motivo del cierre *", size=12, weight=700),
            rect(362, 482, 716, 92, fill=PALETTE["bg"], stroke=PALETTE["line"], rx=6),
            text(376, 504, "La actividad es consistente con el giro declarado. Se verificó", size=11, fill=PALETTE["muted"]),
            text(376, 522, "el origen de fondos y la documentación del cliente. No se", size=11, fill=PALETTE["muted"]),
            text(376, 540, "identifican operaciones adicionales fuera del perfil.", size=11, fill=PALETTE["muted"]),
            text(1062, 558, "186/1.000", size=9, fill=PALETTE["muted"], anchor="end"),
            text(362, 600, "Checklist de cierre *", size=12, weight=700),
            text(362, 622, "☑ Se revisaron todas las alertas vinculadas", size=11),
            text(362, 644, "☑ Se verificó el origen de fondos y la documentación KYC", size=11),
            text(362, 666, "☑ Se dejó constancia del análisis en las notas del caso", size=11),
            rect(362, 686, 716, 44, fill=PALETTE["info_soft"], stroke=None, rx=6),
            text(376, 711, "Al confirmar, el caso quedará CERRADO y no podrá reabrirse.", size=11, weight=600, fill=PALETTE["info"]),
            button(760, 748, 150, 40, "Cancelar", variant="secondary"),
            button(920, 748, 158, 40, "Confirmar cierre", variant="danger"),
        ]
    )
    return wrap(1440, 900, "AML-04 Cierre del caso", "".join(parts))


SCREENS = [
    ("APP-01-inicio.svg", "APP-01 — Inicio", "Aplicación de transferencias", "Cliente", app_inicio),
    ("APP-02-transferencia-local.svg", "APP-02 — Nueva transferencia local", "Aplicación de transferencias", "Cliente", app_local),
    ("APP-03-transferencia-internacional.svg", "APP-03 — Nueva transferencia internacional", "Aplicación de transferencias", "Cliente", app_international),
    ("APP-04-confirmacion.svg", "APP-04 — Confirmación", "Aplicación de transferencias", "Cliente", app_confirm),
    ("APP-05-comprobante.svg", "APP-05 — Comprobante", "Aplicación de transferencias", "Cliente", app_receipt),
    ("APP-06-error.svg", "APP-06 — Error", "Aplicación de transferencias", "Cliente", app_error),
    ("AML-01-bandeja-alertas.svg", "AML-01 — Bandeja de alertas", "Consola de cumplimiento", "Analista AML", aml_inbox),
    ("AML-02-detalle-caso.svg", "AML-02 — Detalle de caso", "Consola de cumplimiento", "Analista AML", aml_case),
    ("AML-03-historial-cliente.svg", "AML-03 — Historial del cliente", "Consola de cumplimiento", "Analista AML", aml_history),
    ("AML-04-cierre-caso.svg", "AML-04 — Cierre del caso", "Consola de cumplimiento", "Analista AML", aml_close),
]


def write_gallery() -> None:
    cards = []
    for filename, title, category, audience, _ in SCREENS:
        cards.append(
            f'<article class="card"><a href="{filename}">'
            f'<img src="{filename}" alt="Wireframe de {esc(title)}" loading="lazy">'
            f"</a><div class=\"meta\"><span class=\"tag\">{esc(category)}</span>"
            f"<h2>{esc(title)}</h2><p>{esc(audience)} · SVG de baja fidelidad</p>"
            f'<a class="link" href="{filename}">Abrir SVG</a></div></article>'
        )
    html = f"""<!doctype html>
<html lang="es-PY">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wireframes — NovaBank Payments &amp; AML Hub</title>
<style>
:root {{ --navy:#0B3B60; --blue:#155E8A; --bg:#F3F4F6; --ink:#111827; --muted:#4B5563; --line:#D1D5DB; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Inter, "Segoe UI", system-ui, sans-serif; background:var(--bg); color:var(--ink); }}
header {{ background:var(--navy); color:#fff; padding:40px 24px; }}
header h1 {{ margin:0 0 8px; font-size:28px; }}
header p {{ margin:0; color:#BFDBFE; max-width:900px; }}
main {{ max-width:1400px; margin:0 auto; padding:24px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:20px; }}
.card {{ background:#fff; border:1px solid var(--line); border-radius:12px; overflow:hidden; }}
.card img {{ display:block; width:100%; height:220px; object-fit:contain; background:#fff; border-bottom:1px solid var(--line); }}
.meta {{ padding:16px; }}
.meta h2 {{ font-size:16px; margin:8px 0 4px; }}
.meta p {{ margin:0 0 12px; color:var(--muted); font-size:12px; }}
.tag {{ display:inline-block; background:#DCEBF5; color:var(--blue); border-radius:999px; padding:3px 10px; font-size:10px; font-weight:700; }}
.link {{ color:var(--blue); font-size:12px; font-weight:700; text-decoration:none; }}
.link:focus {{ outline:2px solid var(--blue); outline-offset:2px; }}
footer {{ max-width:1400px; margin:0 auto; padding:0 24px 40px; color:var(--muted); font-size:12px; }}
</style>
</head>
<body>
<header>
<h1>Wireframes — NovaBank Payments &amp; AML Hub</h1>
<p>Bocetos de baja fidelidad del caso ficticio. Diez pantallas: seis de la app de transferencias y cuatro de la consola de cumplimiento. La especificación completa está en <strong>especificacion-pantallas.md</strong>.</p>
</header>
<main><div class="grid">{''.join(cards)}</div></main>
<footer>Los wireframes no usan datos reales. No constituyen una certificación de accesibilidad ni un diseño visual final.</footer>
</body>
</html>
"""
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, title, _, _, builder in SCREENS:
        (OUT_DIR / filename).write_text(builder(), encoding="utf-8")
        print(f"Generado: {filename}")
    write_gallery()
    print("Generado: index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
