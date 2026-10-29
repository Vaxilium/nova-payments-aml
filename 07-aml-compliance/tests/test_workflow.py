"""Pruebas del flujo de alertas, casos, SLA y transiciones."""

from __future__ import annotations

import pytest

from aml.alerts import get_alert, upsert_alert_for_hit
from aml.rules import RuleHit
from aml.workflow import (
    assign_alert,
    create_case,
    escalate_alert,
    get_case,
    record_transition,
    update_case_status,
)


def _alert(conn) -> int:
    hit = RuleHit(
        rule_id="R01",
        customer_id="CUS-000001",
        account_id="ACC-000001",
        transaction_id=None,
        amount_minor=9_500_000,
        currency="PYG",
        detected_at="2026-10-01T10:00:00",
        detail_json="{}",
    )
    return upsert_alert_for_hit(conn, hit, kyc_score=90)


def test_asignacion_con_sla_y_transicion(conn) -> None:
    alert_id = _alert(conn)
    assign_alert(conn, alert_id, analyst="analista_aml_2")
    alert = get_alert(conn, alert_id)
    assert alert.status == "EN_ANALISIS"
    assert alert.assigned_to == "analista_aml_2"
    transitions = conn.execute(
        "SELECT from_status, to_status, analyst FROM aml_workflow_transitions WHERE entity_id = ?",
        (alert_id,),
    ).fetchall()
    assert transitions[-1]["to_status"] == "EN_ANALISIS"


def test_escalamiento_crea_caso_y_cierre(conn) -> None:
    alert_id = _alert(conn)
    case_id = escalate_alert(conn, alert_id, "Requiere investigación")
    case = get_case(conn, case_id)
    assert case is not None
    assert case["status"] == "ABIERTO"
    assert case["priority"] == "P1"
    assert case["risk_score"] >= 80
    assert get_alert(conn, alert_id).status == "ESCALADA"

    update_case_status(conn, case_id, "EN_ANALISIS", reason="Análisis iniciado")
    update_case_status(conn, case_id, "CERRADO", reason="Cierre", closure_notes="Sin mérito")
    closed = get_case(conn, case_id)
    assert closed["status"] == "CERRADO"
    assert closed["closed_at"] is not None
    assert closed["closure_notes"] == "Sin mérito"

    with pytest.raises(ValueError):
        update_case_status(conn, case_id, "EN_ANALISIS", reason="Inválida")


def test_caso_directo_y_transicion_invalida(conn) -> None:
    case_id = create_case(conn, "CUS-000001", "Caso de prueba", "P2")
    assert get_case(conn, case_id)["status"] == "ABIERTO"
    update_case_status(conn, case_id, "CERRADO", reason="Cierre directo")
    with pytest.raises(ValueError):
        update_case_status(conn, case_id, "REPORTADO", reason="Inválida")
    record_transition(conn, "CASE", case_id, "CERRADO", "CERRADO", reason="Auditoría")
    conn.commit()
