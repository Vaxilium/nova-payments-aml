"""Pruebas de ISO 4217 y precisión de importes."""

from __future__ import annotations

from decimal import Decimal

import pytest

from validator.amounts import format_amount, from_minor, to_minor, validate_amount
from validator.iso4217 import ISO_4217_MINOR, is_iso4217, minor_unit


def test_tabla_iso4217_generada() -> None:
    assert len(ISO_4217_MINOR) >= 170
    assert minor_unit("PYG") == 0
    assert minor_unit("USD") == 2
    assert minor_unit("EUR") == 2
    assert minor_unit("BHD") == 3
    assert minor_unit("XAU") is None
    assert is_iso4217("pyg")
    assert not is_iso4217("ZZZ")


@pytest.mark.parametrize(
    ("amount", "currency"),
    [("1000", "PYG"), ("10.50", "USD"), ("10.5", "USD"), ("1.230", "USD"), ("100000000", "PYG")],
)
def test_importes_validos(amount: str, currency: str) -> None:
    assert validate_amount(amount, currency).valid


@pytest.mark.parametrize(
    ("amount", "currency", "code"),
    [
        ("10.5", "PYG", "AMOUNT_PRECISION"),
        ("10.555", "USD", "AMOUNT_PRECISION"),
        ("0", "USD", "AMOUNT_NOT_POSITIVE"),
        ("-1", "USD", "AMOUNT_NOT_POSITIVE"),
        ("abc", "USD", "AMOUNT_FORMAT"),
        ("1", "ZZZ", "CURRENCY_UNKNOWN"),
        ("1", "XAU", "CURRENCY_NO_MINOR_UNIT"),
        ("9999999999999999", "USD", "AMOUNT_TOO_LARGE"),
    ],
)
def test_importes_invalidos(amount: str, currency: str, code: str) -> None:
    result = validate_amount(amount, currency)
    assert not result.valid
    assert code in {issue.code for issue in result.issues}


def test_conversion_unidad_menor() -> None:
    assert to_minor("1000", "PYG") == 1000
    assert to_minor("10.50", "USD") == 1050
    assert to_minor(Decimal("0.01"), "USD") == 1
    assert from_minor(1050, "USD") == Decimal("10.50")
    assert format_amount(1050, "USD") == "10.50"
    assert format_amount(1000, "PYG") == "1000"


def test_conversion_rechaza_exceso_decimales() -> None:
    with pytest.raises(ValueError):
        to_minor("10.555", "USD")
    with pytest.raises(ValueError):
        to_minor("10.5", "PYG")
