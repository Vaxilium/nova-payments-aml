"""Ejecuta las reglas AML y genera el reporte de evaluación contra la verdad."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

AML_DIR = Path(__file__).resolve().parents[1]
if str(AML_DIR) not in sys.path:
    sys.path.insert(0, str(AML_DIR))

from aml import config
from aml.db import connect, initialize_aml
from aml.evaluation import evaluate_and_report
from aml.rules import run_all_rules


def _ensure_aml(conn, db_path: str):
    exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'aml_alerts'"
    ).fetchone()
    if exists is None:
        conn.close()
        initialize_aml(db_path)
        return connect(db_path)
    return conn


def main() -> int:
    parser = argparse.ArgumentParser(description="Evalúa reglas AML contra la verdad de Fase 3")
    parser.add_argument("--db", default=str(config.DEFAULT_DB), help="Ruta a la base SQLite del core")
    parser.add_argument(
        "--output",
        default=str(config.DOCS_DIR / "evaluacion-verdad.md"),
        help="Ruta del reporte Markdown",
    )
    args = parser.parse_args()
    conn = connect(args.db)
    conn = _ensure_aml(conn, args.db)
    hits = run_all_rules(conn)
    result = evaluate_and_report(conn, hits, Path(args.output))
    print(f"Reporte generado: {args.output}")
    print(
        "Alertadas: {flagged} | TP: {tp} | FP: {fp} | Sin etiqueta: {unlabeled} | "
        "Precisión: {precision:.2%} | Recall: {recall:.2%}".format(
            flagged=result.flagged_transactions,
            tp=result.true_positives,
            fp=result.false_positives,
            unlabeled=result.unlabeled_flagged,
            precision=result.precision,
            recall=result.recall,
        )
    )
    for rule_id, metric in result.by_rule.items():
        print(
            f"  {rule_id}: {metric.flagged} alertadas, {metric.true_positives} TP, "
            f"{metric.false_positives} FP, {metric.unlabeled} sin etiqueta"
        )
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
