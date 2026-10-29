"""Pruebas de la API REST /v1."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.db import connect


def _headers(key: str) -> dict[str, str]:
    return {"Idempotency-Key": key}


def test_health(client: TestClient) -> None:
    response = client.get("/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["accounts"] > 0
    assert response.headers["X-Correlation-ID"].startswith("COR-")


def test_list_and_get_customers(client: TestClient) -> None:
    listing = client.get("/v1/customers", params={"limit": 5})
    assert listing.status_code == 200
    customers = listing.json()
    assert len(customers) == 5
    detail = client.get(f"/v1/customers/{customers[0]['customer_id']}")
    assert detail.status_code == 200
    assert detail.json()["customer_id"] == customers[0]["customer_id"]
    assert detail.json()["account_count"] >= 1


def test_customer_not_found(client: TestClient) -> None:
    response = client.get("/v1/customers/CUS-NOEXISTE")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "CUSTOMER_NOT_FOUND"


def test_customer_accounts_and_account_detail(client: TestClient, pyg_account: dict) -> None:
    response = client.get(f"/v1/customers/{pyg_account['customer_id']}/accounts")
    assert response.status_code == 200
    assert any(item["account_id"] == pyg_account["account_id"] for item in response.json())
    detail = client.get(f"/v1/accounts/{pyg_account['account_id']}")
    assert detail.status_code == 200
    assert detail.json()["account_id"] == pyg_account["account_id"]


def test_account_not_found(client: TestClient) -> None:
    response = client.get("/v1/accounts/ACC-NOEXISTE")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "ACCOUNT_NOT_FOUND"


def test_balance_is_reconciled(client: TestClient, pyg_account: dict) -> None:
    response = client.get(f"/v1/accounts/{pyg_account['account_id']}/balance")
    assert response.status_code == 200
    body = response.json()
    assert body["reconciled"] is True
    assert body["ledger_balance_minor"] == body["balance_minor"]


def test_credit_via_api_and_operation_status(client: TestClient, pyg_account: dict) -> None:
    before = client.get(f"/v1/accounts/{pyg_account['account_id']}/balance").json()["balance_minor"]
    response = client.post(
        f"/v1/accounts/{pyg_account['account_id']}/credits",
        json={"amount": "1500", "currency": "PYG", "description": "Crédito API"},
        headers=_headers("api-credit-0001"),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "POSTED"
    assert body["amount"] == "1500"
    after = client.get(f"/v1/accounts/{pyg_account['account_id']}/balance").json()["balance_minor"]
    assert after == before + 1500
    operation = client.get(f"/v1/operations/{body['operation_id']}")
    assert operation.status_code == 200
    assert operation.json()["entries"][0]["lines"]


def test_idempotent_replay_returns_same_operation(client: TestClient, pyg_account: dict) -> None:
    payload = {"amount": "700", "currency": "PYG"}
    first = client.post(
        f"/v1/accounts/{pyg_account['account_id']}/credits",
        json=payload,
        headers=_headers("api-idem-replay-01"),
    )
    second = client.post(
        f"/v1/accounts/{pyg_account['account_id']}/credits",
        json=payload,
        headers=_headers("api-idem-replay-01"),
    )
    assert first.status_code == second.status_code == 201
    assert first.json()["operation_id"] == second.json()["operation_id"]
    assert first.headers["Idempotent-Replayed"] == "false"
    assert second.headers["Idempotent-Replayed"] == "true"


def test_idempotency_conflict_via_api(client: TestClient, pyg_account: dict) -> None:
    client.post(
        f"/v1/accounts/{pyg_account['account_id']}/credits",
        json={"amount": "100", "currency": "PYG"},
        headers=_headers("api-idem-conflict"),
    )
    response = client.post(
        f"/v1/accounts/{pyg_account['account_id']}/credits",
        json={"amount": "200", "currency": "PYG"},
        headers=_headers("api-idem-conflict"),
    )
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "IDEMPOTENCY_CONFLICT"


def test_missing_idempotency_key_via_api(client: TestClient, pyg_account: dict) -> None:
    response = client.post(
        f"/v1/accounts/{pyg_account['account_id']}/credits",
        json={"amount": "100", "currency": "PYG"},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "IDEMPOTENCY_KEY_REQUIRED"


def test_invalid_idempotency_key_via_api(client: TestClient, pyg_account: dict) -> None:
    response = client.post(
        f"/v1/accounts/{pyg_account['account_id']}/credits",
        json={"amount": "100", "currency": "PYG"},
        headers=_headers("short"),
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_OPERATION"


def test_debit_and_insufficient_funds_via_api(client: TestClient, pyg_account: dict) -> None:
    before = client.get(f"/v1/accounts/{pyg_account['account_id']}/balance").json()["balance_minor"]
    ok = client.post(
        f"/v1/accounts/{pyg_account['account_id']}/debits",
        json={"amount": "500", "currency": "PYG"},
        headers=_headers("api-debit-0001"),
    )
    assert ok.status_code == 201
    assert client.get(f"/v1/accounts/{pyg_account['account_id']}/balance").json()["balance_minor"] == before - 500
    failed = client.post(
        f"/v1/accounts/{pyg_account['account_id']}/debits",
        json={"amount": "999999999999", "currency": "PYG"},
        headers=_headers("api-debit-insufficient"),
    )
    assert failed.status_code == 422
    assert failed.json()["error"]["code"] == "INSUFFICIENT_FUNDS"


def test_transfer_via_api(client: TestClient, pyg_account: dict, second_pyg_account: dict) -> None:
    source_before = client.get(f"/v1/accounts/{pyg_account['account_id']}/balance").json()["balance_minor"]
    target_before = client.get(f"/v1/accounts/{second_pyg_account['account_id']}/balance").json()["balance_minor"]
    response = client.post(
        "/v1/transfers",
        json={
            "from_account_id": pyg_account["account_id"],
            "to_account_id": second_pyg_account["account_id"],
            "amount": "900",
            "currency": "PYG",
        },
        headers=_headers("api-transfer-0001"),
    )
    assert response.status_code == 201
    assert client.get(f"/v1/accounts/{pyg_account['account_id']}/balance").json()["balance_minor"] == source_before - 900
    assert client.get(f"/v1/accounts/{second_pyg_account['account_id']}/balance").json()["balance_minor"] == target_before + 900


def test_transfer_same_account_via_api(client: TestClient, pyg_account: dict) -> None:
    response = client.post(
        "/v1/transfers",
        json={
            "from_account_id": pyg_account["account_id"],
            "to_account_id": pyg_account["account_id"],
            "amount": "10",
            "currency": "PYG",
        },
        headers=_headers("api-transfer-same"),
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_OPERATION"


def test_transfer_currency_mismatch_via_api(client: TestClient, pyg_account: dict, second_pyg_account: dict) -> None:
    response = client.post(
        "/v1/transfers",
        json={
            "from_account_id": pyg_account["account_id"],
            "to_account_id": second_pyg_account["account_id"],
            "amount": "10.00",
            "currency": "USD",
        },
        headers=_headers("api-transfer-currency"),
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "CURRENCY_MISMATCH"


def test_blocked_account_via_api(client: TestClient, db_path: Path, pyg_account: dict) -> None:
    conn = connect(db_path)
    try:
        conn.execute("UPDATE accounts SET status = 'BLOCKED' WHERE account_id = ?", (pyg_account["account_id"],))
    finally:
        conn.close()
    response = client.post(
        f"/v1/accounts/{pyg_account['account_id']}/debits",
        json={"amount": "10", "currency": "PYG"},
        headers=_headers("api-blocked-account"),
    )
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "ACCOUNT_NOT_ACTIVE"


def test_validation_errors_via_api(client: TestClient, pyg_account: dict) -> None:
    negative = client.post(
        f"/v1/accounts/{pyg_account['account_id']}/credits",
        json={"amount": "-5", "currency": "PYG"},
        headers=_headers("api-negative-amount"),
    )
    assert negative.status_code == 422
    assert negative.json()["error"]["code"] == "VALIDATION_ERROR"
    bad_currency = client.post(
        f"/v1/accounts/{pyg_account['account_id']}/credits",
        json={"amount": "5", "currency": "EUR"},
        headers=_headers("api-bad-currency"),
    )
    assert bad_currency.status_code == 422
    assert bad_currency.json()["error"]["code"] == "VALIDATION_ERROR"


def test_operation_not_found(client: TestClient) -> None:
    response = client.get("/v1/operations/OP-NOEXISTE")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "OPERATION_NOT_FOUND"
