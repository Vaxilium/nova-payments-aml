"""Puente contable entre los simuladores y el core de Fase 3.

El core sigue siendo la fuente de verdad del libro mayor. Este adaptador solo
agrega el asiento de una salida internacional (cliente → caja/nostro + comisión)
y reutiliza las mismas invariantes de partida doble.
"""

from __future__ import annotations

import sqlite3
import sys
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from app.audit import write_audit
    from app.db import connect
    from app.errors import AccountBlockedError, AccountNotFoundError, InsufficientFundsError
    from app.ledger import (
        CASH_BY_CURRENCY,
        CUSTOMER_DEPOSITS_BY_CURRENCY,
        FEE_INCOME_BY_CURRENCY,
        LedgerLine,
        post_entry,
    )
    from app.money import format_money
except ImportError:  # pragma: no cover - permite ejecutar la CLI desde 06-mensajeria
    CORE_DIR = Path(__file__).resolve().parents[2] / "05-core-middleware"
    if str(CORE_DIR) not in sys.path:
        sys.path.insert(0, str(CORE_DIR))
    from app.audit import write_audit
    from app.db import connect
    from app.errors import AccountBlockedError, AccountNotFoundError, InsufficientFundsError
    from app.ledger import (
        CASH_BY_CURRENCY,
        CUSTOMER_DEPOSITS_BY_CURRENCY,
        FEE_INCOME_BY_CURRENCY,
        LedgerLine,
        post_entry,
    )
    from app.money import format_money


class CorePostingError(RuntimeError):
    """El core rechazó el asiento solicitado."""


