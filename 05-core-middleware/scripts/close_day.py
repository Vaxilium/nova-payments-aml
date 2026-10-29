"""CLI: ejecuta el cierre diario de saldos para una fecha o para todo el histórico."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.closing import close_day, rebuild_daily_balances  # noqa: E402
from app.config import DEFAULT_DB_PATH  # noqa: E402
from app.db import connect  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Cierre diario de saldos de NovaBank")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--date", default=None, help="Fecha YYYY-MM-DD; si se omite, recalcula todo")
    args = parser.parse_args()

    conn = connect(args.db)
    try:
        if args.date:
            rows = close_day(conn, args.date)
            print(f"Cierre {args.date}: {rows} cuentas actualizadas")
        else:
            rows = rebuild_daily_balances(conn)
            print(f"Cierre completo: {rows} filas generadas")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
