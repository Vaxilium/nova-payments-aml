"""Configuración compartida del core simulado."""

from __future__ import annotations

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
CORE_DIR = PACKAGE_DIR.parent
DB_DIR = CORE_DIR / "db"
SCHEMA_PATH = DB_DIR / "schema.sql"
DROP_PATH = DB_DIR / "drop.sql"
DEFAULT_DB_PATH = DB_DIR / "novabank.db"
OPENAPI_PATH = CORE_DIR / "openapi.yaml"

DEFAULT_SEED = 20261027
DEFAULT_ACTOR = "system"
API_PREFIX = "/v1"
API_VERSION = "1.0.0"
API_TITLE = "NovaBank Core & Payments Middleware API"
API_DESCRIPTION = (
    "API REST ficticia del core bancario y del middleware de pagos de NovaBank. "
    "Expone consulta de clientes y cuentas, saldos, débitos, créditos, "
    "transferencias y estado de operaciones. Todas las operaciones monetarias "
    "usan idempotency-key y quedan registradas en el libro mayor por partida doble."
)


def resolve_db_path(db_path: str | Path | None = None) -> Path:
    """Devuelve la ruta de la base, respetando NOVABANK_DB_PATH."""
    if db_path is not None:
        return Path(db_path)
    return Path(os.getenv("NOVABANK_DB_PATH", str(DEFAULT_DB_PATH)))
