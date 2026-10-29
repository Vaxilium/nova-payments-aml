"""Conexiones SQLite y utilidades de inicialización."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .config import DROP_PATH, SCHEMA_PATH, resolve_db_path


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Abre una conexión configurada para concurrencia y claves foráneas."""
    path = str(resolve_db_path(db_path))
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=30.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 30000")
    if path != ":memory:":
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
    return conn


def init_schema(conn: sqlite3.Connection, *, reset: bool = True) -> None:
    """Crea el esquema; con reset=True elimina primero los objetos existentes."""
    if reset:
        conn.executescript(DROP_PATH.read_text(encoding="utf-8"))
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def table_count(conn: sqlite3.Connection, table: str) -> int:
    return int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
