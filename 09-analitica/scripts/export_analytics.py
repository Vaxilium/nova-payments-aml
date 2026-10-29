"""Exporta el dataset analítico de NovaBank desde SQLite a CSV.

El script trabaja sobre una copia en memoria de la base del core para no
modificar el entorno de la Fase 5. Genera dimensiones, hechos, un resumen
diario y un reporte de exportación.

Uso:
    python 09-analitica/scripts/export_analytics.py
    python 09-analitica/scripts/export_analytics.py --db ruta/novabank.db --out ruta/data
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable

ANALYTICS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = ANALYTICS_DIR.parent
AML_DIR = REPO_ROOT / "07-aml-compliance"
if str(AML_DIR) not in sys.path:
    sys.path.insert(0, str(AML_DIR))

from aml import config as aml_config  # noqa: E402
from aml.alerts import create_alerts  # noqa: E402
from aml.db import (  # noqa: E402
    apply_schema,
    seed_customer_profiles,
    seed_high_risk_countries,
    seed_rule_params,
    seed_watchlist,
)
from aml.kyc import score_all_customers  # noqa: E402
from aml.rules import run_all_rules  # noqa: E402
from aml.workflow import add_business_days  # noqa: E402

DEFAULT_DB = REPO_ROOT / "05-core-middleware" / "db" / "novabank.db"
DEFAULT_OUT = ANALYTICS_DIR / "data"
REFERENCE_DATE = date(2026, 10, 1)

ALERT_STATUSES = (
    "CERRADA_FALSO_POSITIVO",
    "EN_ANALISIS",
    "ESCALADA",
    "REPORTADA",
    "NUEVA",
)


def _hash_int(value: str) -> int:
    return int(hashlib.sha256(value.encode("utf-8")).hexdigest(), 16)


def _money(minor: int | None, currency: str) -> str:
    if minor is None:
        return ""
    if currency in {"PYG"}:
        return str(int(minor))
    return f"{minor / 100:.2f}"


def _iso(value: str | None) -> str:
    return (value or "")[:19]


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _write_csv(path: Path, header: list[str], rows: Iterable[Iterable[Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
            count += 1
    return count


def _copy_to_memory(source_path: Path) -> sqlite3.Connection:
    source = sqlite3.connect(str(source_path))
    target = sqlite3.connect(":memory:")
    target.row_factory = sqlite3.Row
    source.backup(target)
    source.close()
    target.execute("PRAGMA foreign_keys = ON")
    return target


def _ensure_aml(conn: sqlite3.Connection) -> None:
    exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'aml_alerts'"
    ).fetchone()
    if exists is None:
        apply_schema(conn)
        seed_high_risk_countries(conn)
        seed_watchlist(conn)
        seed_customer_profiles(conn)
        seed_rule_params(conn)
        score_all_customers(conn)
    else:
        conn.execute("DELETE FROM aml_case_alerts")
        conn.execute("DELETE FROM aml_workflow_transitions")
        conn.execute("DELETE FROM aml_alerts")
        conn.execute("DELETE FROM aml_cases")
        conn.commit()


def _simulate_lifecycle(conn: sqlite3.Connection) -> dict[str, int]:
    """Asigna un ciclo de vida determinístico a las alertas para la analítica."""
    rows = conn.execute("SELECT * FROM aml_alerts ORDER BY alert_id").fetchall()
    closed = 0
    assigned = 0
    for row in rows:
        seed = _hash_int(f"alert:{row['alert_id']}")
        bucket = seed % 100
        if bucket < 38:
            status = "CERRADA_FALSO_POSITIVO"
        elif bucket < 55:
            status = "EN_ANALISIS"
        elif bucket < 68:
            status = "ESCALADA"
        elif bucket < 78:
            status = "REPORTADA"
        else:
            status = "NUEVA"

        base = _parse(row["last_seen_at"]) + timedelta(minutes=2 + seed % 20)
        analyst = None if status == "NUEVA" else aml_config.ANALYSTS[seed % len(aml_config.ANALYSTS)]
        assignment_minutes = None
        assigned_at = None
        due_at = None
        closed_at = None
        closure_notes = None
        if analyst:
            assigned += 1
            sla_minutes = int(aml_config.SLA[row["priority"]]["assignment_minutes"])
            if row["priority"] == "P1":
                assignment_minutes = (2 + seed % 13) if seed % 100 < 86 else (20 + seed % 70)
            elif row["priority"] == "P2":
                assignment_minutes = (10 + seed % 210) if seed % 100 < 90 else (250 + seed % 300)
            else:
                assignment_minutes = (60 + seed % 1200) if seed % 100 < 92 else (1500 + seed % 600)
            assigned_at = base + timedelta(minutes=assignment_minutes)
            due_at = base + timedelta(minutes=sla_minutes)
        if status in {"CERRADA_FALSO_POSITIVO"}:
            closed += 1
            closure_days = int(aml_config.SLA[row["priority"]]["closure_business_days"])
            closed_at = add_business_days(assigned_at or base, 1 + seed % max(1, closure_days - 1))
            closure_notes = "Cierre analítico sintético: actividad consistente con el perfil."
        conn.execute(
            """
            UPDATE aml_alerts
               SET status = ?, assigned_to = ?, assigned_at = ?, due_at = ?,
                   closed_at = ?, closure_notes = ?, created_at = ?, updated_at = ?
             WHERE alert_id = ?
            """,
            (
                status,
                analyst,
                assigned_at.isoformat() if assigned_at else None,
                due_at.isoformat() if due_at else None,
                closed_at.isoformat() if closed_at else None,
                closure_notes,
                base.isoformat(),
                (closed_at or assigned_at or base).isoformat(),
                row["alert_id"],
            ),
        )
    conn.commit()
    return {"alerts": len(rows), "assigned": assigned, "closed_fp": closed}


def _simulate_cases(conn: sqlite3.Connection) -> int:
    alerts = conn.execute(
        """
        SELECT a.*, c.first_name, c.last_name, c.business_name
          FROM aml_alerts a
          LEFT JOIN customers c ON c.customer_id = a.customer_id
         ORDER BY a.alert_id
        """
    ).fetchall()
    groups: dict[str, list[sqlite3.Row]] = defaultdict(list)
    for alert in alerts:
        if alert["customer_id"]:
            groups[alert["customer_id"]].append(alert)

    order = {"P1": 1, "P2": 2, "P3": 3}
    case_count = 0
    for customer_id, group in groups.items():
        statuses = {row["status"] for row in group}
        if "REPORTADA" in statuses:
            case_status = "REPORTADO"
        elif "ESCALADA" in statuses:
            case_status = "ESCALADO"
        elif statuses == {"CERRADA_FALSO_POSITIVO"}:
            case_status = "CERRADO"
        elif "EN_ANALISIS" in statuses:
            case_status = "EN_ANALISIS"
        else:
            case_status = "ABIERTO"
        priority = min((row["priority"] for row in group), key=lambda value: order.get(value, 9))
        risk_score = max(int(row["risk_score"]) for row in group)
        opened_at = min(_parse(row["created_at"]) for row in group)
        seed = _hash_int(f"case:{customer_id}")
        analyst = aml_config.ANALYSTS[seed % len(aml_config.ANALYSTS)]
        closure_days = int(aml_config.SLA[priority]["closure_business_days"])
        due_at = add_business_days(opened_at, closure_days)
        closed_at = None
        closure_notes = None
        if case_status in {"CERRADO", "REPORTADO"}:
            closed_at = add_business_days(opened_at, 1 + seed % max(1, closure_days - 1))
            closure_notes = "Cierre analítico sintético del caso."
        title = f"Caso AML · {group[0]['alert_type']}"
        cursor = conn.execute(
            """
            INSERT INTO aml_cases
                (customer_id, title, status, priority, risk_score, opened_at,
                 assigned_to, due_at, closed_at, closure_notes, created_at,
                 updated_at, ros_reported)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                customer_id,
                title,
                case_status,
                priority,
                risk_score,
                opened_at.isoformat(),
                analyst,
                due_at.isoformat(),
                closed_at.isoformat() if closed_at else None,
                closure_notes,
                opened_at.isoformat(),
                (closed_at or opened_at).isoformat(),
                1 if case_status == "REPORTADO" else 0,
            ),
        )
        case_id = int(cursor.lastrowid)
        for alert in group:
            conn.execute(
                "INSERT OR IGNORE INTO aml_case_alerts (case_id, alert_id) VALUES (?, ?)",
                (case_id, alert["alert_id"]),
            )
            conn.execute(
                "UPDATE aml_alerts SET case_id = ? WHERE alert_id = ?",
                (case_id, alert["alert_id"]),
            )
        case_count += 1
    conn.commit()
    return case_count


