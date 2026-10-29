"""Modelo KYC/CDD y scoring de riesgo de cliente (0-100)."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Any

from . import config
from .db import high_risk_country_codes, utcnow


@dataclass(frozen=True)
class CustomerProfile:
    customer_id: str
    customer_type: str
    segment: str
    country_code: str
    created_at: str
    activity_risk: str = "LOW"
    is_pep: bool = False
    ubo_identified: bool = True
    source_of_funds_verified: bool = True
    negative_news: bool = False
    channel: str = "BRANCH"
    product_complexity: str = "BASIC"
    expected_monthly_volume_minor: int = 0


@dataclass(frozen=True)
class KycResult:
    customer_id: str
    score: int
    risk_category: str
    requires_edd: bool
    factors: dict[str, dict[str, Any]]
    edd_reasons: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "score": self.score,
            "risk_category": self.risk_category,
            "requires_edd": self.requires_edd,
            "factors": self.factors,
            "edd_reasons": self.edd_reasons,
        }


def _tenure_months(created_at: str, as_of: date) -> int:
    try:
        start = date.fromisoformat(str(created_at)[:10])
    except ValueError:
        return 0
    months = (as_of.year - start.year) * 12 + (as_of.month - start.month)
    if as_of.day < start.day:
        months -= 1
    return max(0, months)


def _tenure_bucket(months: int) -> str:
    if months < 6:
        return "UNDER_6"
    if months <= 24:
        return "FROM_6_TO_24"
    return "OVER_24"


def _volume_bucket(volume_minor: int) -> str:
    if volume_minor < 10_000_000:
        return "LOW"
    if volume_minor < 50_000_000:
        return "MEDIUM"
    if volume_minor < 200_000_000:
        return "HIGH"
    return "VERY_HIGH"


def _country_risk(country_code: str, high_risk: set[str]) -> str:
    code = (country_code or "").upper()
    if code in high_risk:
        return "HIGH"
    if code and code != "PRY":
        return "MEDIUM"
    return "LOW"


def score_profile(profile: CustomerProfile, high_risk_countries: set[str] | None = None) -> KycResult:
    high_risk = high_risk_countries or set()
    country_risk = _country_risk(profile.country_code, high_risk)
    tenure = _tenure_months(profile.created_at, date.today())
    tenure_bucket = _tenure_bucket(tenure)
    volume_bucket = _volume_bucket(profile.expected_monthly_volume_minor)

    factors: dict[str, dict[str, Any]] = {
        "customer_type": {
            "value": profile.customer_type,
            "points": config.KYC_WEIGHTS["customer_type"].get(profile.customer_type, 0),
        },
        "segment": {
            "value": profile.segment,
            "points": config.KYC_WEIGHTS["segment"].get(profile.segment, 0),
        },
        "country_risk": {
            "value": country_risk,
            "points": config.KYC_WEIGHTS["country_risk"][country_risk],
        },
        "activity_risk": {
            "value": profile.activity_risk,
            "points": config.KYC_WEIGHTS["activity_risk"].get(profile.activity_risk, 0),
        },
        "channel": {
            "value": profile.channel,
            "points": config.KYC_WEIGHTS["channel"].get(profile.channel, 0),
        },
        "pep": {
            "value": profile.is_pep,
            "points": config.KYC_WEIGHTS["pep"] if profile.is_pep else 0,
        },
        "ubo": {
            "value": "IDENTIFIED" if profile.ubo_identified else "MISSING",
            "points": 0 if profile.ubo_identified else config.KYC_WEIGHTS["ubo_missing"],
        },
        "source_of_funds": {
            "value": "VERIFIED" if profile.source_of_funds_verified else "UNVERIFIED",
            "points": 0 if profile.source_of_funds_verified else config.KYC_WEIGHTS["sof_unverified"],
        },
        "negative_news": {
            "value": profile.negative_news,
            "points": config.KYC_WEIGHTS["negative_news"] if profile.negative_news else 0,
        },
        "product_complexity": {
            "value": profile.product_complexity,
            "points": config.KYC_WEIGHTS["product_complexity"].get(profile.product_complexity, 0),
        },
        "volume": {
            "value": volume_bucket,
            "points": config.KYC_WEIGHTS["volume"][volume_bucket],
        },
        "tenure": {
            "value": tenure_bucket,
            "points": config.KYC_WEIGHTS["tenure"][tenure_bucket],
        },
    }

    score = min(100, sum(item["points"] for item in factors.values()))
    if score <= config.KYC_LOW_MAX:
        category = "LOW"
    elif score <= config.KYC_MEDIUM_MAX:
        category = "MEDIUM"
    else:
        category = "HIGH"

    edd_reasons: list[str] = []
    if category == "HIGH":
        edd_reasons.append("Clasificación de riesgo alto")
    if profile.is_pep:
        edd_reasons.append("Persona expuesta políticamente")
    if country_risk == "HIGH":
        edd_reasons.append("Jurisdicción de alto riesgo")
    if not profile.ubo_identified:
        edd_reasons.append("Beneficiario final no identificado")
    if not profile.source_of_funds_verified:
        edd_reasons.append("Origen de fondos no verificado")
    if profile.negative_news:
        edd_reasons.append("Noticias negativas")

    return KycResult(
        customer_id=profile.customer_id,
        score=score,
        risk_category=category,
        requires_edd=bool(edd_reasons),
        factors=factors,
        edd_reasons=edd_reasons,
    )


def _profile_from_row(row: sqlite3.Row) -> CustomerProfile:
    return CustomerProfile(
        customer_id=row["customer_id"],
        customer_type=row["customer_type"],
        segment=row["segment"],
        country_code=row["country_code"],
        created_at=row["created_at"],
        activity_risk=row["activity_risk"] or "LOW",
        is_pep=bool(row["is_pep"]),
        ubo_identified=bool(row["beneficial_owner_identified"]),
        source_of_funds_verified=bool(row["source_of_funds_verified"]),
        negative_news=bool(row["negative_news"]),
        channel=row["onboarding_channel"] or "BRANCH",
        product_complexity=row["product_complexity"] or "BASIC",
        expected_monthly_volume_minor=row["expected_monthly_volume_minor"] or 0,
    )


def score_customer_from_db(
    conn: sqlite3.Connection,
    customer_id: str,
    high_risk_countries: set[str] | None = None,
) -> KycResult | None:
    row = conn.execute(
        """
        SELECT c.customer_id, c.customer_type, c.segment, c.country_code, c.created_at,
               COALESCE(p.activity_risk, 'LOW') AS activity_risk,
               COALESCE(p.is_pep, 0) AS is_pep,
               COALESCE(p.beneficial_owner_identified, 1) AS beneficial_owner_identified,
               COALESCE(p.source_of_funds_verified, 1) AS source_of_funds_verified,
               COALESCE(p.negative_news, 0) AS negative_news,
               COALESCE(p.onboarding_channel, 'BRANCH') AS onboarding_channel,
               COALESCE(p.product_complexity, 'BASIC') AS product_complexity,
               COALESCE(p.expected_monthly_volume_minor, 0) AS expected_monthly_volume_minor
        FROM customers c
        LEFT JOIN aml_customer_profile p ON p.customer_id = c.customer_id
        WHERE c.customer_id = ?
        """,
        (customer_id,),
    ).fetchone()
    if row is None:
        return None
    high_risk = high_risk_countries if high_risk_countries is not None else high_risk_country_codes(conn)
    return score_profile(_profile_from_row(row), high_risk)


def score_all_customers(conn: sqlite3.Connection, as_of: datetime | None = None) -> int:
    del as_of
    high_risk = high_risk_country_codes(conn)
    rows = conn.execute(
        """
        SELECT c.customer_id, c.customer_type, c.segment, c.country_code, c.created_at,
               COALESCE(p.activity_risk, 'LOW') AS activity_risk,
               COALESCE(p.is_pep, 0) AS is_pep,
               COALESCE(p.beneficial_owner_identified, 1) AS beneficial_owner_identified,
               COALESCE(p.source_of_funds_verified, 1) AS source_of_funds_verified,
               COALESCE(p.negative_news, 0) AS negative_news,
               COALESCE(p.onboarding_channel, 'BRANCH') AS onboarding_channel,
               COALESCE(p.product_complexity, 'BASIC') AS product_complexity,
               COALESCE(p.expected_monthly_volume_minor, 0) AS expected_monthly_volume_minor
        FROM customers c
        LEFT JOIN aml_customer_profile p ON p.customer_id = c.customer_id
        ORDER BY c.customer_id
        """
    ).fetchall()
    timestamp = utcnow()
    payload = []
    for row in rows:
        result = score_profile(_profile_from_row(row), high_risk)
        payload.append(
            (
                result.customer_id,
                result.score,
                result.risk_category,
                int(result.requires_edd),
                json.dumps(result.as_dict(), ensure_ascii=False, sort_keys=True),
                timestamp,
            )
        )
    conn.executemany(
        """
        INSERT OR REPLACE INTO aml_kyc_scores
            (customer_id, score, risk_category, requires_edd, factors_json, calculated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        payload,
    )
    conn.commit()
    return len(payload)


def kyc_score_for_customer(conn: sqlite3.Connection, customer_id: str) -> tuple[int, str]:
    row = conn.execute(
        "SELECT score, risk_category FROM aml_kyc_scores WHERE customer_id = ?",
        (customer_id,),
    ).fetchone()
    if row is not None:
        return int(row["score"]), row["risk_category"]
    result = score_customer_from_db(conn, customer_id)
    if result is None:
        return 0, "LOW"
    return result.score, result.risk_category


__all__ = [
    "CustomerProfile",
    "KycResult",
    "kyc_score_for_customer",
    "score_all_customers",
    "score_customer_from_db",
    "score_profile",
]
