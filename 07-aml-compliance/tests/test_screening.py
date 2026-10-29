"""Pruebas del screening difuso contra listas ficticias."""

from __future__ import annotations

from aml.screening import (
    decision_for_score,
    load_watchlist,
    name_similarity,
    normalize_name,
    record_screening,
    screen_name,
)


def test_normalizacion_de_nombres() -> None:
    assert normalize_name("  José Ángel  ") == "JOSE ANGEL"
    assert normalize_name("ACME S.A.") == "ACME"


def test_coincidencia_exacta_bloquea(conn) -> None:
    outcome = screen_name("Viktor Solano", load_watchlist(conn))
    assert outcome.decision == "BLOCK"
    assert outcome.score == 1.0
    assert outcome.best_match is not None


def test_variante_parcial_revisa_o_bloquea(conn) -> None:
    outcome = screen_name("Viktor Solano Gomez", load_watchlist(conn))
    assert outcome.score >= 0.80
    assert outcome.decision in {"REVIEW", "BLOCK"}


def test_nombre_normal_no_coincide(conn) -> None:
    outcome = screen_name("Proveedor Normal S.A.", load_watchlist(conn))
    assert outcome.decision == "NO_MATCH"
    assert outcome.score < 0.80


def test_similitud_y_umbrales() -> None:
    assert name_similarity("Ana Perez", "Ana Perez") == 1.0
    assert decision_for_score(0.99) == "BLOCK"
    assert decision_for_score(0.90) == "REVIEW"
    assert decision_for_score(0.50) == "NO_MATCH"


def test_registro_de_screening(conn) -> None:
    outcome = screen_name("Viktor Solano", load_watchlist(conn))
    screening_id = record_screening(conn, outcome, payment_ref="TEST-SCREEN-1")
    assert screening_id > 0
    row = conn.execute(
        "SELECT decision, payment_ref FROM aml_screening_results WHERE screening_id = ?",
        (screening_id,),
    ).fetchone()
    assert row["decision"] == "BLOCK"
    assert row["payment_ref"] == "TEST-SCREEN-1"
