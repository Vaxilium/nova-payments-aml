"""Constraints y triggers que protegen la integridad contable."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from app.db import connect


def _gl_id(conn: sqlite3.Connection, code: str) -> int:
    return int(conn.execute("SELECT gl_account_id FROM gl_accounts WHERE code = ?", (code,)).fetchone()[0])


def _insert_entry(conn: sqlite3.Connection, entry_id: str = "JE-TEST") -> None:
    conn.execute(
        """
        INSERT INTO journal_entries
            (entry_id, entry_date, description, source_type, status, created_by, created_at)
        VALUES (?, '2026-05-01', 'Asiento de prueba', 'ADJUSTMENT', 'DRAFT', 'test', '2026-05-01T10:00:00')
        """,
        (entry_id,),
    )


def _insert_line(
    conn: sqlite3.Connection,
    entry_id: str,
    line_no: int,
    code: str,
    *,
    debit: int = 0,
    credit: int = 0,
) -> None:
    conn.execute(
        """
        INSERT INTO journal_lines
            (entry_id, line_no, gl_account_id, currency, debit_minor, credit_minor)
        VALUES (?, ?, ?, 'PYG', ?, ?)
        """,
        (entry_id, line_no, _gl_id(conn, code), debit, credit),
    )


def test_schema_contains_core_tables_and_triggers(schema_db: Path) -> None:
    conn = connect(schema_db)
    try:
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        triggers = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'trigger'")}
    finally:
        conn.close()
    assert {"customers", "accounts", "journal_entries", "journal_lines", "transactions", "daily_balances"} <= tables
    assert "trg_journal_entries_balanced_update" in triggers
    assert "trg_journal_lines_no_update_posted" in triggers
    assert "trg_accounts_non_negative_update" in triggers


def test_line_requires_exactly_one_side(schema_db: Path) -> None:
    conn = connect(schema_db)
    try:
        _insert_entry(conn)
        with pytest.raises(sqlite3.IntegrityError):
            _insert_line(conn, "JE-TEST", 1, "1101", debit=100, credit=100)
    finally:
        conn.close()


def test_entry_with_one_line_cannot_be_posted(schema_db: Path) -> None:
    conn = connect(schema_db)
    try:
        _insert_entry(conn)
        _insert_line(conn, "JE-TEST", 1, "1101", debit=100)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("UPDATE journal_entries SET status = 'POSTED' WHERE entry_id = 'JE-TEST'")
    finally:
        conn.close()


def test_unbalanced_entry_is_rejected_by_trigger(schema_db: Path) -> None:
    conn = connect(schema_db)
    try:
        _insert_entry(conn)
        _insert_line(conn, "JE-TEST", 1, "1101", debit=100)
        _insert_line(conn, "JE-TEST", 2, "2101", credit=90)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("UPDATE journal_entries SET status = 'POSTED' WHERE entry_id = 'JE-TEST'")
    finally:
        conn.close()


def test_balanced_entry_can_be_posted_and_becomes_immutable(schema_db: Path) -> None:
    conn = connect(schema_db)
    try:
        _insert_entry(conn)
        _insert_line(conn, "JE-TEST", 1, "1101", debit=100)
        _insert_line(conn, "JE-TEST", 2, "2101", credit=100)
        conn.execute("UPDATE journal_entries SET status = 'POSTED' WHERE entry_id = 'JE-TEST'")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "UPDATE journal_lines SET debit_minor = 50 WHERE entry_id = 'JE-TEST' AND line_no = 1"
            )
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("DELETE FROM journal_lines WHERE entry_id = 'JE-TEST' AND line_no = 1")
        with pytest.raises(sqlite3.IntegrityError):
            _insert_line(conn, "JE-TEST", 3, "1101", debit=10)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("DELETE FROM journal_entries WHERE entry_id = 'JE-TEST'")
    finally:
        conn.close()


def test_line_currency_must_match_account(schema_db: Path) -> None:
    conn = connect(schema_db)
    try:
        _insert_entry(conn)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                """
                INSERT INTO journal_lines
                    (entry_id, line_no, gl_account_id, account_id, currency,
                     debit_minor, credit_minor)
                VALUES ('JE-TEST', 1, ?, 'ACC-TEST', 'USD', 100, 0)
                """,
                (_gl_id(conn, "1101"),),
            )
    finally:
        conn.close()


def test_account_balance_cannot_break_overdraft_limit(schema_db: Path) -> None:
    conn = connect(schema_db)
    try:
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("UPDATE accounts SET balance_minor = -1 WHERE account_id = 'ACC-TEST'")
    finally:
        conn.close()
