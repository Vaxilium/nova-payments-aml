"""Banner de GitHub, social preview y portada de LinkedIn."""

from __future__ import annotations

import html
from pathlib import Path

from .assetlib import (
    BRAND_DIR,
    FONT_MONO,
    FONT_UI,
    IMG_DIR,
    LINKEDIN_DIR,
    PALETTE,
    render_html,
)


def _logo(name: str) -> str:
    path = BRAND_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Falta {path}. Ejecutar primero --only brand.")
    return path.read_text(encoding="utf-8")


def _base_css() -> str:
    return f"""
    * {{ box-sizing:border-box; margin:0; padding:0; }}
    html, body {{ font-family:{FONT_UI}; }}
    .mono {{ font-family:{FONT_MONO}; font-variant-numeric:tabular-nums; }}
    """


def _banner(dark: bool) -> tuple[str, str, str]:
    if dark:
        bg = PALETTE["navy_900"]
        panel = "rgba(16,59,92,.72)"
        border = "rgba(34,211,238,.22)"
        title = PALETTE["white"]
        body = PALETTE["slate_300"]
        muted = PALETTE["slate_400"]
        accent = PALETTE["cyan_400"]
        secondary = PALETTE["turquoise_400"]
        grid = "rgba(34,211,238,.08)"
        logo = _logo("logo-horizontal-dark.svg")
    else:
        bg = PALETTE["slate_50"]
        panel = PALETTE["white"]
        border = PALETTE["slate_200"]
        title = PALETTE["navy_900"]
        body = PALETTE["slate_500"]
        muted = PALETTE["slate_500"]
        accent = PALETTE["navy_600"]
        secondary = PALETTE["turquoise_500"]
        grid = "rgba(21,94,138,.08)"
        logo = _logo("logo-horizontal.svg")

    metrics = [
        ("49.582", "movimientos sintéticos"),
        ("377", "alertas AML deduplicadas"),
        ("204", "pruebas pytest"),
        ("100 %", "recall sobre etiquetadas"),
    ]
    metric_html = "".join(
        f"""<div class="metric"><div class="value mono">{value}</div>
        <div class="label">{html.escape(label)}</div></div>"""
        for value, label in metrics
    )

    body = f"""
    <div class="canvas">
      <div class="grid"></div>
      <div class="glow"></div>
      <div class="left">
        <div class="logo">{logo}</div>
        <div class="kicker">CASO DE NEGOCIO · BUSINESS ANALYSIS</div>
        <h1>Pagos que fluyen.<br><span>Riesgo bajo control.</span></h1>
        <p>Pagos instantáneos, cross-border y monitoreo AML en un mismo flujo,
        con trazabilidad de negocio a prueba.</p>
        <div class="chips">
          <span>BPMN · DMN</span><span>ISO 20022</span><span>SQL · FastAPI</span><span>UAT</span>
        </div>
      </div>
      <div class="right">
        <div class="tag">NovaBank · caso ficticio</div>
        <div class="metrics">{metric_html}</div>
        <div class="foot">Datos sintéticos reproducibles · semilla fija · sin PII</div>
      </div>
    </div>"""

    css = _base_css() + f"""
    html, body {{ width:1600px; height:480px; overflow:hidden; background:{bg}; }}
    .canvas {{ position:relative; width:1600px; height:480px; overflow:hidden;
      background:{bg}; color:{title}; padding:54px 64px 44px; display:flex;
      gap:54px; align-items:center; }}
    .grid {{ position:absolute; inset:0;
      background-image:linear-gradient({grid} 1px, transparent 1px),
        linear-gradient(90deg, {grid} 1px, transparent 1px);
      background-size:44px 44px; mask-image:linear-gradient(90deg,#000 0%,transparent 72%); }}
    .glow {{ position:absolute; width:720px; height:720px; right:-260px; top:-330px;
      background:radial-gradient(circle, {accent}33 0%, transparent 66%); filter:blur(12px); }}
    .left {{ position:relative; width:920px; z-index:2; }}
    .logo {{ margin-bottom:28px; }}
    .logo svg {{ width:360px; height:auto; display:block; }}
    .kicker {{ color:{secondary}; font-size:14px; font-weight:800; letter-spacing:3.2px;
      margin-bottom:14px; }}
    h1 {{ font-size:54px; line-height:1.02; letter-spacing:-2px; color:{title}; font-weight:800; }}
    h1 span {{ color:{accent}; }}
    p {{ margin-top:18px; width:790px; color:{body}; font-size:17px; line-height:1.55; }}
    .chips {{ display:flex; gap:9px; margin-top:24px; flex-wrap:wrap; }}
    .chips span {{ border:1px solid {border}; background:{panel}; color:{body};
      border-radius:999px; padding:7px 13px; font-size:12px; font-weight:700; }}
    .right {{ position:relative; z-index:2; width:470px; margin-left:auto; }}
    .tag {{ text-align:right; color:{muted}; font-size:12px; font-weight:700;
      letter-spacing:1.1px; margin-bottom:14px; }}
    .metrics {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
    .metric {{ background:{panel}; border:1px solid {border}; border-radius:16px;
      padding:20px 20px 17px; min-height:118px; }}
    .value {{ color:{accent}; font-size:34px; font-weight:800; letter-spacing:-1px; }}
    .metric:nth-child(2) .value, .metric:nth-child(3) .value {{ color:{secondary}; }}
    .label {{ color:{body}; font-size:12.5px; line-height:1.35; margin-top:6px; }}
    .foot {{ margin-top:16px; text-align:right; color:{muted}; font-size:11.5px; }}
    """

    name = "banner-dark.png" if dark else "banner-light.png"
    return body, css, name  # type: ignore[return-value]


