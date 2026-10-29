"""Evaluación de reglas contra la verdad generada en Fase 3."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from . import config
from .rules import RuleHit


@dataclass(frozen=True)
class RuleMetric:
    rule_id: str
    rule_name: str
    flagged: int
    true_positives: int
    false_positives: int
    false_negatives: int
    unlabeled: int
    precision: float
    precision_lower_bound: float
    recall: float
    f1: float


@dataclass(frozen=True)
class EvaluationResult:
    total_transactions: int
    labeled_transactions: int
    suspicious_transactions: int
    normal_transactions: int
    flagged_transactions: int
    true_positives: int
    false_positives: int
    false_negatives: int
    unlabeled_flagged: int
    precision: float
    precision_lower_bound: float
    recall: float
    f1: float
    by_rule: dict[str, RuleMetric] = field(default_factory=dict)
    by_pattern: dict[str, dict[str, float | int]] = field(default_factory=dict)


def load_truth(conn: sqlite3.Connection) -> dict[str, dict[str, str | None]]:
    truth: dict[str, dict[str, str | None]] = {}
    for row in conn.execute("SELECT transaction_id, label, pattern_type FROM _aml_ground_truth"):
        truth[row["transaction_id"]] = {"label": row["label"], "pattern": row["pattern_type"]}
    return truth


def _ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def _rule_metric(
    rule_id: str,
    flagged_ids: set[str],
    truth: dict[str, dict[str, str | None]],
    suspicious_ids: set[str],
) -> RuleMetric:
    labeled_hits = {tx for tx in flagged_ids if tx in truth}
    tp = {tx for tx in labeled_hits if truth[tx]["label"] == "SUSPICIOUS"}
    fp = {tx for tx in labeled_hits if truth[tx]["label"] == "NORMAL"}
    unlabeled = {tx for tx in flagged_ids if tx not in truth}
    fn = suspicious_ids - flagged_ids
    precision = _ratio(len(tp), len(tp) + len(fp))
    lower = _ratio(len(tp), len(tp) + len(fp) + len(unlabeled))
    recall = _ratio(len(tp), len(tp) + len(fn))
    f1 = round(2 * precision * recall / (precision + recall), 4) if precision + recall else 0.0
    return RuleMetric(
        rule_id=rule_id,
        rule_name=config.RULE_META[rule_id]["name"],
        flagged=len(flagged_ids),
        true_positives=len(tp),
        false_positives=len(fp),
        false_negatives=len(fn),
        unlabeled=len(unlabeled),
        precision=precision,
        precision_lower_bound=lower,
        recall=recall,
        f1=f1,
    )


def _pattern_metrics(
    truth: dict[str, dict[str, str | None]],
    flagged_ids: set[str],
) -> dict[str, dict[str, float | int]]:
    patterns: dict[str, set[str]] = {}
    for tx_id, item in truth.items():
        if item["label"] != "SUSPICIOUS" or not item["pattern"]:
            continue
        for pattern in str(item["pattern"]).split("|"):
            patterns.setdefault(pattern.strip(), set()).add(tx_id)
    result: dict[str, dict[str, float | int]] = {}
    for pattern, ids in sorted(patterns.items()):
        detected = ids & flagged_ids
        result[pattern] = {
            "total": len(ids),
            "detected": len(detected),
            "recall": _ratio(len(detected), len(ids)),
        }
    return result


def evaluate(conn: sqlite3.Connection, hits_by_rule: dict[str, Iterable[RuleHit]]) -> EvaluationResult:
    truth = load_truth(conn)
    total_transactions = int(conn.execute("SELECT COUNT(*) AS n FROM transactions").fetchone()["n"])
    suspicious_ids = {tx for tx, item in truth.items() if item["label"] == "SUSPICIOUS"}
    normal_ids = {tx for tx, item in truth.items() if item["label"] == "NORMAL"}

    flagged_ids: set[str] = set()
    by_rule: dict[str, RuleMetric] = {}
    for rule_id, hits in hits_by_rule.items():
        rule_ids = {hit.transaction_id for hit in hits if hit.transaction_id}
        flagged_ids |= rule_ids
        by_rule[rule_id] = _rule_metric(rule_id, rule_ids, truth, suspicious_ids)

    labeled_flagged = flagged_ids & truth.keys()
    tp = {tx for tx in labeled_flagged if truth[tx]["label"] == "SUSPICIOUS"}
    fp = {tx for tx in labeled_flagged if truth[tx]["label"] == "NORMAL"}
    unlabeled = flagged_ids - truth.keys()
    fn = suspicious_ids - flagged_ids
    precision = _ratio(len(tp), len(tp) + len(fp))
    lower = _ratio(len(tp), len(tp) + len(fp) + len(unlabeled))
    recall = _ratio(len(tp), len(tp) + len(fn))
    f1 = round(2 * precision * recall / (precision + recall), 4) if precision + recall else 0.0

    return EvaluationResult(
        total_transactions=total_transactions,
        labeled_transactions=len(truth),
        suspicious_transactions=len(suspicious_ids),
        normal_transactions=len(normal_ids),
        flagged_transactions=len(flagged_ids),
        true_positives=len(tp),
        false_positives=len(fp),
        false_negatives=len(fn),
        unlabeled_flagged=len(unlabeled),
        precision=precision,
        precision_lower_bound=lower,
        recall=recall,
        f1=f1,
        by_rule=by_rule,
        by_pattern=_pattern_metrics(truth, flagged_ids),
    )


def _percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def render_markdown(result: EvaluationResult) -> str:
    lines = [
        "# Evaluación de reglas contra la verdad de Fase 3",
        "",
        f"Generado: {datetime.now(timezone.utc).replace(microsecond=0).isoformat()}",
        "",
        "## Resumen",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Transacciones totales | {result.total_transactions:,} |".replace(",", "."),
        f"| Transacciones etiquetadas | {result.labeled_transactions:,} |".replace(",", "."),
        f"| Sospechosas (truth) | {result.suspicious_transactions:,} |".replace(",", "."),
        f"| Normales muestreadas (truth) | {result.normal_transactions:,} |".replace(",", "."),
        f"| Transacciones alertadas | {result.flagged_transactions:,} |".replace(",", "."),
        f"| Verdaderos positivos | {result.true_positives} |",
        f"| Falsos positivos | {result.false_positives} |",
        f"| Falsos negativos | {result.false_negatives} |",
        f"| Alertadas sin etiqueta | {result.unlabeled_flagged:,} |".replace(",", "."),
        f"| Precisión (solo etiquetadas) | {_percent(result.precision)} |",
        f"| Precisión conservadora (no etiquetadas = FP) | {_percent(result.precision_lower_bound)} |",
        f"| Recall | {_percent(result.recall)} |",
        f"| F1 | {result.f1:.4f} |",
        "",
        "## Detalle por regla",
        "",
        "| Regla | Nombre | Alertadas | TP | FP | FN | Sin etiqueta | Precisión | Precisión conservadora | Recall | F1 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for metric in result.by_rule.values():
        lines.append(
            "| {rule} | {name} | {flagged} | {tp} | {fp} | {fn} | {unlabeled} | {p} | {pl} | {r} | {f1} |".format(
                rule=metric.rule_id,
                name=metric.rule_name,
                flagged=metric.flagged,
                tp=metric.true_positives,
                fp=metric.false_positives,
                fn=metric.false_negatives,
                unlabeled=metric.unlabeled,
                p=_percent(metric.precision),
                pl=_percent(metric.precision_lower_bound),
                r=_percent(metric.recall),
                f1=f"{metric.f1:.4f}",
            )
        )

    lines.extend(
        [
            "",
            "## Cobertura por patrón",
            "",
            "| Patrón | Casos truth | Detectados | Recall |",
            "|---|---:|---:|---:|",
        ]
    )
    for pattern, values in result.by_pattern.items():
        lines.append(
            f"| {pattern} | {values['total']} | {values['detected']} | {_percent(float(values['recall']))} |"
        )

    lines.extend(
        [
            "",
            "## Lectura metodológica",
            "",
            "- La muestra `NORMAL` de Fase 3 es una muestra, no el universo de transacciones normales.",
            "- La precisión principal solo cuenta transacciones etiquetadas; la precisión conservadora suma las alertadas sin etiqueta como falsos positivos.",
            "- El recall se calcula sobre las 341 transacciones sospechosas etiquetadas.",
            "- R07 (geografía) y R09 (cambio de comportamiento) pueden alertar transacciones normales no muestreadas; se reportan por separado y no se ocultan.",
            "- Los resultados son reproducibles con la semilla fija del seed de Fase 3.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(result: EvaluationResult, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return path


def evaluate_and_report(
    conn: sqlite3.Connection,
    hits_by_rule: dict[str, Iterable[RuleHit]],
    path: Path | None = None,
) -> EvaluationResult:
    result = evaluate(conn, hits_by_rule)
    write_report(result, path or config.DOCS_DIR / "evaluacion-verdad.md")
    return result


__all__ = [
    "EvaluationResult",
    "RuleMetric",
    "evaluate",
    "evaluate_and_report",
    "load_truth",
    "render_markdown",
    "write_report",
]
