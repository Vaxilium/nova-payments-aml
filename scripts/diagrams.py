"""Renderizado de arquitectura, secuencias y BPMN con Playwright.

Mermaid y bpmn-js se instalan en una caché temporal fuera del repositorio.
El script es reproducible: si las dependencias no están, indica el comando exacto.
"""

from __future__ import annotations

import base64
import re
from pathlib import Path

from .assetlib import (
    DEFAULT_NODE_MODULES,
    FONT_UI,
    IMG_DIR,
    PALETTE,
    ROOT,
    optimize_png,
    read_text,
    render_html,
    write_text,
)

MERMAID_JS = DEFAULT_NODE_MODULES / "mermaid" / "dist" / "mermaid.min.js"
BPMN_JS = DEFAULT_NODE_MODULES / "bpmn-js" / "dist" / "bpmn-viewer.production.min.js"
BPMN_CSS_DIR = DEFAULT_NODE_MODULES / "bpmn-js" / "dist" / "assets"

ARCHITECTURE_MMD = """flowchart LR
    subgraph CAN["Canales"]
        C1["Cliente persona"]
        C2["Cliente empresa"]
        C3["API FastAPI /v1"]
    end
    subgraph ORQ["Orquestación"]
        O1["Orquestador de pagos"]
        O2["Idempotencia y correlación"]
    end
    subgraph VAL["Validación"]
        V1["Validador ISO 20022<br/>IBAN · BIC · ISO 4217"]
    end
    subgraph RSK["Riesgo y cumplimiento"]
        R1["KYC y screening"]
        R2["Monitoreo AML<br/>12 reglas SQL"]
        R3["Alertas · casos · ROS"]
    end
    subgraph MSG["Mensajería"]
        M1["pacs.008 · pacs.002<br/>MT103"]
    end
    subgraph CORE["Core simulado"]
        K1["SQLite"]
        K2["Libro mayor<br/>partida doble"]
    end
    subgraph DAT["Analítica"]
        D1["Dataset analítico"]
        D2["Excel · Power BI<br/>Tableau"]
    end
    subgraph AUD["Control"]
        A1["Auditoría<br/>y trazabilidad"]
    end

    C1 --> C3
    C2 --> C3
    C3 --> O1
    O1 --> O2
    O1 --> V1
    O1 --> R1
    R1 --> R2
    R2 --> R3
    V1 --> M1
    M1 --> K1
    K1 --> K2
    R3 --> D1
    K2 --> D1
    D1 --> D2
    C3 --> A1
    K1 --> A1
    R2 --> A1

    classDef channel fill:#155E8A,stroke:#22D3EE,color:#F8FAFC,stroke-width:2px;
    classDef process fill:#103B5C,stroke:#5EEAD4,color:#F8FAFC,stroke-width:1.5px;
    classDef risk fill:#3B2A0B,stroke:#FBBF24,color:#FEF3C7,stroke-width:1.5px;
    classDef core fill:#0B3B60,stroke:#22D3EE,color:#F8FAFC,stroke-width:1.5px;
    classDef data fill:#134E4A,stroke:#2DD4BF,color:#CCFBF1,stroke-width:1.5px;
    class C1,C2,C3 channel;
    class O1,O2,V1,M1 process;
    class R1,R2,R3 risk;
    class K1,K2 core;
    class D1,D2 data;
    class A1 process;
"""

SEQUENCE_FILES = [
    (
        ROOT / "06-mensajeria" / "diagrams" / "flujo-instantaneo.mmd",
        "Pago instantáneo local",
        "Flujo de la máquina de estados del simulador inspirado en el SPI del BCP.",
        "sequence-instant.png",
    ),
    (
        ROOT / "06-mensajeria" / "diagrams" / "flujo-internacional.mmd",
        "Pago internacional",
        "Validación, hook AML, gateway simulado y posteo contable de una transferencia internacional.",
        "sequence-international.png",
    ),
]

