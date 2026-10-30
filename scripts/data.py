"""Carga de datos reales del repositorio para gráficos y dashboards."""

from __future__ import annotations

import csv
import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import median

from .assetlib import ROOT

ANALYTICS = ROOT / "09-analitica" / "data"
CORE_DB = ROOT / "05-core-middleware" / "db" / "novabank.db"
EVAL_DOC = ROOT / "07-aml-compliance" / "docs" / "evaluacion-verdad.md"


def load_csv(name: str) -> list[dict[str, str]]:
    path = ANALYTICS / name
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_all() -> dict[str, list[dict[str, str]]]:
    return {
        "transactions": load_csv("fact_transactions.csv"),
        "daily": load_csv("fact_daily_ops.csv"),
        "alerts": load_csv("fact_alerts.csv"),
        "sla": load_csv("fact_payment_sla.csv"),
        "cases": load_csv("fact_cases.csv"),
        "rules": load_csv("dim_rule.csv"),
        "currency": load_csv("dim_currency.csv"),
    }


def percentile(values: list[int], pct: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round(pct / 100 * (len(ordered) - 1)))))
    return ordered[index]


def daily_series(rows: list[dict[str, str]]) -> list[tuple[str, int, float]]:
    daily: dict[str, dict[str, float]] = defaultdict(lambda: {"ops": 0.0, "amount": 0.0})
    for row in rows:
        bucket = daily[row["date_key"]]
        bucket["ops"] += float(row["ops"])
        bucket["amount"] += float(row["amount"])
    return [(day, int(vals["ops"]), vals["amount"]) for day, vals in sorted(daily.items())]


def currency_summary(transactions: list[dict[str, str]]) -> list[dict[str, object]]:
    counts: Counter[str] = Counter()
    amounts: Counter[str] = Counter()
    for row in transactions:
        currency = row["currency"]
        counts[currency] += 1
        amounts[currency] += float(row["amount"])
    total = sum(counts.values())
    result = []
    for currency in sorted(counts):
        result.append(
            {
                "currency": currency,
                "ops": counts[currency],
                "share": counts[currency] / total if total else 0.0,
                "amount_minor": amounts[currency],
            }
        )
    return result


def latency_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    values = [int(row["latency_ms"]) for row in rows]
    within = sum(int(row["within_sla"]) for row in rows)
    return {
        "values": values,
        "count": len(values),
        "min": min(values),
        "p50": percentile(values, 50),
        "p95": percentile(values, 95),
        "p99": percentile(values, 99),
        "max": max(values),
        "mean": sum(values) / len(values),
        "within_share": within / len(values) if values else 0.0,
        "sla_ms": 10_000,
    }


def alert_counts(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["rule_id"]].append(row)
    result = []
    for rule_id, items in sorted(grouped.items()):
        result.append(
            {
                "rule_id": rule_id,
                "rule_name": items[0]["rule_name"],
                "count": len(items),
                "severity": items[0]["severity"],
                "priority": Counter(item["priority"] for item in items).most_common(1)[0][0],
                "status": Counter(item["status"] for item in items),
            }
        )
    result.sort(key=lambda item: int(item["count"]), reverse=True)  # type: ignore[arg-type]
    return result


def parse_eval_table(path: Path = EVAL_DOC) -> list[dict[str, object]]:
    """Lee la tabla de detalle por regla del reporte real de evaluación AML."""
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| R"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 11:
            continue
        try:
            rows.append(
                {
                    "rule_id": cells[0],
                    "rule_name": cells[1],
                    "flagged": int(cells[2]),
                    "tp": int(cells[3]),
                    "fp": int(cells[4]),
                    "fn": int(cells[5]),
                    "unlabeled": int(cells[6]),
                    "precision": float(cells[7].replace("%", "").replace(",", ".")) / 100,
                    "precision_conservative": float(cells[8].replace("%", "").replace(",", ".")) / 100,
                    "recall": float(cells[9].replace("%", "").replace(",", ".")) / 100,
                    "f1": float(cells[10].replace(",", ".")),
                }
            )
        except ValueError:
            continue
    return rows


@dataclass
class Dataset:
    transactions: list[dict[str, str]]
    daily: list[dict[str, str]]
    alerts: list[dict[str, str]]
    sla: list[dict[str, str]]
    cases: list[dict[str, str]]
    rules: list[dict[str, str]]
    currency: list[dict[str, str]]
    eval_rules: list[dict[str, object]]


def dataset() -> Dataset:
    data = load_all()
    return Dataset(
        transactions=data["transactions"],
        daily=data["daily"],
        alerts=data["alerts"],
        sla=data["sla"],
        cases=data["cases"],
        rules=data["rules"],
        currency=data["currency"],
        eval_rules=parse_eval_table(),
    )


def core_metrics() -> dict[str, object]:
    """Consulta la base del core para métricas de contabilidad verificables."""
    with sqlite3.connect(CORE_DB) as conn:
        conn.row_factory = sqlite3.Row
        counts = {
            "customers": conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0],
            "accounts": conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0],
            "transactions": conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0],
            "journal_entries": conn.execute("SELECT COUNT(*) FROM journal_entries").fetchone()[0],
            "journal_lines": conn.execute("SELECT COUNT(*) FROM journal_lines").fetchone()[0],
        }
        suspicious = conn.execute(
            "SELECT COUNT(*) FROM _aml_ground_truth WHERE label = 'SUSPICIOUS'"
        ).fetchone()[0]
        counts["suspicious"] = suspicious
    return counts


def kpi_block(data: Dataset) -> dict[str, object]:
    alerts = len(data.alerts)
    latency = latency_summary(data.sla)
    return {
        "transactions": len(data.transactions),
        "alerts": alerts,
        "cases": len(data.cases),
        "rules": len(data.rules),
        "precision": 341 / 344,
        "precision_conservative": 341 / 494,
        "recall": 1.0,
        "within_sla": latency["within_share"],
        "p95": latency["p95"],
        "p50": latency["p50"],
    }


def top_alert_rows(data: Dataset, limit: int = 8) -> list[dict[str, str]]:
    priority = {"P1": 0, "P2": 1, "P3": 2}
    ordered = sorted(
        data.alerts,
        key=lambda row: (
            priority.get(row.get("priority", "P3"), 9),
            -int(row.get("risk_score") or 0),
            row.get("date_key", ""),
        ),
    )
    return ordered[:limit]
