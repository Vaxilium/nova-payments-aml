"""Pruebas básicas de concurrencia sobre SQLite."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

from app.errors import DomainError
from app.service import BankingService


def test_concurrent_withdrawals_never_overdraw(service: BankingService, pyg_account: dict) -> None:
    account_id = pyg_account["account_id"]
    before = service.get_balance(account_id)["balance_minor"]
    amount = Decimal(before * 3 // 4)

    def withdraw(key: str):
        try:
            response, status, replayed = service.debit_account(
                account_id=account_id,
                amount=amount,
                currency="PYG",
                idempotency_key=key,
            )
            return ("ok", response["operation_id"], status, replayed)
        except DomainError as exc:
            return ("error", exc.code, None, None)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(withdraw, ["concurrent-debit-a", "concurrent-debit-b"]))

    successes = [item for item in results if item[0] == "ok"]
    failures = [item for item in results if item[0] == "error"]
    assert len(successes) == 1
    assert len(failures) == 1
    assert failures[0][1] in {"INSUFFICIENT_FUNDS", "CONCURRENT_MODIFICATION"}
    assert service.get_balance(account_id)["balance_minor"] == before - int(amount)
    assert service.get_balance(account_id)["balance_minor"] >= 0


def test_concurrent_same_idempotency_key_credits_once(service: BankingService, pyg_account: dict) -> None:
    account_id = pyg_account["account_id"]
    before = service.get_balance(account_id)["balance_minor"]

    def credit(_: int):
        return service.credit_account(
            account_id=account_id,
            amount=Decimal("1000"),
            currency="PYG",
            idempotency_key="concurrent-idem-credit",
        )

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(credit, range(2)))

    operation_ids = {result[0]["operation_id"] for result in results}
    assert len(operation_ids) == 1
    assert sorted(result[2] for result in results) == [False, True]
    assert service.get_balance(account_id)["balance_minor"] == before + 1000
