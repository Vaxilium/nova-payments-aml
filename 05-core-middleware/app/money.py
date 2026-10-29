"""Conversión entre importes decimales y unidades menores.

La base guarda enteros en la unidad menor de cada moneda para que las sumas
contables sean exactas: PYG no tiene decimales y USD usa centavos.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

MINOR_UNITS: dict[str, int] = {"PYG": 0, "USD": 2}
CURRENCY_NAMES: dict[str, str] = {
    "PYG": "Guaraní paraguayo",
    "USD": "Dólar estadounidense",
}
CURRENCY_SYMBOLS: dict[str, str] = {"PYG": "₲", "USD": "US$"}


def minor_unit(currency: str) -> int:
    try:
        return MINOR_UNITS[currency.upper()]
    except KeyError as exc:
        raise ValueError(f"Moneda no soportada: {currency}") from exc


def to_minor(amount: Decimal | int | float | str, currency: str) -> int:
    """Convierte un importe decimal a la unidad menor de la moneda."""
    scale = minor_unit(currency)
    quantum = Decimal(1).scaleb(-scale)
    value = Decimal(str(amount)).quantize(quantum, rounding=ROUND_HALF_UP)
    if value <= 0:
        raise ValueError("El importe debe ser mayor que cero")
    return int(value.scaleb(scale))


def from_minor(value: int, currency: str) -> Decimal:
    """Convierte unidades menores al importe decimal de la moneda."""
    return Decimal(int(value)).scaleb(-minor_unit(currency))


def format_money(value: int, currency: str) -> str:
    """Formatea un importe en unidades menores con los decimales de la moneda."""
    scale = minor_unit(currency)
    return f"{from_minor(value, currency):.{scale}f}"