def _date_dimension(start: str, end: str) -> list[list[Any]]:
    current = date.fromisoformat(start[:10])
    final = date.fromisoformat(end[:10])
    rows: list[list[Any]] = []
    while current <= final:
        iso = current.isoformat()
        rows.append(
            [
                iso,
                current.year,
                (current.month - 1) // 3 + 1,
                current.month,
                current.strftime("%Y-%m"),
                current.isocalendar().week,
                current.weekday() + 1,
                current.strftime("%A"),
                1 if current.weekday() >= 5 else 0,
            ]
        )
        current += timedelta(days=1)
    return rows


def _export_dimensions(conn: sqlite3.Connection, out: Path) -> dict[str, int]:
    min_date, max_date = conn.execute(
        "SELECT MIN(value_date), MAX(value_date) FROM transactions"
    ).fetchone()
    date_rows = _date_dimension(min_date, max_date)
    counts = {
        "dim_date": _write_csv(
            out / "dim_date.csv",
            ["date_key", "year", "quarter", "month", "year_month", "week", "weekday", "weekday_name", "is_weekend"],
            date_rows,
        )
    }

    customer_rows = conn.execute(
        """
        SELECT c.customer_id, c.customer_type,
               COALESCE(c.business_name, c.first_name || ' ' || c.last_name) AS display_name,
               c.document_type, c.country_code, c.city, c.segment, c.risk_rating,
               c.kyc_status, c.is_active, c.created_at,
               k.score AS kyc_score, k.risk_category, k.requires_edd,
               p.is_pep, p.occupation, p.activity_risk, p.onboarding_channel,
               p.product_complexity, p.expected_monthly_volume_minor
          FROM customers c
          LEFT JOIN aml_kyc_scores k ON k.customer_id = c.customer_id
          LEFT JOIN aml_customer_profile p ON p.customer_id = c.customer_id
         ORDER BY c.customer_id
        """
    ).fetchall()
    counts["dim_customer"] = _write_csv(
        out / "dim_customer.csv",
        [
            "customer_id", "customer_type", "display_name", "document_type", "country_code",
            "city", "segment", "risk_rating", "kyc_status", "is_active", "created_at",
            "kyc_score", "risk_category", "requires_edd", "is_pep", "occupation",
            "activity_risk", "onboarding_channel", "product_complexity",
            "expected_monthly_volume_minor",
        ],
        [
            [
                row["customer_id"], row["customer_type"], row["display_name"],
                row["document_type"], row["country_code"], row["city"], row["segment"],
                row["risk_rating"], row["kyc_status"], row["is_active"], row["created_at"],
                row["kyc_score"], row["risk_category"], row["requires_edd"], row["is_pep"],
                row["occupation"], row["activity_risk"], row["onboarding_channel"],
                row["product_complexity"], row["expected_monthly_volume_minor"],
            ]
            for row in customer_rows
        ],
    )

    account_rows = conn.execute(
        """
        SELECT a.account_id, a.customer_id, a.account_number, a.account_type,
               a.currency, a.status, a.balance_minor, a.opened_at,
               c.segment, c.risk_rating, k.score AS kyc_score
          FROM accounts a
          JOIN customers c ON c.customer_id = a.customer_id
          LEFT JOIN aml_kyc_scores k ON k.customer_id = a.customer_id
         ORDER BY a.account_id
        """
    ).fetchall()
    counts["dim_account"] = _write_csv(
        out / "dim_account.csv",
        [
            "account_id", "customer_id", "account_number", "account_type", "currency",
            "status", "balance", "opened_at", "segment", "risk_rating", "kyc_score",
        ],
        [
            [
                row["account_id"], row["customer_id"], row["account_number"], row["account_type"],
                row["currency"], row["status"], _money(row["balance_minor"], row["currency"]),
                row["opened_at"], row["segment"], row["risk_rating"], row["kyc_score"],
            ]
            for row in account_rows
        ],
    )

    rule_rows = []
    for rule_id, meta in aml_config.RULE_META.items():
        intended = meta.get("intended_pattern") or "GENERAL"
        rule_rows.append([rule_id, meta["name"], meta["severity"], meta["base_score"], intended])
    counts["dim_rule"] = _write_csv(
        out / "dim_rule.csv",
        ["rule_id", "rule_name", "severity", "base_score", "intended_pattern"],
        rule_rows,
    )

    priority_rows = [
        [priority, values["assignment_minutes"], values["closure_business_days"]]
        for priority, values in aml_config.SLA.items()
    ]
    counts["dim_priority"] = _write_csv(
        out / "dim_priority.csv",
        ["priority", "assignment_sla_minutes", "closure_sla_business_days"],
        priority_rows,
    )

    currency_rows = [
        ["PYG", "Guaraní paraguayo", 0],
        ["USD", "Dólar estadounidense", 2],
        ["EUR", "Euro", 2],
    ]
    counts["dim_currency"] = _write_csv(
        out / "dim_currency.csv",
        ["currency", "name", "minor_unit"],
        currency_rows,
    )
    return counts


