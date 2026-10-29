"""Casos de borde UAT que complementan la suite de fases 3 a 6."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.db import connect
from app.service import BankingService
from simulator.instant import InstantPaymentSimulator
from simulator.models import InstantPaymentRequest, PaymentState, SimulationValidationError


def _request(account_id: str, amount: str, key: str, currency: str = "PYG") -> InstantPaymentRequest:
    return InstantPaymentRequest(
        instruction_id=f"UAT-{key}",
        debtor_account_id=account_id,
        creditor_name="BENEFICIARIO UAT",
        amount=Decimal(amount),
        currency=currency,
        creditor_alias="BENEFICIARIO-UAT-001",
        idempotency_key=key,
        description="Caso de borde UAT",
    )


def _account_with_balance(db_path, customer_id: str, balance_minor: int) -> str:
    account_id = "ACC-UAT-LIMIT"
    conn = connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO accounts
                (account_id, customer_id, account_number, account_type, currency,
                 status, balance_minor, overdraft_limit_minor, version, opened_at)
            VALUES (?, ?, '99999999999997', 'SAVINGS', 'PYG', 'ACTIVE', ?, 0, 1, '2026-01-01T00:00:00')
            """,
            (account_id, customer_id, balance_minor),
        )
        conn.commit()
    finally:
        conn.close()
    return account_id


def test_limite_exacto_aprobado(db_path, service: BankingService, pyg_account: dict) -> None:
    account_id = _account_with_balance(db_path, pyg_account["customer_id"], 20_000_000)
    simulator = InstantPaymentSimulator(service)
    record = simulator.submit(_request(account_id, "10000000", "uat-limit-exact-01"))
    assert record.state == PaymentState.SETTLED
    assert service.get_balance(account_id)["balance_minor"] == 10_000_000


def test_monto_cero_rechazado(instant_simulator: InstantPaymentSimulator, pyg_account: dict) -> None:
    with pytest.raises(SimulationValidationError):
        instant_simulator.submit(_request(pyg_account["account_id"], "0", "uat-zero-amount-01"))
    record = instant_simulator.get("UAT-uat-zero-amount-01")
    assert record.state == PaymentState.REJECTED
    assert record.reason_code == "AMOUNT_NOT_POSITIVE"


def test_monto_negativo_rechazado(instant_simulator: InstantPaymentSimulator, pyg_account: dict) -> None:
    with pytest.raises(SimulationValidationError):
        instant_simulator.submit(_request(pyg_account["account_id"], "-1", "uat-negative-amount-01"))
    record = instant_simulator.get("UAT-uat-negative-amount-01")
    assert record.state == PaymentState.REJECTED
    assert record.reason_code == "AMOUNT_NOT_POSITIVE"


def test_pyg_con_decimales_rechazado(instant_simulator: InstantPaymentSimulator, pyg_account: dict) -> None:
    with pytest.raises(SimulationValidationError):
        instant_simulator.submit(_request(pyg_account["account_id"], "10.5", "uat-pyg-decimals-01"))
    record = instant_simulator.get("UAT-uat-pyg-decimals-01")
    assert record.state == PaymentState.REJECTED
    assert record.reason_code == "AMOUNT_PRECISION"


def test_moneda_no_local_rechazada(instant_simulator: InstantPaymentSimulator, pyg_account: dict) -> None:
    request = _request(pyg_account["account_id"], "1000", "uat-currency-local-01", currency="USD")
    with pytest.raises(SimulationValidationError):
        instant_simulator.submit(request)
    record = instant_simulator.get("UAT-uat-currency-local-01")
    assert record.state == PaymentState.REJECTED
    assert record.reason_code in {"CURRENCY_NOT_LOCAL", "DEBTOR_CURRENCY"}
