"""Generación y deduplicación de alertas AML."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Any, Iterable

from . import config
from .db import utcnow
from .rules import RuleHit


@dataclass(frozen=True)
class Alert:
    alert_id: int
    dedup_key: str
    alert_type: str
    rule_id: str
    customer_id: str
    account_id: str | None
    transaction_id: str | None
    risk_score: int
    priority: str
    status: str
    transaction_count: int
    created_at: str
    last_seen_at: str
    detail_json: str | None
    assigned_to: str | None = None
    assigned_at: str | None = None
    due_at: str | None = None
    closed_at: str | None = None
    closure_notes: str | None = None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Alert":
        return cls(
            alert_id=row["alert_id"],
            dedup_key=row["dedup_key"],
            alert_type=row["alert_type"],
            rule_id=row["rule_id"],
            customer_id=row["customer_id"],
            account_id=row["account_id"],
            transaction_id=row["transaction_id"],
            risk_score=row["risk_score"],
            priority=row["priority"],
            status=row["status"],
            transaction_count=row["transaction_count"],
            created_at=row["created_at"],
            last_seen_at=row["last_seen_at"],
            detail_json=row["detail_json"],
            assigned_to=row["assigned_to"],
            assigned_at=row["assigned_at"],
            due_at=row["due_at"],
            closed_at=row["closed_at"],
            closure_notes=row["closure_notes"],
        )


def _kyc_score(conn: sqlite3.Connection, customer_id: str) -> int:
    row = conn.execute(
        "SELECT score FROM aml_kyc_scores WHERE customer_id = ?",
        (customer_id,),
    ).fetchone()
    return int(row["score"]) if row is not None else 0


def _dedup_key(hit: RuleHit) -> str:
    day = (hit.detected_at or "")[:10]
    return f"{hit.rule_id}:{hit.customer_id}:{hit.account_id or ''}:{day}"


def _risk_score(rule_id: str, kyc_score: int) -> int:
    meta = config.RULE_META[rule_id]
    kyc_component = min(5, max(0, kyc_score // 20))
    return min(100, int(meta["base_score"]) + kyc_component)


def _higher_priority(current: str, candidate: str) -> str:
    order = {"P1": 1, "P2": 2, "P3": 3}
    return candidate if order.get(candidate, 9) < order.get(current, 9) else current


def upsert_alert_for_hit(
    conn: sqlite3.Connection,
    hit: RuleHit,
    *,
    kyc_score: int | None = None,
    status: str = "NUEVA",
) -> int:
    meta = config.RULE_META[hit.rule_id]
    score = _risk_score(hit.rule_id, _kyc_score(conn, hit.customer_id) if kyc_score is None else kyc_score)
    priority = config.priority_for_score(score)
    key = _dedup_key(hit)
    timestamp = utcnow()
    row = conn.execute(
        "SELECT alert_id, priority FROM aml_alerts WHERE dedup_key = ?",
        (key,),
    ).fetchone()
    if row is not None:
        new_priority = _higher_priority(row["priority"], priority)
        conn.execute(
            """
            UPDATE aml_alerts
               SET transaction_count = transaction_count + 1,
                   risk_score = MAX(risk_score, ?),
                   priority = ?,
                   last_seen_at = ?,
                   updated_at = ?
             WHERE alert_id = ?
            """,
            (score, new_priority, hit.detected_at, timestamp, row["alert_id"]),
        )
        conn.commit()
        return int(row["alert_id"])

    cursor = conn.execute(
        """
        INSERT INTO aml_alerts
            (dedup_key, alert_type, rule_id, customer_id, account_id, transaction_id,
             severity, risk_score, priority, status, transaction_count, created_at,
             updated_at, last_seen_at, detail_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?)
        """,
        (
            key,
            meta["name"],
            hit.rule_id,
            hit.customer_id,
            hit.account_id,
            hit.transaction_id,
            meta["severity"],
            score,
            priority,
            status,
            timestamp,
            timestamp,
            hit.detected_at,
            hit.detail_json,
        ),
    )
    conn.commit()
    return int(cursor.lastrowid)


def create_alerts(conn: sqlite3.Connection, hits: Iterable[RuleHit]) -> list[int]:
    return [upsert_alert_for_hit(conn, hit) for hit in hits]


def get_alert(conn: sqlite3.Connection, alert_id: int) -> Alert | None:
    row = conn.execute("SELECT * FROM aml_alerts WHERE alert_id = ?", (alert_id,)).fetchone()
    return Alert.from_row(row) if row is not None else None


def list_alerts(
    conn: sqlite3.Connection,
    *,
    status: str | None = None,
    priority: str | None = None,
    customer_id: str | None = None,
    limit: int = 100,
) -> list[Alert]:
    query = "SELECT * FROM aml_alerts WHERE 1 = 1"
    params: list[Any] = []
    if status:
        query += " AND status = ?"
        params.append(status)
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    if customer_id:
        query += " AND customer_id = ?"
        params.append(customer_id)
    query += " ORDER BY risk_score DESC, alert_id ASC LIMIT ?"
    params.append(limit)
    return [Alert.from_row(row) for row in conn.execute(query, params)]


def count_alerts(conn: sqlite3.Connection) -> dict[str, int]:
    total = conn.execute("SELECT COUNT(*) AS n FROM aml_alerts").fetchone()["n"]
    by_priority = {
        row["priority"]: row["n"]
        for row in conn.execute(
            "SELECT priority, COUNT(*) AS n FROM aml_alerts GROUP BY priority ORDER BY priority"
        )
    }
    return {"total": int(total), **by_priority}


__all__ = [
    "Alert",
    "count_alerts",
    "create_alerts",
    "get_alert",
    "list_alerts",
    "upsert_alert_for_hit",
]
