"""Dashboard HTML autocontenido y sus capturas claro/oscuro."""

from __future__ import annotations

import html
from pathlib import Path

from .assetlib import (
    ASSETS,
    BRAND_DIR,
    FONT_MONO,
    FONT_UI,
    IMG_DIR,
    PALETTE,
    format_int,
    format_pct,
    optimize_png,
    write_text,
)
from .data import (
    Dataset,
    alert_counts,
    currency_summary,
    daily_series,
    kpi_block,
    latency_summary,
    dataset as load_dataset,
    top_alert_rows,
)

SHORT_RULES = {
    "R01": "Estructuración",
    "R02": "Velocidad (cantidad)",
    "R03": "Velocidad (monto)",
    "R04": "Cuenta de paso",
    "R05": "Depósitos redondos",
    "R06": "Cuenta dormida",
    "R07": "Jurisdicción de riesgo",
    "R08": "Importe atípico",
    "R09": "Cambio de conducta",
    "R10": "Fondos circulares",
    "R11": "Contraparte concentrada",
    "R12": "Fan-in de remitentes",
}

DASHBOARD = ASSETS / "dashboard"


def _logo() -> str:
    return (BRAND_DIR / "logo-horizontal.svg").read_text(encoding="utf-8")


def _dark_logo() -> str:
    return (BRAND_DIR / "logo-horizontal-dark.svg").read_text(encoding="utf-8")


def _line_chart(data: Dataset) -> str:
    series = daily_series(data.daily)
    values = [value for _, value, _ in series]
    width, height = 820, 250
    left, top, right, bottom = 46, 22, 14, 32
    plot_w = width - left - right
    plot_h = height - top - bottom
    ceiling = max(values) * 1.16
    points = []
    for index, value in enumerate(values):
        x = left + plot_w * index / (len(values) - 1)
        y = top + plot_h * (1 - value / ceiling)
        points.append((x, y))
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    area = f"M{left},{top + plot_h} L" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points)
    area += f" L{left + plot_w},{top + plot_h} Z"
    grid = "".join(
        f'<line x1="{left}" y1="{top + plot_h * i / 4:.1f}" x2="{left + plot_w}" '
        f'y2="{top + plot_h * i / 4:.1f}" class="grid"/>'
        for i in range(5)
    )
    months = [(0, "Abr"), (30, "May"), (61, "Jun"), (91, "Jul"), (122, "Ago"), (153, "Sep")]
    labels = "".join(
        f'<text x="{left + plot_w * index / 182:.1f}" y="{height - 8}" class="axis" text-anchor="middle">{label}</text>'
        for index, label in months
    )
    return f"""
    <svg viewBox="0 0 {width} {height}" role="img" aria-label="Volumen diario de transacciones">
      {grid}
      <path d="{area}" class="area"/>
      <polyline points="{line}" class="line"/>
      {labels}
    </svg>"""


def _donut(data: Dataset) -> str:
    summary = currency_summary(data.transactions)
    total = sum(int(item["ops"]) for item in summary)
    circumference = 2 * 3.14159 * 54
    offset = 0.0
    arcs = []
    colors = [PALETTE["cyan_400"], PALETTE["turquoise_400"]]
    for index, item in enumerate(summary):
        share = float(item["share"])
        dash = circumference * share
        arcs.append(
            f'<circle cx="92" cy="92" r="54" fill="none" stroke="{colors[index]}" '
            f'stroke-width="20" stroke-dasharray="{dash:.2f} {circumference - dash:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 92 92)"/>'
        )
        offset += dash
    rows = "".join(
        f"""<div class="legend-row"><span class="dot" style="background:{colors[i]}"></span>
        <strong>{item['currency']}</strong><span>{format_int(int(item['ops']))} ops</span>
        <span class="muted">{format_pct(float(item['share']) * 100)}</span></div>"""
        for i, item in enumerate(summary)
    )
    return f"""
    <div class="donut-wrap">
      <svg viewBox="0 0 184 184" role="img" aria-label="Distribución por moneda">
        {''.join(arcs)}
        <text x="92" y="88" text-anchor="middle" class="donut-n">{format_int(total)}</text>
        <text x="92" y="108" text-anchor="middle" class="donut-l">operaciones</text>
      </svg>
      <div class="legend">{rows}</div>
    </div>"""


