"""Hook AML para el simulador de pagos internacionales de Fase 4."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from . import config
from .db import account_customer, connect, high_risk_country_codes, initialize_aml, utcnow
from .kyc import kyc_score_for_customer
from .screening import ScreeningOutcome, record_screening, screen_name_in_db

ISO2_TO_ISO3 = {
    "IR": "IRN",
    "KP": "PRK",
    "SY": "SYR",
    "AF": "AFG",
    "MM": "MMR",
    "YE": "YEM",
    "LY": "LBY",
    "SS": "SSD",
}


@dataclass(frozen=True)
class AmlDecision:
    status: str = "ALLOW"
    reason: str | None = None


class NovabankAmlHook:
    """Evalúa KYC, screening y reglas de contexto antes de enviar un pago."""

    HIGH_VALUE_HOLD_MINOR = 10_000_000

    def __init__(self, db_path: Path | str | None = None) -> None:
        self.db_path = Path(db_path) if db_path is not None else config.DEFAULT_DB
        self.last_screening: ScreeningOutcome | None = None
        self.last_decision: AmlDecision | None = None

    def _connection(self) -> sqlite3.Connection:
        conn = connect(self.db_path)
        exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'aml_alerts'"
        ).fetchone()
        if exists is None:
            conn.close()
            initialize_aml(self.db_path)
            conn = connect(self.db_path)
        return conn

    def _amount_minor(self, request: Any) -> int:
        amount = request.amount if isinstance(request.amount, Decimal) else Decimal(str(request.amount))
        return int((amount * Decimal("100")).to_integral_value())

    def _screen(self, conn: sqlite3.Connection, name: str, payment_ref: str) -> ScreeningOutcome:
        outcome = screen_name_in_db(conn, name)
        record_screening(conn, outcome, payment_ref=payment_ref)
        return outcome

    def __call__(self, request: Any) -> AmlDecision:
        conn = self._connection()
        try:
            account = account_customer(conn, request.debtor_account_id)
            customer_id = account["customer_id"] if account is not None else None
            amount_minor = self._amount_minor(request)
            payment_id = request.instruction_id
            conn.execute(
                """
                INSERT OR REPLACE INTO aml_payment_context
                    (payment_id, customer_id, account_id, direction, counterparty_name,
                     counterparty_country, amount_minor, currency, source, created_at)
                VALUES (?, ?, ?, 'OUTBOUND', ?, ?, ?, ?, 'SIMULATOR', ?)
                """,
                (
                    payment_id,
                    customer_id,
                    request.debtor_account_id,
                    request.creditor_name,
                    getattr(request, "creditor_country", None),
                    amount_minor,
                    request.currency,
                    utcnow(),
                ),
            )
            conn.commit()

            creditor_screening = self._screen(conn, request.creditor_name, payment_id)
            debtor_screening = self._screen(conn, getattr(request, "debtor_name", "") or "", payment_id)
            self.last_screening = (
                creditor_screening
                if creditor_screening.score >= debtor_screening.score
                else debtor_screening
            )

            reasons: list[str] = []
            if creditor_screening.decision == "BLOCK" or debtor_screening.decision == "BLOCK":
                self.last_decision = AmlDecision(
                    status="REJECT",
                    reason="Coincidencia fuerte en lista de screening AML",
                )
                return self.last_decision
            if creditor_screening.decision == "REVIEW" or debtor_screening.decision == "REVIEW":
                reasons.append("Coincidencia parcial en screening AML")
            country = (getattr(request, "creditor_country", None) or "").upper()
            normalized_country = ISO2_TO_ISO3.get(country, country)
            if normalized_country and normalized_country in high_risk_country_codes(conn):
                reasons.append(f"Jurisdicción de alto riesgo: {normalized_country}")
            if amount_minor >= self.HIGH_VALUE_HOLD_MINOR:
                reasons.append("Pago internacional de alto valor")
            if customer_id:
                kyc_score, kyc_category = kyc_score_for_customer(conn, customer_id)
                if kyc_category == "HIGH" and kyc_score >= 70:
                    reasons.append("Cliente con riesgo KYC alto que requiere EDD")

            if reasons:
                self.last_decision = AmlDecision(status="HOLD", reason="; ".join(reasons))
            else:
                self.last_decision = AmlDecision(status="ALLOW")
            return self.last_decision
        finally:
            conn.close()


def build_default_hook(db_path: Path | str | None = None) -> NovabankAmlHook:
    return NovabankAmlHook(db_path)


__all__ = ["AmlDecision", "NovabankAmlHook", "build_default_hook"]
