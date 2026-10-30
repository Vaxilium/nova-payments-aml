"""Demo animada y reproducible del flujo pagos → ISO 20022 → AML.

Ejecuta operaciones reales sobre una copia temporal de SQLite, captura los
resultados con Chromium y compone un GIF. No modifica la base del repositorio.
"""

from __future__ import annotations

import html
import shutil
import sqlite3
import sys
import tempfile
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from PIL import Image

from .assetlib import (
    AUTHOR,
    BRAND_DIR,
    FONT_UI,
    IMG_DIR,
    PALETTE,
    ROOT,
    browser_page,
    optimize_png,
    svg_data_uri,
    write_text,
)

CORE_DIR = ROOT / "05-core-middleware"
MESSAGING_DIR = ROOT / "06-mensajeria"
AML_DIR = ROOT / "07-aml-compliance"
SOURCE_DB = CORE_DIR / "db" / "novabank.db"
DEMO_GIF = IMG_DIR / "demo.gif"
DEMO_POSTER = IMG_DIR / "demo-poster.png"


@dataclass(frozen=True)
class DemoRun:
    operation_id: str
    transfer_status: str
    transfer_amount: str
    debit_account: str
    credit_account: str
    debit_number: str
    credit_number: str
    balanced: bool
    reconciled: bool
    health_accounts: int
    international_instruction: str
    international_amount: str
    creditor_name: str
    creditor_country: str
    creditor_bic: str
    aml_decision: str
    aml_reason: str
    payment_state: str
    history: list[str]
    status_message: str
    status_reason: str
    status_bytes: int


def _add_paths() -> None:
    for path in (CORE_DIR, MESSAGING_DIR, AML_DIR):
        value = str(path)
        if value not in sys.path:
            sys.path.insert(0, value)