BPMN_FILES = [
    ("onboarding-kyc.bpmn", "Onboarding y KYC"),
    ("transferencia-instantanea-as-is.bpmn", "Transferencia instantánea — AS-IS"),
    ("transferencia-instantanea-to-be.bpmn", "Transferencia instantánea — TO-BE"),
    ("transferencia-internacional-to-be.bpmn", "Transferencia internacional — TO-BE"),
    ("alerta-aml.bpmn", "Gestión de alertas AML"),
    ("investigacion-ros.bpmn", "Investigación y ROS"),
]


def _base_css() -> str:
    return f"""
    * {{ box-sizing: border-box; }}
    html, body {{ margin:0; padding:0; background:{PALETTE['navy_900']}; color:#E6F1F8;
      font-family:{FONT_UI}; }}
    .card {{ width:1800px; background:{PALETTE['navy_900']}; padding:52px 64px 44px; }}
    .eyebrow {{ color:{PALETTE['turquoise_400']}; font-size:15px; font-weight:700;
      letter-spacing:2.4px; text-transform:uppercase; margin-bottom:10px; }}
    h1 {{ margin:0 0 8px; font-size:38px; line-height:1.1; letter-spacing:-0.8px; }}
    .sub {{ color:{PALETTE['slate_300']}; font-size:17px; margin:0 0 30px; max-width:1300px; }}
    .diagram {{ background:{PALETTE['navy_800']}; border:1px solid #1E4E75; border-radius:18px;
      padding:36px 44px; min-height:300px; }}
    .diagram svg {{ display:block; width:100%; max-width:none !important; height:auto; margin:0 auto; }}
    .foot {{ margin-top:24px; color:{PALETTE['slate_400']}; font-size:13px; display:flex;
      justify-content:space-between; gap:24px; }}
    .pill {{ color:{PALETTE['cyan_300']}; font-weight:700; }}
    """


def _mermaid_config() -> dict[str, object]:
    return {
        "startOnLoad": False,
        "securityLevel": "loose",
        "theme": "base",
        "fontFamily": FONT_UI,
        "themeVariables": {
            "background": PALETTE["navy_800"],
            "primaryColor": PALETTE["navy_700"],
            "primaryTextColor": "#E6F1F8",
            "primaryBorderColor": PALETTE["cyan_400"],
            "lineColor": PALETTE["mint_300"],
            "secondaryColor": PALETTE["navy_600"],
            "tertiaryColor": PALETTE["navy_900"],
            "mainBkg": PALETTE["navy_700"],
            "nodeBorder": PALETTE["cyan_400"],
            "clusterBkg": PALETTE["navy_800"],
            "clusterBorder": "#1E4E75",
            "titleColor": "#E6F1F8",
            "edgeLabelBackground": PALETTE["navy_900"],
            "actorBkg": PALETTE["navy_700"],
            "actorBorder": PALETTE["cyan_400"],
            "actorTextColor": "#E6F1F8",
            "signalColor": PALETTE["mint_300"],
            "signalTextColor": "#E6F1F8",
            "labelBoxBkgColor": PALETTE["navy_700"],
            "labelBoxBorderColor": PALETTE["turquoise_400"],
            "labelTextColor": "#E6F1F8",
            "loopTextColor": "#E6F1F8",
            "noteBkgColor": "#3B2A0B",
            "noteBorderColor": PALETTE["amber_400"],
            "noteTextColor": "#FEF3C7",
            "activationBkgColor": PALETTE["navy_600"],
            "activationBorderColor": PALETTE["cyan_400"],
        },
        "flowchart": {"curve": "basis", "htmlLabels": True, "nodeSpacing": 44, "rankSpacing": 64},
        "sequence": {
            "useMaxWidth": True,
            "mirrorActors": False,
            "wrap": True,
            "diagramMarginX": 30,
            "diagramMarginY": 30,
        },
    }