def render_banners() -> list[Path]:
    outputs: list[Path] = []
    for dark in (False, True):
        body, css, name = _banner(dark)
        out = IMG_DIR / name
        render_html(body, out, width=1600, height=480, css=css, wait_ms=250, max_kb=500)
        outputs.append(out)
    return outputs


def render_social_preview() -> Path:
    out = IMG_DIR / "social-preview.png"
    logo = _logo("logo-horizontal-dark.svg")
    body = f"""
    <div class="canvas">
      <div class="grid"></div>
      <div class="orb a"></div><div class="orb b"></div>
      <header>
        <div class="logo">{logo}</div>
        <div class="badge">Caso ficticio · portafolio</div>
      </header>
      <main>
        <div class="copy">
          <div class="kicker">PAGOS · RIESGO · DATOS</div>
          <h1>Pagos que fluyen.<br><span>Riesgo bajo control.</span></h1>
          <p>Un caso de negocio end-to-end: pagos instantáneos, cross-border
          y monitoreo AML con evidencia reproducible.</p>
          <div class="chips"><span>BPMN</span><span>ISO 20022</span><span>SQL</span>
          <span>FastAPI</span><span>UAT</span></div>
        </div>
        <div class="stats">
          <div class="stat"><div class="n mono">49.582</div><div class="l">movimientos sintéticos</div></div>
          <div class="stat"><div class="n mono">12</div><div class="l">reglas AML</div></div>
          <div class="stat"><div class="n mono">204</div><div class="l">pruebas pytest</div></div>
          <div class="stat"><div class="n mono">100 %</div><div class="l">recall etiquetado</div></div>
        </div>
      </main>
      <footer><span>github.com/Vaxilium/nova-payments-aml</span><span>Franco Tillería Centurión · Business Analyst</span></footer>
    </div>"""
    css = _base_css() + f"""
    html, body {{ width:1280px; height:640px; overflow:hidden; background:{PALETTE['navy_950']}; }}
    .canvas {{ position:relative; width:1280px; height:640px; overflow:hidden;
      background:linear-gradient(135deg,{PALETTE['navy_950']} 0%,{PALETTE['navy_800']} 62%,#0B4A5F 100%);
      color:{PALETTE['white']}; padding:44px 58px 34px; display:flex; flex-direction:column; }}
    .grid {{ position:absolute; inset:0; opacity:.55;
      background-image:linear-gradient(rgba(34,211,238,.09) 1px,transparent 1px),
        linear-gradient(90deg,rgba(34,211,238,.09) 1px,transparent 1px);
      background-size:48px 48px; mask-image:linear-gradient(120deg,#000,transparent 78%); }}
    .orb {{ position:absolute; border-radius:50%; filter:blur(4px); }}
    .orb.a {{ width:520px; height:520px; right:-160px; top:-220px;
      background:radial-gradient(circle,{PALETTE['cyan_400']}38,transparent 68%); }}
    .orb.b {{ width:420px; height:420px; left:-170px; bottom:-220px;
      background:radial-gradient(circle,{PALETTE['turquoise_500']}33,transparent 68%); }}
    header {{ position:relative; display:flex; justify-content:space-between; align-items:center; z-index:2; }}
    .logo svg {{ width:300px; height:auto; display:block; }}
    .badge {{ border:1px solid rgba(34,211,238,.3); background:rgba(4,18,31,.55);
      color:{PALETTE['slate_300']}; border-radius:999px; padding:8px 14px; font-size:12px; font-weight:700; }}
    main {{ position:relative; z-index:2; display:flex; align-items:center; gap:44px; flex:1; }}
    .copy {{ width:700px; }}
    .kicker {{ color:{PALETTE['turquoise_400']}; font-size:12px; font-weight:800; letter-spacing:3.4px; }}
    h1 {{ margin-top:14px; font-size:52px; line-height:1.04; letter-spacing:-2px; }}
    h1 span {{ color:{PALETTE['cyan_400']}; }}
    p {{ margin-top:16px; color:{PALETTE['slate_300']}; font-size:16.5px; line-height:1.5; width:660px; }}
    .chips {{ display:flex; gap:8px; margin-top:22px; }}
    .chips span {{ border:1px solid rgba(34,211,238,.22); background:rgba(16,59,92,.6);
      color:{PALETTE['slate_200']}; padding:6px 11px; border-radius:999px; font-size:11px; font-weight:700; }}
    .stats {{ width:426px; display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
    .stat {{ background:rgba(4,18,31,.58); border:1px solid rgba(34,211,238,.2);
      border-radius:16px; padding:18px; min-height:112px; backdrop-filter:blur(4px); }}
    .n {{ color:{PALETTE['cyan_300']}; font-size:30px; font-weight:800; letter-spacing:-1px; }}
    .stat:nth-child(2) .n, .stat:nth-child(3) .n {{ color:{PALETTE['mint_300']}; }}
    .l {{ color:{PALETTE['slate_300']}; font-size:11.5px; line-height:1.4; margin-top:6px; }}
    footer {{ position:relative; z-index:2; display:flex; justify-content:space-between;
      color:{PALETTE['slate_500']}; font-size:11.5px; }}
    """
    render_html(body, out, width=1280, height=640, css=css, wait_ms=250, max_kb=500)
    return out


