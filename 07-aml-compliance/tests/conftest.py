"""Fixtures de Fase 5: base del core con esquema y datos AML inicializados."""

from __future__ import annotations

import shutil
import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CORE_DB = REPO_ROOT / "05-core-middleware" / "db" / "novabank.db"
for path in (
    REPO_ROOT / "05-core-middleware",
    REPO_ROOT / "06-mensajeria",
    REPO_ROOT / "07-aml-compliance",
):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from aml.db import connect, initialize_aml  # noqa: E402


@pytest.fixture(scope="session")
def initialized_db(tmp_path_factory: pytest.TempPathFactory) -> Path:
    directory = tmp_path_factory.mktemp("novabank-aml-base")
    destination = directory / "novabank_aml.db"
    shutil.copy2(CORE_DB, destination)
    initialize_aml(destination)
    return destination


@pytest.fixture
def db_path(initialized_db: Path, tmp_path: Path) -> Path:
    destination = tmp_path / "novabank_aml.db"
    source = sqlite3.connect(initialized_db)
    target = sqlite3.connect(destination)
    try:
        source.backup(target)
    finally:
        target.close()
        source.close()
    return destination


@pytest.fixture
def conn(db_path: Path):
    connection = connect(db_path)
    try:
        yield connection
    finally:
        connection.close()


@pytest.fixture
def usd_account(conn: sqlite3.Connection) -> dict:
    row = conn.execute(
        """
        SELECT a.* FROM accounts a
        JOIN aml_kyc_scores k ON k.customer_id = a.customer_id
        WHERE a.currency = 'USD' AND a.status = 'ACTIVE' AND a.balance_minor >= 100000
          AND k.risk_category = 'LOW'
        ORDER BY a.account_id LIMIT 1
        """
    ).fetchone()
    if row is None:
        raise AssertionError("No hay cuenta USD activa para las pruebas AML")
    return dict(row)
