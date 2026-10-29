"""Ejecuta las consultas SQL de control y registra el resultado real."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = REPO_ROOT / "05-core-middleware"
SQL_DIR = CORE_DIR / "sql"
DEFAULT_DB = CORE_DIR / "db" / "novabank.db"
sys.path.insert(0, str(CORE_DIR))

from app.db import connect  # noqa: E402


def ensure_database(db_path: Path) -> None:
    if db_path.exists():
        return
    db_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, str(CORE_DIR / "scripts" / "seed.py"), "--db", str(db_path)],
        check=True,
        cwd=REPO_ROOT,
    )


def run(db_path: Path, output: Path) -> int:
    ensure_database(db_path)
    conn = connect(db_path)
    started = datetime.now(timezone.utc).isoformat()
    queries: list[dict] = []
    failures = 0
    try:
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_keys = conn.execute("PRAGMA foreign_key_check").fetchall()
        for path in sorted(SQL_DIR.glob("*.sql")):
            query_started = time.perf_counter()
            try:
                rows = conn.execute(path.read_text(encoding="utf-8")).fetchall()
                status = "ok"
                row_count = len(rows)
            except Exception as exc:  # noqa: BLE001 - se registra el error real
                status = "error"
                row_count = 0
                failures += 1
                queries.append(
                    {
                        "file": path.name,
                        "status": status,
                        "rows": row_count,
                        "error": f"{type(exc).__name__}: {exc}",
                        "duration_ms": round((time.perf_counter() - query_started) * 1000, 2),
                    }
                )
                continue
            queries.append(
                {
                    "file": path.name,
                    "status": status,
                    "rows": row_count,
                    "error": None,
                    "duration_ms": round((time.perf_counter() - query_started) * 1000, 2),
                }
            )
    finally:
        conn.close()

    report = {
        "generated_at": started,
        "database": str(db_path),
        "integrity_check": integrity,
        "foreign_key_violations": len(foreign_keys),
        "queries_total": len(queries),
        "queries_ok": sum(1 for query in queries if query["status"] == "ok"),
        "queries_failed": failures,
        "queries": queries,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"SQL: {report['queries_ok']}/{report['queries_total']} consultas OK; "
        f"integrity_check={integrity}; fk_violations={report['foreign_key_violations']}"
    )
    return 0 if failures == 0 and integrity == "ok" and not foreign_keys else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Controles SQL de NovaBank")
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument(
        "--output",
        default=str(REPO_ROOT / "08-qa-uat" / "resultados" / "sql-controls.json"),
    )
    args = parser.parse_args()
    return run(Path(args.db), Path(args.output))


if __name__ == "__main__":
    raise SystemExit(main())
