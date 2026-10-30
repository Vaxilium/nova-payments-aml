"""Carrusel LinkedIn 1080×1350 y PDF listo para publicar."""

from __future__ import annotations

import base64
from pathlib import Path

import img2pdf

from .assetlib import (
    ASSETS,
    BRAND_DIR,
    IMG_DIR,
    PALETTE,
    ROOT,
    browser_page,
    optimize_png,
    svg_data_uri,
    write_text,
)

LINKEDIN_DIR = ASSETS / "linkedin"
CAROUSEL_DIR = LINKEDIN_DIR / "carousel"
PDF_PATH = LINKEDIN_DIR / "carousel-novabank.pdf"
HTML_PATH = ASSETS / "src" / "carousel.html"
UX_DIR = IMG_DIR / "ux"

SLIDES = [
    ("01-portada.png", "Portada"),
    ("02-reto.png", "El reto"),
    ("03-rol.png", "Rol y alcance"),
    ("04-arquitectura.png", "Arquitectura"),
    ("05-diseno.png", "Diseño funcional"),
    ("06-datos.png", "Datos y AML"),
    ("07-calidad.png", "Calidad del monitoreo"),
    ("08-producto.png", "Producto"),
    ("09-limites.png", "Lectura honesta"),
    ("10-cierre.png", "Cierre"),
]