class CoreLedgerBridge:
    """Operaciones mínimas de lectura y contabilización para el simulador."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)

    def get_account(self, account_id: str) -> dict[str, Any]:
        with closing(connect(self.db_path)) as conn:
            row = conn.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,)).fetchone()
            if row is None:
                raise AccountNotFoundError(f"Cuenta no encontrada: {account_id}")
            return dict(row)

    def post_outbound(
        self,
        *,
        account_id: str,
        amount_minor: int,
        fee_minor: int,
        currency: str,
        external_ref: str,
        instruction_id: str,
        idempotency_key: str,
        value_date: str | None = None,
        created_at: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Debita cliente por importe + comisión y acredita caja y comisión."""
        if amount_minor <= 0:
            raise CorePostingError("El importe debe ser mayor que cero")
        if fee_minor < 0:
            raise CorePostingError("La comisión no puede ser negativa")
        total_minor = amount_minor + fee_minor
        timestamp = created_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        entry_date = value_date or timestamp[:10]
        operation_id = f"OP-{uuid.uuid4().hex[:16].upper()}"
        entry_id = f"JE-{operation_id}"
        with closing(connect(self.db_path)) as conn:
            try:
                conn.execute("BEGIN IMMEDIATE")
                account = conn.execute(
                    "SELECT * FROM accounts WHERE account_id = ?",
                    (account_id,),
                ).fetchone()
                if account is None:
                    raise AccountNotFoundError(f"Cuenta no encontrada: {account_id}")
                if account["status"] != "ACTIVE":
                    raise AccountBlockedError(f"La cuenta {account_id} no está activa")
                if account["currency"] != currency:
                    raise CorePostingError(
                        f"La cuenta opera en {account['currency']} y el pago en {currency}"
                    )
                available = int(account["balance_minor"]) + int(account["overdraft_limit_minor"])
                if total_minor > available:
                    raise InsufficientFundsError(
                        "Saldo insuficiente para cubrir importe y comisión",
                        details={
                            "account_id": account_id,
                            "available_minor": available,
                            "requested_minor": total_minor,
                            "currency": currency,
                        },
                    )
                updated = conn.execute(
                    """
                    UPDATE accounts
                       SET balance_minor = balance_minor - ?, version = version + 1
                     WHERE account_id = ? AND version = ? AND status = 'ACTIVE'
                       AND balance_minor - ? >= -overdraft_limit_minor
                    """,
                    (total_minor, account_id, account["version"], total_minor),
                )
                if updated.rowcount != 1:
                    raise CorePostingError("La cuenta cambió durante la operación; reintente")
                conn.execute(
                    """
                    INSERT INTO transactions
                        (transaction_id, transaction_type, status, currency, amount_minor,
                         counter_amount_minor, debit_account_id, credit_account_id, fx_rate_id,
                         fee_minor, description, channel, idempotency_key, correlation_id,
                         external_ref, created_at, value_date, posted_at)
                    VALUES (?, 'TRANSFER', 'POSTED', ?, ?, NULL, ?, NULL, NULL, ?, ?, 'API', ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        operation_id,
                        currency,
                        amount_minor,
                        account_id,
                        fee_minor,
                        description or f"Pago internacional {instruction_id}",
                        idempotency_key,
                        instruction_id,
                        external_ref,
                        timestamp,
                        entry_date,
                        timestamp,
                    ),
                )
                lines = [
                    LedgerLine(
                        CUSTOMER_DEPOSITS_BY_CURRENCY[currency],
                        currency,
                        debit_minor=total_minor,
                        account_id=account_id,
                    ),
                    LedgerLine(CASH_BY_CURRENCY[currency], currency, credit_minor=amount_minor),
                ]
                if fee_minor:
                    lines.append(
                        LedgerLine(
                            FEE_INCOME_BY_CURRENCY[currency],
                            currency,
                            credit_minor=fee_minor,
                        )
                    )
                post_entry(
                    conn,
                    entry_id=entry_id,
                    entry_date=entry_date,
                    description=description or f"Pago internacional {instruction_id}",
                    source_type="TRANSFER",
                    source_id=operation_id,
                    created_by="simulator",
                    correlation_id=instruction_id,
                    created_at=timestamp,
                    lines=lines,
                )
                if fee_minor:
                    fee_gl = conn.execute(
                        "SELECT gl_account_id FROM gl_accounts WHERE code = ?",
                        (FEE_INCOME_BY_CURRENCY[currency],),
                    ).fetchone()
                    if fee_gl is None:
                        raise CorePostingError("No existe la cuenta contable de comisiones")
                    conn.execute(
                        """
                        INSERT INTO fees (transaction_id, fee_type, currency, amount_minor, gl_account_id, created_at)
                        VALUES (?, 'TRANSFER', ?, ?, ?, ?)
                        """,
                        (operation_id, currency, fee_minor, fee_gl["gl_account_id"], timestamp),
                    )
                write_audit(
                    conn,
                    event_type="INTERNATIONAL_PAYMENT_POSTED",
                    entity_type="TRANSACTION",
                    entity_id=operation_id,
                    actor="simulator",
                    correlation_id=instruction_id,
                    created_at=timestamp,
                    payload={
                        "instruction_id": instruction_id,
                        "account_id": account_id,
                        "amount_minor": amount_minor,
                        "fee_minor": fee_minor,
                        "currency": currency,
                        "external_ref": external_ref,
                        "formatted_amount": format_money(amount_minor, currency),
                    },
                )
                conn.execute("COMMIT")
                return {
                    "operation_id": operation_id,
                    "entry_id": entry_id,
                    "amount_minor": amount_minor,
                    "fee_minor": fee_minor,
                    "total_minor": total_minor,
                    "currency": currency,
                }
            except (AccountNotFoundError, AccountBlockedError, InsufficientFundsError, CorePostingError):
                conn.execute("ROLLBACK")
                raise
            except sqlite3.IntegrityError as exc:
                conn.execute("ROLLBACK")
                raise CorePostingError(f"No se pudo registrar la operación: {exc}") from exc
            except BaseException:
                conn.execute("ROLLBACK")
                raise


__all__ = ["CoreLedgerBridge", "CorePostingError"]
