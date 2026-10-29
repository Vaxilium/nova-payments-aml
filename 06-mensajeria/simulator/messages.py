"""Constructores XML de los mensajes ISO 20022 del simulador."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
import xml.etree.ElementTree as ET

from validator.iso4217 import minor_unit

PACS008_NS = "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08"
PACS002_NS = "urn:iso:std:iso:20022:tech:xsd:pacs.002.001.10"
PACS008_NAME = "pacs.008.001.08"


def _qn(namespace: str, name: str) -> str:
    return f"{{{namespace}}}{name}"


def _add(parent: ET.Element, name: str, text: str | None = None, **attrs: str) -> ET.Element:
    element = ET.SubElement(parent, _qn(parent.tag.split("}")[0][1:], name))
    if text is not None:
        element.text = str(text)
    for key, value in attrs.items():
        element.set(key, value)
    return element


def _format_amount(amount: Decimal | str | int, currency: str) -> str:
    scale = minor_unit(currency) or 0
    value = Decimal(str(amount))
    return f"{value:.{scale}f}"


def _account(parent: ET.Element, name: str, value: str, *, is_iban: bool) -> None:
    account = _add(parent, name)
    identification = _add(account, "Id")
    if is_iban:
        _add(identification, "IBAN", value)
    else:
        other = _add(identification, "Othr")
        _add(other, "Id", value)


def _party(
    parent: ET.Element,
    name: str,
    *,
    party_name: str,
    account: str,
    is_iban: bool,
) -> None:
    party = _add(parent, name)
    _add(party, "Nm", party_name)
    _account(party, "Acct", account, is_iban=is_iban)


def _agent(parent: ET.Element, name: str, bic: str | None) -> None:
    if not bic:
        return
    agent = _add(parent, name)
    institution = _add(agent, "FinInstnId")
    _add(institution, "BICFI", bic)


def _declaration(namespace: str, root: ET.Element) -> str:
    ET.register_namespace("", namespace)
    try:
        ET.indent(root, space="  ")
    except AttributeError:  # pragma: no cover - Python 3.8 no es objetivo
        pass
    body = ET.tostring(root, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + body


def build_pacs008(
    *,
    message_id: str,
    creation_datetime: str,
    instruction_id: str,
    end_to_end_id: str,
    amount: Decimal | str | int,
    currency: str,
    settlement_date: str,
    debtor_name: str,
    debtor_account: str,
    creditor_name: str,
    creditor_account: str,
    uetr: str | None = None,
    debtor_agent_bic: str | None = None,
    creditor_agent_bic: str | None = None,
    debtor_account_is_iban: bool = False,
    creditor_account_is_iban: bool = False,
    charge_bearer: str = "SHAR",
    remittance_information: str | None = None,
) -> str:
    root = ET.Element(_qn(PACS008_NS, "Document"))
    body = _add(root, "FIToFICstmrCdtTrf")
    header = _add(body, "GrpHdr")
    _add(header, "MsgId", message_id)
    _add(header, "CreDtTm", creation_datetime)
    _add(header, "NbOfTxs", "1")
    settlement = _add(body, "SttlmInf")
    _add(settlement, "SttlmMtd", "CLRG")
    tx = _add(body, "CdtTrfTxInf")
    payment_id = _add(tx, "PmtId")
    _add(payment_id, "InstrId", instruction_id)
    _add(payment_id, "EndToEndId", end_to_end_id)
    if uetr:
        _add(payment_id, "UETR", uetr)
    settlement_amount = _add(tx, "IntrBkSttlmAmt", _format_amount(amount, currency))
    settlement_amount.set("Ccy", currency)
    _add(tx, "IntrBkSttlmDt", settlement_date)
    _add(tx, "ChrgBr", charge_bearer)
    _party(
        tx,
        "Dbtr",
        party_name=debtor_name,
        account=debtor_account,
        is_iban=debtor_account_is_iban,
    )
    _agent(tx, "DbtrAgt", debtor_agent_bic)
    _party(
        tx,
        "Cdtr",
        party_name=creditor_name,
        account=creditor_account,
        is_iban=creditor_account_is_iban,
    )
    _agent(tx, "CdtrAgt", creditor_agent_bic)
    if remittance_information:
        remittance = _add(tx, "RmtInf")
        _add(remittance, "Ustrd", remittance_information)
    return _declaration(PACS008_NS, root)


def build_pacs002(
    *,
    message_id: str,
    creation_datetime: str,
    original_message_id: str,
    original_end_to_end_id: str,
    status: str,
    original_instruction_id: str | None = None,
    original_uetr: str | None = None,
    original_message_name: str = PACS008_NAME,
    reason_code: str | None = None,
    reason_proprietary: str | None = None,
) -> str:
    root = ET.Element(_qn(PACS002_NS, "Document"))
    body = _add(root, "FIToFIPmtStsRpt")
    header = _add(body, "GrpHdr")
    _add(header, "MsgId", message_id)
    _add(header, "CreDtTm", creation_datetime)
    _add(header, "NbOfTxs", "1")
    original_group = _add(body, "OrgnlGrpInfAndSts")
    _add(original_group, "OrgnlMsgId", original_message_id)
    _add(original_group, "OrgnlMsgNmId", original_message_name)
    tx = _add(body, "TxInfAndSts")
    if original_instruction_id:
        _add(tx, "OrgnlInstrId", original_instruction_id)
    _add(tx, "OrgnlEndToEndId", original_end_to_end_id)
    if original_uetr:
        _add(tx, "OrgnlUETR", original_uetr)
    _add(tx, "TxSts", status)
    if reason_code or reason_proprietary:
        status_reason = _add(tx, "StsRsnInf")
        reason = _add(status_reason, "Rsn")
        if reason_code:
            _add(reason, "Cd", reason_code)
        else:
            _add(reason, "Prtry", reason_proprietary)
    return _declaration(PACS002_NS, root)


def build_pain001(
    *,
    message_id: str,
    creation_datetime: str,
    payment_info_id: str,
    requested_execution_date: str,
    debtor_name: str,
    debtor_account: str,
    creditor_name: str,
    creditor_iban: str,
    amount: Decimal | str | int,
    currency: str,
    end_to_end_id: str,
    creditor_bic: str | None = None,
    remittance_information: str | None = None,
) -> str:
    """Construye un pain.001 mínimo para ejemplos y pruebas de contrato."""
    namespace = "urn:iso:std:iso:20022:tech:xsd:pain.001.001.09"
    root = ET.Element(_qn(namespace, "Document"))
    body = _add(root, "CstmrCdtTrfInitn")
    header = _add(body, "GrpHdr")
    _add(header, "MsgId", message_id)
    _add(header, "CreDtTm", creation_datetime)
    _add(header, "NbOfTxs", "1")
    _add(header, "CtrlSum", _format_amount(amount, currency))
    payment = _add(body, "PmtInf")
    _add(payment, "PmtInfId", payment_info_id)
    _add(payment, "PmtMtd", "TRF")
    _add(payment, "NbOfTxs", "1")
    requested = _add(payment, "ReqdExctnDt")
    _add(requested, "Dt", requested_execution_date)
    _party(payment, "Dbtr", party_name=debtor_name, account=debtor_account, is_iban=False)
    tx = _add(payment, "CdtTrfTxInf")
    payment_id = _add(tx, "PmtId")
    _add(payment_id, "EndToEndId", end_to_end_id)
    instructed = _add(tx, "Amt")
    amount_element = _add(instructed, "InstdAmt", _format_amount(amount, currency))
    amount_element.set("Ccy", currency)
    _party(tx, "Cdtr", party_name=creditor_name, account=creditor_iban, is_iban=True)
    _agent(tx, "CdtrAgt", creditor_bic)
    if remittance_information:
        remittance = _add(tx, "RmtInf")
        _add(remittance, "Ustrd", remittance_information)
    return _declaration(namespace, root)


def timestamp(value: datetime | None = None) -> str:
    moment = value or datetime.utcnow()
    return moment.replace(microsecond=0).isoformat() + "Z"


def today_iso() -> str:
    return date.today().isoformat()


__all__ = [
    "PACS002_NS",
    "PACS008_NAME",
    "PACS008_NS",
    "build_pacs002",
    "build_pacs008",
    "build_pain001",
    "timestamp",
    "today_iso",
]
