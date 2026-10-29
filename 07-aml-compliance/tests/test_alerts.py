"""Pruebas de generación, deduplicación y priorización de alertas."""

from __future__ import annotations

from aml.alerts import count_alerts, create_alerts, get_alert, list_alerts, upsert_alert_for_hit
from aml.rules import RuleHit


def _hit(rule_id: str = "R01", transaction_id: str | None = None, detected_at: str = "2026-10-01T10:00:00") -> RuleHit:
    return RuleHit(
        rule_id=rule_id,
        customer_id="CUS-000001",
        account_id="ACC-000001",
        transaction_id=transaction_id,
        amount_minor=9_500_000,
        currency="PYG",
        detected_at=detected_at,
        detail_json='{"test": true}',
    )


def test_alerta_se_crea_y_deduplica(conn) -> None:
    first = upsert_alert_for_hit(conn, _hit(), kyc_score=90)
    second = upsert_alert_for_hit(conn, _hit(), kyc_score=90)
    assert first == second
    alert = get_alert(conn, first)
    assert alert is not None
    assert alert.transaction_count == 2
    assert alert.priority == "P1"
    assert alert.risk_score >= 80
    assert alert.dedup_key.startswith("R01:CUS-000001:ACC-000001:2026-10-01")


def test_alertas_distintas_y_listado(conn) -> None:
    hits = [
        _hit(detected_at="2026-10-02T10:00:00"),
        _hit(detected_at="2026-10-03T10:00:00"),
        RuleHit(
            rule_id="R07",
            customer_id="CUS-000002",
            account_id="ACC-000002",
            transaction_id=None,
            amount_minor=1_000_000,
            currency="PYG",
            detected_at="2026-10-02T10:00:00",
            detail_json='{"country_code": "IRN"}',
        ),
    ]
    ids = create_alerts(conn, hits)
    assert len(set(ids)) == 3
    counts = count_alerts(conn)
    assert counts["total"] == 3
    assert list_alerts(conn, priority="P1")

