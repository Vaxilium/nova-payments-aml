"""Pruebas de las reglas SQL y de sus casos positivos sintéticos."""

from __future__ import annotations

import pytest

from aml.db import connect
from aml.rules import RULE_FILES, evaluate_rule, run_all_rules


@pytest.fixture(scope="module")
def rule_hits(initialized_db):
    conn = connect(initialized_db)
    try:
        return run_all_rules(conn)
    finally:
        conn.close()


def test_las_doce_reglas_ejecutan(rule_hits) -> None:
    assert len(RULE_FILES) == 12
    assert set(rule_hits) == set(RULE_FILES)
    for hits in rule_hits.values():
        for hit in hits:
            assert hit.rule_id in RULE_FILES
            assert hit.transaction_id


def test_reglas_de_patrones_detectan_la_verdad(rule_hits) -> None:
    assert len(rule_hits["R01"]) == 100
    assert len(rule_hits["R02"]) == 67
    assert len(rule_hits["R03"]) == 67
    assert len(rule_hits["R04"]) == 160
    assert len(rule_hits["R05"]) == 75
    assert len(rule_hits["R06"]) == 29
    assert len(rule_hits["R08"]) == 139
    assert len(rule_hits["R09"]) == 143
    assert len(rule_hits["R12"]) == 6


def test_r07_jurisdiccion_alto_riesgo(conn) -> None:
    row = conn.execute(
        """
        SELECT a.customer_id
        FROM accounts a
        JOIN transactions t ON t.credit_account_id = a.account_id OR t.debit_account_id = a.account_id
        LIMIT 1
        """
    ).fetchone()
    conn.execute("UPDATE customers SET country_code = 'IRN' WHERE customer_id = ?", (row["customer_id"],))
    conn.commit()
    hits = evaluate_rule(conn, "R07")
    assert hits
    assert all(hit.customer_id == row["customer_id"] for hit in hits)


def test_r06_dormancia_real_sintetica(conn) -> None:
    customer_id = conn.execute("SELECT customer_id FROM customers LIMIT 1").fetchone()["customer_id"]
    conn.execute(
        """
        INSERT INTO accounts
            (account_id, customer_id, account_number, account_type, currency, status,
             balance_minor, overdraft_limit_minor, version, opened_at)
        VALUES ('ACC-TEST-DORM', ?, '99900000000001', 'SAVINGS', 'PYG', 'ACTIVE', 0, 0, 1, '2025-01-01T00:00:00')
        """,
        (customer_id,),
    )
    for tx_id, amount, created_at in (
        ("TX-TEST-DORM-1", 100_000, "2026-06-01T10:00:00"),
        ("TX-TEST-DORM-2", 6_000_000, "2026-06-15T10:00:00"),
    ):
        conn.execute(
            """
            INSERT INTO transactions
                (transaction_id, transaction_type, status, currency, amount_minor,
                 credit_account_id, description, channel, created_at, value_date, posted_at)
            VALUES (?, 'DEPOSIT', 'POSTED', 'PYG', ?, 'ACC-TEST-DORM', 'Prueba dormancia',
                    'BRANCH', ?, ?, ?)
            """,
            (tx_id, amount, created_at, created_at[:10], created_at),
        )
    conn.commit()
    hits = evaluate_rule(conn, "R06")
    assert any(hit.transaction_id == "TX-TEST-DORM-2" for hit in hits)


def test_r10_circularidad_sintetica(conn) -> None:
    accounts = conn.execute(
        "SELECT account_id FROM accounts WHERE currency = 'PYG' ORDER BY account_id LIMIT 2"
    ).fetchall()
    left, right = accounts[0]["account_id"], accounts[1]["account_id"]
    conn.execute(
        """
        INSERT INTO transactions
            (transaction_id, transaction_type, status, currency, amount_minor,
             debit_account_id, credit_account_id, description, channel,
             created_at, value_date, posted_at)
        VALUES ('TX-TEST-CIRC-1', 'TRANSFER', 'POSTED', 'PYG', 2000000, ?, ?,
                'Prueba circular', 'API', '2026-10-01T10:00:00', '2026-10-01', '2026-10-01T10:00:00')
        """,
        (left, right),
    )
    conn.execute(
        """
        INSERT INTO transactions
            (transaction_id, transaction_type, status, currency, amount_minor,
             debit_account_id, credit_account_id, description, channel,
             created_at, value_date, posted_at)
        VALUES ('TX-TEST-CIRC-2', 'TRANSFER', 'POSTED', 'PYG', 2000000, ?, ?,
                'Prueba circular retorno', 'API', '2026-10-01T11:00:00', '2026-10-01', '2026-10-01T11:00:00')
        """,
        (right, left),
    )
    conn.commit()
    hits = evaluate_rule(conn, "R10")
    ids = {hit.transaction_id for hit in hits}
    assert {"TX-TEST-CIRC-1", "TX-TEST-CIRC-2"} <= ids


def test_r11_concentracion_sintetica(conn) -> None:
    customer_id = conn.execute("SELECT customer_id FROM customers LIMIT 1").fetchone()["customer_id"]
    counterparty = conn.execute("SELECT account_id FROM accounts WHERE currency = 'PYG' LIMIT 1").fetchone()["account_id"]
    conn.execute(
        """
        INSERT INTO accounts
            (account_id, customer_id, account_number, account_type, currency, status,
             balance_minor, overdraft_limit_minor, version, opened_at)
        VALUES ('ACC-TEST-R11', ?, '99900000000002', 'CHECKING', 'PYG', 'ACTIVE', 0, 0, 1, '2025-01-01T00:00:00')
        """,
        (customer_id,),
    )
    for index in range(5):
        conn.execute(
            """
            INSERT INTO transactions
                (transaction_id, transaction_type, status, currency, amount_minor,
                 debit_account_id, credit_account_id, description, channel,
                 created_at, value_date, posted_at)
            VALUES (?, 'TRANSFER', 'POSTED', 'PYG', 2000000, 'ACC-TEST-R11', ?,
                    'Prueba concentración', 'API', ?, '2026-09-01', ?)
            """,
            (f"TX-TEST-R11-{index}", counterparty, f"2026-09-0{index + 1}T10:00:00", f"2026-09-0{index + 1}T10:00:00"),
        )
    conn.commit()
    hits = evaluate_rule(conn, "R11")
    assert len(hits) == 5
    assert all(hit.account_id == "ACC-TEST-R11" for hit in hits)
