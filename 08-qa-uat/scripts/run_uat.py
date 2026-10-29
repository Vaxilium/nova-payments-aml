"""Ejecuta la UAT automatizable, consolida resultados y genera la matriz Excel.

Los casos manuales se dejan explícitamente como pendientes de ejecución manual.
No se inventan resultados ni se marcan como aprobadas pruebas que no corrieron.
"""

from __future__ import annotations

import argparse
import csv
import json
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
QA_DIR = REPO_ROOT / "08-qa-uat"
CORE_DB = REPO_ROOT / "05-core-middleware" / "db" / "novabank.db"
sys.path.insert(0, str(QA_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from uat.cases import CASES  # noqa: E402
from build_workbook import build as build_workbook  # noqa: E402
from run_sql_controls import ensure_database, run as run_sql_controls  # noqa: E402


def _relative(path: Path) -> str:
    """Devuelve la ruta relativa al repo para no publicar rutas personales."""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.name


def _sanitize(text: str) -> str:
    """Elimina rutas absolutas del entorno local en artefactos de evidencia."""
    return (
        text.replace(str(REPO_ROOT), ".")
        .replace(REPO_ROOT.as_posix(), ".")
        .replace(str(REPO_ROOT.parent), "<repo-parent>")
    )

MASTER_COLUMNS = [
    "id",
    "tipo",
    "nivel",
    "historia_id",
    "epica_id",
    "titulo",
    "precondiciones",
    "pasos",
    "resultado_esperado",
    "datos_prueba",
    "prioridad",
    "automatizacion",
    "referencia_automatizada",
    "observaciones",
    "estado_ejecucion",
    "evidencia",
]


def _node_id(classname: str, name: str) -> str:
    if not classname:
        return name
    return f"{classname.replace('.', '/')}.py::{name}"


def parse_junit(path: Path) -> dict:
    if not path.exists():
        return {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "testcases": []}
    tree = ET.parse(path)
    testcases = []
    passed = failed = skipped = 0
    for element in tree.iter("testcase"):
        status = "passed"
        message = ""
        if element.find("failure") is not None:
            status = "failed"
            message = (element.findtext("failure") or "").strip().splitlines()[0:3]
            message = " ".join(message)
            failed += 1
        elif element.find("error") is not None:
            status = "error"
            message = (element.findtext("error") or "").strip().splitlines()[0:3]
            message = " ".join(message)
            failed += 1
        elif element.find("skipped") is not None:
            status = "skipped"
            skipped += 1
        else:
            passed += 1
        testcases.append(
            {
                "nodeid": _node_id(element.get("classname", ""), element.get("name", "")),
                "classname": element.get("classname", ""),
                "name": element.get("name", ""),
                "status": status,
                "time": float(element.get("time", "0") or 0),
                "message": message,
            }
        )
    return {
        "total": len(testcases),
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "testcases": testcases,
    }


def evaluate_case(case: dict, tests: dict[str, dict]) -> tuple[str, str, float]:
    if case["automatizacion"].startswith("Automatizado"):
        refs = [ref.strip() for ref in case["referencia"].split(";") if ref.strip()]
        if not refs:
            return "Fallido", "Sin referencia automatizada", 0.0
        missing = [ref for ref in refs if ref not in tests]
        if missing:
            return "Fallido", f"Referencia no encontrada: {'; '.join(missing)}", 0.0
        failed = [ref for ref in refs if tests[ref]["status"] != "passed"]
        duration = round(sum(tests[ref]["time"] for ref in refs), 3)
        if failed:
            return "Fallido", f"pytest falló: {'; '.join(failed)}", duration
        return "Aprobado", f"pytest: {'; '.join(refs)}", duration
    if case["automatizacion"] == "Manual":
        return "Pendiente de ejecución manual", "Requiere ejecución y captura del autor", 0.0
    return (
        "No ejecutable - funcionalidad fuera del prototipo",
        "No aplica: funcionalidad no implementada",
        0.0,
    )


def update_master(statuses: dict[str, tuple[str, str]]) -> None:
    path = QA_DIR / "casos-prueba.csv"
    if not path.exists():
        return
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        status, evidence = statuses.get(row["id"], ("", ""))
        row["estado_ejecucion"] = status
        row["evidencia"] = evidence
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MASTER_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def write_results_csv(cases: list[dict], path: Path) -> None:
    columns = [
        "id",
        "tipo",
        "nivel",
        "historia_id",
        "epica_id",
        "titulo",
        "prioridad",
        "automatizacion",
        "estado_ejecucion",
        "duracion_s",
        "evidencia",
        "observaciones",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for case in cases:
            writer.writerow({column: case.get(column, "") for column in columns})


def main() -> int:
    parser = argparse.ArgumentParser(description="Ejecución UAT de NovaBank")
    parser.add_argument("--db", default=str(CORE_DB))
    parser.add_argument("--skip-pytest", action="store_true", help="Reutiliza el JUnit existente")
    args = parser.parse_args()

    db_path = Path(args.db)
    results_dir = QA_DIR / "resultados"
    results_dir.mkdir(parents=True, exist_ok=True)
    junit_path = results_dir / "junit-uat.xml"
    sql_path = results_dir / "sql-controls.json"

    ensure_database(db_path)

    pytest_output = ""
    command = "python -m pytest -q --junitxml=08-qa-uat/resultados/junit-uat.xml"
    if not args.skip_pytest:
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", f"--junitxml={junit_path}"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
        )
        pytest_output = (completed.stdout or "") + (completed.stderr or "")
        (results_dir / "pytest-output.txt").write_text(
            _sanitize(pytest_output), encoding="utf-8"
        )

    pytest_results = parse_junit(junit_path)
    tests = {test["nodeid"]: test for test in pytest_results["testcases"]}

    sql_exit = run_sql_controls(db_path, sql_path)
    sql_results = json.loads(sql_path.read_text(encoding="utf-8"))

    evaluated = []
    statuses: dict[str, tuple[str, str]] = {}
    for case in CASES:
        status, evidence, duration = evaluate_case(case, tests)
        statuses[case["id"]] = (status, evidence)
        evaluated.append(
            {
                "id": case["id"],
                "tipo": case["tipo"],
                "nivel": case["nivel"],
                "historia_id": case["historia_id"],
                "epica_id": case["epica_id"],
                "titulo": case["titulo"],
                "prioridad": case["prioridad"],
                "automatizacion": case["automatizacion"],
                "estado_ejecucion": status,
                "duracion_s": duration,
                "evidencia": evidence,
                "observaciones": case["observaciones"],
            }
        )

    automated = [case for case in evaluated if case["automatizacion"].startswith("Automatizado")]
    automated_passed = sum(1 for case in automated if case["estado_ejecucion"] == "Aprobado")
    automated_failed = sum(1 for case in automated if case["estado_ejecucion"] == "Fallido")
    manual_pending = sum(1 for case in evaluated if case["automatizacion"] == "Manual")
    not_implemented = sum(
        1 for case in evaluated if case["automatizacion"] == "No implementado"
    )
    pass_rate = (
        f"{automated_passed}/{len(automated)} ({automated_passed / len(automated) * 100:.1f} %)"
        if automated
        else "0/0 (0 %)"
    )

    results = {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "command": command,
        "environment": (
            f"{platform.system()} {platform.release()}; Python {platform.python_version()}; "
            f"base {_relative(db_path)}; pytest {pytest_results['total']} pruebas"
        ),
        "pytest": pytest_results,
        "sql": sql_results,
        "summary": {
            "cases_total": len(evaluated),
            "automated_total": len(automated),
            "automated_passed": automated_passed,
            "automated_failed": automated_failed,
            "manual_pending": manual_pending,
            "not_implemented": not_implemented,
            "automated_pass_rate": pass_rate,
        },
        "cases": evaluated,
    }
    results_json = results_dir / "resultados-uat.json"
    results_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    write_results_csv(evaluated, results_dir / "resultados-uat.csv")
    update_master(statuses)
    build_workbook(results_json, sql_path, QA_DIR / "matriz-ejecucion.xlsx")

    print(
        "UAT: "
        f"{automated_passed}/{len(automated)} automatizados aprobados; "
        f"{automated_failed} fallidos; {manual_pending} manuales pendientes; "
        f"{not_implemented} no implementados; "
        f"pytest {pytest_results['passed']}/{pytest_results['total']}."
    )
    return 0 if automated_failed == 0 and pytest_results["failed"] == 0 and sql_exit == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
