"""Pruebas del simulador internacional y de su asiento contable."""

from __future__ import annotations

from contextlib import closing
from decimal import Decimal

import pytest

from app.db import connect
from app.ledger import ledger_balance
from simulator.international import InternationalPaymentSimulator
from simulator.models import (
    AmlResult,
    GatewayOutcome,
    GatewayResult,
    IdempotencyConflict,
    InternationalPaymentRequest,
    PaymentState,
    SimulatedGateway,
    SimulationValidationError,
)
from validator.xml_messages import validate_message, validate_pacs008_international


def _request(usd_account: dict, **overrides):
    payload = {
        "instruction_id": "INTL-2026-0001",
        "debtor_account_id": usd_account["account_id"],
        "debtor_name": "ANA DEMO",
        "creditor_name": "JOHN DEMO",
        "creditor_iban": "DE89370400440532013000",
        "creditor_bic": "NOVBDEFF",
        "creditor_country": "DE",
        "amount": Decimal("100.00"),
        "currency": "USD",
        "fee": Decimal("25.00"),
        "charge_bearer": "SHA",
        "remittance_information": "INVOICE 2026-001",
        "idempotency_key": "idem-intl-0001",
    }
    payload.update(overrides)
    return InternationalPaymentRequest(**payload)


def test_internacional_liquida_y_contabiliza(service, usd_account) -> None:
    simulator = InternationalPaymentSimulator(service)
    before = service.get_balance(usd_account["account_id"])["balance_minor"]
    record = simulator.submit(_request(usd_account))
    after = service.get_balance(usd_account["account_id"])["balance_minor"]
    assert record.state == PaymentState.SETTLED
    assert record.pacs008 and validate_pacs008_international(record.pacs008).valid
    assert record.pacs002 and validate_message(record.pacs002).valid
    assert after == before - 12500
    with closing(connect(service.db_path)) as ledger_conn:
        assert ledger_balance(ledger_conn, usd_account["account_id"]) == after

    conn = connect(service.db_path)
    try:
        entry = conn.execute(
            "SELECT entry_id FROM journal_entries WHERE source_id = ?",
            (record.operation_id,),
        ).fetchone()
        assert entry is not None
        rows = conn.execute(
            """
            SELECT gl.code, jl.debit_minor, jl.credit_minor
            FROM journal_lines jl JOIN gl_accounts gl ON gl.gl_account_id = jl.gl_account_id
            WHERE jl.entry_id = ?
            """,
            (entry["entry_id"],),
        ).fetchall()
        totals = {row["code"]: (row["debit_minor"], row["credit_minor"]) for row in rows}
        assert totals["2102"] == (12500, 0)
        assert totals["1102"] == (0, 10000)
        assert totals["4102"] == (0, 2500)
        fee = conn.execute(
            "SELECT amount_minor FROM fees WHERE transaction_id = ?",
            (record.operation_id,),
        ).fetchone()
        assert fee["amount_minor"] == 2500
    finally:
        conn.close()


def test_internacional_sin_comision(service, usd_account) -> None:
    simulator = InternationalPaymentSimulator(service)
    record = simulator.submit(_request(usd_account, fee=Decimal("0"), idempotency_key="idem-intl-0002"))
    assert record.state == PaymentState.SETTLED
    conn = connect(service.db_path)
    try:
        fee = conn.execute(
            "SELECT COUNT(*) AS total FROM fees WHERE transaction_id = ?",
            (record.operation_id,),
        ).fetchone()
        assert fee["total"] == 0
    finally:
        conn.close()


def test_internacional_idempotencia(service, usd_account) -> None:
    simulator = InternationalPaymentSimulator(service)
    request = _request(usd_account)
    first = simulator.submit(request)
    second = simulator.submit(request)
    assert first is second


def test_internacional_idempotencia_conflicto(service, usd_account) -> None:
    simulator = InternationalPaymentSimulator(service)
    simulator.submit(_request(usd_account))
    with pytest.raises(IdempotencyConflict):
        simulator.submit(_request(usd_account, amount=Decimal("200.00")))


