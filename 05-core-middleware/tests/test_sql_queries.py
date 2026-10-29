"""Ejecuta todas las consultas operativas sobre el dataset sintético."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.db import connect

SQL_DIR = Path(__file__).resolve().parents[1] / "sql"
QUERY_FILES = sorted(SQL_DIR.glob("*.sql"))


def test_at_least_twenty_queries() -> None:
    assert len(QUERY_FILES) >= 20


@pytest.mark.parametrize("query_file", QUERY_FILES, ids=[path.name for path in QUERY_FILES])
def test_query_executes(db_path: Path, query_file: Path) -> None:
    sql = query_file.read_text(encoding="utf-8")
    assert "Propósito de negocio" in sql
    conn = connect(db_path)
    try:
        rows = conn.execute(sql).fetchall()
    finally:
        conn.close()
    assert isinstance(rows, list)


def test_all_queries_use_cte_or_window() -> None:
    for query_file in QUERY_FILES:
        sql = query_file.read_text(encoding="utf-8").upper()
        assert "WITH " in sql or "OVER (" in sql, query_file.name


def test_passthrough_query_returns_pairs(db_path: Path) -> None:
    sql = (SQL_DIR / "13_passthrough_rapido.sql").read_text(encoding="utf-8")
    conn = connect(db_path)
    try:
        rows = conn.execute(sql).fetchall()
    finally:
        conn.close()
    assert rows, "el seed debe producir al menos un pass-through etiquetado"
    assert rows[0]["deposit_id"] != rows[0]["outflow_id"]