def render_linkedin_cover() -> Path:
    out = LINKEDIN_DIR / "portada-linkedin.png"
    logo = _logo("logo-horizontal-dark.svg")
    body = f"""
    <div class="canvas">
      <div class="grid"></div>
      <div class="glow"></div>
      <div class="content">
        <div class="logo">{logo}</div>
        <div class="kicker">BUSINESS ANALYSIS · PAGOS &amp; AML</div>
        <h1>Pagos que fluyen.<br><span>Riesgo bajo control.</span></h1>
        <div class="row">
          <div class="name">Franco Tillería Centurión</div>
          <div class="pill">NovaBank · caso ficticio</div>
        </div>
      </div>
      <div class="pills">
        <span>BPMN · DMN</span><span>ISO 20022</span><span>SQL</span><span>Power BI</span>
      </div>
    </div>"""
    css = _base_css() + f"""
    html, body {{ width:1584px; height:396px; overflow:hidden; background:{PALETTE['navy_950']}; }}
    .canvas {{ position:relative; width:1584px; height:396px; overflow:hidden;
      background:linear-gradient(120deg,{PALETTE['navy_950']} 0%,{PALETTE['navy_800']} 58%,#0A4358 100%);
      color:{PALETTE['white']}; padding:42px 58px 34px 360px; }}
    .grid {{ position:absolute; inset:0; opacity:.5;
      background-image:linear-gradient(rgba(34,211,238,.1) 1px,transparent 1px),
        linear-gradient(90deg,rgba(34,211,238,.1) 1px,transparent 1px);
      background-size:42px 42px; mask-image:linear-gradient(90deg,#000,transparent 82%); }}
    .glow {{ position:absolute; width:600px; height:600px; right:-180px; top:-260px;
      background:radial-gradient(circle,{PALETTE['cyan_400']}38,transparent 65%); }}
    .content {{ position:relative; z-index:2; }}
    .logo svg {{ width:280px; height:auto; display:block; margin-bottom:20px; }}
    .kicker {{ color:{PALETTE['turquoise_400']}; font-size:11.5px; font-weight:800; letter-spacing:3px; }}
    h1 {{ margin-top:8px; font-size:42px; line-height:1.04; letter-spacing:-1.6px; }}
    h1 span {{ color:{PALETTE['cyan_400']}; }}
    .row {{ display:flex; align-items:center; gap:16px; margin-top:18px; }}
    .name {{ color:{PALETTE['slate_200']}; font-size:15px; font-weight:700; }}
    .pill {{ border:1px solid rgba(94,234,212,.28); color:{PALETTE['mint_300']};
      border-radius:999px; padding:5px 11px; font-size:10.5px; font-weight:700; }}
    .pills {{ position:absolute; right:58px; bottom:40px; z-index:2; display:flex; gap:8px; }}
    .pills span {{ border:1px solid rgba(34,211,238,.22); background:rgba(4,18,31,.5);
      color:{PALETTE['slate_200']}; border-radius:999px; padding:6px 11px; font-size:10.5px; font-weight:700; }}
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    render_html(body, out, width=1584, height=396, css=css, wait_ms=250, max_kb=500)
    return out


def render_all() -> list[Path]:
    outputs = render_banners()
    outputs.append(render_social_preview())
    outputs.append(render_linkedin_cover())
    return outputs
