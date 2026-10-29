"""Fixtures de la suite UAT automatizada (Fase 7)."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = REPO_ROOT / "05-core-middleware"
MESSAGING_DIR = REPO_ROOT / "06-mensajeria"
for path in (CORE_DIR, MESSAGING_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.db import connect  # noqa: E402
from app.seed import SeedConfig, seed_database  # noqa: E402
from app.service import BankingService  # noqa: E402

from simulator.instant import InstantPaymentSimulator  # noqa: E402


@pytest.fixture(scope="session")
def seeded_db(tmp_path_factory: pytest.TempPathFactory) -> Path:
    directory = tmp_path_factory.mktemp("novabank-uat-seed")
    path = directory / "novabank_uat.db"
    seed_database(
        path,
        config=SeedConfig(customers=40, accounts=60, transactions=800, months=3, seed=707070),
        reset=True,
    )
    return path


@pytest.fixture
def db_path(seeded_db: Path, tmp_path: Path) -> Path:
    destination = tmp_path / "novabank_uat.db"
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
def instant_simulator(service: BankingService) -> InstantPaymentSimulator:
    return InstantPaymentSimulator(service)


@pytest.fixture
def pyg_account(db_path: Path) -> dict:
    conn = connect(db_path)
    try:
        row = conn.execute(
            """
            SELECT * FROM accounts
            WHERE currency = 'PYG' AND status = 'ACTIVE' AND balance_minor >= 2000000
            ORDER BY account_id
            LIMIT 1
            """
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        raise AssertionError("No hay cuenta PYG activa con saldo suficiente para UAT")
    return dict(row)