def _render_mermaid(
    code: str,
    out: Path,
    *,
    title: str,
    subtitle: str,
    source: str,
    width: int = 1800,
) -> None:
    from .assetlib import browser_page

    if not MERMAID_JS.exists():
        raise FileNotFoundError(
            f"No se encontró mermaid en {MERMAID_JS}. "
            "Instalar con: npm install --prefix %TEMP%\\opencode\\assets-npm mermaid@11.12.0"
        )
    mermaid_js = MERMAID_JS.read_text(encoding="utf-8")
    body = f"""
    <div class="card" id="card">
      <div class="eyebrow">NovaBank · arquitectura y procesos</div>
      <h1>{title}</h1>
      <p class="sub">{subtitle}</p>
      <div class="diagram" id="diagram"></div>
      <div class="foot"><span>Fuente: {source}</span><span class="pill">Caso ficticio · datos sintéticos</span></div>
    </div>"""
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<style>{_base_css()}</style></head><body>{body}</body></html>"""
    with browser_page(width + 128, 1200) as page:
        page.set_content(html, wait_until="load")  # type: ignore[attr-defined]
        page.add_script_tag(content=mermaid_js)  # type: ignore[attr-defined]
        page.evaluate(  # type: ignore[attr-defined]
            """([code, config]) => {
                mermaid.initialize(config);
                return mermaid.render('asset-diagram', code)
                  .then((result) => { document.getElementById('diagram').innerHTML = result.svg; window.__ok = true; })
                  .catch((error) => { window.__err = String(error); });
            }""",
            [code, _mermaid_config()],
        )
        page.wait_for_function("window.__ok || window.__err", timeout=30000)  # type: ignore[attr-defined]
        error = page.evaluate("window.__err || null")  # type: ignore[attr-defined]
        if error:
            raise RuntimeError(f"Mermaid falló para {out.name}: {error}")
        page.wait_for_timeout(500)  # type: ignore[attr-defined]
        page.locator("#card").screenshot(path=str(out))  # type: ignore[attr-defined]
    optimize_png(out, max_kb=500)


def render_architecture() -> Path:
    out = IMG_DIR / "architecture.png"
    _render_mermaid(
        ARCHITECTURE_MMD,
        out,
        title="Arquitectura lógica de NovaBank",
        subtitle="Pagos instantáneos, cross-border y monitoreo AML en un mismo flujo, con trazabilidad de punta a punta.",
        source="02-procesos/diagramas-sistema.md y README.md (fuente Mermaid generada por scripts/diagrams.py).",
    )
    return out


def render_sequences() -> list[Path]:
    outputs: list[Path] = []
    for path, title, subtitle, filename in SEQUENCE_FILES:
        code = read_text(path)
        out = IMG_DIR / filename
        _render_mermaid(
            code,
            out,
            title=title,
            subtitle=subtitle,
            source=str(path.relative_to(ROOT)).replace("\\", "/"),
            width=1700,
        )
        outputs.append(out)
    return outputs


def _bpmn_css() -> str:
    """Incrusta las fuentes de bpmn-js para que el render no dependa de rutas."""
    if not BPMN_CSS_DIR.exists():
        raise FileNotFoundError(
            f"No se encontró bpmn-js en {BPMN_CSS_DIR}. "
            "Instalar con: npm install --prefix %TEMP%\\opencode\\assets-npm bpmn-js@18.6.2"
        )
    css = "\n".join(
        [
            read_text(BPMN_CSS_DIR / "diagram-js.css"),
            read_text(BPMN_CSS_DIR / "bpmn-js.css"),
            read_text(BPMN_CSS_DIR / "bpmn-font" / "css" / "bpmn-embedded.css"),
        ]
    )

    def replace_font(match: re.Match[str]) -> str:
        relative = match.group(1).split("?", 1)[0].split("#", 1)[0]
        font_path = BPMN_CSS_DIR / "bpmn-font" / relative.lstrip("./")
        if not font_path.exists():
            return match.group(0)
        suffix = font_path.suffix.lower().lstrip(".")
        mime = {
            "woff2": "font/woff2",
            "woff": "font/woff",
            "ttf": "font/ttf",
            "eot": "application/vnd.ms-fontobject",
            "svg": "image/svg+xml",
        }.get(suffix, "application/octet-stream")
        payload = base64.b64encode(font_path.read_bytes()).decode("ascii")
        return f"url('data:{mime};base64,{payload}')"

    return re.sub(r"url\('([^']+)'\)", replace_font, css)


def render_bpmn() -> list[Path]:
    from .assetlib import browser_page

    if not BPMN_JS.exists():
        raise FileNotFoundError(f"No se encontró bpmn-js en {BPMN_JS}")
    bpmn_js = read_text(BPMN_JS)
    css = _bpmn_css()
    outputs: list[Path] = []

    for filename, title in BPMN_FILES:
        source_path = ROOT / "02-procesos" / "bpmn" / filename
        xml = read_text(source_path)
        out = IMG_DIR / "bpmn" / f"{source_path.stem}.png"
        html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<style>{css}
* {{ box-sizing:border-box; }}
html,body {{ margin:0; background:#F8FAFC; font-family:{FONT_UI}; }}
#canvas {{ width:1688px; height:760px; background:#FFFFFF; }}
</style></head>
<body><div id="canvas"></div></body></html>"""

        with browser_page(1800, 1000, scale=1) as page:
            page.set_content(html, wait_until="load")  # type: ignore[attr-defined]
            page.add_script_tag(content=bpmn_js)  # type: ignore[attr-defined]
            page.evaluate("(xml) => { window.XML = xml; }", xml)  # type: ignore[attr-defined]
            page.evaluate(  # type: ignore[attr-defined]
                """() => {
                    window.__viewer = new BpmnJS({ container: document.getElementById('canvas') });
                    window.__done = false;
                    window.__viewer.importXML(window.XML)
                      .then(() => { window.__done = true; })
                      .catch((error) => { window.__err = String(error); });
                }"""
            )
            page.wait_for_function("window.__done || window.__err", timeout=30000)  # type: ignore[attr-defined]
            error = page.evaluate("window.__err || null")  # type: ignore[attr-defined]
            if error:
                raise RuntimeError(f"bpmn-js falló para {filename}: {error}")
            page.wait_for_timeout(300)  # type: ignore[attr-defined]
            svg = page.evaluate(  # type: ignore[attr-defined]
                "window.__viewer.saveSVG().then((result) => result.svg)"
            )

        svg_path = IMG_DIR / "bpmn" / f"{source_path.stem}.svg"
        write_text(svg_path, svg)

        card_css = f"""
        * {{ box-sizing:border-box; }}
        html, body {{ margin:0; background:#F8FAFC; font-family:{FONT_UI}; }}
        .card {{ width:1800px; padding:44px 56px 36px; background:#F8FAFC; }}
        .eyebrow {{ color:{PALETTE['navy_600']}; font-size:14px; font-weight:700; letter-spacing:2.2px;
          text-transform:uppercase; }}
        h1 {{ margin:8px 0 6px; color:{PALETTE['navy_800']}; font-size:34px; letter-spacing:-0.6px; }}
        .sub {{ margin:0 0 22px; color:{PALETTE['slate_500']}; font-size:15px; }}
        .canvas {{ background:#FFFFFF; border:1px solid {PALETTE['slate_200']}; border-radius:14px;
          padding:22px 26px; }}
        .canvas svg {{ display:block; width:100%; height:auto; }}
        .foot {{ margin-top:18px; display:flex; justify-content:space-between; color:{PALETTE['slate_500']};
          font-size:12px; }}
        """
        body = f"""<div class="card" id="card">
        <div class="eyebrow">BPMN 2.0 · proceso de negocio</div>
        <h1>{title}</h1>
        <p class="sub">Diagrama importado del archivo BPMN 2.0 del repositorio y renderizado con bpmn-js.</p>
        <div class="canvas">{svg}</div>
        <div class="foot"><span>Fuente: 02-procesos/bpmn/{filename}</span><span>NovaBank · caso ficticio</span></div>
        </div>"""
        render_html(
            body,
            out,
            width=1800,
            height=1200,
            selector="#card",
            wait_ms=250,
            max_kb=500,
            css=card_css,
            title=f"{title} · NovaBank",
        )
        optimize_png(out, max_kb=500)
        outputs.append(out)
    return outputs


def render_all() -> list[Path]:
    outputs = [render_architecture()]
    outputs.extend(render_sequences())
    outputs.extend(render_bpmn())
    return outputs
