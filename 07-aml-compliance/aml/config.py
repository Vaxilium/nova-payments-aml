"""Configuración y parámetros del motor AML de Fase 5."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
AML_DIR = BASE_DIR.parent
REPO_ROOT = AML_DIR.parent
DATA_DIR = AML_DIR / "data"
SQL_DIR = AML_DIR / "sql"
RULES_DIR = SQL_DIR / "rules"
DOCS_DIR = AML_DIR / "docs"
DEFAULT_DB = REPO_ROOT / "05-core-middleware" / "db" / "novabank.db"

WATCHLIST_CSV = DATA_DIR / "lista_sanciones_pep.csv"
HIGH_RISK_COUNTRIES_CSV = DATA_DIR / "high_risk_countries.csv"
RULE_PARAMS_JSON = DATA_DIR / "rule_params.json"

KYC_LOW_MAX = 39
KYC_MEDIUM_MAX = 69

SCREENING_AUTO_BLOCK = 0.95
SCREENING_MANUAL_REVIEW = 0.88
SCREENING_MINIMUM = 0.80

SLA = {
    "P1": {"assignment_minutes": 15, "closure_business_days": 10},
    "P2": {"assignment_minutes": 240, "closure_business_days": 15},
    "P3": {"assignment_minutes": 1440, "closure_business_days": 20},
}

ANALYSTS = ("analista_aml_1", "analista_aml_2", "analista_aml_3")

RULE_META: dict[str, dict[str, Any]] = {
    "R01": {
        "name": "Estructuración por debajo del umbral",
        "intended_pattern": "STRUCTURING",
        "base_score": 80,
        "severity": "HIGH",
        "sql": "R01_structuring.sql",
    },
    "R02": {
        "name": "Velocidad transaccional por cantidad",
        "intended_pattern": "HIGH_VELOCITY",
        "base_score": 78,
        "severity": "HIGH",
        "sql": "R02_velocity_count.sql",
    },
    "R03": {
        "name": "Velocidad transaccional por monto",
        "intended_pattern": "HIGH_VELOCITY",
        "base_score": 62,
        "severity": "MEDIUM",
        "sql": "R03_velocity_amount.sql",
    },
    "R04": {
        "name": "Cuenta de paso (entrada y salida rápida)",
        "intended_pattern": "PASS_THROUGH",
        "base_score": 85,
        "severity": "HIGH",
        "sql": "R04_pass_through.sql",
    },
    "R05": {
        "name": "Depósitos redondos reiterados",
        "intended_pattern": "ROUND_MULE",
        "base_score": 70,
        "severity": "MEDIUM",
        "sql": "R05_round_deposits.sql",
    },
    "R06": {
        "name": "Reactivación de cuenta inactiva",
        "intended_pattern": "DORMANT_ACTIVATION",
        "base_score": 66,
        "severity": "MEDIUM",
        "sql": "R06_dormant_activation.sql",
    },
    "R07": {
        "name": "Jurisdicción de alto riesgo",
        "intended_pattern": None,
        "base_score": 92,
        "severity": "CRITICAL",
        "sql": "R07_high_risk_geography.sql",
    },
    "R08": {
        "name": "Importe atípico frente al perfil",
        "intended_pattern": None,
        "base_score": 58,
        "severity": "MEDIUM",
        "sql": "R08_profile_deviation.sql",
    },
    "R09": {
        "name": "Cambio abrupto de comportamiento",
        "intended_pattern": None,
        "base_score": 64,
        "severity": "MEDIUM",
        "sql": "R09_behavior_change.sql",
    },
    "R10": {
        "name": "Transferencias circulares",
        "intended_pattern": None,
        "base_score": 88,
        "severity": "HIGH",
        "sql": "R10_circular_funds.sql",
    },
    "R11": {
        "name": "Concentración de contraparte",
        "intended_pattern": None,
        "base_score": 60,
        "severity": "MEDIUM",
        "sql": "R11_counterparty_concentration.sql",
    },
    "R12": {
        "name": "Fan-in de múltiples remitentes",
        "intended_pattern": None,
        "base_score": 76,
        "severity": "HIGH",
        "sql": "R12_fan_in.sql",
    },
}

KYC_WEIGHTS: dict[str, dict[str, int]] = {
    "customer_type": {"INDIVIDUAL": 4, "BUSINESS": 8},
    "segment": {"RETAIL": 4, "PREMIUM": 6, "SME": 8, "CORPORATE": 10},
    "country_risk": {"LOW": 0, "MEDIUM": 8, "HIGH": 20},
    "activity_risk": {"LOW": 0, "MEDIUM": 8, "HIGH": 15},
    "channel": {"BRANCH": 0, "WEB": 2, "MOBILE": 4, "API": 6},
    "pep": 35,
    "ubo_missing": 10,
    "sof_unverified": 8,
    "negative_news": 10,
    "product_complexity": {"BASIC": 0, "MEDIUM": 4, "COMPLEX": 8},
    "volume": {"LOW": 0, "MEDIUM": 3, "HIGH": 6, "VERY_HIGH": 8},
    "tenure": {"OVER_24": 0, "FROM_6_TO_24": 2, "UNDER_6": 4},
}


def load_rule_params(overrides: dict[str, dict[str, Any]] | None = None) -> dict[str, dict[str, Any]]:
    params = json.loads(RULE_PARAMS_JSON.read_text(encoding="utf-8"))
    if overrides:
        for rule_id, values in overrides.items():
            params.setdefault(rule_id, {}).update(values)
    return params


def priority_for_score(score: int) -> str:
    if score >= 80:
        return "P1"
    if score >= 50:
        return "P2"
    return "P3"


