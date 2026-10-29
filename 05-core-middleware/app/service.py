"""Servicio del core bancario: consultas y operaciones monetarias."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import uuid
from contextlib import closing
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable

from .audit import write_audit
from .config import DEFAULT_ACTOR, resolve_db_path
from .db import connect
from .errors import (
    AccountBlockedError,
    AccountNotFoundError,
    ConcurrentModificationError,
    CurrencyMismatchError,
    CustomerNotFoundError,
    IdempotencyConflictError,
    IdempotencyKeyRequiredError,
    InsufficientFundsError,
    InvalidOperationError,
    OperationNotFoundError,
)
from .ledger import (
    CASH_BY_CURRENCY,
    CUSTOMER_DEPOSITS_BY_CURRENCY,
    LedgerLine,
    ledger_balance,
    post_entry,
)
from .money import format_money, to_minor

IDEMPOTENCY_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{8,128}$")
CHANNELS = {"API", "MOBILE", "WEB", "BRANCH", "ATM", "BATCH"}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _new_operation_id() -> str:
    return f"OP-{uuid.uuid4().hex[:16].upper()}"


def _request_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _customer_dict(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    data["is_active"] = bool(data["is_active"])
    return data


def _account_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "account_id": row["account_id"],
        "customer_id": row["customer_id"],
        "account_number": row["account_number"],
        "account_type": row["account_type"],
        "currency": row["currency"],
        "status": row["status"],
        "balance": format_money(row["balance_minor"], row["currency"]),
        "balance_minor": row["balance_minor"],
        "overdraft_limit": format_money(row["overdraft_limit_minor"], row["currency"]),
        "overdraft_limit_minor": row["overdraft_limit_minor"],
        "available_balance": format_money(
            row["balance_minor"] + row["overdraft_limit_minor"], row["currency"]
        ),
        "version": row["version"],
        "opened_at": row["opened_at"],
        "closed_at": row["closed_at"],
    }


class BankingService:
    """Fachada de negocio sobre SQLite. Cada operación usa su propia conexión."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = resolve_db_path(db_path)

    def _connect(self) -> sqlite3.Connection:
        return connect(self.db_path)

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------
    def health(self) -> dict[str, Any]:
        with closing(self._connect()) as conn:
            accounts = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
            entries = conn.execute("SELECT COUNT(*) FROM journal_entries").fetchone()[0]
        return {"status": "ok", "database": "connected", "accounts": accounts, "journal_entries": entries}

    def list_customers(self, *, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        limit = max(1, min(int(limit), 200))
        offset = max(0, int(offset))
        with closing(self._connect()) as conn:
            rows = conn.execute(
                """
                SELECT c.*, (SELECT COUNT(*) FROM accounts a WHERE a.customer_id = c.customer_id) AS account_count
                FROM customers c
                ORDER BY c.customer_id
                LIMIT ? OFFSET ?
                """,
                (limit, offset),
            ).fetchall()
        return [dict(_customer_dict(row), account_count=row["account_count"]) for row in rows]

    def get_customer(self, customer_id: str) -> dict[str, Any]:
        with closing(self._connect()) as conn:
            row = conn.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,)).fetchone()
            if row is None:
                raise CustomerNotFoundError(f"Cliente no encontrado: {customer_id}")
            account_count = conn.execute(
                "SELECT COUNT(*) FROM accounts WHERE customer_id = ?", (customer_id,)
            ).fetchone()[0]
        return dict(_customer_dict(row), account_count=account_count)

    def list_accounts(
        self, *, customer_id: str | None = None, limit: int = 50, offset: int = 0
    ) -> list[dict[str, Any]]:
        limit = max(1, min(int(limit), 200))
        offset = max(0, int(offset))
        with closing(self._connect()) as conn:
            if customer_id is not None:
                exists = conn.execute(
                    "SELECT 1 FROM customers WHERE customer_id = ?", (customer_id,)
                ).fetchone()
                if exists is None:
                    raise CustomerNotFoundError(f"Cliente no encontrado: {customer_id}")
                rows = conn.execute(
                    "SELECT * FROM accounts WHERE customer_id = ? ORDER BY account_id LIMIT ? OFFSET ?",
                    (customer_id, limit, offset),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM accounts ORDER BY account_id LIMIT ? OFFSET ?",
                    (limit, offset),
                ).fetchall()
        return [_account_dict(row) for row in rows]

    def get_account(self, account_id: str) -> dict[str, Any]:
        with closing(self._connect()) as conn:
            return _account_dict(self._fetch_account(conn, account_id))

    def get_balance(self, account_id: str) -> dict[str, Any]:
        with closing(self._connect()) as conn:
            row = self._fetch_account(conn, account_id)
            ledger = ledger_balance(conn, account_id)
        account = _account_dict(row)
        account["ledger_balance"] = format_money(ledger, row["currency"])
        account["ledger_balance_minor"] = ledger
        account["reconciled"] = ledger == row["balance_minor"]
        return account

    def get_operation(self, operation_id: str) -> dict[str, Any]:
        with closing(self._connect()) as conn:
            return self._operation_response(conn, operation_id)

    # ------------------------------------------------------------------
    # Operaciones
    # ------------------------------------------------------------------
    def credit_account(
        self,
        *,
        account_id: str,
        amount: Decimal,
        currency: str,
        idempotency_key: str | None,
        description: str | None = None,
        channel: str = "API",
        actor: str = DEFAULT_ACTOR,
        correlation_id: str | None = None,
    ) -> tuple[dict[str, Any], int, bool]:
        currency = currency.upper()
        amount_minor = to_minor(amount, currency)
        if channel not in CHANNELS:
            raise InvalidOperationError(f"Canal inválido: {channel}")
        payload = {
            "operation": "CREDIT",
            "account_id": account_id,
            "amount_minor": amount_minor,
            "currency": currency,
            "description": description,
            "channel": channel,
        }

        def operation(conn: sqlite3.Connection) -> tuple[dict[str, Any], int]:
            account = self._fetch_account(conn, account_id)
            if account["status"] != "ACTIVE":
                raise AccountBlockedError(f"La cuenta {account_id} no está activa")
            if account["currency"] != currency:
                raise CurrencyMismatchError(
                    f"La cuenta opera en {account['currency']} y se recibió {currency}"
                )
            timestamp = _now()
            operation_id = _new_operation_id()
            self._ensure_transaction_id(conn, operation_id)
            conn.execute(
                """
                INSERT INTO transactions
                    (transaction_id, transaction_type, status, currency, amount_minor,
                     counter_amount_minor, debit_account_id, credit_account_id, fx_rate_id,
                     fee_minor, description, channel, idempotency_key, correlation_id,
                     external_ref, created_at, value_date, posted_at)
                VALUES (?, 'DEPOSIT', 'POSTED', ?, ?, NULL, NULL, ?, NULL, 0, ?, ?, ?, ?, NULL, ?, ?, ?)
                """,
                (
                    operation_id,
                    currency,
                    amount_minor,
                    account_id,
                    description,
                    channel,
                    idempotency_key,
                    correlation_id,
                    timestamp,
                    timestamp[:10],
                    timestamp,
                ),
            )
            updated = conn.execute(
                """
                UPDATE accounts
                   SET balance_minor = balance_minor + ?, version = version + 1
                 WHERE account_id = ? AND version = ? AND status = 'ACTIVE'
                """,
                (amount_minor, account_id, account["version"]),
            )
            if updated.rowcount != 1:
                raise ConcurrentModificationError("La cuenta cambió durante la operación; reintente")
            post_entry(
                conn,
                entry_id=f"JE-{operation_id}",
                entry_date=timestamp[:10],
                description=description or f"Crédito a cuenta {account_id}",
                source_type="DEPOSIT",
                source_id=operation_id,
                created_by=actor,
                correlation_id=correlation_id,
                created_at=timestamp,
                lines=[
                    LedgerLine(CASH_BY_CURRENCY[currency], currency, debit_minor=amount_minor),
                    LedgerLine(
                        CUSTOMER_DEPOSITS_BY_CURRENCY[currency],
                        currency,
                        credit_minor=amount_minor,
                        account_id=account_id,
                    ),
                ],
            )
            write_audit(
                conn,
                event_type="ACCOUNT_CREDITED",
                entity_type="ACCOUNT",
                entity_id=account_id,
                actor=actor,
                correlation_id=correlation_id,
                created_at=timestamp,
                payload={
                    "operation_id": operation_id,
                    "amount_minor": amount_minor,
                    "currency": currency,
                },
            )
            return self._operation_response(conn, operation_id), 201

        return self._with_idempotency(idempotency_key, payload, operation)

    def debit_account(
        self,
        *,
        account_id: str,
        amount: Decimal,
        currency: str,
        idempotency_key: str | None,
        description: str | None = None,
        channel: str = "API",
        actor: str = DEFAULT_ACTOR,
        correlation_id: str | None = None,
    ) -> tuple[dict[str, Any], int, bool]:
        currency = currency.upper()
        amount_minor = to_minor(amount, currency)
        if channel not in CHANNELS:
            raise InvalidOperationError(f"Canal inválido: {channel}")
        payload = {
            "operation": "DEBIT",
            "account_id": account_id,
            "amount_minor": amount_minor,
            "currency": currency,
            "description": description,
            "channel": channel,
        }

        def operation(conn: sqlite3.Connection) -> tuple[dict[str, Any], int]:
            account = self._fetch_account(conn, account_id)
            if account["status"] != "ACTIVE":
                raise AccountBlockedError(f"La cuenta {account_id} no está activa")
            if account["currency"] != currency:
                raise CurrencyMismatchError(
                    f"La cuenta opera en {account['currency']} y se recibió {currency}"
                )
            timestamp = _now()
            operation_id = _new_operation_id()
            self._ensure_transaction_id(conn, operation_id)
            self._debit_balance(conn, account, amount_minor)
            conn.execute(
                """
                INSERT INTO transactions
                    (transaction_id, transaction_type, status, currency, amount_minor,
                     counter_amount_minor, debit_account_id, credit_account_id, fx_rate_id,
                     fee_minor, description, channel, idempotency_key, correlation_id,
                     external_ref, created_at, value_date, posted_at)
                VALUES (?, 'WITHDRAWAL', 'POSTED', ?, ?, NULL, ?, NULL, NULL, 0, ?, ?, ?, ?, NULL, ?, ?, ?)
                """,
                (
                    operation_id,
                    currency,
                    amount_minor,
                    account_id,
                    description,
                    channel,
                    idempotency_key,
                    correlation_id,
                    timestamp,
                    timestamp[:10],
                    timestamp,
                ),
            )
            post_entry(
                conn,
                entry_id=f"JE-{operation_id}",
                entry_date=timestamp[:10],
                description=description or f"Débito a cuenta {account_id}",
                source_type="WITHDRAWAL",
                source_id=operation_id,
                created_by=actor,
                correlation_id=correlation_id,
                created_at=timestamp,
                lines=[
                    LedgerLine(
                        CUSTOMER_DEPOSITS_BY_CURRENCY[currency],
                        currency,
                        debit_minor=amount_minor,
                        account_id=account_id,
                    ),
                    LedgerLine(CASH_BY_CURRENCY[currency], currency, credit_minor=amount_minor),
                ],
            )
            write_audit(
                conn,
                event_type="ACCOUNT_DEBITED",
                entity_type="ACCOUNT",
                entity_id=account_id,
                actor=actor,
                correlation_id=correlation_id,
                created_at=timestamp,
                payload={
                    "operation_id": operation_id,
                    "amount_minor": amount_minor,
                    "currency": currency,
                },
            )
            return self._operation_response(conn, operation_id), 201

        return self._with_idempotency(idempotency_key, payload, operation)

    def transfer(
        self,
        *,
        from_account_id: str,
        to_account_id: str,
        amount: Decimal,
        currency: str,
        idempotency_key: str | None,
        description: str | None = None,
        channel: str = "API",
        actor: str = DEFAULT_ACTOR,
        correlation_id: str | None = None,
    ) -> tuple[dict[str, Any], int, bool]:
        currency = currency.upper()
        amount_minor = to_minor(amount, currency)
        if channel not in CHANNELS:
            raise InvalidOperationError(f"Canal inválido: {channel}")
        if from_account_id == to_account_id:
            raise InvalidOperationError("La cuenta de origen y destino deben ser distintas")
        payload = {
            "operation": "TRANSFER",
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
            "amount_minor": amount_minor,
            "currency": currency,
            "description": description,
            "channel": channel,
        }

        def operation(conn: sqlite3.Connection) -> tuple[dict[str, Any], int]:
            source = self._fetch_account(conn, from_account_id)
            target = self._fetch_account(conn, to_account_id)
            for account in (source, target):
                if account["status"] != "ACTIVE":
                    raise AccountBlockedError(f"La cuenta {account['account_id']} no está activa")
            if source["currency"] != currency or target["currency"] != currency:
                raise CurrencyMismatchError(
                    "La transferencia requiere que ambas cuentas operen en la moneda indicada"
                )
            timestamp = _now()
            operation_id = _new_operation_id()
            self._ensure_transaction_id(conn, operation_id)
            self._debit_balance(conn, source, amount_minor)
            credited = conn.execute(
                """
                UPDATE accounts
                   SET balance_minor = balance_minor + ?, version = version + 1
                 WHERE account_id = ? AND version = ? AND status = 'ACTIVE'
                """,
                (amount_minor, to_account_id, target["version"]),
            )
            if credited.rowcount != 1:
                raise ConcurrentModificationError(
                    "La cuenta destino cambió durante la operación; reintente"
                )
            conn.execute(
                """
                INSERT INTO transactions
                    (transaction_id, transaction_type, status, currency, amount_minor,
                     counter_amount_minor, debit_account_id, credit_account_id, fx_rate_id,
                     fee_minor, description, channel, idempotency_key, correlation_id,
                     external_ref, created_at, value_date, posted_at)
                VALUES (?, 'TRANSFER', 'POSTED', ?, ?, NULL, ?, ?, NULL, 0, ?, ?, ?, ?, NULL, ?, ?, ?)
                """,
                (
                    operation_id,
                    currency,
                    amount_minor,
                    from_account_id,
                    to_account_id,
                    description,
                    channel,
                    idempotency_key,
                    correlation_id,
                    timestamp,
                    timestamp[:10],
                    timestamp,
                ),
            )
            post_entry(
                conn,
                entry_id=f"JE-{operation_id}",
                entry_date=timestamp[:10],
                description=description or f"Transferencia {from_account_id} -> {to_account_id}",
                source_type="TRANSFER",
                source_id=operation_id,
                created_by=actor,
                correlation_id=correlation_id,
                created_at=timestamp,
                lines=[
                    LedgerLine(
                        CUSTOMER_DEPOSITS_BY_CURRENCY[currency],
                        currency,
                        debit_minor=amount_minor,
                        account_id=from_account_id,
                    ),
                    LedgerLine(
                        CUSTOMER_DEPOSITS_BY_CURRENCY[currency],
                        currency,
                        credit_minor=amount_minor,
                        account_id=to_account_id,
                    ),
                ],
            )
            write_audit(
                conn,
                event_type="TRANSFER_POSTED",
                entity_type="TRANSACTION",
                entity_id=operation_id,
                actor=actor,
                correlation_id=correlation_id,
                created_at=timestamp,
                payload={
                    "from_account_id": from_account_id,
                    "to_account_id": to_account_id,
                    "amount_minor": amount_minor,
                    "currency": currency,
                },
            )
            return self._operation_response(conn, operation_id), 201

        return self._with_idempotency(idempotency_key, payload, operation)

    # ------------------------------------------------------------------
    # Internos
    # ------------------------------------------------------------------
    def _fetch_account(self, conn: sqlite3.Connection, account_id: str) -> sqlite3.Row:
        row = conn.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,)).fetchone()
        if row is None:
            raise AccountNotFoundError(f"Cuenta no encontrada: {account_id}")
        return row

    def _ensure_transaction_id(self, conn: sqlite3.Connection, operation_id: str) -> None:
        exists = conn.execute(
            "SELECT 1 FROM transactions WHERE transaction_id = ?", (operation_id,)
        ).fetchone()
        if exists is not None:
            raise InvalidOperationError(f"Identificador de operación duplicado: {operation_id}")

    def _debit_balance(self, conn: sqlite3.Connection, account: sqlite3.Row, amount_minor: int) -> None:
        updated = conn.execute(
            """
            UPDATE accounts
               SET balance_minor = balance_minor - ?, version = version + 1
             WHERE account_id = ?
               AND version = ?
               AND status = 'ACTIVE'
               AND balance_minor - ? >= -overdraft_limit_minor
            """,
            (amount_minor, account["account_id"], account["version"], amount_minor),
        )
        if updated.rowcount == 1:
            return
        current = self._fetch_account(conn, account["account_id"])
        if current["status"] != "ACTIVE":
            raise AccountBlockedError(f"La cuenta {account['account_id']} no está activa")
        available = current["balance_minor"] + current["overdraft_limit_minor"]
        if available < amount_minor:
            raise InsufficientFundsError(
                "Saldo insuficiente",
                details={
                    "account_id": account["account_id"],
                    "available_minor": available,
                    "requested_minor": amount_minor,
                    "currency": current["currency"],
                },
            )
        raise ConcurrentModificationError("La cuenta cambió durante la operación; reintente")

    def _operation_response(self, conn: sqlite3.Connection, operation_id: str) -> dict[str, Any]:
        row = conn.execute(
            """
            SELECT t.*, da.account_number AS debit_account_number,
                   ca.account_number AS credit_account_number
            FROM transactions t
            LEFT JOIN accounts da ON da.account_id = t.debit_account_id
            LEFT JOIN accounts ca ON ca.account_id = t.credit_account_id
            WHERE t.transaction_id = ?
            """,
            (operation_id,),
        ).fetchone()
        if row is None:
            raise OperationNotFoundError(f"Operación no encontrada: {operation_id}")
        entries = conn.execute(
            """
            SELECT * FROM journal_entries
            WHERE source_id = ? AND source_type IN ('DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'FEE', 'FX')
            ORDER BY entry_id
            """,
            (operation_id,),
        ).fetchall()
        entry_payload = []
        for entry in entries:
            lines = conn.execute(
                """
                SELECT line_no, gl_account_id, account_id, currency, debit_minor, credit_minor, description
                FROM journal_lines WHERE entry_id = ? ORDER BY line_no
                """,
                (entry["entry_id"],),
            ).fetchall()
            entry_payload.append(
                {
                    "entry_id": entry["entry_id"],
                    "status": entry["status"],
                    "entry_date": entry["entry_date"],
                    "description": entry["description"],
                    "lines": [
                        {
                            "line_no": line["line_no"],
                            "gl_account_id": line["gl_account_id"],
                            "account_id": line["account_id"],
                            "currency": line["currency"],
                            "debit": format_money(line["debit_minor"], line["currency"]),
                            "credit": format_money(line["credit_minor"], line["currency"]),
                            "debit_minor": line["debit_minor"],
                            "credit_minor": line["credit_minor"],
                            "description": line["description"],
                        }
                        for line in lines
                    ],
                }
            )
        counter = row["counter_amount_minor"]
        return {
            "operation_id": row["transaction_id"],
            "type": row["transaction_type"],
            "status": row["status"],
            "currency": row["currency"],
            "amount": format_money(row["amount_minor"], row["currency"]),
            "amount_minor": row["amount_minor"],
            "counter_amount": None
            if counter is None
            else format_money(counter, "USD" if row["currency"] == "PYG" else "PYG"),
            "counter_amount_minor": counter,
            "fee": format_money(row["fee_minor"], row["currency"]),
            "fee_minor": row["fee_minor"],
            "debit_account_id": row["debit_account_id"],
            "credit_account_id": row["credit_account_id"],
            "debit_account_number": row["debit_account_number"],
            "credit_account_number": row["credit_account_number"],
            "description": row["description"],
            "channel": row["channel"],
            "created_at": row["created_at"],
            "value_date": row["value_date"],
            "posted_at": row["posted_at"],
            "entries": entry_payload,
        }

    def _with_idempotency(
        self,
        idempotency_key: str | None,
        payload: dict[str, Any],
        operation: Callable[[sqlite3.Connection], tuple[dict[str, Any], int]],
    ) -> tuple[dict[str, Any], int, bool]:
        self._validate_idempotency_key(idempotency_key)
        assert idempotency_key is not None
        key = idempotency_key.strip()
        request_hash = _request_hash(payload)
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            existing = conn.execute(
                "SELECT request_hash, status_code, response_json FROM idempotency_keys WHERE idempotency_key = ?",
                (key,),
            ).fetchone()
            if existing is not None:
                if existing["request_hash"] != request_hash:
                    raise IdempotencyConflictError(
                        "La idempotency-key ya se usó con un contenido diferente",
                        details={"idempotency_key": key},
                    )
                conn.execute("COMMIT")
                return json.loads(existing["response_json"]), int(existing["status_code"]), True
            response, status_code = operation(conn)
            conn.execute(
                """
                INSERT INTO idempotency_keys
                    (idempotency_key, request_hash, operation_id, status_code, response_json, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, NULL)
                """,
                (
                    key,
                    request_hash,
                    response["operation_id"],
                    status_code,
                    json.dumps(response, ensure_ascii=False, sort_keys=True),
                    _now(),
                ),
            )
            conn.execute("COMMIT")
            return response, status_code, False
        except BaseException:
            try:
                conn.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise
        finally:
            conn.close()

    @staticmethod
    def _validate_idempotency_key(idempotency_key: str | None) -> None:
        if idempotency_key is None or not idempotency_key.strip():
            raise IdempotencyKeyRequiredError(
                "El header Idempotency-Key es obligatorio para operaciones monetarias"
            )
        if not IDEMPOTENCY_PATTERN.match(idempotency_key.strip()):
            raise InvalidOperationError(
                "Idempotency-Key inválida: use entre 8 y 128 caracteres [A-Za-z0-9._:-]"
            )

