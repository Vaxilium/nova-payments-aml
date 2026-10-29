"""Actualiza la matriz de trazabilidad de Fase 2 con los IDs y estados de Fase 7."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
QA_DIR = REPO_ROOT / "08-qa-uat"
sys.path.insert(0, str(QA_DIR))

from uat.cases import CASES  # noqa: E402

TRACE_PATH = REPO_ROOT / "03-requerimientos" / "matriz-trazabilidad.csv"
RESULTS_PATH = QA_DIR / "resultados" / "resultados-uat.json"

DEFECT_BY_STORY = {
    "US-002": "DEF-001",
    "US-004": "DEF-002",
    "US-010": "DEF-002",
    "US-037": "DEF-003",
    "US-029": "DEF-004",
    "US-005": "DEF-005",
    "US-034": "DEF-005",
}


def _status(case: dict) -> str:
    automation = case["automatizacion"]
    result = case.get("estado_ejecucion", "")
    if automation.startswith("Automatizado") and result == "Aprobado":
        return "Automatizado parcial - aprobado" if "parcial" in automation else "Automatizado - aprobado"
    if automation == "Manual":
        return "Pendiente de ejecución manual"
    defect = DEFECT_BY_STORY.get(case["historia_id"])
    return f"No implementado - ver {defect}" if defect else "No implementado"


def main() -> int:
    by_story: dict[str, list[dict]] = {}
    for case in CASES:
        by_story.setdefault(case["historia_id"], []).append(case)

    results = {}
    if RESULTS_PATH.exists():
        data = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
        results = {case["id"]: case for case in data.get("cases", [])}

    with TRACE_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys()) if rows else []

    for row in rows:
        story = row["historia_id"]
        cases = by_story.get(story, [])
        if not cases:
            continue
        for case in cases:
            case.update(results.get(case["id"], {}))
        row["caso_prueba_id"] = ";".join(case["id"] for case in cases)
        row["caso_prueba_estado"] = _status(cases[0])
        defect = DEFECT_BY_STORY.get(story)
        if defect and defect not in row.get("notas", ""):
            row["notas"] = f"{row.get('notas', '').rstrip('; ')}; {defect}"

    with TRACE_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Trazabilidad actualizada: {len(rows)} filas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