def _export_facts(conn: sqlite3.Connection, out: Path) -> dict[str, int]:
    truth = {
        row["transaction_id"]: (row["label"], row["pattern_type"])
        for row in conn.execute("SELECT transaction_id, label, pattern_type FROM _aml_ground_truth")
    }
    alert_by_tx = {
        row["transaction_id"]: row["alert_id"]
        for row in conn.execute(
            "SELECT transaction_id, MIN(alert_id) AS alert_id FROM aml_alerts WHERE transaction_id IS NOT NULL GROUP BY transaction_id"
        )
    }
    tx_rows = conn.execute(
        """
        SELECT t.transaction_id, t.created_at, t.value_date, t.transaction_type, t.status,
               t.currency, t.amount_minor, t.fee_minor, t.channel,
               t.debit_account_id, t.credit_account_id,
               COALESCE(da.customer_id, ca.customer_id) AS customer_id,
               c.segment, c.risk_rating, k.score AS kyc_score
          FROM transactions t
          LEFT JOIN accounts da ON da.account_id = t.debit_account_id
          LEFT JOIN accounts ca ON ca.account_id = t.credit_account_id
          LEFT JOIN customers c ON c.customer_id = COALESCE(da.customer_id, ca.customer_id)
          LEFT JOIN aml_kyc_scores k ON k.customer_id = COALESCE(da.customer_id, ca.customer_id)
         ORDER BY t.transaction_id
        """
    ).fetchall()

    tx_fact: list[list[Any]] = []
    sla_fact: list[list[Any]] = []
    for row in tx_rows:
        tx_id = row["transaction_id"]
        label, pattern = truth.get(tx_id, (None, None))
        alert_id = alert_by_tx.get(tx_id)
        is_stp = 1 if row["status"] == "POSTED" and alert_id is None else 0
        scope = "LOCAL" if row["currency"] == "PYG" else "INTERNATIONAL"
        latency_ms = ""
        within_sla = ""
        if row["transaction_type"] == "TRANSFER" and row["currency"] == "PYG":
            seed = _hash_int(f"sla:{tx_id}")
            if seed % 100 < 5:
                latency_ms = 5400 + seed % 6600
            else:
                latency_ms = 280 + seed % 4520
            within_sla = 1 if int(latency_ms) <= 5000 else 0
            sla_fact.append(
                [
                    tx_id, row["value_date"], row["customer_id"], row["segment"],
                    row["channel"], _money(row["amount_minor"], row["currency"]),
                    latency_ms, within_sla,
                ]
            )
        tx_fact.append(
            [
                tx_id, row["value_date"], _iso(row["created_at"]), row["transaction_type"],
                row["status"], row["currency"], _money(row["amount_minor"], row["currency"]),
                _money(row["fee_minor"], row["currency"]), row["channel"],
                row["debit_account_id"] or "", row["credit_account_id"] or "",
                row["customer_id"] or "", row["segment"] or "", row["risk_rating"] or "",
                row["kyc_score"] or "", scope,
                label or "", pattern or "", alert_id or "", is_stp,
            ]
        )

    counts = {
        "fact_transactions": _write_csv(
            out / "fact_transactions.csv",
            [
                "transaction_id", "date_key", "created_at", "transaction_type", "status",
                "currency", "amount", "fee", "channel", "debit_account_id",
                "credit_account_id", "customer_id", "segment", "risk_rating", "kyc_score",
                "payment_scope", "truth_label", "truth_pattern", "alert_id", "is_stp",
            ],
            tx_fact,
        ),
        "fact_payment_sla": _write_csv(
            out / "fact_payment_sla.csv",
            ["transaction_id", "date_key", "customer_id", "segment", "channel", "amount", "latency_ms", "within_sla"],
            sla_fact,
        ),
    }

    rule_map = {rule_id: meta for rule_id, meta in aml_config.RULE_META.items()}
    alert_rows = conn.execute(
        """
        SELECT a.*, substr(a.last_seen_at, 1, 10) AS alert_date,
               c.segment, c.risk_rating, k.score AS kyc_score
          FROM aml_alerts a
          LEFT JOIN customers c ON c.customer_id = a.customer_id
          LEFT JOIN aml_kyc_scores k ON k.customer_id = a.customer_id
         ORDER BY a.alert_id
        """
    ).fetchall()

    alert_fact: list[list[Any]] = []
    for row in alert_rows:
        meta = rule_map.get(row["rule_id"], {})
        rule_name = meta.get("name", "")
        severity = meta.get("severity", "")
        assignment_minutes = ""
        if row["assigned_at"] and row["created_at"]:
            assignment_minutes = int((_parse(row["assigned_at"]) - _parse(row["created_at"])).total_seconds() // 60)
        is_fp = 1 if row["status"] == "CERRADA_FALSO_POSITIVO" else 0
        is_closed = 1 if row["status"] in {"CERRADA_FALSO_POSITIVO", "REPORTADA"} else 0
        is_escalated = 1 if row["status"] in {"ESCALADA", "REPORTADA"} or row["case_id"] else 0
        alert_fact.append(
            [
                row["alert_id"], row["alert_date"], _iso(row["created_at"]), row["alert_type"],
                row["rule_id"], rule_name, severity, row["priority"], row["risk_score"],
                row["status"], row["transaction_count"], row["customer_id"] or "",
                row["account_id"] or "", row["transaction_id"] or "",
                row["assigned_to"] or "", _iso(row["assigned_at"]), assignment_minutes,
                _iso(row["due_at"]), _iso(row["closed_at"]), row["closure_notes"] or "",
                row["case_id"] or "", row["segment"] or "", row["risk_rating"] or "",
                row["kyc_score"] or "", is_fp, is_closed, is_escalated,
            ]
        )
    counts["fact_alerts"] = _write_csv(
        out / "fact_alerts.csv",
        [
            "alert_id", "date_key", "created_at", "alert_type", "rule_id", "rule_name",
            "severity", "priority", "risk_score", "status", "transaction_count",
            "customer_id", "account_id", "transaction_id", "assigned_to", "assigned_at",
            "assignment_minutes", "due_at", "closed_at", "closure_notes", "case_id",
            "segment", "risk_rating", "kyc_score", "is_false_positive", "is_closed",
            "is_escalated",
        ],
        alert_fact,
    )

    case_rows = conn.execute(
        """
        SELECT c.*, (SELECT COUNT(*) FROM aml_case_alerts ca WHERE ca.case_id = c.case_id) AS alert_count
          FROM aml_cases c
         ORDER BY c.case_id
        """
    ).fetchall()
    case_fact: list[list[Any]] = []
    for row in case_rows:
        closed_at = _parse(row["closed_at"]) if row["closed_at"] else None
        due_at = _parse(row["due_at"]) if row["due_at"] else None
        is_closed = 1 if row["status"] in {"CERRADO", "REPORTADO"} else 0
        on_time = 1 if closed_at and due_at and closed_at <= due_at else (0 if closed_at else "")
        case_fact.append(
            [
                row["case_id"], row["customer_id"] or "", row["title"], row["status"],
                row["priority"], row["risk_score"], _iso(row["opened_at"]),
                row["assigned_to"] or "", _iso(row["due_at"]), _iso(row["closed_at"]),
                row["ros_reported"], row["alert_count"], is_closed,
                1 if row["status"] == "REPORTADO" else 0, on_time,
            ]
        )
    counts["fact_cases"] = _write_csv(
        out / "fact_cases.csv",
        [
            "case_id", "customer_id", "title", "status", "priority", "risk_score",
            "opened_at", "assigned_to", "due_at", "closed_at", "ros_reported",
            "alert_count", "is_closed", "is_reported", "is_on_time_close",
        ],
        case_fact,
    )

    daily = conn.execute(
        """
        SELECT value_date, currency, COUNT(*) AS ops,
               SUM(amount_minor) AS amount_minor, SUM(fee_minor) AS fee_minor
          FROM transactions
         GROUP BY value_date, currency
         ORDER BY value_date, currency
        """
    ).fetchall()
    daily_rows = []
    for row in daily:
        local = conn.execute(
            """
            SELECT COUNT(*) AS n,
                   SUM(CASE WHEN t.transaction_id IN (SELECT transaction_id FROM aml_alerts WHERE transaction_id IS NOT NULL) THEN 0 ELSE 1 END) AS stp
              FROM transactions t
             WHERE t.value_date = ? AND t.currency = ?
            """,
            (row["value_date"], row["currency"]),
        ).fetchone()
        daily_rows.append(
            [
                row["value_date"], row["currency"], row["ops"],
                _money(row["amount_minor"], row["currency"]),
                _money(row["fee_minor"], row["currency"]),
                local["stp"] if local else 0,
            ]
        )
    counts["fact_daily_ops"] = _write_csv(
        out / "fact_daily_ops.csv",
        ["date_key", "currency", "ops", "amount", "fee", "stp_ops"],
        daily_rows,
    )

    ledger = conn.execute(
        """
        SELECT je.entry_date, jl.currency, COUNT(DISTINCT je.entry_id) AS entries,
               SUM(jl.debit_minor) AS debit_minor, SUM(jl.credit_minor) AS credit_minor
          FROM journal_entries je
          JOIN journal_lines jl ON jl.entry_id = je.entry_id
         WHERE je.source_type IN ('TRANSFER', 'DEPOSIT', 'WITHDRAWAL', 'FEE', 'FX')
         GROUP BY je.entry_date, jl.currency
         ORDER BY je.entry_date, jl.currency
        """
    ).fetchall()
    ledger_rows = [
        [
            row["entry_date"], row["currency"], row["entries"],
            _money(row["debit_minor"], row["currency"]),
            _money(row["credit_minor"], row["currency"]),
        ]
        for row in ledger
    ]
    counts["fact_ledger_daily"] = _write_csv(
        out / "fact_ledger_daily.csv",
        ["date_key", "currency", "entries", "debit", "credit"],
        ledger_rows,
    )

    return counts


def export(db_path: Path, out_dir: Path) -> dict[str, Any]:
    conn = _copy_to_memory(db_path)
    try:
        _ensure_aml(conn)
        hits = run_all_rules(conn)
        create_alerts(conn, (hit for rule_hits in hits.values() for hit in rule_hits))
        lifecycle = _simulate_lifecycle(conn)
        cases = _simulate_cases(conn)
        out_dir.mkdir(parents=True, exist_ok=True)
        counts = _export_dimensions(conn, out_dir)
        counts.update(_export_facts(conn, out_dir))
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        foreign = conn.execute("PRAGMA foreign_key_check").fetchall()
        try:
            source_label = db_path.resolve().relative_to(REPO_ROOT).as_posix()
        except ValueError:
            source_label = db_path.name
        report = {
            "source_db": source_label,
            "generated_at": datetime.now().replace(microsecond=0).isoformat(),
            "reference_date": REFERENCE_DATE.isoformat(),
            "rows": counts,
            "alert_lifecycle": lifecycle,
            "cases": cases,
            "integrity_check": integrity,
            "foreign_key_violations": len(foreign),
            "notes": [
                "La latencia de fact_payment_sla es sintética y determinística; el core no registra timestamps separados.",
                "Los estados de alertas y casos son un ciclo de vida analítico sintético para demostrar los tableros.",
                "No se modificó la base del core: todo se ejecuta sobre una copia en memoria.",
            ],
        }
        (out_dir / "export_report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return report
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Exporta el dataset analítico de NovaBank")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Base SQLite del core")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Carpeta de salida")
    args = parser.parse_args()
    report = export(Path(args.db), Path(args.out))
    print("Exportación completada")
    for name, count in report["rows"].items():
        print(f"  {name}: {count} filas")
    print(f"  alerts: {report['alert_lifecycle']}")
    print(f"  cases: {report['cases']}")
    return 0 if report["integrity_check"] == "ok" and not report["foreign_key_violations"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
