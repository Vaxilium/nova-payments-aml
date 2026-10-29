"""Fixtures de Fase 4: base sembrada, servicio y simuladores."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

CORE_DIR = Path(__file__).resolve().parents[2] / "05-core-middleware"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from app.db import connect  # noqa: E402
from app.seed import SeedConfig, seed_database  # noqa: E402
from app.service import BankingService  # noqa: E402

from simulator.instant import InstantPaymentSimulator  # noqa: E402
from simulator.international import InternationalPaymentSimulator  # noqa: E402
from simulator.models import SimulatedGateway  # noqa: E402


@pytest.fixture(scope="session")
def seeded_db(tmp_path_factory: pytest.TempPathFactory) -> Path:
    directory = tmp_path_factory.mktemp("novabank-messaging-seed")
    path = directory / "novabank_messaging.db"
    seed_database(
        path,
        config=SeedConfig(customers=40, accounts=60, transactions=800, months=3, seed=909090),
        reset=True,
    )
    return path


@pytest.fixture
def db_path(seeded_db: Path, tmp_path: Path) -> Path:
    destination = tmp_path / "novabank_messaging.db"
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
def international_simulator(service: BankingService) -> InternationalPaymentSimulator:
    return InternationalPaymentSimulator(service)


def _pick_account(db_path: Path, *, currency: str = "PYG", min_balance: int = 1_000_000) -> dict:
    conn = connect(db_path)
    try:
        row = conn.execute(
            """
            SELECT * FROM accounts
            WHERE currency = ? AND status = 'ACTIVE' AND balance_minor >= ?
            ORDER BY account_id
            LIMIT 1
            """,
            (currency, min_balance),
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        raise AssertionError(f"No hay cuenta {currency} activa con saldo suficiente")
    return dict(row)


@pytest.fixture
def pyg_account(db_path: Path) -> dict:
    return _pick_account(db_path, currency="PYG", min_balance=2_000_000)


@pytest.fixture
def second_pyg_account(db_path: Path, pyg_account: dict) -> dict:
    conn = connect(db_path)
    try:
        row = conn.execute(
            """
            SELECT * FROM accounts
            WHERE currency = 'PYG' AND status = 'ACTIVE' AND account_id <> ?
            ORDER BY account_id
            LIMIT 1
            """,
            (pyg_account["account_id"],),
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        raise AssertionError("No hay una segunda cuenta PYG")
    return dict(row)


@pytest.fixture
def usd_account(db_path: Path) -> dict:
    return _pick_account(db_path, currency="USD", min_balance=100_000)


@pytest.fixture
def scripted_gateway() -> SimulatedGateway:
    return SimulatedGateway()
