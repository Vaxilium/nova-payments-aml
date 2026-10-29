"""Fixtures compartidas de la suite de Fase 3."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

CORE_DIR = Path(__file__).resolve().parents[1]
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from app.api import create_app  # noqa: E402
from app.db import connect, init_schema  # noqa: E402
from app.ledger import GL_ACCOUNTS  # noqa: E402
from app.seed import SeedConfig, seed_database  # noqa: E402
from app.service import BankingService  # noqa: E402


@pytest.fixture(scope="session")
def seeded_db(tmp_path_factory: pytest.TempPathFactory) -> Path:
    directory = tmp_path_factory.mktemp("novabank-seed")
    path = directory / "novabank_seed.db"
    config = SeedConfig(customers=70, accounts=100, transactions=1_600, months=3, seed=424242)
    seed_database(path, config=config, reset=True)
    return path


@pytest.fixture
def db_path(seeded_db: Path, tmp_path: Path) -> Path:
    """Copia la base sembrada para aislar cada prueba."""
    destination = tmp_path / "novabank.db"
    source_conn = sqlite3.connect(seeded_db)
    target_conn = sqlite3.connect(destination)
    try:
        source_conn.backup(target_conn)
    finally:
        target_conn.close()
        source_conn.close()
    return destination


@pytest.fixture
def service(db_path: Path) -> BankingService:
    return BankingService(db_path)


@pytest.fixture
def client(db_path: Path) -> TestClient:
    app = create_app(db_path)
    with TestClient(app) as test_client:
        yield test_client


def _pick_account(
    db_path: Path,
    *,
    currency: str = "PYG",
    status: str = "ACTIVE",
    exclude: str | None = None,
    min_balance: int = 100_000,
) -> dict:
    conn = connect(db_path)
    try:
        rows = conn.execute(
            """
            SELECT * FROM accounts
            WHERE currency = ? AND status = ? AND balance_minor >= ?
              AND (? IS NULL OR account_id <> ?)
            ORDER BY account_id
            """,
            (currency, status, min_balance, exclude, exclude),
        ).fetchall()
    finally:
        conn.close()
    if not rows:
        raise AssertionError(f"No hay cuenta {currency} {status} con saldo suficiente")
    return dict(rows[0])


def _pick_pair(db_path: Path, *, currency: str = "PYG") -> tuple[dict, dict]:
    conn = connect(db_path)
    try:
        rows = conn.execute(
            """
            SELECT * FROM accounts
            WHERE currency = ? AND status = 'ACTIVE'
            ORDER BY account_id
            LIMIT 2
            """,
            (currency,),
        ).fetchall()
    finally:
        conn.close()
    if len(rows) < 2:
        raise AssertionError(f"No hay dos cuentas activas en {currency}")
    return dict(rows[0]), dict(rows[1])


@pytest.fixture
def pyg_account(db_path: Path) -> dict:
    return _pick_account(db_path, currency="PYG")


@pytest.fixture
def second_pyg_account(db_path: Path, pyg_account: dict) -> dict:
    return _pick_account(db_path, currency="PYG", exclude=pyg_account["account_id"])


@pytest.fixture
def usd_account(db_path: Path) -> dict:
    return _pick_account(db_path, currency="USD", min_balance=1_000)


@pytest.fixture
def schema_db(tmp_path: Path) -> Path:
    """Base mínima con catálogos y una cuenta para probar constraints."""
    path = tmp_path / "schema.db"
    conn = connect(path)
    try:
        init_schema(conn, reset=True)
        conn.execute(
            "INSERT INTO currencies (code, name, minor_unit, symbol) VALUES ('PYG', 'Guaraní', 0, '₲')"
        )
        conn.executemany(
            """
            INSERT INTO gl_accounts (code, name, account_class, normal_side, is_active)
            VALUES (?, ?, ?, ?, 1)
            """,
            [(gl["code"], gl["name"], gl["account_class"], gl["normal_side"]) for gl in GL_ACCOUNTS],
        )
        conn.execute(
            """
            INSERT INTO customers
                (customer_id, customer_type, first_name, last_name, document_type,
                 document_number, country_code, city, segment, risk_rating,
                 kyc_status, is_active, created_at)
            VALUES ('CUS-TEST', 'INDIVIDUAL', 'Ana', 'Test', 'CI', 'CI-TEST',
                    'PRY', 'Asunción', 'RETAIL', 'LOW', 'VERIFIED', 1, '2026-01-01T00:00:00')
            """
        )
        conn.execute(
            """
            INSERT INTO accounts
                (account_id, customer_id, account_number, account_type, currency,
                 status, balance_minor, overdraft_limit_minor, version, opened_at)
            VALUES ('ACC-TEST', 'CUS-TEST', '00000000000001', 'SAVINGS', 'PYG',
                    'ACTIVE', 1000000, 0, 1, '2026-01-01T00:00:00')
            """
        )
    finally:
        conn.close()
    return path
