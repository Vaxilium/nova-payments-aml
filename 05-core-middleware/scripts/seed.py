"""CLI: genera la base sintética de NovaBank.

Ejemplos:
    python 05-core-middleware/scripts/seed.py
    python 05-core-middleware/scripts/seed.py --customers 50 --accounts 80 --transactions 2000
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import DEFAULT_DB_PATH, DEFAULT_SEED  # noqa: E402
from app.seed import SeedConfig, seed_database, write_seed_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Generador reproducible del core bancario simulado")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="Ruta de la base SQLite")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Semilla aleatoria fija")
    parser.add_argument("--customers", type=int, default=500)
    parser.add_argument("--accounts", type=int, default=800)
    parser.add_argument("--transactions", type=int, default=50_000)
    parser.add_argument("--months", type=int, default=6)
    parser.add_argument("--no-reset", action="store_true", help="No borra el esquema existente")
    parser.add_argument("--report", default=None, help="Ruta opcional para el resumen JSON")
    args = parser.parse_args()

    config = SeedConfig(
        customers=args.customers,
        accounts=args.accounts,
        transactions=args.transactions,
        months=args.months,
        seed=args.seed,
    )
    summary = seed_database(args.db, config=config, reset=not args.no_reset)
    if args.report:
        write_seed_report(summary, args.report)
    print(json.dumps(summary.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
