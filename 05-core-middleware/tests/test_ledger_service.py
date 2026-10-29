"""Pruebas del servicio y del motor de partida doble."""

from __future__ import annotations

from decimal import Decimal

import pytest

from app.db import connect
from app.errors import (
    CurrencyMismatchError,
    IdempotencyConflictError,
    IdempotencyKeyRequiredError,
    InsufficientFundsError,
    InvalidOperationError,
)
from app.ledger import ledger_balance, trial_balance_imbalance
from app.money import to_minor
from app.service import BankingService


def _assert_entry_balanced(db_path, operation_id: str) -> None:
    conn = connect(db_path)
    try:
        rows = conn.execute(
            """
            SELECT jl.currency, SUM(jl.debit_minor) AS debits, SUM(jl.credit_minor) AS credits,
                   COUNT(*) AS lines
            FROM journal_lines jl
            JOIN journal_entries je ON je.entry_id = jl.entry_id
            WHERE je.source_id = ?
            GROUP BY jl.currency
            """,
            (operation_id,),
        ).fetchall()
    finally:
        conn.close()
    assert rows
    for row in rows:
        assert row["debits"] == row["credits"]
        assert row["lines"] >= 2


def test_credit_account_creates_balanced_entry(service: BankingService, pyg_account: dict) -> None:
    amount = Decimal("1500")
    before = service.get_balance(pyg_account["account_id"])["balance_minor"]
    response, status, replayed = service.credit_account(
        account_id=pyg_account["account_id"],
        amount=amount,
        currency="PYG",
        idempotency_key="test-credit-0001",
        description="Prueba de crédito",
    )
    assert status == 201
    assert replayed is False
    assert response["status"] == "POSTED"
    assert service.get_balance(pyg_account["account_id"])["balance_minor"] == before + to_minor(amount, "PYG")
    _assert_entry_balanced(service.db_path, response["operation_id"])
    assert all(value == 0 for value in trial_balance_imbalance(connect(service.db_path)).values())
    assert ledger_balance(connect(service.db_path), pyg_account["account_id"]) == before + to_minor(amount, "PYG")


def test_credit_is_idempotent(service: BankingService, pyg_account: dict) -> None:
    before = service.get_balance(pyg_account["account_id"])["balance_minor"]
    first, _, replayed_first = service.credit_account(
        account_id=pyg_account["account_id"],
        amount=Decimal("2000"),
        currency="PYG",
        idempotency_key="test-idem-credit-01",
    )
    second, _, replayed_second = service.credit_account(
        account_id=pyg_account["account_id"],
        amount=Decimal("2000"),
        currency="PYG",
        idempotency_key="test-idem-credit-01",
    )
    assert replayed_first is False
    assert replayed_second is True
    assert first["operation_id"] == second["operation_id"]
    assert service.get_balance(pyg_account["account_id"])["balance_minor"] == before + 2000


def test_idempotency_conflict_on_different_payload(service: BankingService, pyg_account: dict) -> None:
    service.credit_account(
        account_id=pyg_account["account_id"],
        amount=Decimal("1000"),
        currency="PYG",
        idempotency_key="test-idem-conflict-01",
    )
    with pytest.raises(IdempotencyConflictError):
        service.credit_account(
            account_id=pyg_account["account_id"],
            amount=Decimal("9999"),
            currency="PYG",
            idempotency_key="test-idem-conflict-01",
        )


def test_missing_and_invalid_idempotency_key(service: BankingService, pyg_account: dict) -> None:
    with pytest.raises(IdempotencyKeyRequiredError):
        service.credit_account(
            account_id=pyg_account["account_id"],
            amount=Decimal("100"),
            currency="PYG",
            idempotency_key=None,
        )
    with pytest.raises(InvalidOperationError):
        service.credit_account(
            account_id=pyg_account["account_id"],
            amount=Decimal("100"),
            currency="PYG",
            idempotency_key="short",
        )


def test_debit_account_updates_balance(service: BankingService, pyg_account: dict) -> None:
    before = service.get_balance(pyg_account["account_id"])["balance_minor"]
    response, status, _ = service.debit_account(
        account_id=pyg_account["account_id"],
        amount=Decimal("800"),
        currency="PYG",
        idempotency_key="test-debit-0001",
    )
    assert status == 201
    assert service.get_balance(pyg_account["account_id"])["balance_minor"] == before - 800
    _assert_entry_balanced(service.db_path, response["operation_id"])


def test_debit_insufficient_funds(service: BankingService, pyg_account: dict) -> None:
    with pytest.raises(InsufficientFundsError):
        service.debit_account(
            account_id=pyg_account["account_id"],
            amount=Decimal("999999999999"),
            currency="PYG",
            idempotency_key="test-debit-insufficient",
        )


def test_debit_currency_mismatch(service: BankingService, pyg_account: dict) -> None:
    with pytest.raises(CurrencyMismatchError):
        service.debit_account(
            account_id=pyg_account["account_id"],
            amount=Decimal("10.00"),
            currency="USD",
            idempotency_key="test-debit-currency",
        )


def test_transfer_moves_funds_and_balances(service: BankingService, pyg_account: dict, second_pyg_account: dict) -> None:
    source_before = service.get_balance(pyg_account["account_id"])["balance_minor"]
    target_before = service.get_balance(second_pyg_account["account_id"])["balance_minor"]
    response, status, _ = service.transfer(
        from_account_id=pyg_account["account_id"],
        to_account_id=second_pyg_account["account_id"],
        amount=Decimal("1200"),
        currency="PYG",
        idempotency_key="test-transfer-0001",
    )
    assert status == 201
    assert service.get_balance(pyg_account["account_id"])["balance_minor"] == source_before - 1200
    assert service.get_balance(second_pyg_account["account_id"])["balance_minor"] == target_before + 1200
    _assert_entry_balanced(service.db_path, response["operation_id"])


def test_transfer_same_account_is_rejected(service: BankingService, pyg_account: dict) -> None:
    with pytest.raises(InvalidOperationError):
        service.transfer(
            from_account_id=pyg_account["account_id"],
            to_account_id=pyg_account["account_id"],
            amount=Decimal("100"),
            currency="PYG",
            idempotency_key="test-transfer-same",
        )


def test_transfer_insufficient_funds(service: BankingService, pyg_account: dict, second_pyg_account: dict) -> None:
    with pytest.raises(InsufficientFundsError):
        service.transfer(
            from_account_id=pyg_account["account_id"],
            to_account_id=second_pyg_account["account_id"],
            amount=Decimal("999999999999"),
            currency="PYG",
            idempotency_key="test-transfer-insufficient",
        )


def test_operation_response_includes_entries(service: BankingService, pyg_account: dict) -> None:
    response, _, _ = service.credit_account(
        account_id=pyg_account["account_id"],
        amount=Decimal("300"),
        currency="PYG",
        idempotency_key="test-operation-response",
    )
    operation = service.get_operation(response["operation_id"])
    assert operation["operation_id"] == response["operation_id"]
    assert operation["entries"]
    assert len(operation["entries"][0]["lines"]) == 2