def _latency_chart(data: Dataset) -> str:
    summary = latency_summary(data.sla)
    values = [int(value) for value in summary["values"]]  # type: ignore[index]
    width, height = 820, 250
    left, top, right, bottom = 46, 22, 14, 32
    plot_w = width - left - right
    plot_h = height - top - bottom
    bins = 24
    counts = [0] * bins
    for value in values:
        index = min(bins - 1, int(value // 500))
        counts[index] += 1
    max_count = max(counts)
    bar_w = plot_w / bins
    bars = []
    for index, count in enumerate(counts):
        h = plot_h * count / max_count
        x = left + index * bar_w
        y = top + plot_h - h
        css = "bar warn" if index * 500 >= 10_000 else "bar"
        bars.append(f'<rect x="{x + 1:.1f}" y="{y:.1f}" width="{bar_w - 2:.1f}" height="{h:.1f}" class="{css}"/>')
    grid = "".join(
        f'<line x1="{left}" y1="{top + plot_h * i / 4:.1f}" x2="{left + plot_w}" '
        f'y2="{top + plot_h * i / 4:.1f}" class="grid"/>'
        for i in range(5)
    )
    ticks = "".join(
        f'<text x="{left + plot_w * i / 6:.1f}" y="{height - 8}" class="axis" text-anchor="middle">{i * 2}s</text>'
        for i in range(7)
    )
    markers = []
    for value, label, color in [
        (summary["p50"], "p50", PALETTE["cyan_400"]),
        (summary["p95"], "p95", PALETTE["mint_300"]),
        (summary["p99"], "p99", PALETTE["amber_400"]),
        (summary["sla_ms"], "SLA", PALETTE["red_400"]),
    ]:
        x = left + plot_w * min(int(value), 12_000) / 12_000
        markers.append(
            f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + plot_h}" class="{label.lower()}-line"/>'
            f'<text x="{x + 3:.1f}" y="{top + 12}" class="marker">{label}</text>'
        )
    return f"""
    <svg viewBox="0 0 {width} {height}" role="img" aria-label="Distribución de latencia del pago instantáneo">
      {grid}{''.join(bars)}{ticks}{''.join(markers)}
    </svg>"""


def _rule_chart(data: Dataset) -> str:
    counts = alert_counts(data.alerts)
    rows = counts[:7]
    width, height = 520, 250
    left, top = 132, 16
    bar_h = 22
    gap = 12
    max_count = max(int(item["count"]) for item in rows)
    bars = []
    for index, item in enumerate(rows):
        y = top + index * (bar_h + gap)
        w = (width - left - 44) * int(item["count"]) / max_count
        color = PALETTE["amber_400"] if item["severity"] == "HIGH" else PALETTE["cyan_400"]
        label = SHORT_RULES.get(str(item["rule_id"]), str(item["rule_name"]))
        bars.append(
            f'<rect x="{left}" y="{y}" width="{w:.1f}" height="{bar_h}" rx="4" fill="{color}"/>'
            f'<text x="{left - 8}" y="{y + 15}" class="axis" text-anchor="end">'
            f"{item['rule_id']} · {html.escape(label)}</text>"
            f'<text x="{left + w + 7:.1f}" y="{y + 15}" class="value">{item["count"]}</text>'
        )
    return f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Alertas por regla">{"".join(bars)}</svg>'


def _confusion(data: Dataset) -> str:
    cells = [
        ("Verdaderos positivos", "341", PALETTE["green_400"], "sospechosa · alertada"),
        ("Falsos positivos", "3", PALETTE["amber_400"], "normal · alertada"),
        ("Falsos negativos", "0", PALETTE["red_400"], "sospechosa · no alertada"),
        ("Verdaderos negativos", "489", PALETTE["cyan_400"], "normal · no alertada"),
    ]
    return "".join(
        f"""<div class="conf-cell" style="--c:{color}">
        <span>{label}</span><strong>{value}</strong><small>{detail}</small></div>"""
        for label, value, color, detail in cells
    )


def _alerts_table(data: Dataset) -> str:
    rows = []
    seen_rules = set()
    for row in top_alert_rows(data, limit=200):
        rule_id = row.get("rule_id", "")
        if rule_id in seen_rules:
            continue
        seen_rules.add(rule_id)
        rows.append(row)
        if len(rows) == 8:
            break
    body = "".join(
        f"""<tr><td><span class="prio {row.get('priority','P3').lower()}">{row.get('priority','P3')}</span></td>
        <td class="mono">{html.escape(row.get('alert_id',''))}</td>
        <td>{html.escape(row.get('rule_id',''))} · {html.escape(row.get('rule_name',''))}</td>
        <td class="mono">{html.escape(row.get('risk_score',''))}</td>
        <td>{html.escape(row.get('status',''))}</td>
        <td class="mono">{html.escape(row.get('due_at','')[:16].replace('T',' '))}</td></tr>"""
        for row in rows
    )
    return f"""<table>
    <thead><tr><th>Prioridad</th><th>Alerta</th><th>Regla</th><th>Score</th><th>Estado</th><th>Vence</th></tr></thead>
    <tbody>{body}</tbody></table>"""


def _metric_cards(data: Dataset) -> str:
    kpis = kpi_block(data)
    cards = [
        (format_int(int(kpis["transactions"])), "movimientos", "49.582 transacciones sintéticas"),
        (format_int(int(kpis["alerts"])), "alertas AML", "deduplicadas en el corte"),
        (format_pct(float(kpis["precision"]) * 100, 2), "precisión", "sobre etiquetadas"),
        (format_pct(float(kpis["recall"]) * 100, 0), "recall", "341 de 341 sospechosas"),
        (format_pct(float(kpis["within_sla"]) * 100, 1), "dentro de SLA", f"p95 {format_int(int(kpis['p95']))} ms"),
    ]
    return "".join(
        f"""<article class="kpi"><div class="kpi-value mono">{value}</div>
        <div class="kpi-label">{label}</div><div class="kpi-note">{note}</div></article>"""
        for value, label, note in cards
    )


def build_html(dark: bool = True) -> str:
    data = load_dataset()
    kpis = kpi_block(data)
    body = f"""
    <div class="shell">
      <header class="top">
        <div class="brand">
          <div class="logo-light">{_logo()}</div>
          <div class="logo-dark">{_dark_logo()}</div>
          <div>
            <h1>Panel de operaciones y cumplimiento</h1>
            <p>Abril–septiembre 2026 · datos sintéticos · corte 2026-10-29</p>
          </div>
        </div>
        <div class="top-right">
          <button id="theme" class="theme" type="button" aria-label="Cambiar tema">Tema</button>
          <span class="badge">Caso ficticio</span>
        </div>
      </header>

      <section class="kpis">{_metric_cards(data)}</section>

      <section class="rows two">
        <article class="card wide">
          <div class="card-head"><div><h2>Volumen diario</h2>
          <p>{format_int(int(kpis['transactions']))} operaciones en 183 días</p></div>
          <span class="pill">Media {round(int(kpis['transactions'])/183)}/día</span></div>
          {_line_chart(data)}
        </article>
        <article class="card">
          <div class="card-head"><div><h2>Mezcla por moneda</h2><p>Participación operativa</p></div></div>
          {_donut(data)}
        </article>
      </section>

      <section class="rows two">
        <article class="card wide">
          <div class="card-head"><div><h2>Latencia del pago instantáneo</h2>
          <p>10.820 pagos locales · latencia sintética y determinista</p></div>
          <span class="pill">{format_pct(float(kpis['within_sla'])*100)} dentro de SLA</span></div>
          {_latency_chart(data)}
        </article>
        <article class="card">
          <div class="card-head"><div><h2>Alertas por regla</h2><p>Top 7 de 12 reglas</p></div></div>
          {_rule_chart(data)}
        </article>
      </section>

      <section class="rows split">
        <article class="card">
          <div class="card-head"><div><h2>Calidad del monitoreo</h2><p>833 transacciones etiquetadas</p></div></div>
          <div class="conf">{_confusion(data)}</div>
          <p class="note">150 alertas sin etiqueta quedan fuera de la matriz. Si se cuentan como FP,
          la precisión conservadora baja a {format_pct(float(kpis['precision_conservative'])*100, 2)}.</p>
        </article>
        <article class="card wide">
          <div class="card-head"><div><h2>Alertas priorizadas</h2><p>Ordenadas por prioridad y score</p></div>
          <span class="pill">P1 / P2 / P3</span></div>
          {_alerts_table(data)}
        </article>
      </section>

      <footer>
        <span>Fuente: 09-analitica/data/*.csv · 07-aml-compliance/docs/evaluacion-verdad.md</span>
        <span>NovaBank · caso ficticio · sin PII</span>
      </footer>
    </div>"""

    css = f"""
    :root {{
      --bg:{PALETTE['slate_50']}; --panel:{PALETTE['white']}; --ink:{PALETTE['ink']};
      --muted:{PALETTE['slate_500']}; --line:{PALETTE['slate_200']}; --soft:{PALETTE['slate_100']};
      --accent:{PALETTE['navy_600']}; --accent2:{PALETTE['turquoise_500']}; --grid:{PALETTE['slate_200']};
      --shadow:0 16px 34px rgba(15,23,42,.08);
    }}
    [data-theme="dark"] {{
      --bg:{PALETTE['navy_950']}; --panel:{PALETTE['navy_800']}; --ink:#E6F1F8;
      --muted:{PALETTE['slate_400']}; --line:#1E4E75; --soft:{PALETTE['navy_700']};
      --accent:{PALETTE['cyan_400']}; --accent2:{PALETTE['turquoise_400']}; --grid:#1E4E75;
      --shadow:0 18px 40px rgba(0,0,0,.28);
    }}
    * {{ box-sizing:border-box; }}
    html, body {{ margin:0; background:var(--bg); color:var(--ink); font-family:{FONT_UI}; }}
    .shell {{ width:1600px; margin:0 auto; padding:34px 44px 26px; }}
    .mono {{ font-family:{FONT_MONO}; font-variant-numeric:tabular-nums; }}
    .top {{ display:flex; justify-content:space-between; align-items:flex-start; gap:24px; }}
    .brand {{ display:flex; align-items:center; gap:22px; }}
    .brand svg {{ width:250px; height:auto; display:block; }}
    .logo-dark {{ display:none; }}
    [data-theme="dark"] .logo-light {{ display:none; }}
    [data-theme="dark"] .logo-dark {{ display:block; }}
    h1 {{ margin:0; font-size:28px; letter-spacing:-.7px; }}
    .brand p {{ margin:5px 0 0; color:var(--muted); font-size:13px; }}
    .top-right {{ display:flex; align-items:center; gap:10px; }}
    .badge {{ border:1px solid var(--line); background:var(--panel); color:var(--muted);
      border-radius:999px; padding:8px 13px; font-size:11px; font-weight:800; letter-spacing:.6px; }}
    .theme {{ border:1px solid var(--line); background:var(--panel); color:var(--ink);
      border-radius:999px; padding:8px 13px; font-size:11px; font-weight:800; cursor:pointer; }}
    .kpis {{ display:grid; grid-template-columns:repeat(5,1fr); gap:14px; margin:26px 0 18px; }}
    .kpi, .card {{ background:var(--panel); border:1px solid var(--line); border-radius:16px;
      box-shadow:var(--shadow); }}
    .kpi {{ padding:18px 19px 16px; }}
    .kpi-value {{ font-size:30px; font-weight:800; letter-spacing:-1px; color:var(--accent); }}
    .kpi:nth-child(3) .kpi-value, .kpi:nth-child(4) .kpi-value {{ color:var(--accent2); }}
    .kpi-label {{ font-size:13px; font-weight:700; margin-top:4px; }}
    .kpi-note {{ font-size:11px; color:var(--muted); margin-top:3px; }}
    .rows {{ display:grid; gap:16px; margin-bottom:16px; }}
    .rows.two {{ grid-template-columns:1.55fr 1fr; }}
    .rows.split {{ grid-template-columns:1fr 1.35fr; }}
    .card {{ padding:20px 22px 18px; min-width:0; }}
    .card-head {{ display:flex; justify-content:space-between; align-items:flex-start; gap:16px; margin-bottom:8px; }}
    h2 {{ margin:0; font-size:17px; letter-spacing:-.2px; }}
    .card-head p {{ margin:4px 0 0; color:var(--muted); font-size:11.5px; }}
    .pill {{ border:1px solid var(--line); background:var(--soft); color:var(--muted);
      border-radius:999px; padding:5px 10px; font-size:10.5px; font-weight:800; white-space:nowrap; }}
    svg {{ display:block; width:100%; height:auto; overflow:visible; }}
    .grid line.grid {{ stroke:var(--grid); stroke-width:1; opacity:.75; }}
    .axis {{ fill:var(--muted); font-size:10.5px; }}
    .line {{ fill:none; stroke:var(--accent); stroke-width:2.4; }}
    .area {{ fill:var(--accent); opacity:.14; }}
    .bar {{ fill:var(--accent); opacity:.78; }}
    .bar.warn {{ fill:{PALETTE['amber_400']}; opacity:.95; }}
    .p50-line, .p95-line, .p99-line, .sla-line {{ stroke-width:1.6; stroke-dasharray:5 4; }}
    .p50-line {{ stroke:{PALETTE['cyan_400']}; }}
    .p95-line {{ stroke:{PALETTE['mint_300']}; }}
    .p99-line {{ stroke:{PALETTE['amber_400']}; }}
    .sla-line {{ stroke:{PALETTE['red_400']}; stroke-dasharray:2 3; }}
    .marker {{ fill:var(--muted); font-size:9.5px; }}
    .value {{ fill:var(--ink); font-size:10.5px; font-weight:800; }}
    .donut-wrap {{ display:flex; align-items:center; gap:18px; padding-top:6px; }}
    .donut-wrap svg {{ width:190px; flex:0 0 190px; }}
    .donut-n {{ fill:var(--ink); font-size:24px; font-weight:800; }}
    .donut-l {{ fill:var(--muted); font-size:10.5px; }}
    .legend {{ display:flex; flex-direction:column; gap:9px; min-width:170px; }}
    .legend-row {{ display:grid; grid-template-columns:10px 46px 1fr; gap:7px;
      align-items:center; color:var(--muted); font-size:11.5px; }}
    .legend-row strong {{ color:var(--ink); font-size:12px; }}
    .legend-row .muted {{ grid-column:2 / 4; font-size:10.5px; }}
    .dot {{ width:9px; height:9px; border-radius:50%; }}
    .conf {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:8px 0 10px; }}
    .conf-cell {{ border:1px solid var(--line); border-left:4px solid var(--c); border-radius:12px;
      padding:12px 14px; background:var(--soft); }}
    .conf-cell span {{ color:var(--c); font-size:11px; font-weight:800; }}
    .conf-cell strong {{ display:block; font-size:30px; line-height:1.1; margin-top:2px; }}
    .conf-cell small {{ color:var(--muted); font-size:10.5px; }}
    .note {{ color:var(--muted); font-size:10.5px; line-height:1.45; margin:2px 0 0; }}
    table {{ width:100%; border-collapse:collapse; font-size:11px; }}
    th {{ text-align:left; color:var(--muted); font-size:10px; text-transform:uppercase;
      letter-spacing:.7px; padding:7px 6px; border-bottom:1px solid var(--line); }}
    td {{ padding:8px 6px; border-bottom:1px solid var(--line); vertical-align:middle; }}
    tr:last-child td {{ border-bottom:0; }}
    .prio {{ display:inline-block; border-radius:999px; padding:3px 8px; font-size:10px; font-weight:800; }}
    .prio.p1 {{ background:{PALETTE['red_500']}22; color:{PALETTE['red_500']}; }}
    .prio.p2 {{ background:{PALETTE['amber_500']}22; color:{PALETTE['amber_500']}; }}
    .prio.p3 {{ background:{PALETTE['slate_500']}22; color:var(--muted); }}
    footer {{ display:flex; justify-content:space-between; color:var(--muted); font-size:10.5px;
      padding:10px 2px 0; }}
    """
    doc = f"""<!doctype html>
<html lang="es" data-theme="{'dark' if dark else 'light'}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>NovaBank · Panel de operaciones y cumplimiento</title>
<link rel="icon" href="../brand/favicon.svg" type="image/svg+xml">
<style>{css}</style></head>
<body>{body}
<script>
const root = document.documentElement;
document.getElementById('theme').addEventListener('click', () => {{
  root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
}});
const params = new URLSearchParams(location.search);
if (params.get('theme')) root.dataset.theme = params.get('theme');
</script>
</body></html>"""
    return doc


def build() -> Path:
    DASHBOARD.mkdir(parents=True, exist_ok=True)
    path = DASHBOARD / "index.html"
    write_text(path, build_html(dark=True))
    return path


def screenshot(dark: bool) -> Path:
    from .assetlib import browser_page

    path = build()
    out = IMG_DIR / ("dashboard-dark.png" if dark else "dashboard-light.png")
    with browser_page(1600, 1200) as page:
        page.goto(path.as_uri(), wait_until="load")  # type: ignore[attr-defined]
        page.evaluate("(theme) => { document.documentElement.dataset.theme = theme; }", "dark" if dark else "light")
        page.wait_for_timeout(300)  # type: ignore[attr-defined]
        page.screenshot(path=str(out), full_page=True)  # type: ignore[attr-defined]
    optimize_png(out, max_kb=500)
    return out


def render_all() -> list[Path]:
    return [screenshot(False), screenshot(True)]
