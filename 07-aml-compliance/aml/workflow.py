"""Flujo de alertas y casos: asignación, escalamiento, SLA y cierre."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

from . import config
from .alerts import get_alert
from .db import utcnow

ALERT_TRANSITIONS: dict[str, set[str]] = {
    "NUEVA": {"EN_ANALISIS", "ESCALADA", "CERRADA_FALSO_POSITIVO"},
    "EN_ANALISIS": {"ESCALADA", "CERRADA_FALSO_POSITIVO", "REPORTADA"},
    "ESCALADA": {"EN_ANALISIS", "CERRADA_FALSO_POSITIVO", "REPORTADA"},
    "CERRADA_FALSO_POSITIVO": set(),
    "REPORTADA": set(),
}

CASE_TRANSITIONS: dict[str, set[str]] = {
    "ABIERTO": {"EN_ANALISIS", "ESCALADO", "CERRADO", "REPORTADO"},
    "EN_ANALISIS": {"ESCALADO", "CERRADO", "REPORTADO"},
    "ESCALADO": {"EN_ANALISIS", "CERRADO", "REPORTADO"},
    "CERRADO": set(),
    "REPORTADO": set(),
}


def _default_analyst() -> str:
    return config.ANALYSTS[0]


def add_business_days(start: datetime, days: int) -> datetime:
    current = start
    remaining = days
    while remaining > 0:
        current += timedelta(days=1)
        if current.weekday() < 5:
            remaining -= 1
    return current


def _due_at(priority: str) -> str:
    now = datetime.now(timezone.utc)
    sla = config.SLA[priority]
    return (now + timedelta(minutes=int(sla["assignment_minutes"]))).replace(microsecond=0).isoformat()


def _case_due_at(priority: str) -> str:
    now = datetime.now(timezone.utc)
    sla = config.SLA[priority]
    return add_business_days(now, int(sla["closure_business_days"])).replace(microsecond=0).isoformat()


def record_transition(
    conn: sqlite3.Connection,
    entity_type: str,
    entity_id: int,
    from_status: str | None,
    to_status: str,
    *,
    analyst: str | None = None,
    reason: str | None = None,
) -> int:
    cursor = conn.execute(
        """
        INSERT INTO aml_workflow_transitions
            (entity_type, entity_id, from_status, to_status, analyst, reason, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (entity_type, entity_id, from_status, to_status, analyst or _default_analyst(), reason, utcnow()),
    )
    return int(cursor.lastrowid)


def _change_alert_status(
    conn: sqlite3.Connection,
    alert_id: int,
    to_status: str,
    *,
    analyst: str | None = None,
    reason: str | None = None,
) -> None:
    alert = get_alert(conn, alert_id)
    if alert is None:
        raise ValueError(f"Alerta inexistente: {alert_id}")
    if alert.status == to_status:
        return
    if to_status not in ALERT_TRANSITIONS.get(alert.status, set()):
        raise ValueError(f"Transición de alerta inválida: {alert.status} -> {to_status}")
    conn.execute(
        "UPDATE aml_alerts SET status = ?, updated_at = ? WHERE alert_id = ?",
        (to_status, utcnow(), alert_id),
    )
    record_transition(conn, "ALERT", alert_id, alert.status, to_status, analyst=analyst, reason=reason)


def assign_alert(conn: sqlite3.Connection, alert_id: int, analyst: str | None = None) -> None:
    alert = get_alert(conn, alert_id)
    if alert is None:
        raise ValueError(f"Alerta inexistente: {alert_id}")
    assigned = analyst or _default_analyst()
    conn.execute(
        """
        UPDATE aml_alerts
           SET assigned_to = ?, assigned_at = ?, due_at = ?, updated_at = ?
         WHERE alert_id = ?
        """,
        (assigned, utcnow(), _due_at(alert.priority), utcnow(), alert_id),
    )
    if alert.status == "NUEVA":
        _change_alert_status(conn, alert_id, "EN_ANALISIS", analyst=assigned, reason="Asignación inicial")
    conn.commit()


def close_alert_as_false_positive(
    conn: sqlite3.Connection,
    alert_id: int,
    reason: str,
    *,
    analyst: str | None = None,
) -> None:
    alert = get_alert(conn, alert_id)
    if alert is None:
        raise ValueError(f"Alerta inexistente: {alert_id}")
    _change_alert_status(
        conn,
        alert_id,
        "CERRADA_FALSO_POSITIVO",
        analyst=analyst,
        reason=reason,
    )
    conn.execute(
        "UPDATE aml_alerts SET closed_at = ?, closure_notes = ?, updated_at = ? WHERE alert_id = ?",
        (utcnow(), reason, utcnow(), alert_id),
    )
    conn.commit()


