"""Mapeo funcional MT103 ↔ pacs.008 usado por documentos y pruebas."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from .mt103 import MT103

CHARGE_TO_ISO = {"OUR": "DEBT", "SHA": "SHAR", "BEN": "CRED"}
ISO_TO_CHARGE = {value: key for key, value in CHARGE_TO_ISO.items()}

MAPPING_ROWS: tuple[dict[str, str], ...] = (
    {
        "mt103_field": "20",
        "iso_path": "PmtId/InstrId y PmtId/EndToEndId",
        "direction": "MT103 → pacs.008",
        "notes": "Referencia del ordenante; se conserva como instrucción y referencia extremo a extremo cuando no existe otro identificador.",
    },
    {
        "mt103_field": "23B",
        "iso_path": "PmtTpInf (informativo)",
        "direction": "MT103 → pacs.008",
        "notes": "Código de operación bancaria; no tiene una equivalencia ISO única en el perfil del caso.",
    },
    {
        "mt103_field": "32A",
        "iso_path": "IntrBkSttlmAmt/@Ccy e IntrBkSttlmDt",
        "direction": "MT103 → pacs.008",
        "notes": "La fecha valor se usa como fecha de liquidación y el par moneda/importe como importe interbancario.",
    },
    {
        "mt103_field": "33B",
        "iso_path": "InstdAmt/@Ccy",
        "direction": "MT103 → pacs.008",
        "notes": "Importe instruido por el ordenante; opcional si coincide con 32A.",
    },
    {
        "mt103_field": "50K",
        "iso_path": "Dbtr/Nm y Dbtr/Acct/Id/Othr/Id",
        "direction": "MT103 → pacs.008",
        "notes": "Ordenante y cuenta de origen; el identificador local se expresa como Othr/Id.",
    },
    {
        "mt103_field": "52A",
        "iso_path": "DbtrAgt/FinInstnId/BICFI",
        "direction": "MT103 → pacs.008",
        "notes": "Institución del ordenante.",
    },
    {
        "mt103_field": "57A",
        "iso_path": "CdtrAgt/FinInstnId/BICFI",
        "direction": "MT103 → pacs.008",
        "notes": "Institución del beneficiario.",
    },
    {
        "mt103_field": "59",
        "iso_path": "Cdtr/Nm, Cdtr/Acct y Cdtr/Agt",
        "direction": "MT103 → pacs.008",
        "notes": "Beneficiario, cuenta/IBAN y, si se informa, BIC del beneficiario.",
    },
    {
        "mt103_field": "70",
        "iso_path": "RmtInf/Ustrd",
        "direction": "MT103 → pacs.008",
        "notes": "Información de remesa no estructurada.",
    },
    {
        "mt103_field": "71A",
        "iso_path": "ChrgBr",
        "direction": "MT103 → pacs.008",
        "notes": "OUR→DEBT, SHA→SHAR, BEN→CRED.",
    },
    {
        "mt103_field": "72",
        "iso_path": "RmtInf o datos suplementarios",
        "direction": "MT103 → pacs.008",
        "notes": "Información remitente-destinatario; el caso no la usa para el flujo principal.",
    },
    {
        "mt103_field": "PmtId/EndToEndId",
        "iso_path": "20 (referencia del ordenante)",
        "direction": "pacs.008 → MT103",
        "notes": "Se conserva la referencia extremo a extremo como referencia del mensaje MT103.",
    },
    {
        "mt103_field": "IntrBkSttlmAmt + IntrBkSttlmDt",
        "iso_path": "32A",
        "direction": "pacs.008 → MT103",
        "notes": "Se compone la fecha valor y el par moneda/importe.",
    },
    {
        "mt103_field": "ChrgBr",
        "iso_path": "71A",
        "direction": "pacs.008 → MT103",
        "notes": "DEBT→OUR, SHAR→SHA, CRED→BEN.",
    },
)


def _max35(value: str) -> str:
    return value[:35]


def mt103_to_pacs008_fields(
    message: MT103,
    *,
    message_id: str | None = None,
    uetr: str | None = None,
) -> dict[str, object]:
    """Devuelve un diccionario equivalente a los campos relevantes de pacs.008."""
    sender_reference = _max35(message.sender_reference)
    charge = CHARGE_TO_ISO.get(message.charge_bearer)
    return {
        "message_id": _max35(message_id or f"MSG-{sender_reference}"),
        "instruction_id": sender_reference,
        "end_to_end_id": sender_reference,
        "uetr": uetr,
        "interbank_settlement_amount": {
            "currency": message.currency,
            "value": f"{message.amount:.2f}" if message.currency != "PYG" else f"{message.amount:.0f}",
        },
        "interbank_settlement_date": message.value_date.isoformat(),
        "debtor": {
            "name": message.ordering_customer.name,
            "account": message.ordering_customer.account,
        },
        "debtor_agent_bic": message.ordering_institution_bic,
        "creditor": {
            "name": message.beneficiary.name,
            "account": message.beneficiary.account,
        },
        "creditor_agent_bic": message.beneficiary_institution_bic,
        "charge_bearer": charge,
        "remittance_information": message.remittance_information,
        "source_mt103": message.fields,
    }


def _party_lines(account: str | None, name: str | None) -> list[str]:
    lines: list[str] = []
    if account:
        lines.append(f"/{account}")
    if name:
        lines.append(name)
    return lines


def pacs008_to_mt103_fields(payload: dict[str, object]) -> dict[str, str | list[str]]:
    """Convierte los campos extraídos de un pacs.008 a una representación MT103."""
    settlement_date = str(payload.get("settlement_date") or date.today().isoformat())
    try:
        parsed_date = date.fromisoformat(settlement_date[:10])
    except ValueError as exc:
        raise ValueError("La fecha de liquidación debe ser ISO 8601") from exc
    amount = Decimal(str(payload.get("amount") or "0"))
    currency = str(payload.get("currency") or "").upper()
    scale = 0 if currency == "PYG" else 2
    amount_text = f"{amount:.{scale}f}".replace(".", ",")
    charge = ISO_TO_CHARGE.get(str(payload.get("charge_bearer") or "SHAR"), "SHA")
    reference = str(payload.get("end_to_end_id") or payload.get("instruction_id") or "")
    fields: dict[str, str | list[str]] = {
        "20": reference,
        "23B": "CRED",
        "32A": f"{parsed_date:%y%m%d}{currency}{amount_text}",
        "50K": _party_lines(
            str(payload.get("debtor_account") or "") or None,
            str(payload.get("debtor_name") or "") or None,
        ),
        "59": _party_lines(
            str(payload.get("creditor_account") or "") or None,
            str(payload.get("creditor_name") or "") or None,
        ),
        "71A": charge,
    }
    if payload.get("debtor_bic"):
        fields["52A"] = str(payload["debtor_bic"])
    if payload.get("creditor_bic"):
        fields["57A"] = str(payload["creditor_bic"])
    if payload.get("remittance_information"):
        fields["70"] = str(payload["remittance_information"])
    return fields


__all__ = [
    "CHARGE_TO_ISO",
    "ISO_TO_CHARGE",
    "MAPPING_ROWS",
    "mt103_to_pacs008_fields",
    "pacs008_to_mt103_fields",
]
