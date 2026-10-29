"""Construye el workbook Excel avanzado de NovaBank con openpyxl.

El workbook usa fórmulas reales (XLOOKUP, INDEX/MATCH, SUMIFS, COUNTIFS,
PERCENTILE), tablas con nombres, rangos definidos, validaciones de datos,
formato condicional y un simulador de comisiones.

Uso:
    python 09-analitica/scripts/build_excel.py
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, DataBarRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

ANALYTICS_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ANALYTICS_DIR / "data"
DEFAULT_OUT = ANALYTICS_DIR / "excel" / "NovaBank_analitica.xlsx"

NAVY = "0B3B60"
BLUE = "155E8A"
TEAL = "0F766E"
INK = "111827"
MUTED = "4B5563"
LINE = "D1D5DB"
SURFACE = "FFFFFF"
BG = "F3F4F6"
WARN = "B45309"
WARN_SOFT = "FEF3C7"
DANGER = "B91C1C"
DANGER_SOFT = "FEE2E2"
OK_SOFT = "CCFBF1"

THIN = Side(style="thin", color=LINE)
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEADER_FILL = PatternFill("solid", fgColor=NAVY)
HEADER_FONT = Font(name="Calibri", bold=True, color=SURFACE, size=11)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def as_number(value: str) -> float | int | str:
    if value is None or value == "":
        return ""
    try:
        number = float(value)
    except ValueError:
        return value
    return int(number) if number.is_integer() else number


def title(ws, text: str, subtitle: str = "", *, width: int = 8) -> None:
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=width)
    cell = ws.cell(row=1, column=1, value=text)
    cell.font = Font(name="Calibri", bold=True, size=18, color=SURFACE)
    cell.fill = PatternFill("solid", fgColor=NAVY)
    cell.alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[1].height = 34
    if subtitle:
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=width)
        note = ws.cell(row=2, column=1, value=subtitle)
        note.font = Font(name="Calibri", size=10, color=MUTED, italic=True)
        note.alignment = Alignment(vertical="center", indent=1)
        ws.row_dimensions[2].height = 20


def style_header(row) -> None:
    for cell in row:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.border = BORDER
        cell.alignment = Alignment(vertical="center", wrap_text=True)


def add_table(ws, name: str, ref: str, *, style: str = "TableStyleMedium2") -> Table:
    table = Table(displayName=name, ref=ref)
    table.tableStyleInfo = TableStyleInfo(
        name=style, showFirstColumn=False, showLastColumn=False,
        showRowStripes=True, showColumnStripes=False,
    )
    ws.add_table(table)
    return table


def write_rows(ws, headers: list[str], rows: list[list[Any]], *, start_row: int = 4) -> int:
    for column, header in enumerate(headers, start=1):
        ws.cell(row=start_row, column=column, value=header)
    style_header(ws[start_row])
    for r_index, row in enumerate(rows, start=start_row + 1):
        for c_index, value in enumerate(row, start=1):
            ws.cell(row=r_index, column=c_index, value=value)
    return start_row + len(rows)


def set_widths(ws, widths: dict[str, int]) -> None:
    for column, width in widths.items():
        ws.column_dimensions[column].width = width


def add_defined_name(wb: Workbook, name: str, attr_text: str) -> None:
    wb.defined_names.add(DefinedName(name, attr_text=attr_text))


def build_portada(wb: Workbook) -> None:
    ws = wb.active
    ws.title = "Portada"
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = NAVY
    title(ws, "NovaBank · Analítica de pagos y cumplimiento", "Caso ficticio · datos sintéticos reproducibles", width=6)
    rows = [
        ("Proyecto", "NovaBank Instant & Cross-Border Payments + AML Hub"),
        ("Autor", "Franco Tillería Centurión — Business Analyst"),
        ("Fecha del dataset", "2026-04-01 a 2026-09-30"),
        ("Fuente", "SQLite del core (Fase 3) + evaluador AML (Fase 5)"),
        ("Semilla", "20261027 · sin PII real"),
        ("Uso", "Portafolio y demostración funcional; no es un reporte regulatorio."),
        ("Actualización", "2026-10-29"),
    ]
    start = 4
    for index, (label, value) in enumerate(rows, start=start):
        ws.cell(row=index, column=1, value=label).font = Font(bold=True, color=NAVY)
        ws.cell(row=index, column=2, value=value)
        ws.merge_cells(start_row=index, start_column=2, end_row=index, end_column=6)
        ws.cell(row=index, column=2).alignment = Alignment(vertical="center", wrap_text=True)
    notes = [
        "El workbook usa fórmulas reales. Excel calcula los valores al abrir el archivo.",
        "Las hojas de hechos son un extracto agregado del dataset CSV de la carpeta /data.",
        "La conciliación compara débitos y créditos del libro mayor por fecha y moneda.",
        "Los estados de alertas y casos son un ciclo de vida analítico sintético para demostrar los tableros.",
        "La latencia de Pagos_Local es sintética y determinística: el core no registra timestamps separados.",
        "No se afirma que este archivo haya sido abierto en Power BI ni en Tableau.",
    ]
    row = start + len(rows) + 2
    ws.cell(row=row, column=1, value="Notas de lectura").font = Font(bold=True, size=12, color=NAVY)
    for note in notes:
        row += 1
        ws.cell(row=row, column=1, value="•")
        ws.cell(row=row, column=2, value=note)
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=6)
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    row += 2
    ws.cell(row=row, column=1, value="Índice de hojas").font = Font(bold=True, size=12, color=NAVY)
    sheets = [
        ("Parámetros", "Comisiones, umbrales, tipos de cambio y listas de validación."),
        ("KPIs", "Tablero ejecutivo con fórmulas y semáforo."),
        ("Conciliación", "XLOOKUP, INDEX/MATCH y SUMIFS por fecha y moneda."),
        ("Hechos_Diarios", "Operaciones, importes, comisiones y STP por día/moneda."),
        ("Libro_Diario", "Débitos y créditos agregados del libro mayor."),
        ("Alertas", "Alertas AML con prioridad, SLA y resultado."),
        ("Casos", "Casos AML, cierres y reporte de operaciones sospechosas."),
        ("Pagos_Local", "Detalle de transferencias locales con latencia sintética."),
        ("Simulador", "Calculadora de comisiones con validaciones."),
        ("Reglas", "Catálogo R01–R12 y SLA por prioridad."),
    ]
    row += 1
    for name, description in sheets:
        ws.cell(row=row, column=1, value=name).font = Font(bold=True, color=BLUE)
        ws.cell(row=row, column=2, value=description)
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=6)
        row += 1
    set_widths(ws, {"A": 26, "B": 42, "C": 18, "D": 18, "E": 18, "F": 18})


def build_parametros(wb: Workbook) -> None:
    ws = wb.create_sheet("Parámetros")
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = BLUE
    title(ws, "Parámetros del modelo", "Valores ficticios de configuración del caso", width=4)
    params = [
        ("Param_ComisionLocalPct", "Comisión local (%)", 0.0025, "%", "Comisión sobre importe local."),
        ("Param_ComisionIntlUSD", "Comisión internacional", 25.00, "USD", "Cargo fijo por transferencia internacional."),
        ("Param_ComisionFX_Pct", "Comisión FX (%)", 0.015, "%", "Referencia para conversión de moneda."),
        ("Param_ComisionMinimaLocal_PYG", "Comisión mínima local", 2000, "PYG", "Piso de comisión local."),
        ("Param_DescuentoPremium", "Descuento premium", 0.50, "factor", "Descuento aplicado a clientes premium."),
        ("Param_TopeLocalPYG", "Tope por operación local", 10000000, "PYG", "Tope operativo simulado."),
        ("Param_SLA_Instantaneo_ms", "SLA instantáneo", 5000, "ms", "Objetivo de acreditación local."),
        ("Param_Meta_STP", "Meta STP", 0.95, "%", "Objetivo de straight-through processing."),
        ("Param_Meta_FalsosPositivos", "Meta falsos positivos", 0.30, "%", "Techo de falsos positivos sobre alertas cerradas."),
        ("Param_Meta_P1_a_tiempo", "Meta P1 a tiempo", 0.95, "%", "Asignación de alertas P1 dentro de 15 min."),
        ("Param_Meta_Conciliacion", "Meta conciliación", 0.995, "%", "Asientos conciliados al cierre."),
    ]
    ws.cell(row=4, column=1, value="Parámetro")
    ws.cell(row=4, column=2, value="Nombre")
    ws.cell(row=4, column=3, value="Valor")
    ws.cell(row=4, column=4, value="Unidad")
    ws.cell(row=4, column=5, value="Descripción")
    style_header(ws[4])
    for index, (key, label, value, unit, description) in enumerate(params, start=5):
        ws.cell(row=index, column=1, value=label)
        ws.cell(row=index, column=2, value=key)
        ws.cell(row=index, column=3, value=value)
        ws.cell(row=index, column=4, value=unit)
        ws.cell(row=index, column=5, value=description)
        ws.cell(row=index, column=3).number_format = (
            "0.00%" if unit == "%" else ("#,##0" if unit in {"PYG", "ms"} else "0.00")
        )
        ws.cell(row=index, column=2).font = Font(name="Consolas", size=9, color=MUTED)
    add_defined_name(wb, "Param_ComisionLocalPct", "'Parámetros'!$C$5")
    add_defined_name(wb, "Param_ComisionIntlUSD", "'Parámetros'!$C$6")
    add_defined_name(wb, "Param_ComisionFX_Pct", "'Parámetros'!$C$7")
    add_defined_name(wb, "Param_ComisionMinimaLocal_PYG", "'Parámetros'!$C$8")
    add_defined_name(wb, "Param_DescuentoPremium", "'Parámetros'!$C$9")
    add_defined_name(wb, "Param_TopeLocalPYG", "'Parámetros'!$C$10")
    add_defined_name(wb, "Param_SLA_Instantaneo_ms", "'Parámetros'!$C$11")
    add_defined_name(wb, "Param_Meta_STP", "'Parámetros'!$C$12")
    add_defined_name(wb, "Param_Meta_FalsosPositivos", "'Parámetros'!$C$13")
    add_defined_name(wb, "Param_Meta_P1_a_tiempo", "'Parámetros'!$C$14")
    add_defined_name(wb, "Param_Meta_Conciliacion", "'Parámetros'!$C$15")

    fx_header_row = 19
    ws.cell(row=fx_header_row, column=1, value="Moneda")
    ws.cell(row=fx_header_row, column=2, value="Tasa_PYG")
    ws.cell(row=fx_header_row, column=3, value="Descripción")
    style_header(ws[fx_header_row])
    fx = [("PYG", 1, "Moneda base"), ("USD", 7300, "Tipo de cambio ficticio"), ("EUR", 7900, "Tipo de cambio ficticio")]
    for index, row in enumerate(fx, start=fx_header_row + 1):
        for col, value in enumerate(row, start=1):
            ws.cell(row=index, column=col, value=value)
    add_table(ws, "tblTiposCambio", f"A{fx_header_row}:C{fx_header_row + len(fx)}")
    add_defined_name(wb, "Lista_Monedas", "'Parámetros'!$A$20:$A$22")
    add_defined_name(wb, "Lista_Tipos", "'Parámetros'!$A$25:$A$26")
    add_defined_name(wb, "Lista_SiNo", "'Parámetros'!$A$27:$A$28")

    ws.cell(row=24, column=1, value="Tipo").font = Font(bold=True, color=NAVY)
    ws.cell(row=25, column=1, value="LOCAL")
    ws.cell(row=26, column=1, value="INTERNACIONAL")
    ws.cell(row=24, column=3, value="Sí/No").font = Font(bold=True, color=NAVY)
    ws.cell(row=27, column=1, value="SI")
    ws.cell(row=28, column=1, value="NO")
    ws.column_dimensions["E"].width = 44
    set_widths(ws, {"A": 30, "B": 26, "C": 16, "D": 10})


def build_hechos(wb: Workbook, data_dir: Path) -> None:
    ws = wb.create_sheet("Hechos_Diarios")
    ws.sheet_properties.tabColor = TEAL
    title(ws, "Hechos diarios", "Operaciones y comisiones por día y moneda", width=7)
    rows = read_csv(data_dir / "fact_daily_ops.csv")
    headers = ["Fecha", "Moneda", "Operaciones", "Importe", "Comision", "STP", "Clave"]
    body = []
    for row in rows:
        body.append([
            row["date_key"], row["currency"], int(row["ops"]), as_number(row["amount"]),
            as_number(row["fee"]), int(row["stp_ops"]), f"{row['date_key']}|{row['currency']}",
        ])
    last = write_rows(ws, headers, body, start_row=4)
    add_table(ws, "tblHechosDiarios", f"A4:G{last}")
    ws.freeze_panes = "A5"
    for row in ws.iter_rows(min_row=5, max_row=last, min_col=4, max_col=5):
        for cell in row:
            cell.number_format = "#,##0.00"
    ws.conditional_formatting.add(
        f"D5:E{last}",
        DataBarRule(start_type="min", end_type="max", color="155E8A"),
    )
    set_widths(ws, {"A": 13, "B": 9, "C": 13, "D": 16, "E": 14, "F": 8, "G": 18})


def build_libro(wb: Workbook, data_dir: Path) -> None:
    ws = wb.create_sheet("Libro_Diario")
    ws.sheet_properties.tabColor = NAVY
    title(ws, "Libro diario agregado", "Débitos y créditos por fecha y moneda", width=6)
    rows = read_csv(data_dir / "fact_ledger_daily.csv")
    headers = ["Fecha", "Moneda", "Asientos", "Debitos", "Creditos", "Clave"]
    body = []
    for row in rows:
        body.append([
            row["date_key"], row["currency"], int(row["entries"]), as_number(row["debit"]),
            as_number(row["credit"]), f"{row['date_key']}|{row['currency']}",
        ])
    last = write_rows(ws, headers, body, start_row=4)
    add_table(ws, "tblLibroDiario", f"A4:F{last}")
    ws.freeze_panes = "A5"
    for row in ws.iter_rows(min_row=5, max_row=last, min_col=4, max_col=5):
        for cell in row:
            cell.number_format = "#,##0.00"
    set_widths(ws, {"A": 13, "B": 9, "C": 11, "D": 18, "E": 18, "F": 18})


def build_conciliacion(wb: Workbook, data_dir: Path) -> None:
    ws = wb.create_sheet("Conciliación")
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = WARN
    title(ws, "Conciliación por fecha y moneda", "XLOOKUP + INDEX/MATCH + SUMIFS sobre tablas", width=9)
    ops = read_csv(data_dir / "fact_daily_ops.csv")
    headers = [
        "Clave", "Fecha", "Moneda", "Operaciones_sistema", "Importe_operaciones",
        "Debitos_libro", "Creditos_libro", "Diferencia", "Resultado", "Verificacion",
    ]
    ws.cell(row=4, column=1, value=headers[0])
    for index, header in enumerate(headers, start=1):
        ws.cell(row=4, column=index, value=header)
    style_header(ws[4])
    for index, row in enumerate(ops, start=5):
        key = f"{row['date_key']}|{row['currency']}"
        ws.cell(row=index, column=1, value=key)
        ws.cell(row=index, column=2, value=row["date_key"])
        ws.cell(row=index, column=3, value=row["currency"])
        ws.cell(
            row=index, column=4,
            value=f'=SUMIFS(tblHechosDiarios[Operaciones],tblHechosDiarios[Fecha],$B{index},tblHechosDiarios[Moneda],$C{index})',
        )
        ws.cell(
            row=index, column=5,
            value=f'=SUMIFS(tblHechosDiarios[Importe],tblHechosDiarios[Fecha],$B{index},tblHechosDiarios[Moneda],$C{index})',
        )
        ws.cell(
            row=index, column=6,
            value=f'=_xlfn.XLOOKUP($A{index},tblLibroDiario[Clave],tblLibroDiario[Debitos],"SIN DATO")',
        )
        ws.cell(
            row=index, column=7,
            value=f'=IFERROR(INDEX(tblLibroDiario[Creditos],MATCH($A{index},tblLibroDiario[Clave],0)),"SIN DATO")',
        )
        ws.cell(row=index, column=8, value=f"=ROUND(F{index}-G{index},2)")
        ws.cell(row=index, column=9, value=f'=IF(ABS(H{index})<0.01,"CUADRADO","DIFERENCIA")')
        ws.cell(row=index, column=10, value=f'=IF(ABS(H{index})<0.01,"OK","REVISAR")')
        for col in (5, 6, 7, 8):
            ws.cell(row=index, column=col).number_format = "#,##0.00"
    last = 4 + len(ops)
    add_table(ws, "tblConciliacion", f"A4:J{last}")
    ws.freeze_panes = "A5"
    ws.conditional_formatting.add(
        f"H5:H{last}",
        CellIsRule(operator="notEqual", formula=["0"], fill=PatternFill("solid", fgColor=DANGER_SOFT), font=Font(color=DANGER, bold=True)),
    )
    ws.conditional_formatting.add(
        f"I5:I{last}",
        CellIsRule(operator="equal", formula=['"DIFERENCIA"'], fill=PatternFill("solid", fgColor=DANGER_SOFT), font=Font(color=DANGER, bold=True)),
    )
    ws.conditional_formatting.add(
        f"I5:I{last}",
        CellIsRule(operator="equal", formula=['"CUADRADO"'], fill=PatternFill("solid", fgColor=OK_SOFT), font=Font(color=TEAL, bold=True)),
    )
    ws.conditional_formatting.add(
        f"J5:J{last}",
        CellIsRule(operator="equal", formula=['"REVISAR"'], fill=PatternFill("solid", fgColor=WARN_SOFT), font=Font(color=WARN, bold=True)),
    )
    set_widths(ws, {"A": 18, "B": 12, "C": 9, "D": 19, "E": 18, "F": 15, "G": 15, "H": 12, "I": 13, "J": 12})


def build_alertas(wb: Workbook, data_dir: Path) -> None:
    ws = wb.create_sheet("Alertas")
    ws.sheet_properties.tabColor = DANGER
    title(ws, "Alertas AML", "Bandeja analítica de alertas y su ciclo de vida", width=14)
    rows = read_csv(data_dir / "fact_alerts.csv")
    headers = [
        "alert_id", "date_key", "rule_id", "prioridad", "risk_score", "status",
        "transaction_count", "customer_id", "assigned_to", "assignment_minutes",
        "due_at", "closed_at", "is_false_positive", "is_escalated",
    ]
    body = []
    for row in rows:
        body.append([
            int(row["alert_id"]), row["date_key"], row["rule_id"], row["priority"],
            int(row["risk_score"]), row["status"], int(row["transaction_count"]),
            row["customer_id"], row["assigned_to"], as_number(row["assignment_minutes"]),
            row["due_at"], row["closed_at"], int(row["is_false_positive"]), int(row["is_escalated"]),
        ])
    last = write_rows(ws, headers, body, start_row=4)
    add_table(ws, "tblAlertas", f"A4:N{last}")
    ws.freeze_panes = "A5"
    for row in ws.iter_rows(min_row=5, max_row=last, min_col=10, max_col=10):
        for cell in row:
            cell.number_format = "0"
    ws.conditional_formatting.add(
        f"D5:D{last}",
        CellIsRule(operator="equal", formula=['"P1"'], fill=PatternFill("solid", fgColor=DANGER_SOFT), font=Font(color=DANGER, bold=True)),
    )
    ws.conditional_formatting.add(
        f"D5:D{last}",
        CellIsRule(operator="equal", formula=['"P2"'], fill=PatternFill("solid", fgColor=WARN_SOFT), font=Font(color=WARN, bold=True)),
    )
    ws.conditional_formatting.add(
        f"M5:M{last}",
        CellIsRule(operator="equal", formula=["1"], fill=PatternFill("solid", fgColor=BG)),
    )
    ws.conditional_formatting.add(
        f"J5:J{last}",
        CellIsRule(operator="greaterThan", formula=["15"], fill=PatternFill("solid", fgColor=DANGER_SOFT), font=Font(color=DANGER)),
    )
    set_widths(ws, {"A": 10, "B": 11, "C": 8, "D": 9, "E": 9, "F": 22, "G": 12, "H": 13, "I": 16, "J": 12, "K": 20, "L": 20, "M": 10, "N": 10})


def build_casos(wb: Workbook, data_dir: Path) -> None:
    ws = wb.create_sheet("Casos")
    ws.sheet_properties.tabColor = WARN
    title(ws, "Casos AML", "Casos, cierres y reporte de operaciones sospechosas", width=12)
    rows = read_csv(data_dir / "fact_cases.csv")
    headers = [
        "case_id", "customer_id", "status", "priority", "risk_score", "opened_at",
        "assigned_to", "due_at", "closed_at", "ros_reported", "alert_count",
        "is_closed", "is_on_time_close",
    ]
    body = []
    for row in rows:
        body.append([
            int(row["case_id"]), row["customer_id"], row["status"], row["priority"],
            int(row["risk_score"]), row["opened_at"], row["assigned_to"], row["due_at"],
            row["closed_at"], int(row["ros_reported"]), int(row["alert_count"]),
            int(row["is_closed"]), as_number(row["is_on_time_close"]),
        ])
    last = write_rows(ws, headers, body, start_row=4)
    add_table(ws, "tblCasos", f"A4:M{last}")
    ws.freeze_panes = "A5"
    ws.conditional_formatting.add(
        f"D5:D{last}",
        CellIsRule(operator="equal", formula=['"P1"'], fill=PatternFill("solid", fgColor=DANGER_SOFT), font=Font(color=DANGER, bold=True)),
    )
    ws.conditional_formatting.add(
        f"L5:L{last}",
        CellIsRule(operator="equal", formula=["1"], fill=PatternFill("solid", fgColor=OK_SOFT), font=Font(color=TEAL)),
    )
    set_widths(ws, {"A": 9, "B": 13, "C": 16, "D": 9, "E": 10, "F": 20, "G": 16, "H": 20, "I": 20, "J": 9, "K": 11, "L": 9, "M": 15})


def build_pagos_local(wb: Workbook, data_dir: Path) -> None:
    ws = wb.create_sheet("Pagos_Local")
    ws.sheet_properties.tabColor = TEAL
    title(ws, "Pagos locales · SLA sintético", "Una fila por transferencia local; latencia generada de forma determinística", width=8)
    rows = read_csv(data_dir / "fact_payment_sla.csv")
    headers = ["transaction_id", "date_key", "customer_id", "segment", "channel", "amount", "latency_ms", "within_sla"]
    body = []
    for row in rows:
        body.append([
            row["transaction_id"], row["date_key"], row["customer_id"], row["segment"],
            row["channel"], as_number(row["amount"]), int(row["latency_ms"]), int(row["within_sla"]),
        ])
    last = write_rows(ws, headers, body, start_row=4)
    add_table(ws, "tblPagosLocal", f"A4:H{last}")
    ws.freeze_panes = "A5"
    for row in ws.iter_rows(min_row=5, max_row=last, min_col=6, max_col=6):
        for cell in row:
            cell.number_format = "#,##0"
    ws.conditional_formatting.add(
        f"H5:H{last}",
        CellIsRule(operator="equal", formula=["0"], fill=PatternFill("solid", fgColor=DANGER_SOFT), font=Font(color=DANGER)),
    )
    ws.conditional_formatting.add(
        f"G5:G{last}",
        DataBarRule(start_type="min", end_type="max", color="155E8A"),
    )
    set_widths(ws, {"A": 16, "B": 12, "C": 14, "D": 12, "E": 10, "F": 12, "G": 12, "H": 11})


def build_reglas(wb: Workbook, data_dir: Path) -> None:
    ws = wb.create_sheet("Reglas")
    ws.sheet_properties.tabColor = BLUE
    title(ws, "Catálogo de reglas y SLA", "Reglas R01–R12 y tiempos objetivo por prioridad", width=7)
    rows = read_csv(data_dir / "dim_rule.csv")
    headers = ["rule_id", "rule_name", "severity", "base_score", "intended_pattern"]
    body = [[r["rule_id"], r["rule_name"], r["severity"], int(r["base_score"]), r["intended_pattern"]] for r in rows]
    last = write_rows(ws, headers, body, start_row=4)
    add_table(ws, "tblReglas", f"A4:E{last}")
    sla_start = last + 3
    ws.cell(row=sla_start, column=1, value="Prioridad").font = Font(bold=True, color=NAVY)
    ws.cell(row=sla_start, column=2, value="Asignación (min)").font = Font(bold=True, color=NAVY)
    ws.cell(row=sla_start, column=3, value="Cierre (días hábiles)").font = Font(bold=True, color=NAVY)
    style_header(ws[sla_start])
    sla = [("P1", 15, 10), ("P2", 240, 15), ("P3", 1440, 20)]
    for index, row in enumerate(sla, start=sla_start + 1):
        for col, value in enumerate(row, start=1):
            ws.cell(row=index, column=col, value=value)
    add_table(ws, "tblSLA", f"A{sla_start}:C{sla_start + len(sla)}")
    set_widths(ws, {"A": 12, "B": 46, "C": 12, "D": 12, "E": 20})


def build_simulador(wb: Workbook) -> None:
    ws = wb.create_sheet("Simulador")
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = WARN
    title(ws, "Simulador de comisiones", "Entradas con validación y resultados con fórmulas", width=5)
    inputs = [
        ("Tipo de transferencia", "LOCAL", "B4"),
        ("Moneda", "PYG", "B5"),
        ("Importe", 850000, "B6"),
        ("¿Cliente premium?", "NO", "B7"),
        ("Canal", "APP", "B8"),
    ]
    for index, (label, value, _) in enumerate(inputs, start=4):
        ws.cell(row=index, column=1, value=label).font = Font(bold=True, color=NAVY)
        ws.cell(row=index, column=2, value=value).fill = PatternFill("solid", fgColor=WARN_SOFT)
        ws.cell(row=index, column=2).border = BORDER
    results = [
        ("Comisión base", '=IF($B$4="LOCAL",MAX(Param_ComisionMinimaLocal_PYG,$B$6*Param_ComisionLocalPct),Param_ComisionIntlUSD*_xlfn.XLOOKUP("USD",tblTiposCambio[Moneda],tblTiposCambio[Tasa_PYG])/_xlfn.XLOOKUP($B$5,tblTiposCambio[Moneda],tblTiposCambio[Tasa_PYG]))', "#,##0.00"),
        ("Descuento premium", '=IF(AND($B$4="LOCAL",$B$7="SI"),B10*Param_DescuentoPremium,0)', "#,##0.00"),
        ("Comisión final", "=B10-B11", "#,##0.00"),
        ("Total a debitar", "=B6+B12", "#,##0.00"),
        ("Tope local", '=IF($B$4="LOCAL",IF($B$5<>"PYG","SOLO PYG",IF($B$6<=Param_TopeLocalPYG,"DENTRO","EXCEDE")),"N/A")', "General"),
        ("Tasa a PYG", '=_xlfn.XLOOKUP($B$5,tblTiposCambio[Moneda],tblTiposCambio[Tasa_PYG],"SIN DATO")', "#,##0.00"),
        ("Total estimado en PYG", "=B13*B15", "#,##0.00"),
    ]
    for index, (label, formula, number_format) in enumerate(results, start=10):
        ws.cell(row=index, column=1, value=label).font = Font(bold=True, color=NAVY)
        cell = ws.cell(row=index, column=2, value=formula)
        cell.number_format = number_format
        cell.fill = PatternFill("solid", fgColor=BG)
        cell.border = BORDER
    ws.cell(row=18, column=1, value="Escenarios de referencia").font = Font(bold=True, size=12, color=NAVY)
    scenario_headers = ["Escenario", "Tipo", "Moneda", "Importe", "Comisión", "Total", "Tope"]
    for col, header in enumerate(scenario_headers, start=1):
        ws.cell(row=19, column=col, value=header)
    style_header(ws[19])
    scenarios = [
        ("Local estándar", "LOCAL", "PYG", 850000),
        ("Local tope", "LOCAL", "PYG", 10000000),
        ("Local excedido", "LOCAL", "PYG", 12000000),
        ("Internacional USD", "INTERNACIONAL", "USD", 1250),
        ("Internacional EUR", "INTERNACIONAL", "EUR", 900),
    ]
    for index, (name, kind, currency, amount) in enumerate(scenarios, start=20):
        ws.cell(row=index, column=1, value=name)
        ws.cell(row=index, column=2, value=kind)
        ws.cell(row=index, column=3, value=currency)
        ws.cell(row=index, column=4, value=amount)
        ws.cell(row=index, column=5, value=f'=IF(B{index}="LOCAL",MAX(Param_ComisionMinimaLocal_PYG,D{index}*Param_ComisionLocalPct),Param_ComisionIntlUSD*_xlfn.XLOOKUP("USD",tblTiposCambio[Moneda],tblTiposCambio[Tasa_PYG])/_xlfn.XLOOKUP(C{index},tblTiposCambio[Moneda],tblTiposCambio[Tasa_PYG]))')
        ws.cell(row=index, column=6, value=f"=D{index}+E{index}")
        ws.cell(row=index, column=7, value=f'=IF(B{index}="LOCAL",IF(D{index}<=Param_TopeLocalPYG,"DENTRO","EXCEDE"),"N/A")')
        for col in (4, 5, 6):
            ws.cell(row=index, column=col).number_format = "#,##0.00"
    add_table(ws, "tblEscenarios", "A19:G24")
    ws.conditional_formatting.add(
        "G20:G24",
        CellIsRule(operator="equal", formula=['"EXCEDE"'], fill=PatternFill("solid", fgColor=DANGER_SOFT), font=Font(color=DANGER, bold=True)),
    )
    ws.conditional_formatting.add(
        "G20:G24",
        CellIsRule(operator="equal", formula=['"DENTRO"'], fill=PatternFill("solid", fgColor=OK_SOFT), font=Font(color=TEAL, bold=True)),
    )
    dv_tipo = DataValidation(type="list", formula1="Lista_Tipos", allow_blank=False, showErrorMessage=True, errorTitle="Tipo inválido", error="Seleccione LOCAL o INTERNACIONAL.")
    dv_moneda = DataValidation(type="list", formula1="Lista_Monedas", allow_blank=False, showErrorMessage=True, errorTitle="Moneda inválida", error="Seleccione PYG, USD o EUR.")
    dv_sino = DataValidation(type="list", formula1="Lista_SiNo", allow_blank=False, showErrorMessage=True, errorTitle="Valor inválido", error="Seleccione SI o NO.")
    dv_importe = DataValidation(type="decimal", operator="greaterThan", formula1="0", allow_blank=False,
                                showErrorMessage=True, error="El importe debe ser mayor que cero.", errorTitle="Importe inválido")
    dv_canal = DataValidation(type="list", formula1='"APP,WEB,API,BRANCH"', allow_blank=False, showErrorMessage=True, errorTitle="Canal inválido", error="Seleccione APP, WEB, API o BRANCH.")
    ws.add_data_validation(dv_tipo)
    ws.add_data_validation(dv_moneda)
    ws.add_data_validation(dv_sino)
    ws.add_data_validation(dv_importe)
    ws.add_data_validation(dv_canal)
    dv_tipo.add("B4")
    dv_moneda.add("B5")
    dv_importe.add("B6")
    dv_sino.add("B7")
    dv_canal.add("B8")
    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 22
    set_widths(ws, {"C": 14, "D": 14, "E": 16, "F": 16, "G": 12})


def build_kpis(wb: Workbook) -> None:
    ws = wb.create_sheet("KPIs", 1)
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = TEAL
    title(ws, "Tablero de KPIs", "Fórmulas recalculadas por Excel sobre las tablas del workbook", width=8)
    cards = [
        ("Operaciones totales", "=B7", "#,##0", "B3:C4"),
        ("STP local", "=B11", "0.0%", "D3:E4"),
        ("p95 latencia local", "=B13", "#,##0", "F3:G4"),
        ("Falsos positivos", "=B18", "0.0%", "H3:I4"),
    ]
    for label, formula, number_format, merge in cards:
        start, end = merge.split(":")
        label_end_col = end[0]
        label_row = start[1:]
        ws.merge_cells(f"{start}:{label_end_col}{label_row}")
        cell = ws[start]
        cell.value = label
        cell.font = Font(bold=True, color=MUTED, size=10)
        cell.alignment = Alignment(vertical="center", indent=1)
        cell.fill = PatternFill("solid", fgColor=BG)
        value_row = int(start[1:]) + 1
        value_col = start[0]
        vcell = ws[f"{value_col}{value_row}"]
        vcell.value = formula
        vcell.font = Font(bold=True, size=20, color=NAVY)
        vcell.number_format = number_format
        vcell.alignment = Alignment(vertical="center", indent=1)
        vcell.fill = PatternFill("solid", fgColor=BG)

    headers = ["KPI", "Valor", "Meta", "Direccion", "Estado", "Unidad", "Definicion"]
    for col, header in enumerate(headers, start=1):
        ws.cell(row=6, column=col, value=header)
    style_header(ws[6])
    kpis = [
        ("Operaciones totales", "=SUM(tblHechosDiarios[Operaciones])", "", "", "operaciones", "Suma de operaciones del período."),
        ("Volumen PYG", '=SUMIFS(tblHechosDiarios[Importe],tblHechosDiarios[Moneda],"PYG")', "", "", "PYG", "Importe operado en guaraníes."),
        ("Volumen USD", '=SUMIFS(tblHechosDiarios[Importe],tblHechosDiarios[Moneda],"USD")', "", "", "USD", "Importe operado en dólares."),
        ("Ticket promedio PYG", '=IFERROR(B8/SUMIFS(tblHechosDiarios[Operaciones],tblHechosDiarios[Moneda],"PYG"),0)', "", "", "PYG", "Volumen PYG / operaciones PYG."),
        ("STP local", "=IFERROR(SUM(tblHechosDiarios[STP])/SUM(tblHechosDiarios[Operaciones]),0)", "=Param_Meta_STP", "MAX", "%", "Operaciones sin alerta AML asociada (proxy)."),
        ("Operaciones locales", '=SUMIFS(tblHechosDiarios[Operaciones],tblHechosDiarios[Moneda],"PYG")', "", "", "operaciones", "Operaciones en PYG."),
        ("p95 latencia local", "=PERCENTILE(tblPagosLocal[latency_ms],0.95)", "=Param_SLA_Instantaneo_ms", "MIN", "ms", "Percentil 95 de latencia sintética."),
        ("Pagos locales ≤ 5 s", "=AVERAGE(tblPagosLocal[within_sla])", "=Param_Meta_STP", "MAX", "%", "Proporción dentro del SLA objetivo."),
        ("Alertas totales", "=COUNTA(tblAlertas[alert_id])", "", "", "alertas", "Alertas deduplicadas."),
        ("Alertas P1", '=COUNTIF(tblAlertas[prioridad],"P1")', "", "", "alertas", "Alertas de prioridad 1."),
        ("P1 asignadas a tiempo", '=IFERROR(COUNTIFS(tblAlertas[prioridad],"P1",tblAlertas[assignment_minutes],">=0",tblAlertas[assignment_minutes],"<=15")/COUNTIF(tblAlertas[prioridad],"P1"),0)', "=Param_Meta_P1_a_tiempo", "MAX", "%", "Asignación dentro de 15 minutos."),
        ("Falsos positivos", "=IFERROR(SUM(tblAlertas[is_false_positive])/SUM(tblAlertas[is_closed]),0)", "=Param_Meta_FalsosPositivos", "MIN", "%", "Cierres FP / alertas cerradas."),
        ("Casos totales", "=COUNTA(tblCasos[case_id])", "", "", "casos", "Casos abiertos en el dataset."),
        ("Casos cerrados", '=COUNTIF(tblCasos[status],"CERRADO")+COUNTIF(tblCasos[status],"REPORTADO")', "", "", "casos", "Casos en estado terminal."),
        ("Casos en plazo", "=IFERROR(SUM(tblCasos[is_on_time_close])/SUM(tblCasos[is_closed]),0)", "=Param_Meta_P1_a_tiempo", "MAX", "%", "Cierres antes del vencimiento."),
        ("Conciliación cuadrada", '=IFERROR(COUNTIF(tblConciliacion[Resultado],"CUADRADO")/COUNTA(tblConciliacion[Clave]),0)', "=Param_Meta_Conciliacion", "MAX", "%", "Filas fecha/moneda con débitos = créditos."),
        ("Diferencia total libro", "=SUM(tblConciliacion[Diferencia])", 0, "ABS", "PYG/USD", "Suma de diferencias; debe ser 0."),
    ]
    for index, (name, formula, meta, direction, unit, definition) in enumerate(kpis, start=7):
        ws.cell(row=index, column=1, value=name).font = Font(bold=True)
        value_cell = ws.cell(row=index, column=2, value=formula)
        value_cell.number_format = "0.00%" if unit == "%" else ("#,##0.00" if unit in {"PYG", "USD", "PYG/USD", "ms"} else "#,##0")
        ws.cell(row=index, column=3, value=meta)
        ws.cell(row=index, column=4, value=direction)
        status = ws.cell(row=index, column=5)
        status.value = (
            f'=IF($C{index}="","",IF($D{index}="MAX",IF($B{index}>=$C{index},"CUMPLE","NO CUMPLE"),'
            f'IF($D{index}="MIN",IF($B{index}<=$C{index},"CUMPLE","NO CUMPLE"),'
            f'IF(ABS($B{index})<=$C{index},"CUMPLE","NO CUMPLE"))))'
        )
        ws.cell(row=index, column=6, value=unit)
        ws.cell(row=index, column=7, value=definition)
        for col in range(1, 8):
            ws.cell(row=index, column=col).border = BORDER
    last_kpi = 6 + len(kpis)
    add_table(ws, "tblKPIs", f"A6:G{last_kpi}")
    ws.conditional_formatting.add(
        f"E7:E{last_kpi}",
        CellIsRule(operator="equal", formula=['"NO CUMPLE"'], fill=PatternFill("solid", fgColor=DANGER_SOFT), font=Font(color=DANGER, bold=True)),
    )
    ws.conditional_formatting.add(
        f"E7:E{last_kpi}",
        CellIsRule(operator="equal", formula=['"CUMPLE"'], fill=PatternFill("solid", fgColor=OK_SOFT), font=Font(color=TEAL, bold=True)),
    )
    ws.conditional_formatting.add(
        f"B7:B{last_kpi}",
        ColorScaleRule(start_type="min", start_color="FEE2E2", mid_type="percentile", mid_value=50, mid_color="FEF3C7", end_type="max", end_color="CCFBF1"),
    )
    set_widths(ws, {"A": 25, "B": 18, "C": 12, "D": 11, "E": 14, "F": 12, "G": 52})
    ws.freeze_panes = "A7"


def build_workbook(data_dir: Path, out_path: Path) -> Path:
    wb = Workbook()
    build_portada(wb)
    build_kpis(wb)
    build_parametros(wb)
    build_conciliacion(wb, data_dir)
    build_hechos(wb, data_dir)
    build_libro(wb, data_dir)
    build_alertas(wb, data_dir)
    build_casos(wb, data_dir)
    build_pagos_local(wb, data_dir)
    build_simulador(wb)
    build_reglas(wb, data_dir)
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"
    wb.properties.title = "NovaBank · Analítica de pagos y cumplimiento"
    wb.properties.creator = "Franco Tillería Centurión"
    wb.properties.description = "Workbook avanzado del caso ficticio NovaBank. Fórmulas reales y datos sintéticos."
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera el workbook Excel de NovaBank")
    parser.add_argument("--data", default=str(DEFAULT_DATA), help="Carpeta con los CSV")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Ruta del .xlsx")
    args = parser.parse_args()
    path = build_workbook(Path(args.data), Path(args.out))
    print(f"Workbook generado: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
