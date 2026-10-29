"""Motor de contabilización por partida doble."""

from __future__ import annotations

import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from .audit import utcnow

GL_ACCOUNTS: tuple[dict[str, str], ...] = (
    {"code": "1101", "name": "Caja y bancos PYG", "account_class": "ASSET", "normal_side": "DEBIT"},
    {"code": "1102", "name": "Caja y bancos USD", "account_class": "ASSET", "normal_side": "DEBIT"},
    {"code": "1901", "name": "Posición de cambio PYG", "account_class": "ASSET", "normal_side": "DEBIT"},
    {"code": "1902", "name": "Posición de cambio USD", "account_class": "ASSET", "normal_side": "DEBIT"},
    {"code": "2101", "name": "Depósitos de clientes PYG", "account_class": "LIABILITY", "normal_side": "CREDIT"},
    {"code": "2102", "name": "Depósitos de clientes USD", "account_class": "LIABILITY", "normal_side": "CREDIT"},
    {"code": "3101", "name": "Patrimonio de apertura PYG", "account_class": "EQUITY", "normal_side": "CREDIT"},
    {"code": "3102", "name": "Patrimonio de apertura USD", "account_class": "EQUITY", "normal_side": "CREDIT"},
    {"code": "4101", "name": "Ingresos por comisiones PYG", "account_class": "INCOME", "normal_side": "CREDIT"},
    {"code": "4102", "name": "Ingresos por comisiones USD", "account_class": "INCOME", "normal_side": "CREDIT"},
)

GL_BY_CONCEPT: dict[str, str] = {
    "CASH_PYG": "1101",
    "CASH_USD": "1102",
    "FX_POSITION_PYG": "1901",
    "FX_POSITION_USD": "1902",
    "CUSTOMER_DEPOSITS_PYG": "2101",
    "CUSTOMER_DEPOSITS_USD": "2102",
    "OPENING_EQUITY_PYG": "3101",
    "OPENING_EQUITY_USD": "3102",
    "FEE_INCOME_PYG": "4101",
    "FEE_INCOME_USD": "4102",
}

CASH_BY_CURRENCY = {"PYG": "1101", "USD": "1102"}
CUSTOMER_DEPOSITS_BY_CURRENCY = {"PYG": "2101", "USD": "2102"}
FEE_INCOME_BY_CURRENCY = {"PYG": "4101", "USD": "4102"}
OPENING_EQUITY_BY_CURRENCY = {"PYG": "3101", "USD": "3102"}
FX_POSITION_BY_CURRENCY = {"PYG": "1901", "USD": "1902"}


@dataclass(frozen=True)
class LedgerLine:
    """Línea de asiento: una cuenta contable, una moneda y un solo lado."""

    gl_code: str
    currency: str
    debit_minor: int = 0
    credit_minor: int = 0
    account_id: str | None = None
    description: str | None = None


def load_gl_map(conn: sqlite3.Connection) -> dict[str, int]:
    """Devuelve {código contable: id} para evitar consultas repetidas."""
    return {row["code"]: int(row["gl_account_id"]) for row in conn.execute("SELECT code, gl_account_id FROM gl_accounts")}


def validate_lines(lines: Iterable[LedgerLine]) -> None:
    """Valida partida doble, lados únicos y monedas antes de escribir."""
    line_list = list(lines)
    if len(line_list) < 2:
        raise ValueError("Un asiento requiere al menos dos líneas")
    totals: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for line in line_list:
        if line.debit_minor < 0 or line.credit_minor < 0:
            raise ValueError("Los importes contables no pueden ser negativos")
        if (line.debit_minor > 0) == (line.credit_minor > 0):
            raise ValueError("Cada línea debe tener exactamente un débito o un crédito")
        totals[line.currency][0] += line.debit_minor
        totals[line.currency][1] += line.credit_minor
    for currency, (debit, credit) in totals.items():
        if debit != credit:
            raise ValueError(f"Asiento desbalanceado en {currency}: débito {debit} vs crédito {credit}")


def post_entry(
    conn: sqlite3.Connection,
    *,
    entry_id: str,
    entry_date: str,
    description: str,
    source_type: str,
    lines: Iterable[LedgerLine],
    created_by: str,
    source_id: str | None = None,
    correlation_id: str | None = None,
    created_at: str | None = None,
    gl_map: dict[str, int] | None = None,
    status: str = "POSTED",
) -> str:
    """Inserta un asiento DRAFT, sus líneas y lo contabiliza si corresponde.

    El llamador debe manejar la transacción. El trigger de la base vuelve a
    validar el balance por moneda al pasar el asiento a POSTED.
    """
    line_list = list(lines)
    validate_lines(line_list)
    mapping = gl_map or load_gl_map(conn)
    timestamp = created_at or utcnow()

    conn.execute(
        """
        INSERT INTO journal_entries
            (entry_id, entry_date, description, source_type, source_id, status,
             correlation_id, created_by, created_at)
        VALUES (?, ?, ?, ?, ?, 'DRAFT', ?, ?, ?)
        """,
        (entry_id, entry_date, description, source_type, source_id, correlation_id, created_by, timestamp),
    )

    rows = []
    for line_no, line in enumerate(line_list, start=1):
        try:
            gl_id = mapping[line.gl_code]
        except KeyError as exc:
            raise ValueError(f"Cuenta contable inexistente: {line.gl_code}") from exc
        rows.append(
            (
                entry_id,
                line_no,
                gl_id,
                line.account_id,
                line.currency,
                line.debit_minor,
                line.credit_minor,
                line.description,
            )
        )
    conn.executemany(
        """
        INSERT INTO journal_lines
            (entry_id, line_no, gl_account_id, account_id, currency,
             debit_minor, credit_minor, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )

    if status == "POSTED":
        conn.execute(
            "UPDATE journal_entries SET status = 'POSTED', posted_at = ? WHERE entry_id = ? AND status = 'DRAFT'",
            (timestamp, entry_id),
        )
    return entry_id


def ledger_balance(conn: sqlite3.Connection, account_id: str) -> int:
    """Saldo de una cuenta según el libro mayor (créditos menos débitos)."""
    row = conn.execute(
        """
        SELECT COALESCE(SUM(credit_minor - debit_minor), 0) AS balance
        FROM journal_lines
        WHERE account_id = ?
        """,
        (account_id,),
    ).fetchone()
    return int(row["balance"])


def trial_balance_imbalance(conn: sqlite3.Connection) -> dict[str, int]:
    """Desbalance global por moneda; debe ser cero en todo momento."""
    rows = conn.execute(
        """
        SELECT currency, SUM(debit_minor) - SUM(credit_minor) AS imbalance
        FROM journal_lines jl
        JOIN journal_entries je ON je.entry_id = jl.entry_id
        WHERE je.status = 'POSTED'
        GROUP BY currency
        """
    ).fetchall()
    return {row["currency"]: int(row["imbalance"]) for row in rows}
