"""Genera los artefactos de casos de prueba desde el catálogo reproducible."""

from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
QA_DIR = REPO_ROOT / "08-qa-uat"
sys.path.insert(0, str(QA_DIR))

from uat.cases import CASES  # noqa: E402

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

REQUIRED = {
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
    "referencia",
    "observaciones",
}


def validate() -> None:
    if len(CASES) < 60:
        raise SystemExit(f"Se esperaban al menos 60 casos, hay {len(CASES)}")
    ids = [case["id"] for case in CASES]
    if len(ids) != len(set(ids)):
        raise SystemExit("Hay IDs de caso duplicados")
    stories = {case["historia_id"] for case in CASES}
    missing = {f"US-{index:03d}" for index in range(1, 41)} - stories
    if missing:
        raise SystemExit(f"Historias sin caso de prueba: {sorted(missing)}")
    for case in CASES:
        absent = REQUIRED - set(case)
        if absent:
            raise SystemExit(f"{case.get('id')} sin campos: {sorted(absent)}")
        if case["automatizacion"].startswith("Automatizado") and not case["referencia"]:
            raise SystemExit(f"{case['id']} automatizado sin referencia")


def default_status(case: dict) -> str:
    if case["automatizacion"].startswith("Automatizado"):
        return "Pendiente de ejecución automatizada"
    if case["automatizacion"] == "Manual":
        return "Pendiente de ejecución manual"
    return "No ejecutable - funcionalidad fuera del prototipo"


def steps_text(case: dict) -> str:
    return "\n".join(
        f"{index}. {action} -> {expected}"
        for index, (action, expected) in enumerate(case["pasos"], start=1)
    )


def write_master(path: Path) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MASTER_COLUMNS)
        writer.writeheader()
        for case in CASES:
            writer.writerow(
                {
                    "id": case["id"],
                    "tipo": case["tipo"],
                    "nivel": case["nivel"],
                    "historia_id": case["historia_id"],
                    "epica_id": case["epica_id"],
                    "titulo": case["titulo"],
                    "precondiciones": case["precondiciones"],
                    "pasos": steps_text(case),
                    "resultado_esperado": case["resultado_esperado"],
                    "datos_prueba": case["datos_prueba"],
                    "prioridad": case["prioridad"],
                    "automatizacion": case["automatizacion"],
                    "referencia_automatizada": case["referencia"],
                    "observaciones": case["observaciones"],
                    "estado_ejecucion": default_status(case),
                    "evidencia": "",
                }
            )


def write_ado(path: Path) -> None:
    columns = [
        "ID",
        "Work Item Type",
        "Title",
        "Test Step",
        "Step Action",
        "Step Expected",
        "Area Path",
        "Assigned To",
        "State",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for case in CASES:
            steps = [("Verificar precondiciones: " + case["precondiciones"], "Precondiciones cumplidas")]
            steps.extend(case["pasos"])
            for index, (action, expected) in enumerate(steps, start=1):
                writer.writerow(
                    {
                        "ID": "",
                        "Work Item Type": "Test Case",
                        "Title": f"{case['id']} - {case['titulo']}",
                        "Test Step": index,
                        "Step Action": action,
                        "Step Expected": expected,
                        "Area Path": "NovaBank-Payments\\QA",
                        "Assigned To": "",
                        "State": "Design",
                    }
                )


def write_markdown(path: Path) -> None:
    automated = sum(1 for case in CASES if case["automatizacion"].startswith("Automatizado"))
    manual = sum(1 for case in CASES if case["automatizacion"] == "Manual")
    blocked = sum(1 for case in CASES if case["automatizacion"] == "No implementado")
    lines = [
        "# Casos de prueba y UAT",
        "",
        "Catálogo generado desde `08-qa-uat/uat/cases.py`. No se declaran resultados",
        "hasta ejecutar `08-qa-uat/scripts/run_uat.py`.",
        "",
        f"- Casos totales: **{len(CASES)}**",
        f"- Automatizados: **{automated}**",
        f"- Manuales pendientes: **{manual}**",
        f"- No implementados en el prototipo: **{blocked}**",
        "",
        "| ID | Tipo | Historia | Título | Prioridad | Automatización |",
        "|---|---|---|---|---|---|",
    ]
    for case in CASES:
        lines.append(
            f"| {case['id']} | {case['tipo']} | {case['historia_id']} | {case['titulo']} | "
            f"{case['prioridad']} | {case['automatizacion']} |"
        )
    lines.extend(
        [
            "",
            "## Cobertura por tipo",
            "",
            "| Tipo | Casos |",
            "|---|---|",
        ]
    )
    for tipo in ("Positivo", "Negativo", "Límite"):
        lines.append(f"| {tipo} | {sum(1 for case in CASES if case['tipo'] == tipo)} |")
    lines.extend(
        [
            "",
            "## Artefactos",
            "",
            "- `casos-prueba.csv`: catálogo completo con pasos, datos y resultado esperado.",
            "- `casos-prueba-ado-testplans.csv`: importación en Azure Test Plans (una fila por paso).",
            "- `matriz-cobertura.csv`: cobertura por historia y estado de automatización.",
            "- `matriz-ejecucion.xlsx`: workbook con resumen, casos, ejecución, cobertura y defectos.",
            "- `resultados/resultados-uat.json`: resultados reales de la última ejecución.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_coverage(path: Path) -> None:
    stories: dict[str, list[dict]] = {}
    for case in CASES:
        stories.setdefault(case["historia_id"], []).append(case)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "historia_id",
                "casos",
                "total_casos",
                "automatizados",
                "manuales",
                "no_implementados",
            ]
        )
        for story in sorted(stories):
            cases = stories[story]
            writer.writerow(
                [
                    story,
                    ";".join(case["id"] for case in cases),
                    len(cases),
                    sum(1 for case in cases if case["automatizacion"].startswith("Automatizado")),
                    sum(1 for case in cases if case["automatizacion"] == "Manual"),
                    sum(1 for case in cases if case["automatizacion"] == "No implementado"),
                ]
            )


def main() -> int:
    validate()
    write_master(QA_DIR / "casos-prueba.csv")
    write_ado(QA_DIR / "casos-prueba-ado-testplans.csv")
    write_markdown(QA_DIR / "casos-prueba.md")
    write_coverage(QA_DIR / "matriz-cobertura.csv")
    print(f"Generados {len(CASES)} casos en {QA_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
