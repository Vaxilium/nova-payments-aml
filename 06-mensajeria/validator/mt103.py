"""Lectura y validación básica de MT103 (Single Customer Credit Transfer).

El parser cubre los campos usados por el caso. No sustituye un motor SWIFT ni
una guía de traducción certificada (S-064, SNV-09).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation
import re

from .amounts import validate_amount
from .identifiers import validate_bic, validate_iban, validate_reference
from .iso4217 import normalize_currency
from .validation import ValidationResult

_FIELD_RE = re.compile(r"^:([0-9]{2}[A-Z]?):(.*)$")
_32A_RE = re.compile(r"^(\d{6})([A-Z]{3})([0-9]+(?:[.,][0-9]+)?)$")
_BIC_RE = re.compile(r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$")


@dataclass(frozen=True)
class MT103Party:
    account: str | None
    name: str | None
    address: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class MT103:
    sender_reference: str
    bank_operation_code: str
    value_date: date
    currency: str
    amount: Decimal
    ordering_customer: MT103Party
    beneficiary: MT103Party
    remittance_information: str | None
    charge_bearer: str
    ordering_institution_bic: str | None = None
    beneficiary_institution_bic: str | None = None
    fields: dict[str, str] = field(default_factory=dict)


def _parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = raw_line.rstrip()
        if line.startswith("{") or line.strip() in {"-}", "}"}:
            continue
        match = _FIELD_RE.match(line)
        if match:
            current = match.group(1)
            fields.setdefault(current, []).append(match.group(2).strip())
            continue
        if current and line.strip():
            fields[current].append(line.strip())
    return {key: "\n".join(value).strip() for key, value in fields.items()}


def _parse_party(value: str | None) -> MT103Party:
    if not value:
        return MT103Party(account=None, name=None)
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    account: str | None = None
    name: str | None = None
    address: list[str] = []
    for line in lines:
        if account is None and line.startswith("/"):
            account = line[1:].strip() or None
        elif name is None:
            name = line
        else:
            address.append(line)
    return MT103Party(account=account, name=name, address=tuple(address))


def _parse_32a(value: str) -> tuple[date, str, Decimal]:
    compact = value.replace(" ", "")
    match = _32A_RE.fullmatch(compact)
    if not match:
        raise ValueError("El campo 32A debe tener fecha YYMMDD, moneda ISO y valor")
    yymmdd, currency, amount_text = match.groups()
    try:
        value_date = date(2000 + int(yymmdd[:2]), int(yymmdd[2:4]), int(yymmdd[4:6]))
    except ValueError as exc:
        raise ValueError("La fecha del campo 32A no es válida") from exc
    try:
        amount = Decimal(amount_text.replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError("El importe del campo 32A no es numérico") from exc
    return value_date, normalize_currency(currency), amount


def _first_bic(value: str | None) -> str | None:
    if not value:
        return None
    for line in value.splitlines():
        candidate = line.strip().upper()
        if _BIC_RE.fullmatch(candidate):
            return candidate
    return None


def parse_mt103(text: str) -> MT103:
    """Parsea un MT103 y falla si faltan los campos mínimos del caso."""
    fields = _parse_fields(text)
    missing = [name for name in ("20", "32A", "50K", "59", "71A") if name not in fields]
    if missing:
        raise ValueError(f"Faltan campos MT103 obligatorios: {', '.join(missing)}")
    value_date, currency, amount = _parse_32a(fields["32A"])
    return MT103(
        sender_reference=fields["20"].splitlines()[0].strip(),
        bank_operation_code=fields.get("23B", "CRED").splitlines()[0].strip() or "CRED",
        value_date=value_date,
        currency=currency,
        amount=amount,
        ordering_customer=_parse_party(fields["50K"]),
        beneficiary=_parse_party(fields["59"]),
        remittance_information=fields.get("70"),
        charge_bearer=fields["71A"].splitlines()[0].strip().upper(),
        ordering_institution_bic=_first_bic(fields.get("52A")),
        beneficiary_institution_bic=_first_bic(fields.get("57A")),
        fields=fields,
    )


def validate_mt103(text: str) -> ValidationResult:
    result = ValidationResult()
    try:
        message = parse_mt103(text)
    except ValueError as exc:
        result.add("MT103_REQUIRED", "mt103", str(exc))
        return result
    result.merge(validate_reference(message.sender_reference, field="20"))
    result.merge(validate_amount(message.amount, message.currency, field="32A"))
    if message.charge_bearer not in {"OUR", "SHA", "BEN"}:
        result.add("MT103_CHARGE_BEARER", "71A", "71A debe ser OUR, SHA o BEN")
    if message.bank_operation_code not in {"CRED", "SPAY", "SPRI"}:
        result.add("MT103_OPERATION_CODE", "23B", "23B debe ser CRED, SPAY o SPRI")
    if not message.ordering_customer.name:
        result.add("MT103_ORDERING_NAME", "50K", "El ordenante debe informar un nombre")
    if not message.beneficiary.name:
        result.add("MT103_BENEFICIARY_NAME", "59", "El beneficiario debe informar un nombre")
    if message.ordering_institution_bic:
        result.merge(validate_bic(message.ordering_institution_bic, field="52A"))
    if message.beneficiary_institution_bic:
        result.merge(validate_bic(message.beneficiary_institution_bic, field="57A"))
    account = message.beneficiary.account
    if account and re.fullmatch(r"[A-Za-z]{2}[0-9]{2}[A-Za-z0-9]{11,30}", account.replace(" ", "")):
        result.merge(validate_iban(account, field="59"))
    return result


__all__ = ["MT103", "MT103Party", "parse_mt103", "validate_mt103"]