def create_case(
    conn: sqlite3.Connection,
    customer_id: str,
    title: str,
    priority: str,
    alert_ids: Iterable[int] = (),
    *,
    analyst: str | None = None,
) -> int:
    if priority not in config.SLA:
        raise ValueError(f"Prioridad inválida: {priority}")
    assigned = analyst or _default_analyst()
    timestamp = utcnow()
    cursor = conn.execute(
        """
        INSERT INTO aml_cases
            (customer_id, title, status, priority, assigned_to, opened_at, due_at, created_at, updated_at)
        VALUES (?, ?, 'ABIERTO', ?, ?, ?, ?, ?, ?)
        """,
        (customer_id, title, priority, assigned, timestamp, _case_due_at(priority), timestamp, timestamp),
    )
    case_id = int(cursor.lastrowid)
    record_transition(conn, "CASE", case_id, None, "ABIERTO", analyst=assigned, reason="Apertura de caso")
    for alert_id in alert_ids:
        alert = get_alert(conn, alert_id)
        if alert is None:
            raise ValueError(f"Alerta inexistente: {alert_id}")
        conn.execute(
            """
            INSERT OR IGNORE INTO aml_case_alerts (case_id, alert_id) VALUES (?, ?)
            """,
            (case_id, alert_id),
        )
        if alert.status != "ESCALADA":
            _change_alert_status(conn, alert_id, "ESCALADA", analyst=assigned, reason=f"Escalada al caso {case_id}")
        conn.execute(
            "UPDATE aml_alerts SET case_id = ?, updated_at = ? WHERE alert_id = ?",
            (case_id, utcnow(), alert_id),
        )
    conn.execute(
        "UPDATE aml_cases SET risk_score = (SELECT COALESCE(MAX(risk_score), 0) FROM aml_alerts WHERE case_id = ?) WHERE case_id = ?",
        (case_id, case_id),
    )
    conn.commit()
    return case_id


def escalate_alert(
    conn: sqlite3.Connection,
    alert_id: int,
    reason: str,
    *,
    analyst: str | None = None,
) -> int:
    alert = get_alert(conn, alert_id)
    if alert is None:
        raise ValueError(f"Alerta inexistente: {alert_id}")
    case_id = create_case(
        conn,
        alert.customer_id,
        f"Caso AML - {alert.customer_id} - {alert.alert_type}",
        alert.priority,
        [alert_id],
        analyst=analyst,
    )
    return case_id


def update_case_status(
    conn: sqlite3.Connection,
    case_id: int,
    to_status: str,
    *,
    analyst: str | None = None,
    reason: str | None = None,
    closure_notes: str | None = None,
) -> None:
    row = conn.execute("SELECT status FROM aml_cases WHERE case_id = ?", (case_id,)).fetchone()
    if row is None:
        raise ValueError(f"Caso inexistente: {case_id}")
    current = row["status"]
    if current == to_status:
        return
    if to_status not in CASE_TRANSITIONS.get(current, set()):
        raise ValueError(f"Transición de caso inválida: {current} -> {to_status}")
    values: list[Any] = [to_status, utcnow(), case_id]
    query = "UPDATE aml_cases SET status = ?, updated_at = ?"
    if to_status == "CERRADO":
        query += ", closed_at = ?, closure_notes = ?"
        values = [to_status, utcnow(), utcnow(), closure_notes, case_id]
    query += " WHERE case_id = ?"
    conn.execute(query, values)
    record_transition(conn, "CASE", case_id, current, to_status, analyst=analyst, reason=reason)
    conn.commit()


def get_case(conn: sqlite3.Connection, case_id: int) -> dict[str, Any] | None:
    row = conn.execute("SELECT * FROM aml_cases WHERE case_id = ?", (case_id,)).fetchone()
    return dict(row) if row is not None else None


def list_cases(conn: sqlite3.Connection, status: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
    query = "SELECT * FROM aml_cases"
    params: list[Any] = []
    if status:
        query += " WHERE status = ?"
        params.append(status)
    query += " ORDER BY risk_score DESC, case_id ASC LIMIT ?"
    params.append(limit)
    return [dict(row) for row in conn.execute(query, params)]


def case_alerts(conn: sqlite3.Connection, case_id: int) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT a.*
        FROM aml_alerts a
        JOIN aml_case_alerts ca ON ca.alert_id = a.alert_id
        WHERE ca.case_id = ?
        ORDER BY a.risk_score DESC, a.alert_id
        """,
        (case_id,),
    ).fetchall()
    return [dict(row) for row in rows]


__all__ = [
    "ALERT_TRANSITIONS",
    "CASE_TRANSITIONS",
    "add_business_days",
    "assign_alert",
    "case_alerts",
    "close_alert_as_false_positive",
    "create_case",
    "escalate_alert",
    "get_case",
    "list_cases",
    "record_transition",
    "update_case_status",
]