def _png_uri(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def _logo(dark: bool) -> str:
    name = "logo-horizontal-dark.svg" if dark else "logo-horizontal.svg"
    return svg_data_uri((BRAND_DIR / name).read_text(encoding="utf-8"))


CSS = """
* { box-sizing:border-box; }
html, body { margin:0; width:1080px; background:#020A12; }
body { font-family:"Segoe UI", Inter, system-ui, -apple-system, Arial, sans-serif; }
.slide { position:relative; width:1080px; height:1350px; overflow:hidden; padding:46px 80px 58px; }
.dark { color:#E2E8F0; background:
  radial-gradient(circle at 90% 3%, rgba(34,211,238,.18), transparent 30%),
  radial-gradient(circle at 0% 92%, rgba(20,184,166,.13), transparent 32%),
  linear-gradient(150deg, #071A2F 0%, #04121F 62%, #020A12 100%); }
.light { color:#0F172A; background:
  radial-gradient(circle at 95% 2%, rgba(34,211,238,.12), transparent 28%),
  linear-gradient(145deg, #FFFFFF 0%, #F3F7FB 58%, #E8F1F8 100%); }
.dark::before, .light::before { content:""; position:absolute; inset:0; pointer-events:none;
  background-image:linear-gradient(rgba(148,163,184,.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148,163,184,.06) 1px, transparent 1px);
  background-size:44px 44px; mask-image:linear-gradient(180deg, rgba(0,0,0,.65), transparent 72%); }
.top { position:relative; z-index:2; display:flex; justify-content:space-between; align-items:center; height:50px; }
.top img { height:34px; display:block; }
.pageno { font-size:13px; font-weight:800; letter-spacing:2px; color:#64748B; }
.dark .pageno { color:#7DD3FC; }
.content { position:relative; z-index:2; padding-top:52px; }
.kicker { font-size:16px; font-weight:800; letter-spacing:2.6px; text-transform:uppercase; color:#0E7490; }
.dark .kicker { color:#67E8F9; }
h1 { margin:22px 0 18px; font-size:66px; line-height:1.03; letter-spacing:-2.4px; font-weight:800; }
h1.small { font-size:58px; }
.lead { margin:0; font-size:26px; line-height:1.42; color:#475569; max-width:850px; }
.dark .lead { color:#CBD5E1; }
.accent { color:#0E7490; }
.dark .accent { color:#5EEAD4; }
.rule { width:76px; height:5px; border-radius:9px; background:#14B8A6; margin:28px 0 0; }
.foot { position:absolute; z-index:2; left:80px; right:80px; bottom:34px;
  display:flex; justify-content:space-between; align-items:center;
  color:#94A3B8; font-size:13px; letter-spacing:.1px; }
.light .foot { color:#64748B; }
.foot b { color:#E2E8F0; }
.light .foot b { color:#0F172A; }
.grid3 { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:42px; }
.card { border-radius:18px; padding:24px 22px; min-height:254px;
  background:#FFFFFF; border:1px solid #DCE5EF; box-shadow:0 12px 28px rgba(15,23,42,.06); }
.dark .card { background:rgba(127,180,210,.06); border-color:#1E3A52; box-shadow:none; }
.card .n { font-size:13px; font-weight:800; letter-spacing:1.4px; color:#0E7490; }
.dark .card .n { color:#67E8F9; }
.card h3 { font-size:27px; line-height:1.1; margin:24px 0 13px; letter-spacing:-.5px; }
.card p { font-size:19px; line-height:1.45; margin:0; color:#475569; }
.dark .card p { color:#AFC3D6; }
.card.mini { min-height:158px; padding:20px 20px; }
.card.mini h3 { font-size:22px; margin:14px 0 7px; }
.card.mini p { font-size:16px; }
.dark .stat { background:rgba(127,180,210,.06); border-color:#1E3A52; box-shadow:none; }
.dark .stat span { color:#94A3B8; }
.band { margin-top:44px; border-radius:18px; padding:24px 28px;
  background:#0A2540; color:#E2E8F0; font-size:22px; line-height:1.45; }
.band b { color:#67E8F9; }
.metrics { display:grid; grid-template-columns:repeat(2,1fr); gap:18px; margin-top:38px; }
.metric { border-radius:16px; padding:22px 22px 20px; background:rgba(127,180,210,.06);
  border:1px solid #1E3A52; }
.light .metric { background:#FFFFFF; border-color:#DCE5EF; box-shadow:0 10px 24px rgba(15,23,42,.05); }
.metric .big { font-size:48px; line-height:1; font-weight:800; letter-spacing:-2px; }
.metric .cap { font-size:14px; color:#94A3B8; margin-top:8px; }
.light .metric .cap { color:#64748B; }
.metric .big.cyan { color:#22D3EE; }
.metric .big.mint { color:#2DD4BF; }
.metric .big.amber { color:#FBBF24; }
.split { display:grid; grid-template-columns:1fr 1fr; gap:26px; margin-top:38px; align-items:start; }
.chart { border-radius:16px; overflow:hidden; border:1px solid #1E3A52; background:#071A2F; }
.light .chart { border-color:#DCE5EF; }
.chart img { width:100%; display:block; }
.note { margin-top:18px; font-size:16px; line-height:1.45; color:#94A3B8; }
.light .note { color:#64748B; }
.arch { margin-top:36px; display:flex; flex-direction:column; gap:11px; }
.layer { border-radius:14px; border:1px solid #DCE5EF; background:#FFFFFF; padding:16px 20px;
  display:flex; align-items:center; gap:18px; box-shadow:0 8px 20px rgba(15,23,42,.04); }
.layer .label { width:152px; flex:none; font-size:13px; font-weight:800; letter-spacing:1.2px;
  text-transform:uppercase; color:#0E7490; }
.layer .chips { display:flex; flex-wrap:wrap; gap:8px; }
.chip { border-radius:999px; padding:7px 12px; font-size:14px; font-weight:700;
  background:#E8F1F8; color:#155E8A; }
.connector { height:18px; width:2px; background:#CBD5E1; margin-left:75px; }
.dark .layer { background:rgba(127,180,210,.06); border-color:#1E3A52; box-shadow:none; }
.dark .layer .label { color:#67E8F9; }
.dark .chip { background:rgba(34,211,238,.10); color:#A5F3FC; }
.dark .connector { background:#1E3A52; }
.columns { display:grid; grid-template-columns:1fr 1fr; gap:28px; margin-top:40px; }
.listbox { border-radius:16px; border:1px solid #DCE5EF; background:#FFFFFF; padding:24px 24px 22px; }
.dark .listbox { background:rgba(127,180,210,.06); border-color:#1E3A52; }
.listbox h3 { font-size:17px; letter-spacing:1.3px; text-transform:uppercase; margin:0 0 16px; color:#0E7490; }
.dark .listbox h3 { color:#67E8F9; }
.listbox ul { list-style:none; padding:0; margin:0; }
.listbox li { font-size:19px; line-height:1.38; padding:7px 0 7px 20px; position:relative; color:#334155; }
.dark .listbox li { color:#CBD5E1; }
.listbox li::before { content:""; position:absolute; left:0; top:15px; width:7px; height:7px;
  border-radius:50%; background:#14B8A6; }
.bigline { margin-top:38px; padding:26px 30px; border-radius:18px; background:#0A2540; color:#E2E8F0;
  font-size:25px; line-height:1.42; }
.bigline b { color:#5EEAD4; }
.visual { display:grid; grid-template-columns:278px 1fr; gap:22px; margin-top:34px; align-items:start; }
.phone { width:278px; height:604px; border-radius:28px; overflow:hidden; border:7px solid #0A2540;
  background:#fff; box-shadow:0 22px 46px rgba(15,23,42,.18); }
.phone img { width:100%; height:100%; object-fit:cover; object-position:top; }
.screen { border-radius:16px; overflow:hidden; border:1px solid #DCE5EF; background:#071A2F;
  box-shadow:0 18px 40px rgba(15,23,42,.12); }
.screen img { width:100%; height:350px; object-fit:cover; object-position:top; display:block; }
.screen-cap { font-size:14px; color:#64748B; margin:10px 2px 0; }
.tag { display:inline-block; border-radius:999px; padding:8px 14px; background:#E0F2FE;
  color:#155E8A; font-size:14px; font-weight:800; letter-spacing:.4px; margin-bottom:18px; }
.dark .tag { background:rgba(34,211,238,.12); color:#A5F3FC; }
.statrow { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:26px; }
.stat { border-radius:14px; padding:16px; background:#FFFFFF; border:1px solid #DCE5EF; }
.stat b { display:block; font-size:30px; letter-spacing:-1px; line-height:1; }
.stat span { display:block; margin-top:7px; color:#64748B; font-size:13px; }
.funnel { display:flex; align-items:stretch; gap:14px; margin-top:54px; }
.funnel .stat { flex:1; padding:22px 18px; }
.funnel .stat b { font-size:42px; letter-spacing:-2px; }
.funnel .stat span { font-size:14px; }
.funnel .arrow { display:flex; align-items:center; color:#94A3B8; font-size:28px; font-weight:800; }
.formulas { display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:26px; }
.formula { border-radius:14px; padding:18px 20px; background:#FFFFFF; border:1px solid #DCE5EF;
  font-size:18px; color:#475569; }
.dark .formula { background:rgba(127,180,210,.06); border-color:#1E3A52; color:#CBD5E1; }
.formula b { color:#0E7490; font-size:24px; }
.dark .formula b { color:#5EEAD4; }
.cover-title { margin-top:64px; font-size:85px; line-height:1.0; letter-spacing:-3.6px; font-weight:800; max-width:880px; }
.cover-sub { margin-top:26px; font-size:29px; line-height:1.4; color:#CBD5E1; max-width:770px; }
.cover-meta { position:absolute; left:80px; bottom:104px; z-index:2; font-size:19px; color:#CBD5E1; }
.cover-meta b { color:#FFFFFF; }
.cover-line { position:absolute; right:-80px; bottom:-160px; width:650px; height:650px;
  border-radius:50%; border:1px solid rgba(34,211,238,.22); }
.cover-line::before, .cover-line::after { content:""; position:absolute; border-radius:50%;
  border:1px solid rgba(34,211,238,.16); }
.cover-line::before { inset:70px; } .cover-line::after { inset:150px; }
.cta { margin-top:50px; }
.cta h1 { font-size:62px; max-width:880px; }
.links { margin-top:34px; display:grid; gap:12px; font-size:22px; color:#CBD5E1; }
.links b { color:#FFFFFF; }
.links span { color:#67E8F9; }
.checklist { display:grid; gap:14px; margin-top:36px; }
.checkrow { display:flex; gap:16px; align-items:flex-start; border-radius:14px; padding:18px 20px;
  background:rgba(127,180,210,.06); border:1px solid #1E3A52; }
.checkrow .mark { flex:none; width:28px; height:28px; border-radius:50%; display:grid; place-items:center;
  font-size:16px; font-weight:900; background:rgba(45,212,191,.15); color:#5EEAD4; }
.checkrow .mark.no { background:rgba(251,191,36,.13); color:#FCD34D; }
.checkrow p { margin:0; font-size:19px; line-height:1.4; color:#CBD5E1; }
.checkrow b { color:#FFFFFF; }
"""


def slide_cover() -> str:
    return f"""<section class="slide dark" id="slide-1">
<div class="top"><img src="{_logo(True)}" alt="NovaBank"><span class="pageno">01 / 10</span></div>
<div class="cover-line"></div>
<div class="content" style="padding-top:52px">
  <div class="kicker">Caso de portafolio · 2026</div>
  <div class="cover-title">Pagos instantáneos, cross-border y AML.</div>
  <div class="cover-sub">De la definición funcional a un sistema reproducible, probado y auditable.</div>
  <div class="rule"></div>
  <div class="band" style="margin-top:42px;max-width:770px">NovaBank es un banco <b>ficticio</b> de Paraguay.
  El caso conecta negocio, procesos, requerimientos, core, mensajería, compliance y UAT.</div>
  <div class="statrow" style="max-width:770px;margin-top:24px">
    <div class="stat"><b style="color:#67E8F9">49.582</b><span>movimientos sintéticos</span></div>
    <div class="stat"><b style="color:#5EEAD4">12</b><span>reglas AML</span></div>
    <div class="stat"><b style="color:#FCD34D">204</b><span>pruebas automatizadas</span></div>
  </div>
</div>
<div class="cover-meta"><b>Franco Tillería Centurión</b> · Business Analyst<br>
Caso ficticio · datos sintéticos · sin PII</div>
</section>"""


def slide_problem() -> str:
    cards = [
        ("01", "Pagos 24/7", "Instantáneos locales inspirados en el SPI, con estados claros y experiencia móvil."),
        ("02", "Cross-border", "ISO 20022 y MT103, IBAN/BIC, validaciones y simulación de corresponsalía."),
        ("03", "Cumplimiento", "KYC, screening, 12 reglas SQL, alertas priorizadas, casos y ROS ficticios."),
    ]
    body = "".join(
        f'<div class="card"><div class="n">{n}</div><h3>{title}</h3><p>{text}</p></div>'
        for n, title, text in cards
    )
    return f"""<section class="slide light" id="slide-2">
<div class="top"><img src="{_logo(False)}" alt="NovaBank"><span class="pageno">02 / 10</span></div>
<div class="content">
  <div class="kicker">01 / El reto</div>
  <h1>Un banco no necesita tres proyectos. Necesita una sola experiencia.</h1>
  <p class="lead">Velocidad para el cliente. Control para el banco. Trazabilidad para auditoría.
  El reto es diseñar las tres cosas sin que se estorben.</p>
  <div class="grid3">{body}</div>
  <div class="band" style="background:#E8F1F8;color:#0F172A">La tensión central: <b style="color:#0E7490">
  cada excepción de pago también es una decisión de riesgo.</b></div>
  <div class="bigline" style="margin-top:48px">Diseñar pagos es diseñar excepciones.
  <b>El camino feliz es la parte fácil.</b></div>
</div>
<div class="foot"><span><b>NovaBank</b> · caso ficticio</span><span>Payments &amp; AML Hub</span></div>
</section>"""


def slide_role() -> str:
    rows = [
        ("01", "Descubrimiento", "BRD, stakeholders, riesgos, KPIs y contexto regulatorio."),
        ("02", "Procesos", "6 BPMN y 4 DMN con AS-IS y TO-BE."),
        ("03", "Requerimientos", "10 épicas, 40 historias Gherkin, 198 SP y 16 NFR."),
        ("04", "Diseño funcional", "Core, mensajería, AML, wireframes y analítica."),
        ("05", "UAT", "65 casos, 51 automatizados y trazabilidad historia → prueba."),
    ]
    body = "".join(
        f'<div class="checkrow"><span class="mark">{n}</span><p><b>{title}</b><br>{text}</p></div>'
        for n, title, text in rows
    )
    return f"""<section class="slide dark" id="slide-3">
<div class="top"><img src="{_logo(True)}" alt="NovaBank"><span class="pageno">03 / 10</span></div>
<div class="content">
  <div class="kicker">02 / Mi rol</div>
  <h1 class="small">BA end-to-end, no solo documentos.</h1>
  <p class="lead">El alcance cubre el ciclo completo: entender el negocio, modelar el proceso,
  escribir requerimientos verificables y demostrar que el sistema responde.</p>
  <div class="checklist">{body}</div>
</div>
<div class="foot"><span><b>Franco Tillería Centurión</b> · Business Analyst</span><span>10 épicas · 40 historias · 198 SP</span></div>
</section>"""


def slide_architecture() -> str:
    layers = f"""
    <div class="layer"><div class="label">Canales</div><div class="chips">
      <span class="chip">App móvil</span><span class="chip">Banca web</span><span class="chip">API / socio</span></div></div>
    <div class="connector"></div>
    <div class="layer"><div class="label">Orquestación</div><div class="chips">
      <span class="chip">idempotencia</span><span class="chip">máquina de estados</span><span class="chip">auditoría</span></div></div>
    <div class="connector"></div>
    <div class="layer"><div class="label">Servicios</div><div class="chips">
      <span class="chip">ISO 20022 / MT103</span><span class="chip">KYC + screening</span><span class="chip">12 reglas AML</span><span class="chip">core SQLite</span></div></div>
    <div class="connector"></div>
    <div class="layer"><div class="label">Control</div><div class="chips">
      <span class="chip">libro mayor</span><span class="chip">alertas / casos</span><span class="chip">KPIs</span><span class="chip">Excel / BI</span></div></div>
    """
    return f"""<section class="slide light" id="slide-4">
<div class="top"><img src="{_logo(False)}" alt="NovaBank"><span class="pageno">04 / 10</span></div>
<div class="content">
  <div class="kicker">03 / Arquitectura</div>
  <h1 class="small">Del canal al libro mayor, con control en el camino.</h1>
  <p class="lead">Una arquitectura lógica simple, con decisiones explícitas: idempotencia,
  partida doble, validación de mensajes y alertas deduplicadas.</p>
  <div class="arch">{layers}</div>
  <div class="note">Prototipo funcional. No hay conectividad real con SPI, SWIFT, corresponsales ni cámaras.</div>
  <div class="grid3" style="margin-top:24px">
    <div class="card mini"><div class="n">DECISIÓN 01</div><h3>Idempotencia</h3>
      <p>Un reintento no duplica el pago.</p></div>
    <div class="card mini"><div class="n">DECISIÓN 02</div><h3>Partida doble</h3>
      <p>Cada débito tiene su crédito.</p></div>
    <div class="card mini"><div class="n">DECISIÓN 03</div><h3>Deduplicación</h3>
      <p>Una alerta por cliente, regla y ventana.</p></div>
  </div>
</div>
<div class="foot"><span><b>Diseño funcional</b> · no es una integración productiva</span><span>04 / 10</span></div>
</section>"""


def slide_design() -> str:
    return f"""<section class="slide dark" id="slide-5">
<div class="top"><img src="{_logo(True)}" alt="NovaBank"><span class="pageno">05 / 10</span></div>
<div class="content">
  <div class="kicker">04 / Diseño funcional</div>
  <h1 class="small">Procesos que se pueden probar, no solo dibujar.</h1>
  <p class="lead">Cada flujo tiene actores, reglas, excepciones y evidencia. La trazabilidad
  conecta el objetivo de negocio con la prueba que lo verifica.</p>
  <div class="columns">
    <div class="listbox"><h3>BPMN · 6 procesos</h3><ul>
      <li>Onboarding y KYC</li><li>Pago instantáneo local</li><li>Pago internacional</li>
      <li>Bandeja y priorización de alertas</li><li>Investigación y ROS</li><li>AS-IS / TO-BE</li></ul></div>
    <div class="listbox"><h3>DMN · 4 decisiones</h3><ul>
      <li>Scoring de riesgo</li><li>Ruteo de pagos</li><li>Prioridad de alertas</li>
      <li>Límites y excepciones</li></ul>
      <div style="margin-top:18px;padding-top:18px;border-top:1px solid #1E3A52;font-size:18px;line-height:1.45;color:#CBD5E1">
      <b style="color:#5EEAD4">40/40 historias</b> con al menos un caso de prueba asociado.</div></div>
  </div>
  <div class="bigline"><b>198 story points</b> priorizados en 10 épicas. El alcance también se negocia.</div>
  <div class="bigline" style="margin-top:26px">Un requisito sin criterio de aceptación es una intención.
  <b>La prueba lo convierte en contrato.</b></div>
</div>
<div class="foot"><span><b>BPMN 2.0 · DMN</b> · artefactos listos para importar</span><span>05 / 10</span></div>
</section>"""


def slide_data() -> str:
    chart = _png_uri(IMG_DIR / "chart-alerts-by-rule.png")
    return f"""<section class="slide light" id="slide-6">
<div class="top"><img src="{_logo(False)}" alt="NovaBank"><span class="pageno">06 / 10</span></div>
<div class="content">
  <div class="kicker">05 / Datos y AML</div>
  <h1 class="small">377 alertas no son 377 casos.</h1>
  <p class="lead">Deduplicar por cliente, regla y ventana evita inflar la cola y distorsionar
  la lectura del riesgo.</p>
  <div class="split">
    <div>
      <div class="metrics">
        <div class="metric"><div class="big">49.582</div><div class="cap">movimientos sintéticos</div></div>
        <div class="metric"><div class="big">183</div><div class="cap">días de operación</div></div>
        <div class="metric"><div class="big cyan">12</div><div class="cap">reglas SQL de monitoreo</div></div>
        <div class="metric"><div class="big mint">377</div><div class="cap">alertas deduplicadas</div></div>
      </div>
      <div class="note">500 clientes · 800 cuentas · 494 transacciones alertadas · 59 casos.
      Corte analítico reproducible.</div>
    </div>
    <div>
      <div class="chart"><img src="{chart}" alt="Alertas por regla AML"></div>
      <div class="note">Una transacción puede disparar varias reglas. La alerta consolidada
      es la unidad de trabajo del analista.</div>
    </div>
  </div>
  <div class="funnel">
    <div class="stat"><b>494</b><span>transacciones alertadas</span></div>
    <div class="arrow">→</div>
    <div class="stat"><b>377</b><span>alertas deduplicadas</span></div>
    <div class="arrow">→</div>
    <div class="stat"><b>59</b><span>casos para investigar</span></div>
  </div>
  <div class="note" style="margin-top:18px">El embudo importa: una transacción puede activar
  varias reglas y un caso puede agrupar varias alertas.</div>
  <div class="bigline" style="margin-top:34px">La alerta es el inicio de la investigación.
  <b>El caso es la unidad de decisión.</b></div>
</div>
<div class="foot"><span><b>Datos sintéticos</b> · semilla fija · sin PII</span><span>06 / 10</span></div>
</section>"""


def slide_quality() -> str:
    chart = _png_uri(IMG_DIR / "chart-confusion-matrix.png")
    return f"""<section class="slide dark" id="slide-7">
<div class="top"><img src="{_logo(True)}" alt="NovaBank"><span class="pageno">07 / 10</span></div>
<div class="content">
  <div class="kicker">06 / Calidad del monitoreo</div>
  <h1 class="small">La métrica más favorable no siempre es la más honesta.</h1>
  <div class="split" style="margin-top:34px">
    <div>
      <div style="display:grid;gap:13px">
        <div class="metric"><div class="big mint">100 %</div><div class="cap">recall sobre 341 sospechosas</div></div>
        <div class="metric"><div class="big cyan">99,13 %</div><div class="cap">precisión sobre etiquetadas</div></div>
        <div class="metric"><div class="big amber">69,03 %</div>
          <div class="cap">precisión conservadora: 341 TP / 494 alertadas</div></div>
      </div>
      <div class="note">3 falsos positivos etiquetados. 150 alertas sin ground truth:
      no se pueden contar como error ni como acierto.</div>
    </div>
    <div class="chart"><img src="{chart}" alt="Matriz de confusión AML"></div>
  </div>
  <div class="bigline" style="margin-top:28px"><b>Recall 100 %</b> no significa “cero riesgo”.
  Significa que el corte recuperó todas las sospechosas etiquetadas.</div>
  <div class="formulas">
    <div class="formula">341 / (341 + 3) = <b>99,13 %</b><br>
      <span style="font-size:14px;color:#94A3B8">precisión sobre etiquetadas</span></div>
    <div class="formula">341 / 494 = <b>69,03 %</b><br>
      <span style="font-size:14px;color:#94A3B8">precisión conservadora</span></div>
  </div>
</div>
<div class="foot"><span><b>Lectura conservadora</b> · la limitación está documentada</span><span>07 / 10</span></div>
</section>"""


def slide_product() -> str:
    phone = _png_uri(UX_DIR / "ux-app-local.png")
    dashboard = _png_uri(IMG_DIR / "dashboard-dark.png")
    return f"""<section class="slide light" id="slide-8">
<div class="top"><img src="{_logo(False)}" alt="NovaBank"><span class="pageno">08 / 10</span></div>
<div class="content">
  <div class="kicker">07 / Producto</div>
  <h1 class="small">Un caso que se puede ver, ejecutar y discutir.</h1>
  <p class="lead">Wireframes, dashboard y una demo reproducible que corre sobre una copia
  temporal de SQLite.</p>
  <div class="visual">
    <div>
      <div class="phone"><img src="{phone}" alt="Wireframe de transferencia local"></div>
      <div class="screen-cap">10 wireframes · app y consola AML</div>
    </div>
    <div>
      <div class="screen"><img src="{dashboard}" alt="Dashboard de pagos y AML"></div>
      <div class="screen-cap">Dashboard claro/oscuro · KPIs, SLA, alertas y calidad</div>
      <div class="statrow">
        <div class="stat"><b>10</b><span>wireframes</span></div>
        <div class="stat"><b>6</b><span>gráficos</span></div>
        <div class="stat"><b>GIF</b><span>demo reproducible</span></div>
      </div>
    </div>
  </div>
</div>
<div class="foot"><span><b>Artefactos generados por código</b> · capturas externas pendientes</span><span>08 / 10</span></div>
</section>"""


def slide_limits() -> str:
    rows = [
        ("", "Core con partida doble, API idempotente y conciliación."),
        ("", "ISO 20022 validado estructuralmente y simuladores deterministas."),
        ("", "12 reglas AML, alertas, casos, SLA y evaluación honesta."),
        ("no", "No hay SPI, SWIFT, corresponsales ni cámaras reales."),
        ("no", "No hay autenticación, autorización ni certificación XSD."),
        ("no", "No se declara rendimiento, alta disponibilidad ni uso de herramientas externas."),
    ]
    body = "".join(
        f'<div class="checkrow"><span class="mark {"no" if no else ""}">{"–" if no else "+"}</span><p>{text}</p></div>'
        for no, text in rows
    )
    return f"""<section class="slide dark" id="slide-9">
<div class="top"><img src="{_logo(True)}" alt="NovaBank"><span class="pageno">09 / 10</span></div>
<div class="content">
  <div class="kicker">08 / Lectura honesta</div>
  <h1 class="small">La credibilidad también se diseña.</h1>
  <p class="lead">Un portafolio serio distingue lo implementado, lo manual y lo pendiente.
  El prototipo no pretende ser un banco en producción.</p>
  <div class="checklist">{body}</div>
  <div class="bigline" style="margin-top:44px"><b>El objetivo no es parecer un banco.</b>
  Es demostrar criterio, trazabilidad y límites.</div>
</div>
<div class="foot"><span><b>Límites explícitos</b> · el alcance es parte del entregable</span><span>09 / 10</span></div>
</section>"""


def slide_close() -> str:
    return f"""<section class="slide dark" id="slide-10">
<div class="top"><img src="{_logo(True)}" alt="NovaBank"><span class="pageno">10 / 10</span></div>
<div class="cover-line" style="right:-180px;bottom:-230px"></div>
<div class="content cta" style="padding-top:118px">
  <div class="kicker">Siguiente conversación</div>
  <h1>¿Hablamos de pagos, riesgo y buenos requerimientos?</h1>
  <p class="lead">Me interesa el espacio donde el negocio, los procesos y la tecnología
  tienen que ponerse de acuerdo.</p>
  <div class="links">
    <div><b>Franco Tillería Centurión</b> · Business Analyst</div>
    <div>LinkedIn · <span>linkedin.com/in/franco-tilleria-centurion</span></div>
    <div>GitHub · <span>github.com/Vaxilium</span></div>
    <div>Repositorio · <span>github.com/Vaxilium/nova-payments-aml</span></div>
  </div>
</div>
<div class="foot"><span><b>Caso ficticio</b> · datos sintéticos · sin PII</span><span>Gracias</span></div>
</section>"""


def build_html() -> str:
    slides = [
        slide_cover(),
        slide_problem(),
        slide_role(),
        slide_architecture(),
        slide_design(),
        slide_data(),
        slide_quality(),
        slide_product(),
        slide_limits(),
        slide_close(),
    ]
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Carrusel NovaBank</title>
<style>{CSS}</style></head><body>{''.join(slides)}</body></html>"""


def render_all() -> list[Path]:
    CAROUSEL_DIR.mkdir(parents=True, exist_ok=True)
    document = build_html()
    write_text(HTML_PATH, document)
    outputs: list[Path] = []
    with browser_page(1080, 1350, scale=1) as page:
        page.set_content(document, wait_until="load")  # type: ignore[attr-defined]
        page.wait_for_timeout(500)  # type: ignore[attr-defined]
        for index, (filename, _) in enumerate(SLIDES, start=1):
            path = CAROUSEL_DIR / filename
            page.locator(f"#slide-{index}").screenshot(path=str(path))  # type: ignore[attr-defined]
            optimize_png(path, max_kb=500)
            outputs.append(path)
    with PDF_PATH.open("wb") as handle:
        handle.write(img2pdf.convert([str(path) for path in outputs]))
    outputs.append(PDF_PATH)
    outputs.append(HTML_PATH)
    return outputs


if __name__ == "__main__":
    for output in render_all():
        print(output)