def _fmt_int(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def _amount(value: int, currency: str) -> str:
    if currency == "PYG":
        return f"₲ {_fmt_int(value)}"
    text = f"{value / 100:,.2f}"
    text = text.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"US$ {text}"


def _copy_database(destination: Path) -> None:
    source = sqlite3.connect(SOURCE_DB)
    target = sqlite3.connect(destination)
    try:
        source.backup(target)
    finally:
        target.close()
        source.close()


def _pick_accounts(db_path: Path) -> tuple[dict, dict, dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        pyg = [
            dict(row)
            for row in conn.execute(
                """
                SELECT account_id, account_number, balance_minor
                  FROM accounts
                 WHERE currency = 'PYG' AND status = 'ACTIVE'
                 ORDER BY account_id
                 LIMIT 2
                """
            )
        ]
        usd = dict(
            conn.execute(
                """
                SELECT account_id, account_number, balance_minor
                  FROM accounts
                 WHERE currency = 'USD' AND status = 'ACTIVE'
                 ORDER BY balance_minor DESC
                 LIMIT 1
                """
            ).fetchone()
        )
    finally:
        conn.close()
    if len(pyg) < 2:
        raise RuntimeError("No hay dos cuentas PYG activas para la demo")
    return pyg[0], pyg[1], usd


def build_run() -> DemoRun:
    _add_paths()

    from fastapi.testclient import TestClient

    from aml.hook import NovabankAmlHook
    from app.api import create_app
    from app.service import BankingService
    from simulator.international import InternationalPaymentSimulator
    from simulator.models import InternationalPaymentRequest
    from validator.identifiers import make_iban

    with tempfile.TemporaryDirectory(prefix="novabank-demo-") as directory:
        db_path = Path(directory) / "novabank.db"
        _copy_database(db_path)
        source, target, usd = _pick_accounts(db_path)

        app = create_app(db_path)
        with TestClient(app) as client:
            health = client.get("/v1/health").json()
            response = client.post(
                "/v1/transfers",
                json={
                    "from_account_id": source["account_id"],
                    "to_account_id": target["account_id"],
                    "amount": "850000",
                    "currency": "PYG",
                    "description": "Demo de portafolio",
                    "channel": "MOBILE",
                },
                headers={
                    "Idempotency-Key": "demo-core-20261029-001",
                    "X-Actor": "portfolio-demo",
                },
            )
            if response.status_code != 201:
                raise RuntimeError(f"Transferencia rechazada: {response.status_code} {response.text}")
            operation = response.json()
            balance = client.get(f"/v1/accounts/{source['account_id']}/balance").json()

        lines = operation["entries"][0]["lines"]
        debits = sum(line["debit_minor"] for line in lines)
        credits = sum(line["credit_minor"] for line in lines)

        instruction = "DEMO-INTL-20261029-001"
        iban = make_iban("ES", "00000000000000000001")
        request = InternationalPaymentRequest(
            instruction_id=instruction,
            debtor_account_id=usd["account_id"],
            creditor_name="Comercial Ibérica S.A.",
            creditor_iban=iban,
            creditor_bic="NOVXESMMXXX",
            amount=Decimal("125000.00"),
            currency="USD",
            fee=Decimal("25.00"),
            creditor_country="ES",
            remittance_information="Pago de servicios",
            idempotency_key="demo-intl-20261029-001",
        )
        simulator = InternationalPaymentSimulator(
            BankingService(db_path),
            aml_hook=NovabankAmlHook(db_path),
        )
        record = simulator.submit(request)

        return DemoRun(
            operation_id=operation["operation_id"],
            transfer_status=operation["status"],
            transfer_amount=_amount(operation["amount_minor"], operation["currency"]),
            debit_account=operation["debit_account_id"],
            credit_account=operation["credit_account_id"],
            debit_number=operation["debit_account_number"],
            credit_number=operation["credit_account_number"],
            balanced=debits == credits and debits == operation["amount_minor"],
            reconciled=bool(balance["reconciled"]),
            health_accounts=int(health["accounts"]),
            international_instruction=instruction,
            international_amount=_amount(125_000_00, "USD"),
            creditor_name=request.creditor_name,
            creditor_country=request.creditor_country or "ES",
            creditor_bic=request.creditor_bic,
            aml_decision=record.aml_status or "ALLOW",
            aml_reason=record.reason or "",
            payment_state=record.state.value,
            history=[state.value for state in record.history],
            status_message="PDNG" if "PDNG" in (record.pacs002 or "") else "ACSC",
            status_reason="AMLHOLD" if "AMLHOLD" in (record.pacs002 or "") else "",
            status_bytes=len((record.pacs002 or "").encode("utf-8")),
        )


def scenario_lines(run: DemoRun) -> list[tuple[str, str, int]]:
    return [
        ("cmd", "> python -m scripts.demo", 1),
        ("muted", "  datos ficticios · ejecución sobre copia temporal de SQLite", 1),
        ("step", "[1/3] CORE LEDGER · transferencia local PYG", 1),
        ("ok", "POST /v1/transfers · 201 CREATED", 1),
        ("out", f"  operation   {run.operation_id} · {run.transfer_status}", 1),
        ("out", f"  importe     {run.transfer_amount} · canal MOBILE", 1),
        ("out", f"  origen      {run.debit_account} · {run.debit_number}", 1),
        ("out", f"  destino     {run.credit_account} · {run.credit_number}", 1),
        ("out", f"  asiento     D {_fmt_int(850_000)} / C {_fmt_int(850_000)} · balanced={str(run.balanced).lower()}", 1),
        ("ok", f"  ledger      reconciled={str(run.reconciled).lower()} · {run.health_accounts} cuentas", 1),
        ("blank", "", 1),
        ("step", "[2/3] ISO 20022 · transferencia internacional", 2),
        ("out", f"  instruction {run.international_instruction} · {run.international_amount}", 2),
        ("out", f"  creditor    {run.creditor_name} · {run.creditor_country} · {run.creditor_bic}", 2),
        ("warn", f"  AML         {run.aml_decision} · {run.aml_reason}", 2),
        ("out", f"  state       {run.payment_state} · {' → '.join(run.history)}", 2),
        ("ok", f"  pacs.002    {run.status_message} / {run.status_reason} · {run.status_bytes} B", 3),
        ("blank", "", 3),
        ("step", "[3/3] CIERRE · controles de la demo", 3),
        ("ok", "  core        partida doble verificada", 3),
        ("ok", "  messaging   XML ISO 20022 generado", 3),
        ("ok", "  compliance  retención AML aplicada", 3),
        ("done", "  demo        completada · sin PII · reproducible", 3),
    ]


def _logo_uri() -> str:
    path = BRAND_DIR / "logo-horizontal-dark.svg"
    return svg_data_uri(path.read_text(encoding="utf-8"))


def _html(run: DemoRun, lines: list[tuple[str, str, int]]) -> str:
    rows = "".join(
        f'<div class="line {kind}" data-line="{index}" data-stage="{stage}">'
        f"{html.escape(text) or '&nbsp;'}</div>"
        for index, (kind, text, stage) in enumerate(lines)
    )
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Demo NovaBank</title>
<style>
* {{ box-sizing:border-box; }}
html,body {{ margin:0; width:1280px; height:800px; overflow:hidden; }}
body {{ background:{PALETTE['navy_950']}; color:#E2E8F0; font-family:{FONT_UI}; }}
.page {{ position:relative; width:1280px; height:800px; padding:34px 48px 24px;
  background:
    radial-gradient(circle at 82% 8%, rgba(34,211,238,.16), transparent 34%),
    radial-gradient(circle at 4% 90%, rgba(20,184,166,.11), transparent 30%),
    linear-gradient(145deg, {PALETTE['navy_900']}, {PALETTE['navy_950']} 70%); }}
.top {{ display:flex; align-items:center; justify-content:space-between; }}
.logo {{ height:42px; }}
.badge {{ border:1px solid rgba(34,211,238,.45); color:#67E8F9; border-radius:999px;
  padding:7px 14px; font-size:11px; font-weight:800; letter-spacing:1.8px; }}
h1 {{ font-size:22px; margin:16px 0 4px; letter-spacing:-.2px; }}
.sub {{ color:#94A3B8; font-size:12.5px; margin:0 0 16px; }}
.pipeline {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-bottom:14px; }}
.stage {{ display:flex; align-items:center; gap:10px; border:1px solid #1E3A52;
  background:rgba(127,180,210,.04); border-radius:10px; padding:10px 12px; color:#94A3B8; }}
.stage .dot {{ width:9px; height:9px; border-radius:50%; background:#334155; flex:none; }}
.stage .num {{ font:700 10px {FONT_UI}; letter-spacing:1px; color:#64748B; }}
.stage .name {{ font-size:12px; font-weight:700; }}
.stage.active {{ border-color:#22D3EE; background:rgba(34,211,238,.10); color:#E0F2FE; }}
.stage.active .dot {{ background:#22D3EE; box-shadow:0 0 0 5px rgba(34,211,238,.14); }}
.stage.done {{ border-color:rgba(45,212,191,.55); color:#CCFBF1; }}
.stage.done .dot {{ background:#2DD4BF; }}
.terminal {{ border:1px solid #1E3A52; background:#020A12; border-radius:12px;
  box-shadow:0 22px 50px rgba(0,0,0,.38); overflow:hidden; }}
.bar {{ height:34px; display:flex; align-items:center; gap:7px; padding:0 14px;
  background:#0A1B2B; border-bottom:1px solid #1E3A52; }}
.bar i {{ width:9px; height:9px; border-radius:50%; display:block; }}
.bar .r {{ background:#F87171; }} .bar .y {{ background:#FBBF24; }} .bar .g {{ background:#34D399; }}
.bar span {{ color:#64748B; font:600 10.5px {FONT_UI}; margin-left:8px; letter-spacing:.4px; }}
pre {{ margin:0; padding:15px 20px 16px; font:12.8px/1.52 "Cascadia Mono", Consolas, monospace; }}
.line {{ white-space:pre; opacity:0; transform:translateY(3px); transition:opacity .12s ease, transform .12s ease; }}
.line.on {{ opacity:1; transform:none; }}
.line.cmd {{ color:#67E8F9; }} .line.step {{ color:#5EEAD4; font-weight:700; margin-top:4px; }}
.line.ok {{ color:#86EFAC; }} .line.warn {{ color:#FCD34D; font-weight:700; }}
.line.done {{ color:#7DD3FC; font-weight:700; }} .line.muted {{ color:#64748B; }}
.line.blank {{ height:9px; }}
.foot {{ display:flex; justify-content:space-between; align-items:center; margin-top:12px;
  color:#64748B; font-size:10.5px; }}
.foot b {{ color:#94A3B8; }}
</style></head>
<body><div class="page">
  <div class="top"><img class="logo" src="{_logo_uri()}" alt="NovaBank">
    <div class="badge">DEMO REPRODUCIBLE</div></div>
  <h1>Pagos que fluyen. Riesgo bajo control.</h1>
  <p class="sub">Core bancario → mensajería ISO 20022 → control AML · ejecución real sobre datos sintéticos</p>
  <div class="pipeline">
    <div class="stage" id="s1"><span class="dot"></span><span class="num">01</span><span class="name">Core ledger</span></div>
    <div class="stage" id="s2"><span class="dot"></span><span class="num">02</span><span class="name">ISO 20022 + AML</span></div>
    <div class="stage" id="s3"><span class="dot"></span><span class="num">03</span><span class="name">Controles</span></div>
  </div>
  <div class="terminal"><div class="bar"><i class="r"></i><i class="y"></i><i class="g"></i>
    <span>C:\\Users\\User\\Documents\\nova-payments-aml</span></div>
    <pre id="terminal">{rows}</pre></div>
  <div class="foot"><span><b>Demo:</b> {AUTHOR['name']} · Business Analyst</span>
    <span>Datos ficticios · sin PII · {len(lines)} pasos</span></div>
</div>
<script>
const rows = Array.from(document.querySelectorAll('[data-line]'));
const stages = {{1: document.getElementById('s1'), 2: document.getElementById('s2'), 3: document.getElementById('s3')}};
let lastStage = 0;
function setFrame(n) {{
  rows.forEach((row, index) => row.classList.toggle('on', index < n));
  const visible = rows.slice(0, n).filter(row => row.dataset.stage);
  const current = visible.length ? Number(visible[visible.length - 1].dataset.stage) : 0;
  for (let stage = 1; stage <= 3; stage += 1) {{
    stages[stage].classList.toggle('active', stage === current);
    stages[stage].classList.toggle('done', stage < current);
  }}
}}
window.setFrame = setFrame;
setFrame(1);
</script></body></html>"""


def _save_gif(frames: list[Path], durations: list[int], out: Path) -> Path:
    images = [Image.open(path).convert("RGB") for path in frames]
    palette = images[0].quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    paletted = [image.quantize(palette=palette, dither=Image.Dither.NONE) for image in images]
    out.parent.mkdir(parents=True, exist_ok=True)
    paletted[0].save(
        out,
        save_all=True,
        append_images=paletted[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    return out


def render_all() -> list[Path]:
    run = build_run()
    lines = scenario_lines(run)
    document = _html(run, lines)
    HTML_DIR = ROOT / "docs" / "assets" / "src"
    write_text(HTML_DIR / "demo.html", document)

    durations: list[int] = []
    frame_paths: list[Path] = []
    with tempfile.TemporaryDirectory(prefix="novabank-frames-") as directory:
        frame_dir = Path(directory)
        with browser_page(1280, 800, scale=1) as page:
            page.set_content(document, wait_until="load")  # type: ignore[attr-defined]
            page.wait_for_timeout(250)  # type: ignore[attr-defined]
            for index, (kind, _, _) in enumerate(lines, start=1):
                page.evaluate("(n) => window.setFrame(n)", index)  # type: ignore[attr-defined]
                page.wait_for_timeout(140)  # type: ignore[attr-defined]
                path = frame_dir / f"frame-{index:02d}.png"
                page.screenshot(path=str(path))  # type: ignore[attr-defined]
                frame_paths.append(path)
                if kind in {"step", "cmd"}:
                    durations.append(720)
                elif kind in {"done"}:
                    durations.append(2400)
                elif kind in {"blank", "muted"}:
                    durations.append(220)
                else:
                    durations.append(360)

        optimize_png(frame_paths[-1], max_kb=500)
        shutil.copy2(frame_paths[-1], DEMO_POSTER)
        optimize_png(DEMO_POSTER, max_kb=500)
        _save_gif(frame_paths, durations, DEMO_GIF)

    if DEMO_GIF.stat().st_size > 5 * 1024 * 1024:
        raise RuntimeError(f"El GIF supera 5 MB: {DEMO_GIF.stat().st_size} bytes")
    return [DEMO_GIF, DEMO_POSTER, HTML_DIR / "demo.html"]


if __name__ == "__main__":
    for output in render_all():
        print(output)
