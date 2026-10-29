"""Validación de identificadores financieros: IBAN, BIC y referencias."""

from __future__ import annotations

import re
import uuid

from .validation import ValidationResult

# Longitudes del registro IBAN consultado (F-14). Se incluyen los países usados
# en el caso y una selección de países con formatos públicos estables.
IBAN_LENGTHS: dict[str, int] = {
    "AD": 24,
    "AE": 23,
    "AL": 28,
    "AT": 20,
    "AZ": 28,
    "BA": 20,
    "BE": 16,
    "BG": 22,
    "BH": 22,
    "BR": 29,
    "BY": 28,
    "CH": 21,
    "CR": 22,
    "CY": 28,
    "CZ": 24,
    "DE": 22,
    "DK": 18,
    "DO": 28,
    "EE": 20,
    "EG": 29,
    "ES": 24,
    "FI": 18,
    "FO": 18,
    "FR": 27,
    "GB": 22,
    "GE": 22,
    "GI": 23,
    "GL": 18,
    "GR": 27,
    "GT": 28,
    "HR": 21,
    "HU": 28,
    "IE": 22,
    "IL": 23,
    "IQ": 23,
    "IS": 26,
    "IT": 27,
    "JO": 30,
    "KW": 30,
    "KZ": 20,
    "LB": 28,
    "LC": 32,
    "LI": 21,
    "LT": 20,
    "LU": 20,
    "LV": 21,
    "MC": 27,
    "MD": 24,
    "ME": 22,
    "MK": 19,
    "MR": 27,
    "MT": 31,
    "MU": 30,
    "NL": 18,
    "NO": 15,
    "PK": 24,
    "PL": 28,
    "PS": 29,
    "PT": 25,
    "QA": 29,
    "RO": 24,
    "RS": 22,
    "SA": 24,
    "SC": 31,
    "SE": 24,
    "SI": 19,
    "SK": 24,
    "SM": 27,
    "ST": 25,
    "SV": 28,
    "TL": 23,
    "TN": 24,
    "TR": 26,
    "UA": 29,
    "VA": 22,
    "VG": 24,
    "XK": 20,
}

_IBAN_PATTERN = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}$")
_BIC_PATTERN = re.compile(r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$")
_REFERENCE_ALLOWED = r"[A-Za-z0-9/+?\-:().,' ]"
_UETR_PATTERN = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)


def normalize_iban(value: str) -> str:
    return re.sub(r"\s+", "", value).upper()


def normalize_bic(value: str) -> str:
    return value.strip().upper()


def calculate_iban_check_digits(country_code: str, bban: str) -> str:
    """Calcula los dos dígitos de control con MOD 97-10 (ISO/IEC 7064)."""
    country = country_code.strip().upper()
    body = bban.strip().upper()
    if len(country) != 2 or not country.isalpha():
        raise ValueError("El código de país debe tener dos letras")
    if not body.isalnum():
        raise ValueError("El BBAN solo admite letras y dígitos")
    rearranged = body + country + "00"
    numeric = "".join(str(int(char, 36)) for char in rearranged)
    remainder = int(numeric) % 97
    return f"{98 - remainder:02d}"


def make_iban(country_code: str, bban: str) -> str:
    return f"{country_code.upper()}{calculate_iban_check_digits(country_code, bban)}{bban.upper()}"


def validate_iban(value: str, *, field: str = "iban") -> ValidationResult:
    result = ValidationResult()
    iban = normalize_iban(value)
    if not iban:
        result.add("IBAN_REQUIRED", field, "El IBAN es obligatorio")
        return result
    if not _IBAN_PATTERN.fullmatch(iban):
        result.add("IBAN_FORMAT", field, "El IBAN debe comenzar con dos letras y dos dígitos y tener entre 15 y 34 caracteres alfanuméricos")
        return result
    country = iban[:2]
    expected = IBAN_LENGTHS.get(country)
    if expected is None:
        result.add("IBAN_COUNTRY_UNSUPPORTED", field, f"El país {country} no está en la tabla IBAN soportada")
        return result
    if len(iban) != expected:
        result.add("IBAN_LENGTH", field, f"El IBAN de {country} debe tener {expected} caracteres; se recibieron {len(iban)}")
        return result
    rearranged = iban[4:] + iban[:4]
    try:
        numeric = "".join(str(int(char, 36)) for char in rearranged)
        check_ok = int(numeric) % 97 == 1
    except ValueError:
        check_ok = False
    if not check_ok:
        result.add("IBAN_CHECKSUM", field, "Los dígitos de control del IBAN no son válidos (MOD 97-10)")
    return result


def is_valid_iban(value: str) -> bool:
    return validate_iban(value).valid


def validate_bic(value: str, *, field: str = "bic", required: bool = True) -> ValidationResult:
    result = ValidationResult()
    bic = normalize_bic(value)
    if not bic:
        if required:
            result.add("BIC_REQUIRED", field, "El BIC es obligatorio")
        return result
    if not _BIC_PATTERN.fullmatch(bic):
        result.add("BIC_FORMAT", field, "El BIC debe tener 8 u 11 caracteres: 4 letras, 2 letras de país y 2 alfanuméricos, más una rama opcional de 3")
        return result
    country = bic[4:6]
    if not country.isalpha():
        result.add("BIC_COUNTRY", field, "El código de país del BIC debe ser alfabético")
    if country in {"XX", "ZZ"}:
        result.add("BIC_COUNTRY", field, "El código de país del BIC no es válido para el caso")
    return result


def is_valid_bic(value: str) -> bool:
    return validate_bic(value).valid


def validate_reference(
    value: str,
    *,
    field: str = "reference",
    max_length: int = 35,
    required: bool = True,
) -> ValidationResult:
    result = ValidationResult()
    reference = value if isinstance(value, str) else ""
    if not reference.strip():
        if required:
            result.add("REFERENCE_REQUIRED", field, "La referencia es obligatoria")
        return result
    if len(reference) > max_length:
        result.add("REFERENCE_LENGTH", field, f"La referencia supera {max_length} caracteres")
    if reference != reference.strip():
        result.add("REFERENCE_WHITESPACE", field, "La referencia no debe comenzar ni terminar con espacios")
    pattern = re.compile(rf"^[A-Za-z0-9]{_REFERENCE_ALLOWED}{{0,{max(0, max_length - 1)}}}$")
    if not pattern.fullmatch(reference):
        result.add("REFERENCE_CHARSET", field, "La referencia contiene caracteres no admitidos o supera el largo permitido")
    return result


def validate_uetr(value: str, *, field: str = "uetr", required: bool = False) -> ValidationResult:
    result = ValidationResult()
    uetr = value.strip() if isinstance(value, str) else ""
    if not uetr:
        if required:
            result.add("UETR_REQUIRED", field, "El UETR es obligatorio")
        return result
    if not _UETR_PATTERN.fullmatch(uetr):
        result.add("UETR_FORMAT", field, "El UETR debe ser un UUID versión 4 en formato canónico")
    return result


def make_uetr() -> str:
    return str(uuid.uuid4())


__all__ = [
    "IBAN_LENGTHS",
    "calculate_iban_check_digits",
    "is_valid_bic",
    "is_valid_iban",
    "make_iban",
    "make_uetr",
    "normalize_bic",
    "normalize_iban",
    "validate_bic",
    "validate_iban",
    "validate_reference",
    "validate_uetr",
]
