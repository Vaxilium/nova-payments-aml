"""Motor de evaluación de las reglas SQL de monitoreo AML."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import config

RULE_FILES: dict[str, str] = {
    "R01": "R01_structuring.sql",
    "R02": "R02_velocity_count.sql",
    "R03": "R03_velocity_amount.sql",
    "R04": "R04_pass_through.sql",
    "R05": "R05_round_deposits.sql",
    "R06": "R06_dormant_activation.sql",
    "R07": "R07_high_risk_geography.sql",
    "R08": "R08_profile_deviation.sql",
    "R09": "R09_behavior_change.sql",
    "R10": "R10_circular_funds.sql",
    "R11": "R11_counterparty_concentration.sql",
    "R12": "R12_fan_in.sql",
}


@dataclass(frozen=True)
class RuleHit:
    rule_id: str
    customer_id: str
    account_id: str | None
    transaction_id: str | None
    amount_minor: int
    currency: str
    detected_at: str
    detail_json: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "customer_id": self.customer_id,
            "account_id": self.account_id,
            "transaction_id": self.transaction_id,
            "amount_minor": self.amount_minor,
            "currency": self.currency,
            "detected_at": self.detected_at,
            "detail_json": self.detail_json,
        }


def rule_path(rule_id: str) -> Path:
    try:
        filename = RULE_FILES[rule_id.upper()]
    except KeyError as exc:
        raise ValueError(f"Regla desconocida: {rule_id}") from exc
    return config.RULES_DIR / filename


def evaluate_rule(conn: sqlite3.Connection, rule_id: str, params: dict[str, Any] | None = None) -> list[RuleHit]:
    code = rule_id.upper()
    query = rule_path(code).read_text(encoding="utf-8")
    bindings = params if params is not None else config.load_rule_params().get(code, {})
    rows = conn.execute(query, bindings).fetchall()
    hits = []
    for row in rows:
        hits.append(
            RuleHit(
                rule_id=row["rule_id"],
                customer_id=row["customer_id"],
                account_id=row["account_id"],
                transaction_id=row["transaction_id"],
                amount_minor=int(row["amount_minor"] or 0),
                currency=row["currency"],
                detected_at=row["detected_at"],
                detail_json=row["detail_json"],
            )
        )
    return hits


def run_all_rules(
    conn: sqlite3.Connection,
    params_by_rule: dict[str, dict[str, Any]] | None = None,
) -> dict[str, list[RuleHit]]:
    results: dict[str, list[RuleHit]] = {}
    for code in RULE_FILES:
        params = params_by_rule.get(code) if params_by_rule else None
        results[code] = evaluate_rule(conn, code, params)
    return results


def rule_catalog() -> list[dict[str, Any]]:
    return [dict(meta) for meta in config.RULE_META.values()]


__all__ = [
    "RULE_FILES",
    "RuleHit",
    "evaluate_rule",
    "rule_catalog",
    "rule_path",
    "run_all_rules",
]
