"""Pruebas de reproducibilidad e integridad del dataset sintético."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from app.db import connect
from app.ledger import trial_balance_imbalance
from app.seed import SeedConfig, seed_database


def test_seed_is_reproducible(tmp_path: Path) -> None:
    config = SeedConfig(customers=35, accounts=50, transactions=700, months=2, seed=777)
    first = seed_database(tmp_path / "first.db", config=config, reset=True)
    second = seed_database(tmp_path / "second.db", config=config, reset=True)
    assert first.to_dict() == second.to_dict()

    def fingerprint(path: Path) -> list[tuple]:
        conn = sqlite3.connect(path)
        try:
            return conn.execute(
                """
                SELECT transaction_id, transaction_type, currency, amount_minor,
                       debit_account_id, credit_account_id, created_at
                FROM transactions ORDER BY transaction_id
                """
            ).fetchall()
        finally:
            conn.close()

    assert fingerprint(tmp_path / "first.db") == fingerprint(tmp_path / "second.db")


def test_seed_ledger_is_balanced_and_reconciled(seeded_db: Path) -> None:
    conn = connect(seeded_db)
    try:
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
        assert all(value == 0 for value in trial_balance_imbalance(conn).values())
        mismatches = conn.execute(
            """
            WITH ledger AS (
                SELECT account_id, SUM(credit_minor - debit_minor) AS balance
                FROM journal_lines
                WHERE account_id IS NOT NULL
                GROUP BY account_id
            )
            SELECT COUNT(*)
            FROM accounts a
            LEFT JOIN ledger l ON l.account_id = a.account_id
            WHERE a.balance_minor <> COALESCE(l.balance, 0)
            """
        ).fetchone()[0]
        assert mismatches == 0
        negatives = conn.execute(
            "SELECT COUNT(*) FROM accounts WHERE balance_minor < -overdraft_limit_minor"
        ).fetchone()[0]
        assert negatives == 0
    finally:
        conn.close()


def test_daily_closing_matches_ledger(seeded_db: Path) -> None:
    conn = connect(seeded_db)
    try:
        mismatches = conn.execute(
            """
            WITH last_close AS (
                SELECT account_id, closing_minor,
                       ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY balance_date DESC) AS rn
                FROM daily_balances
            ),
            ledger AS (
                SELECT account_id, SUM(credit_minor - debit_minor) AS balance
                FROM journal_lines
                WHERE account_id IS NOT NULL
                GROUP BY account_id
            )
            SELECT COUNT(*)
            FROM last_close lc
            JOIN ledger l ON l.account_id = lc.account_id
            WHERE lc.rn = 1 AND lc.closing_minor <> l.balance
            """
        ).fetchone()[0]
        assert mismatches == 0
        assert conn.execute("SELECT COUNT(*) FROM daily_balances").fetchone()[0] > 0
    finally:
        conn.close()


def test_seed_injects_labeled_suspicious_patterns(seeded_db: Path) -> None:
    conn = connect(seeded_db)
    try:
        row = conn.execute(
            """
            SELECT COUNT(*) AS total,
                   COUNT(DISTINCT pattern_type) AS patterns,
                   SUM(CASE WHEN label = 'SUSPICIOUS' THEN 1 ELSE 0 END) AS suspicious,
                   SUM(CASE WHEN label = 'NORMAL' THEN 1 ELSE 0 END) AS normal
            FROM _aml_ground_truth
            """
        ).fetchone()
    finally:
        conn.close()
    assert row["total"] > 0
    assert row["patterns"] >= 5
    assert row["suspicious"] > 0
    assert row["normal"] > 0


def test_seed_contains_expected_scale(seeded_db: Path, tmp_path: Path) -> None:
    summary = seed_database(
        tmp_path / "scale.db",
        config=SeedConfig(customers=20, accounts=30, transactions=500, months=2, seed=999),
        reset=True,
    )
    assert summary.customers == 20
    assert summary.accounts == 30
    assert summary.transactions > 0
    assert summary.journal_lines >= summary.transactions * 2