def test_internacional_rechaza_eur(service, usd_account) -> None:
    simulator = InternationalPaymentSimulator(service)
    with pytest.raises(SimulationValidationError):
        simulator.submit(_request(usd_account, currency="EUR"))
    record = simulator.get("INTL-2026-0001")
    assert record.state == PaymentState.REJECTED
    assert record.reason_code == "CURRENCY_NOT_SETTLEABLE"


def test_internacional_valida_iban_y_bic(service, usd_account) -> None:
    simulator = InternationalPaymentSimulator(service)
    with pytest.raises(SimulationValidationError):
        simulator.submit(
            _request(
                usd_account,
                creditor_iban="DE88370400440532013000",
                creditor_bic="NOVBDEFF",
                idempotency_key="idem-intl-0002",
            )
        )
    simulator = InternationalPaymentSimulator(service)
    with pytest.raises(SimulationValidationError):
        simulator.submit(
            _request(
                usd_account,
                creditor_bic="NOVBDE",
                idempotency_key="idem-intl-0003",
            )
        )


def test_internacional_pais_iban_no_coincide(service, usd_account) -> None:
    simulator = InternationalPaymentSimulator(service)
    with pytest.raises(SimulationValidationError):
        simulator.submit(_request(usd_account, creditor_country="ES"))


def test_internacional_aml_hold(service, usd_account) -> None:
    simulator = InternationalPaymentSimulator(
        service,
        aml_hook=lambda request: AmlResult(status="HOLD", reason="Revisión manual"),
    )
    record = simulator.submit(_request(usd_account))
    assert record.state == PaymentState.HELD
    assert record.aml_status == "HOLD"
    assert record.operation_id is None
    assert record.pacs008 is None
    assert record.pacs002 and validate_message(record.pacs002).valid


def test_internacional_aml_reject(service, usd_account) -> None:
    simulator = InternationalPaymentSimulator(
        service,
        aml_hook=lambda request: AmlResult(status="REJECT", reason="Lista ficticia"),
    )
    record = simulator.submit(_request(usd_account))
    assert record.state == PaymentState.REJECTED
    assert record.reason_code == "FF01"
    assert record.pacs002 and validate_message(record.pacs002).valid


def test_internacional_reintento(service, usd_account) -> None:
    gateway = SimulatedGateway(
        [GatewayResult(GatewayOutcome.RETRYABLE), GatewayResult(GatewayOutcome.ACCEPTED)]
    )
    simulator = InternationalPaymentSimulator(service, gateway=gateway)
    record = simulator.submit(_request(usd_account))
    assert record.state == PaymentState.SETTLED
    assert record.attempts == 2


def test_internacional_timeout(service, usd_account) -> None:
    simulator = InternationalPaymentSimulator(
        service,
        gateway=SimulatedGateway([GatewayResult(GatewayOutcome.TIMEOUT)]),
    )
    record = simulator.submit(_request(usd_account))
    assert record.state == PaymentState.EXPIRED
    assert record.pacs002 and validate_message(record.pacs002).valid


def test_internacional_saldo_insuficiente(db_path, service, usd_account) -> None:
    conn = connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO accounts
                (account_id, customer_id, account_number, account_type, currency,
                 status, balance_minor, overdraft_limit_minor, version, opened_at)
            VALUES ('ACC-LOW-USD', ?, '99999999999998', 'CHECKING', 'USD',
                    'ACTIVE', 100, 0, 1, '2026-01-01T00:00:00')
            """,
            (usd_account["customer_id"],),
        )
    finally:
        conn.close()
    simulator = InternationalPaymentSimulator(service)
    record = simulator.submit(
        _request(usd_account, debtor_account_id="ACC-LOW-USD", idempotency_key="idem-intl-0002")
    )
    assert record.state == PaymentState.REJECTED
    assert record.reason_code == "AM04"


def test_internacional_charge_bearer_our(service, usd_account) -> None:
    simulator = InternationalPaymentSimulator(service)
    record = simulator.submit(_request(usd_account, charge_bearer="OUR"))
    assert record.state == PaymentState.SETTLED
    assert ">DEBT<" in (record.pacs008 or "")
