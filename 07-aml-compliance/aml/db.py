"""Acceso a SQLite y carga de datos de referencia AML."""

from __future__ import annotations

import csv
import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import config


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def connect(db_path: Path | str) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        conn.execute("PRAGMA journal_mode = WAL")
    except sqlite3.DatabaseError:
        pass
    return conn


def apply_schema(conn: sqlite3.Connection) -> None:
    schema = (config.BASE_DIR / "schema_aml.sql").read_text(encoding="utf-8")
    conn.executescript(schema)


def seed_high_risk_countries(conn: sqlite3.Connection) -> int:
    rows = list(csv.DictReader(config.HIGH_RISK_COUNTRIES_CSV.open(encoding="utf-8", newline="")))
    conn.executemany(
        """
        INSERT OR REPLACE INTO aml_high_risk_countries
            (country_code, country_name, source, is_active)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                row["country_code"].strip().upper(),
                row["country_name"].strip(),
                row["source"].strip(),
                int(row["is_active"]),
            )
            for row in rows
        ],
    )
    conn.commit()
    return len(rows)


def seed_watchlist(conn: sqlite3.Connection) -> int:
    rows = list(csv.DictReader(config.WATCHLIST_CSV.open(encoding="utf-8", newline="")))
    conn.executemany(
        """
        INSERT OR REPLACE INTO aml_watchlist
            (list_type, list_id, name, aliases, country_code, date_of_birth,
             program, is_active, is_fictitious)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                row["list_type"].strip().upper(),
                row["list_id"].strip(),
                row["name"].strip(),
                (row.get("aliases") or "").strip() or None,
                (row.get("country_code") or "").strip().upper() or None,
                (row.get("date_of_birth") or "").strip() or None,
                (row.get("program") or "").strip() or None,
                int(row["is_active"]),
                int(row["is_fictitious"]),
            )
            for row in rows
        ],
    )
    conn.commit()
    return len(rows)


def seed_rule_params(conn: sqlite3.Connection, params: dict[str, dict[str, Any]] | None = None) -> int:
    params = params or config.load_rule_params()
    timestamp = utcnow()
    rows: list[tuple[Any, ...]] = []
    for rule_id, values in params.items():
        for name, value in values.items():
            if isinstance(value, bool):
                value_type = "INTEGER"
                stored = int(value)
            elif isinstance(value, int):
                value_type = "INTEGER"
                stored = value
            elif isinstance(value, float):
                value_type = "REAL"
                stored = value
            else:
                value_type = "TEXT"
                stored = str(value)
            rows.append((rule_id, name, str(stored), value_type, "Parámetro calibrado del caso", timestamp))
    conn.executemany(
        """
        INSERT OR REPLACE INTO aml_rule_params
            (rule_id, param_name, param_value, value_type, description, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    return len(rows)


def _digest(customer_id: str) -> int:
    return int(hashlib.sha256(customer_id.encode("utf-8")).hexdigest(), 16)


def _expected_volume(segment: str) -> int:
    return {
        "RETAIL": 5_000_000,
        "PREMIUM": 20_000_000,
        "SME": 80_000_000,
        "CORPORATE": 300_000_000,
    }.get(segment, 5_000_000)


def seed_customer_profiles(conn: sqlite3.Connection) -> int:
    existing = {
        row["customer_id"]
        for row in conn.execute("SELECT customer_id FROM aml_customer_profile")
    }
    customers = conn.execute(
        "SELECT customer_id, customer_type, segment, country_code FROM customers ORDER BY customer_id"
    ).fetchall()
    timestamp = utcnow()
    rows: list[tuple[Any, ...]] = []
    for customer in customers:
        customer_id = customer["customer_id"]
        if customer_id in existing:
            continue
        digest = _digest(customer_id)
        segment = customer["segment"]
        is_business = customer["customer_type"] == "BUSINESS"
        is_pep = 1 if digest % 37 == 0 else 0
        activity_risk = "MEDIUM" if segment == "CORPORATE" else ("MEDIUM" if digest % 10 >= 6 else "LOW")
        if digest % 10 == 9:
            activity_risk = "HIGH"
        if is_business:
            ubo_identified = 0 if digest % 5 == 0 else 1
        else:
            ubo_identified = 1
        source_verified = 0 if digest % 7 == 0 else 1
        negative_news = 1 if digest % 53 == 0 else 0
        channel = ("BRANCH", "WEB", "MOBILE", "API")[digest % 4]
        if segment in {"SME", "CORPORATE"}:
            complexity = "COMPLEX" if digest % 3 == 0 else "MEDIUM"
        else:
            complexity = "MEDIUM" if digest % 4 == 0 else "BASIC"
        occupation = (
            "Comercio minorista",
            "Servicios profesionales",
            "Construcción",
            "Tecnología",
            "Agricultura",
            "Transporte",
        )[digest % 6]
        pep_type = None
        if is_pep:
            pep_type = "NACIONAL" if customer["country_code"] == "PRY" else "EXTRANJERO"
        rows.append(
            (
                customer_id,
                occupation,
                activity_risk,
                is_pep,
                pep_type,
                ubo_identified,
                source_verified,
                negative_news,
                channel,
                complexity,
                _expected_volume(segment),
                timestamp,
            )
        )
    conn.executemany(
        """
        INSERT INTO aml_customer_profile
            (customer_id, occupation, activity_risk, is_pep, pep_type,
             beneficial_owner_identified, source_of_funds_verified, negative_news,
             onboarding_channel, product_complexity, expected_monthly_volume_minor, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    return len(rows)


def high_risk_country_codes(conn: sqlite3.Connection) -> set[str]:
    return {
        row["country_code"]
        for row in conn.execute(
            "SELECT country_code FROM aml_high_risk_countries WHERE is_active = 1"
        )
    }


def initialize_aml(db_path: Path | str) -> dict[str, int]:
    conn = connect(db_path)
    try:
        apply_schema(conn)
        countries = seed_high_risk_countries(conn)
        watchlist = seed_watchlist(conn)
        profiles = seed_customer_profiles(conn)
        params = seed_rule_params(conn)
        from .kyc import score_all_customers

        scores = score_all_customers(conn)
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        return {
            "countries": countries,
            "watchlist": watchlist,
            "profiles": profiles,
            "rule_params": params,
            "kyc_scores": scores,
        }
    finally:
        conn.close()


def account_customer(conn: sqlite3.Connection, account_id: str) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT a.account_id, a.customer_id, a.currency, a.status, a.balance_minor,
               c.customer_type, c.first_name, c.last_name, c.business_name,
               c.country_code, c.segment, c.risk_rating, c.kyc_status
        FROM accounts a
        JOIN customers c ON c.customer_id = a.customer_id
        WHERE a.account_id = ?
        """,
        (account_id,),
    ).fetchone()


__all__ = [
    "account_customer",
    "apply_schema",
    "connect",
    "high_risk_country_codes",
    "initialize_aml",
    "seed_customer_profiles",
    "seed_high_risk_countries",
    "seed_rule_params",
    "seed_watchlist",
    "utcnow",
]
