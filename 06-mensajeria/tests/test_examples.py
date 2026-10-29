"""Verifica que los artefactos de ejemplo publicados sean válidos y consistentes."""

from __future__ import annotations

import csv
from pathlib import Path

from validator.mapping import MAPPING_ROWS, mt103_to_pacs008_fields
from validator.mt103 import parse_mt103, validate_mt103
from validator.xml_messages import validate_message, validate_pacs008_international

BASE = Path(__file__).resolve().parents[1]
ISO_DIR = BASE / "examples" / "iso20022"


def test_ejemplos_iso20022_validos() -> None:
    for name in (
        "pacs.008-customer-credit-transfer.xml",
        "pacs.002-payment-status-report-acsc.xml",
        "pacs.002-payment-status-report-rjct.xml",
        "pain.001-customer-credit-transfer.xml",
        "camt.053-bank-to-customer-statement.xml",
    ):
        result = validate_message(ISO_DIR / name)
        assert result.valid, (name, [issue.as_dict() for issue in result.issues])


def test_ejemplo_pacs008_internacional() -> None:
    result = validate_pacs008_international(ISO_DIR / "pacs.008-customer-credit-transfer.xml")
    assert result.valid, [issue.as_dict() for issue in result.issues]


def test_ejemplo_mt103_valido_y_mapeable() -> None:
    path = BASE / "examples" / "mt" / "mt103-international-transfer.txt"
    text = path.read_text(encoding="utf-8")
    assert validate_mt103(text).valid
    fields = mt103_to_pacs008_fields(parse_mt103(text))
    assert fields["charge_bearer"] == "SHAR"
    assert fields["creditor"]["account"] == "DE89370400440532013000"


def test_csv_de_mapeo_completo() -> None:
    path = BASE / "mapping" / "mt103-pacs008.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == len(MAPPING_ROWS)
    assert set(rows[0]) == {"mt103_field", "iso_path", "direction", "notes"}
    assert any("71A" in row["mt103_field"] for row in rows)
