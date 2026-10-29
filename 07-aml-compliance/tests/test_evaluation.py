"""Pruebas de evaluación contra la verdad sintética de Fase 3."""

from __future__ import annotations

from aml.db import connect
from aml.evaluation import evaluate, render_markdown
from aml.rules import run_all_rules


def test_metricas_globales_y_por_patron(initialized_db) -> None:
    conn = connect(initialized_db)
    try:
        hits = run_all_rules(conn)
        result = evaluate(conn, hits)
    finally:
        conn.close()

    assert result.true_positives == 341
    assert result.false_negatives == 0
    assert result.recall == 1.0
    assert result.precision >= 0.99
    assert result.precision_lower_bound >= 0.65
    assert set(result.by_pattern) == {
        "DORMANT_ACTIVATION",
        "HIGH_VELOCITY",
        "PASS_THROUGH",
        "ROUND_MULE",
        "STRUCTURING",
    }
    for pattern in result.by_pattern.values():
        assert pattern["recall"] == 1.0


def test_reporte_markdown_incluye_trazabilidad(initialized_db) -> None:
    conn = connect(initialized_db)
    try:
        result = evaluate(conn, run_all_rules(conn))
    finally:
        conn.close()
    report = render_markdown(result)
    assert "# Evaluación de reglas" in report
    assert "Precisión conservadora" in report
    assert "STRUCTURING" in report
    assert "341" in report
