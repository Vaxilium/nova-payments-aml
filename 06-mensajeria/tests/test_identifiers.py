"""Pruebas de IBAN, BIC, referencias y UETR."""

from __future__ import annotations

import pytest

from validator.identifiers import (
    calculate_iban_check_digits,
    is_valid_bic,
    is_valid_iban,
    make_iban,
    make_uetr,
    validate_bic,
    validate_iban,
    validate_reference,
    validate_uetr,
)


@pytest.mark.parametrize(
    "iban",
    [
        "DE89370400440532013000",
        "GB29NWBK60161331926819",
        "ES9121000418450200051332",
        "FR7630006000011234567890189",
        "NL91ABNA0417164300",
        "DE89 3704 0044 0532 0130 00",
    ],
)
def test_iban_validos(iban: str) -> None:
    assert validate_iban(iban).valid
    assert is_valid_iban(iban)


def test_iban_checksum_invalido() -> None:
    result = validate_iban("DE88370400440532013000")
    assert not result.valid
    assert {issue.code for issue in result.issues} == {"IBAN_CHECKSUM"}


def test_iban_longitud_por_pais() -> None:
    result = validate_iban("DE8937040044053201300")
    assert not result.valid
    assert result.issues[0].code == "IBAN_LENGTH"


def test_iban_pais_no_soportado() -> None:
    synthetic_py = make_iban("PY", "00000000000000000000")
    result = validate_iban(synthetic_py)
    assert not result.valid
    assert result.issues[0].code == "IBAN_COUNTRY_UNSUPPORTED"


def test_iban_calculo_control_ida_y_vuelta() -> None:
    assert calculate_iban_check_digits("DE", "370400440532013000") == "89"
    assert make_iban("GB", "NWBK60161331926819") == "GB29NWBK60161331926819"


def test_iban_vacio() -> None:
    assert validate_iban("").issues[0].code == "IBAN_REQUIRED"


@pytest.mark.parametrize("bic", ["NOVAPYPA", "NOVBUS33", "NOVBDEFFXXX", "NOVBGB2L"])
def test_bic_valido(bic: str) -> None:
    assert validate_bic(bic).valid
    assert is_valid_bic(bic)


@pytest.mark.parametrize("bic", ["NOVA", "NOVAPYP", "NOVAPYPAXX", "NOV1PYPA", "NOVAPYPAXXXX"])
def test_bic_invalido(bic: str) -> None:
    assert not validate_bic(bic).valid


def test_bic_pais_reservado() -> None:
    assert not validate_bic("NOVAXXPA").valid


def test_bic_requerido() -> None:
    assert validate_bic("", required=True).issues[0].code == "BIC_REQUIRED"
    assert validate_bic("", required=False).valid


def test_referencia_max35() -> None:
    assert validate_reference("NOVA-2026-0001").valid
    assert validate_reference("X" * 36).issues[0].code == "REFERENCE_LENGTH"
    assert validate_reference("NOVA&2026").issues[0].code == "REFERENCE_CHARSET"
    assert validate_reference(" NOVA").issues[0].code == "REFERENCE_WHITESPACE"


def test_reference_long_text() -> None:
    assert validate_reference("A" * 100, max_length=140).valid
    assert validate_reference("A" * 141, max_length=140).issues[0].code == "REFERENCE_LENGTH"


def test_uetr() -> None:
    uetr = make_uetr()
    assert validate_uetr(uetr).valid
    assert not validate_uetr("00000000-0000-0000-0000-000000000000").valid
    assert validate_uetr("", required=True).issues[0].code == "UETR_REQUIRED"
