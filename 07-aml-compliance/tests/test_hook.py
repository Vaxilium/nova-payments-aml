"""Pruebas del hook AML para pagos internacionales."""

from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace

from aml.hook import NovabankAmlHook


def _request(account_id: str, *, name: str = "Proveedor Normal S.A.", amount: str = "100.00", country: str = "USA"):
    return SimpleNamespace(
        instruction_id=f"TEST-{name[:6]}-{amount}-{country}".replace(" ", "-"),
        debtor_account_id=account_id,
        debtor_name="Cliente NovaBank",
        creditor_name=name,
        creditor_country=country,
        amount=Decimal(amount),
        currency="USD",
    )


def test_hook_permite_pago_normal(db_path, usd_account) -> None:
    hook = NovabankAmlHook(db_path)
    decision = hook(_request(usd_account["account_id"]))
    assert decision.status == "ALLOW"
    assert hook.last_screening is not None


def test_hook_rechaza_lista_y_retiene_alto_valor(db_path, usd_account) -> None:
    hook = NovabankAmlHook(db_path)
    blocked = hook(_request(usd_account["account_id"], name="Viktor Solano"))
    assert blocked.status == "REJECT"
    held = hook(_request(usd_account["account_id"], amount="100000.00"))
    assert held.status == "HOLD"
    high_risk = hook(_request(usd_account["account_id"], country="IRN"))
    assert high_risk.status == "HOLD"


def test_hook_registra_contexto_y_screening(db_path, usd_account) -> None:
    hook = NovabankAmlHook(db_path)
    hook(_request(usd_account["account_id"], name="Proveedor Normal S.A."))
    from aml.db import connect

    conn = connect(db_path)
    try:
        assert conn.execute("SELECT COUNT(*) AS n FROM aml_payment_context").fetchone()["n"] == 1
        assert conn.execute("SELECT COUNT(*) AS n FROM aml_screening_results").fetchone()["n"] == 2
    finally:
        conn.close()
