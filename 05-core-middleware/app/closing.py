"""Cierre diario de saldos a partir del libro mayor."""

from __future__ import annotations

import sqlite3

from .audit import utcnow

REBUILD_SQL = """
INSERT INTO daily_balances
    (balance_date, account_id, currency, opening_minor,
     debit_total_minor, credit_total_minor, closing_minor, created_at)
WITH movements AS (
    SELECT jl.account_id,
           jl.currency,
           je.entry_date,
           SUM(jl.debit_minor)  AS debit_total,
           SUM(jl.credit_minor) AS credit_total
    FROM journal_lines jl
    JOIN journal_entries je ON je.entry_id = jl.entry_id
    WHERE jl.account_id IS NOT NULL
      AND je.status = 'POSTED'
    GROUP BY jl.account_id, jl.currency, je.entry_date
),
calculated AS (
    SELECT account_id,
           currency,
           entry_date,
           debit_total,
           credit_total,
           SUM(credit_total - debit_total) OVER (
               PARTITION BY account_id, currency
               ORDER BY entry_date
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ) - (credit_total - debit_total) AS opening_minor,
           SUM(credit_total - debit_total) OVER (
               PARTITION BY account_id, currency
               ORDER BY entry_date
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ) AS closing_minor
    FROM movements
)
SELECT entry_date,
       account_id,
       currency,
       opening_minor,
       debit_total,
       credit_total,
       closing_minor,
       ?
FROM calculated
"""

CLOSE_DAY_SQL = """
INSERT OR REPLACE INTO daily_balances
    (balance_date, account_id, currency, opening_minor,
     debit_total_minor, credit_total_minor, closing_minor, created_at)
WITH through_day AS (
    SELECT jl.account_id,
           jl.currency,
           SUM(CASE WHEN je.entry_date < ? THEN jl.credit_minor - jl.debit_minor ELSE 0 END) AS opening_minor,
           SUM(CASE WHEN je.entry_date = ? THEN jl.debit_minor ELSE 0 END) AS debit_total,
           SUM(CASE WHEN je.entry_date = ? THEN jl.credit_minor ELSE 0 END) AS credit_total
    FROM journal_lines jl
    JOIN journal_entries je ON je.entry_id = jl.entry_id
    WHERE jl.account_id IS NOT NULL
      AND je.status = 'POSTED'
      AND je.entry_date <= ?
    GROUP BY jl.account_id, jl.currency
)
SELECT ?, account_id, currency, opening_minor, debit_total, credit_total,
       opening_minor + credit_total - debit_total, ?
FROM through_day
WHERE debit_total > 0 OR credit_total > 0
"""


def rebuild_daily_balances(conn: sqlite3.Connection) -> int:
    """Recalcula todos los cierres diarios. Devuelve filas insertadas."""
    conn.execute("DELETE FROM daily_balances")
    timestamp = utcnow()
    before = conn.total_changes
    conn.execute(REBUILD_SQL, (timestamp,))
    return conn.total_changes - before


def close_day(conn: sqlite3.Connection, balance_date: str) -> int:
    """Cierra un día concreto; es idempotente por (fecha, cuenta)."""
    timestamp = utcnow()
    before = conn.total_changes
    conn.execute(CLOSE_DAY_SQL, (balance_date, balance_date, balance_date, balance_date, balance_date, timestamp))
    return conn.total_changes - before
