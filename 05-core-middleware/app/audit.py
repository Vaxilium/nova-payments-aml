"""Bitácora de auditoría persistente y logging estructurado."""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("novabank.audit")


def utcnow() -> str:
    """Timestamp ISO-8601 UTC con segundos, usado en toda la aplicación."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_audit(
    conn: sqlite3.Connection,
    *,
    event_type: str,
    entity_type: str,
    entity_id: str | None,
    actor: str,
    payload: dict[str, Any],
    correlation_id: str | None = None,
    created_at: str | None = None,
) -> None:
    """Registra un evento de auditoría en la base y en el log estructurado."""
    timestamp = created_at or utcnow()
    payload_json = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    conn.execute(
        """
        INSERT INTO audit_log
            (event_type, entity_type, entity_id, actor, correlation_id, payload_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (event_type, entity_type, entity_id, actor, correlation_id, payload_json, timestamp),
    )
    logger.info(
        json.dumps(
            {
                "event_type": event_type,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "actor": actor,
                "correlation_id": correlation_id,
                "created_at": timestamp,
            },
            ensure_ascii=False,
        )
    )
