"""Validación y conversión de importes monetarios ISO 4217."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

from .iso4217 import ISO_4217_MINOR, minor_unit, normalize_currency
from .validation import ValidationResult

MAX_AMOUNT = Decimal("999999999999999.9999")


def decimal_value(value: str | int | float | Decimal) -> Decimal:
    """Convierte a Decimal sin pasar por binario cuando el valor es textual."""
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Importe no numérico: {value!r}") from exc
    if not amount.is_finite():
        raise ValueError("El importe debe ser un número finito")
    return amount


def validate_amount(
    value: str | int | float | Decimal,
    currency: str,
    *,
    field: str = "amount",
    max_amount: Decimal | None = MAX_AMOUNT,
) -> ValidationResult:
    result = ValidationResult()
    code = normalize_currency(currency)
    if code not in ISO_4217_MINOR:
        result.add("CURRENCY_UNKNOWN", f"{field}.currency", f"Código ISO 4217 desconocido: {currency}")
        return result
    scale = minor_unit(code)
    if scale is None:
        result.add(
            "CURRENCY_NO_MINOR_UNIT",
            f"{field}.currency",
            f"{code} no tiene una unidad menor monetaria utilizable para importes",
        )
        return result
    try:
        amount = decimal_value(value)
    except ValueError as exc:
        result.add("AMOUNT_FORMAT", field, str(exc))
        return result
    if amount <= 0:
        result.add("AMOUNT_NOT_POSITIVE", field, "El importe debe ser mayor que cero")
    if max_amount is not None and amount > max_amount:
        result.add("AMOUNT_TOO_LARGE", field, f"El importe supera el máximo de {max_amount}")
    quantum = Decimal(1).scaleb(-scale)
    try:
        quantized = amount.quantize(quantum)
    except InvalidOperation:
        result.add("AMOUNT_PRECISION", field, f"No se pudo redondear el importe a {scale} decimales")
        return result
    if quantized != amount:
        result.add(
            "AMOUNT_PRECISION",
            field,
            f"El importe de {code} admite como máximo {scale} decimales",
        )
    return result


def to_minor(value: str | int | float | Decimal, currency: str) -> int:
    """Convierte un importe válido a la unidad menor de la moneda."""
    scale = minor_unit(currency)
    if scale is None:
        raise ValueError(f"{currency} no admite importes monetarios")
    amount = decimal_value(value)
    if amount <= 0:
        raise ValueError("El importe debe ser mayor que cero")
    quantum = Decimal(1).scaleb(-scale)
    if amount.quantize(quantum) != amount:
        raise ValueError(f"El importe de {currency} admite como máximo {scale} decimales")
    return int(amount.scaleb(scale))


def from_minor(value: int, currency: str) -> Decimal:
    scale = minor_unit(currency)
    if scale is None:
        raise ValueError(f"{currency} no admite importes monetarios")
    return Decimal(int(value)).scaleb(-scale)


def format_amount(value: int, currency: str) -> str:
    scale = minor_unit(currency) or 0
    return f"{from_minor(value, currency):.{scale}f}"


__all__ = [
    "MAX_AMOUNT",
    "decimal_value",
    "format_amount",
    "from_minor",
    "to_minor",
    "validate_amount",
]
