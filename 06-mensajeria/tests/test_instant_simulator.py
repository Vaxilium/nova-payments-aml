"""Pruebas del simulador de pago instantáneo local."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.db import connect
from simulator.models import (
    GatewayOutcome,
    GatewayResult,
    IdempotencyConflict,
    PaymentState,
    SimulatedGateway,
    SimulationValidationError,
)
from validator.xml_messages import validate_message


def _request(pyg_account: dict, **overrides):
    from simulator.models import InstantPaymentRequest

    payload = {
        "instruction_id": "INST-2026-0001",
        "debtor_account_id": pyg_account["account_id"],
        "creditor_name": "MARIA DEMO",
        "amount": Decimal("100000"),
        "currency": "PYG",
        "creditor_alias": "MARIA-DEMO-001",
        "idempotency_key": "idem-instant-0001",
        "description": "Pago de prueba",
    }
    payload.update(overrides)
    return InstantPaymentRequest(**payload)


def test_pago_instantaneo_externo_liquida(instant_simulator, pyg_account, service) -> None:
    before = service.get_balance(pyg_account["account_id"])["balance_minor"]
    record = instant_simulator.submit(_request(pyg_account))
    after = service.get_balance(pyg_account["account_id"])["balance_minor"]
    assert record.state == PaymentState.SETTLED
    assert record.history == [
        PaymentState.INITIATED,
        PaymentState.VALIDATED,
        PaymentState.SENT,
        PaymentState.SETTLED,
    ]
    assert record.pacs008 and validate_message(record.pacs008).valid
    assert record.pacs002 and validate_message(record.pacs002).valid
    assert after == before - 100000
    assert record.operation_id


def test_pago_instantaneo_interno_mueve_ambas_cuentas(
    instant_simulator, pyg_account, second_pyg_account, service
) -> None:
    source_before = service.get_balance(pyg_account["account_id"])["balance_minor"]
    target_before = service.get_balance(second_pyg_account["account_id"])["balance_minor"]
    request = _request(
        pyg_account,
        creditor_account_id=second_pyg_account["account_id"],
        creditor_alias=None,
        amount=Decimal("50000"),
    )
    record = instant_simulator.submit(request)
    assert record.state == PaymentState.SETTLED
    assert service.get_balance(pyg_account["account_id"])["balance_minor"] == source_before - 50000
    assert service.get_balance(second_pyg_account["account_id"])["balance_minor"] == target_before + 50000


def test_idempotencia_devuelve_el_mismo_registro(instant_simulator, pyg_account) -> None:
    request = _request(pyg_account)
    first = instant_simulator.submit(request)
    second = instant_simulator.submit(request)
    assert first is second
    assert second.attempts == 1


def test_idempotencia_conflicto(instant_simulator, pyg_account) -> None:
    instant_simulator.submit(_request(pyg_account))
    with pytest.raises(IdempotencyConflict):
        instant_simulator.submit(_request(pyg_account, amount=Decimal("200000")))


def test_limite_local(instant_simulator, pyg_account) -> None:
    with pytest.raises(SimulationValidationError):
        instant_simulator.submit(_request(pyg_account, amount=Decimal("10000001")))
    record = instant_simulator.get("INST-2026-0001")
    assert record.state == PaymentState.REJECTED
    assert record.reason_code == "AMOUNT_LIMIT"
    assert record.pacs002 and validate_message(record.pacs002).valid


def test_reintento_y_exito(service, pyg_account) -> None:
    from simulator.instant import InstantPaymentSimulator

    gateway = SimulatedGateway(
        [
            GatewayResult(GatewayOutcome.RETRYABLE),
            GatewayResult(GatewayOutcome.ACCEPTED),
        ]
    )
    simulator = InstantPaymentSimulator(service, gateway=gateway)
    record = simulator.submit(_request(pyg_account))
    assert record.state == PaymentState.SETTLED
    assert record.attempts == 2


def test_timeout_expira(service, pyg_account) -> None:
    from simulator.instant import InstantPaymentSimulator

    gateway = SimulatedGateway([GatewayResult(GatewayOutcome.TIMEOUT)])
    simulator = InstantPaymentSimulator(service, gateway=gateway)
    record = simulator.submit(_request(pyg_account))
    assert record.state == PaymentState.EXPIRED
    assert record.reason_code == "TIMEOUT"
    assert record.pacs002 and validate_message(record.pacs002).valid


def test_rechazo_del_psp(service, pyg_account) -> None:
    from simulator.instant import InstantPaymentSimulator

    gateway = SimulatedGateway(
        [GatewayResult(GatewayOutcome.REJECTED, reason_code="AC01", detail="Cuenta inválida")]
    )
    simulator = InstantPaymentSimulator(service, gateway=gateway)
    record = simulator.submit(_request(pyg_account))
    assert record.state == PaymentState.REJECTED
    assert record.reason_code == "AC01"
    assert record.pacs002 and validate_message(record.pacs002).valid


def test_saldo_insuficiente(db_path, service, pyg_account) -> None:
    from simulator.instant import InstantPaymentSimulator

    conn = connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO accounts
                (account_id, customer_id, account_number, account_type, currency,
                 status, balance_minor, overdraft_limit_minor, version, opened_at)
            VALUES ('ACC-LOW', ?, '99999999999999', 'SAVINGS', 'PYG',
                    'ACTIVE', 100, 0, 1, '2026-01-01T00:00:00')
            """,
            (pyg_account["customer_id"],),
        )
    finally:
        conn.close()
    simulator = InstantPaymentSimulator(service)
    request = _request(pyg_account, debtor_account_id="ACC-LOW", amount=Decimal("1000"))
    record = simulator.submit(request)
    assert record.state == PaymentState.REJECTED
    assert record.reason_code == "AM04"


def test_cuenta_destino_inexistente(instant_simulator, pyg_account) -> None:
    with pytest.raises(SimulationValidationError):
        instant_simulator.submit(
            _request(pyg_account, creditor_account_id="ACC-NO-EXISTE", creditor_alias=None)
        )


def test_misma_cuenta_rechazada(instant_simulator, pyg_account) -> None:
    with pytest.raises(SimulationValidationError):
        instant_simulator.submit(
            _request(
                pyg_account,
                creditor_account_id=pyg_account["account_id"],
                creditor_alias=None,
            )
        )
