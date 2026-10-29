"""Pruebas del parser MT103 y del mapeo funcional a pacs.008."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from validator.mapping import (
    CHARGE_TO_ISO,
    ISO_TO_CHARGE,
    MAPPING_ROWS,
    mt103_to_pacs008_fields,
    pacs008_to_mt103_fields,
)
from validator.mt103 import parse_mt103, validate_mt103

MT103 = """{1:F01NOVAPYPAXXXX0000000000}{2:I103NOVBGB2LXXXXN}{4:
:20:NOVA-2026-0001
:23B:CRED
:32A:261028USD1250,00
:50K:/00000000000001
ANA DEMO
ASUNCION
:52A:NOVAPYPA
:57A:NOVBGB2L
:59:/GB29NWBK60161331926819
JOHN DEMO
LONDON
:70:INVOICE 2026-001
:71A:SHA
-}
"""


def test_parse_mt103() -> None:
    message = parse_mt103(MT103)
    assert message.sender_reference == "NOVA-2026-0001"
    assert message.value_date == date(2026, 10, 28)
    assert message.currency == "USD"
    assert message.amount == Decimal("1250.00")
    assert message.ordering_customer.name == "ANA DEMO"
    assert message.ordering_customer.account == "00000000000001"
    assert message.beneficiary.name == "JOHN DEMO"
    assert message.beneficiary.account == "GB29NWBK60161331926819"
    assert message.ordering_institution_bic == "NOVAPYPA"
    assert message.beneficiary_institution_bic == "NOVBGB2L"
    assert message.charge_bearer == "SHA"


def test_validate_mt103() -> None:
    assert validate_mt103(MT103).valid


def test_mt103_campo_faltante() -> None:
    result = validate_mt103(MT103.replace(":71A:SHA\n", ""))
    assert not result.valid
    assert result.issues[0].code == "MT103_REQUIRED"


def test_mt103_charge_bearer_invalido() -> None:
    result = validate_mt103(MT103.replace(":71A:SHA", ":71A:XXX"))
    assert not result.valid
    assert "MT103_CHARGE_BEARER" in {issue.code for issue in result.issues}


def test_mt103_beneficiario_iban_invalido() -> None:
    result = validate_mt103(MT103.replace("GB29NWBK60161331926819", "GB28NWBK60161331926819"))
    assert not result.valid
    assert "IBAN_CHECKSUM" in {issue.code for issue in result.issues}


def test_mt103_a_pacs008() -> None:
    message = parse_mt103(MT103)
    payload = mt103_to_pacs008_fields(message, uetr="123e4567-e89b-42d3-a456-426614174000")
    assert payload["message_id"] == "MSG-NOVA-2026-0001"
    assert payload["instruction_id"] == "NOVA-2026-0001"
    assert payload["end_to_end_id"] == "NOVA-2026-0001"
    assert payload["interbank_settlement_amount"] == {"currency": "USD", "value": "1250.00"}
    assert payload["interbank_settlement_date"] == "2026-10-28"
    assert payload["debtor"]["account"] == "00000000000001"
    assert payload["creditor"]["account"] == "GB29NWBK60161331926819"
    assert payload["charge_bearer"] == "SHAR"
    assert payload["uetr"] == "123e4567-e89b-42d3-a456-426614174000"


def test_pacs008_a_mt103() -> None:
    payload = {
        "end_to_end_id": "NOVA-2026-0001",
        "instruction_id": "NOVA-2026-0001",
        "settlement_date": "2026-10-28",
        "amount": "1250.00",
        "currency": "USD",
        "debtor_name": "ANA DEMO",
        "debtor_account": "00000000000001",
        "debtor_bic": "NOVAPYPA",
        "creditor_name": "JOHN DEMO",
        "creditor_account": "GB29NWBK60161331926819",
        "creditor_bic": "NOVBGB2L",
        "charge_bearer": "SHAR",
        "remittance_information": "INVOICE 2026-001",
    }
    fields = pacs008_to_mt103_fields(payload)
    assert fields["20"] == "NOVA-2026-0001"
    assert fields["32A"] == "261028USD1250,00"
    assert fields["71A"] == "SHA"
    assert fields["52A"] == "NOVAPYPA"
    assert fields["57A"] == "NOVBGB2L"
    assert fields["50K"][0] == "/00000000000001"


def test_mapeo_charge_bearer() -> None:
    assert CHARGE_TO_ISO == {"OUR": "DEBT", "SHA": "SHAR", "BEN": "CRED"}
    assert ISO_TO_CHARGE["DEBT"] == "OUR"
    assert any(row["mt103_field"] == "32A" for row in MAPPING_ROWS)


def test_mt103_fecha_invalida() -> None:
    with pytest.raises(ValueError):
        parse_mt103(MT103.replace("261028", "261032"))
