"""Pruebas del scoring KYC y de la persistencia de perfiles."""

from __future__ import annotations

from aml.kyc import CustomerProfile, kyc_score_for_customer, score_customer_from_db, score_profile


def test_score_profile_bajo() -> None:
    profile = CustomerProfile(
        customer_id="CUS-TEST-LOW",
        customer_type="INDIVIDUAL",
        segment="RETAIL",
        country_code="PRY",
        created_at="2020-01-01",
        activity_risk="LOW",
        is_pep=False,
        ubo_identified=True,
        source_of_funds_verified=True,
        negative_news=False,
        channel="BRANCH",
        product_complexity="BASIC",
        expected_monthly_volume_minor=1_000_000,
    )
    result = score_profile(profile)
    assert result.risk_category == "LOW"
    assert result.requires_edd is False
    assert 0 <= result.score <= 39


def test_pep_y_jurisdiccion_alto_riesgo_exigen_edd() -> None:
    profile = CustomerProfile(
        customer_id="CUS-TEST-HIGH",
        customer_type="BUSINESS",
        segment="CORPORATE",
        country_code="IRN",
        created_at="2026-01-01",
        activity_risk="HIGH",
        is_pep=True,
        ubo_identified=False,
        source_of_funds_verified=False,
        negative_news=True,
        channel="API",
        product_complexity="COMPLEX",
        expected_monthly_volume_minor=500_000_000,
    )
    result = score_profile(profile, {"IRN"})
    assert result.risk_category == "HIGH"
    assert result.requires_edd is True
    assert len(result.edd_reasons) >= 4
    assert result.score == 100


def test_scoring_persistido_para_todos_los_clientes(conn) -> None:
    total = conn.execute("SELECT COUNT(*) AS n FROM aml_kyc_scores").fetchone()["n"]
    assert total == 500
    high = conn.execute(
        "SELECT COUNT(*) AS n FROM aml_kyc_scores WHERE risk_category = 'HIGH'"
    ).fetchone()["n"]
    assert high > 0
    customer_id = conn.execute("SELECT customer_id FROM aml_kyc_scores LIMIT 1").fetchone()["customer_id"]
    score, category = kyc_score_for_customer(conn, customer_id)
    assert 0 <= score <= 100
    assert category in {"LOW", "MEDIUM", "HIGH"}
    assert score_customer_from_db(conn, customer_id) is not None
