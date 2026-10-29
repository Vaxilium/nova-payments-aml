"""Inicializa el esquema y los datos de referencia AML sobre la base del core."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

AML_DIR = Path(__file__).resolve().parents[1]
if str(AML_DIR) not in sys.path:
    sys.path.insert(0, str(AML_DIR))

from aml import config
from aml.db import initialize_aml


def main() -> int:
    parser = argparse.ArgumentParser(description="Inicializa el motor AML de NovaBank")
    parser.add_argument("--db", default=str(config.DEFAULT_DB), help="Ruta a la base SQLite del core")
    args = parser.parse_args()
    result = initialize_aml(args.db)
    print(f"Base AML inicializada: {args.db}")
    for key, value in result.items():
        print(f"  {key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
