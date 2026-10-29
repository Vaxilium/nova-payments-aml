"""Validación estructural de mensajes ISO 20022 usados en el caso.

No se descargan ni aplican los XSD oficiales (S-056). Las reglas cubren los
campos que el caso necesita para validar negocio, identificadores, importes,
estados y referencias.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable
import xml.etree.ElementTree as ET

from .amounts import decimal_value, validate_amount
from .identifiers import validate_bic, validate_iban, validate_reference, validate_uetr
from .iso4217 import is_iso4217, normalize_currency
from .validation import ValidationResult

_PACS002_STATUSES = {"ACSC", "ACSP", "ACCP", "RJCT", "PDNG", "RCVD"}
_CHARGE_BEARERS = {"DEBT", "CRED", "SHAR", "SLEV"}


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _parse(xml: str | bytes | Path) -> ET.Element:
    if isinstance(xml, Path):
        return ET.parse(xml).getroot()
    if isinstance(xml, bytes):
        return ET.fromstring(xml)
    text = xml.strip()
    if text.startswith("<"):
        return ET.fromstring(text)
    return ET.parse(text).getroot()


def _child(node: ET.Element | None, name: str) -> ET.Element | None:
    if node is None:
        return None
    for item in list(node):
        if _local(item.tag) == name:
            return item
    return None


def _children(node: ET.Element | None, name: str) -> list[ET.Element]:
    if node is None:
        return []
    return [item for item in list(node) if _local(item.tag) == name]


def _path(node: ET.Element | None, *names: str) -> ET.Element | None:
    current = node
    for name in names:
        current = _child(current, name)
        if current is None:
            return None
    return current


def _text(node: ET.Element | None, *names: str) -> str | None:
    target = _path(node, *names)
    if target is None or target.text is None:
        return None
    value = target.text.strip()
    return value or None


def _attr(node: ET.Element | None, name: str) -> str | None:
    if node is None:
        return None
    value = node.attrib.get(name)
    return value.strip() if value else None


def _require_text(
    node: ET.Element | None,
    names: tuple[str, ...],
    field: str,
    result: ValidationResult,
    *,
    max_length: int = 35,
) -> str | None:
    value = _text(node, *names)
    if value is None:
        result.add("FIELD_REQUIRED", field, "Campo obligatorio ausente")
        return None
    result.merge(validate_reference(value, field=field, max_length=max_length))
    return value


def _validate_iso_datetime(value: str | None, field: str, result: ValidationResult) -> None:
    if not value:
        return
    normalized = value.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(normalized)
    except ValueError:
        result.add("DATETIME_FORMAT", field, f"Fecha/hora ISO 8601 inválida: {value}")


def _validate_date(value: str | None, field: str, result: ValidationResult) -> None:
    if not value:
        return
    try:
        date.fromisoformat(value[:10])
    except ValueError:
        result.add("DATE_FORMAT", field, f"Fecha ISO 8601 inválida: {value}")


def _validate_header(body: ET.Element | None, result: ValidationResult) -> ET.Element | None:
    header = _child(body, "GrpHdr")
    if header is None:
        result.add("GROUP_HEADER_REQUIRED", "GrpHdr", "El grupo de cabecera es obligatorio")
        return None
    _require_text(header, ("MsgId",), "GrpHdr.MsgId", result)
    created = _text(header, "CreDtTm")
    if created is None:
        result.add("FIELD_REQUIRED", "GrpHdr.CreDtTm", "Campo obligatorio ausente")
    _validate_iso_datetime(created, "GrpHdr.CreDtTm", result)
    count_text = _text(header, "NbOfTxs")
    if count_text is None:
        result.add("FIELD_REQUIRED", "GrpHdr.NbOfTxs", "Campo obligatorio ausente")
    else:
        try:
            if int(count_text) <= 0:
                result.add("COUNT_INVALID", "GrpHdr.NbOfTxs", "La cantidad de transacciones debe ser positiva")
        except ValueError:
            result.add("COUNT_FORMAT", "GrpHdr.NbOfTxs", "La cantidad de transacciones debe ser entera")
    control_sum = _text(header, "CtrlSum")
    if control_sum is not None:
        try:
            if decimal_value(control_sum) < 0:
                result.add("CONTROL_SUM_INVALID", "GrpHdr.CtrlSum", "La suma de control no puede ser negativa")
        except ValueError:
            result.add("CONTROL_SUM_FORMAT", "GrpHdr.CtrlSum", "La suma de control no es numérica")
    return header


def _validate_account(node: ET.Element | None, field: str, result: ValidationResult) -> str | None:
    if node is None:
        result.add("ACCOUNT_REQUIRED", field, "La cuenta es obligatoria")
        return None
    iban = _text(node, "Id", "IBAN")
    if iban:
        result.merge(validate_iban(iban, field=f"{field}.IBAN"))
        return "IBAN"
    other = _text(node, "Id", "Othr", "Id")
    if other:
        result.merge(validate_reference(other, field=f"{field}.Othr.Id", max_length=34))
        return "Othr"
    result.add("ACCOUNT_ID_REQUIRED", field, "Se requiere IBAN u Othr/Id")
    return None


def _validate_agent(
    node: ET.Element | None,
    field: str,
    result: ValidationResult,
    *,
    required: bool,
) -> str | None:
    bic = _text(node, "FinInstnId", "BICFI") or _text(node, "FinInstnId", "BIC")
    if not bic:
        if required:
            result.add("AGENT_BIC_REQUIRED", field, "El BIC del agente es obligatorio")
        return None
    result.merge(validate_bic(bic, field=f"{field}.BIC"))
    return bic


def _validate_party(
    node: ET.Element | None,
    field: str,
    result: ValidationResult,
    *,
    require_iban: bool = False,
    require_agent: bool = False,
) -> None:
    if node is None:
        result.add("PARTY_REQUIRED", field, "La parte es obligatoria")
        return
    _require_text(node, ("Nm",), f"{field}.Nm", result, max_length=140)
    account_kind = _validate_account(_child(node, "Acct"), f"{field}.Acct", result)
    if require_iban and account_kind not in (None, "IBAN"):
        result.add("IBAN_REQUIRED", f"{field}.Acct", "La cuenta debe expresarse como IBAN en el tramo internacional")
    _validate_agent(_child(node, "Agt"), f"{field}.Agt", result, required=require_agent)


def _validate_pain001(body: ET.Element, result: ValidationResult) -> None:
    header = _validate_header(body, result)
    payments = _children(body, "PmtInf")
    if not payments:
        result.add("PAYMENT_INFO_REQUIRED", "PmtInf", "Se requiere al menos un bloque PmtInf")
        return
    total_tx = 0
    for index, payment in enumerate(payments, start=1):
        base = f"PmtInf[{index}]"
        _require_text(payment, ("PmtInfId",), f"{base}.PmtInfId", result)
        method = _text(payment, "PmtMtd")
        if method not in {"TRF", "TRA"}:
            result.add("PAYMENT_METHOD", f"{base}.PmtMtd", "PmtMtd debe ser TRF o TRA")
        _validate_date(_text(payment, "ReqdExctnDt", "Dt"), f"{base}.ReqdExctnDt", result)
        _validate_party(_child(payment, "Dbtr"), f"{base}.Dbtr", result)
        txs = _children(payment, "CdtTrfTxInf")
        if not txs:
            result.add("TRANSACTION_REQUIRED", f"{base}.CdtTrfTxInf", "Se requiere al menos una transacción")
        for tx_index, tx in enumerate(txs, start=1):
            tx_base = f"{base}.CdtTrfTxInf[{tx_index}]"
            total_tx += 1
            end_to_end = _text(tx, "PmtId", "EndToEndId")
            if not end_to_end:
                result.add("FIELD_REQUIRED", f"{tx_base}.PmtId.EndToEndId", "Campo obligatorio ausente")
            else:
                result.merge(validate_reference(end_to_end, field=f"{tx_base}.PmtId.EndToEndId"))
            amount_node = _path(tx, "Amt", "InstdAmt")
            currency = _attr(amount_node, "Ccy")
            if amount_node is None or amount_node.text is None:
                result.add("AMOUNT_REQUIRED", f"{tx_base}.Amt.InstdAmt", "El importe es obligatorio")
            else:
                result.merge(
                    validate_amount(
                        amount_node.text.strip(),
                        currency or "",
                        field=f"{tx_base}.Amt.InstdAmt",
                    )
                )
            _validate_party(_child(tx, "Cdtr"), f"{tx_base}.Cdtr", result)
            _validate_agent(_child(tx, "CdtrAgt"), f"{tx_base}.CdtrAgt", result, required=False)
    if header is not None:
        expected = _text(header, "NbOfTxs")
        if expected and expected.isdigit() and int(expected) != total_tx:
            result.add("COUNT_MISMATCH", "GrpHdr.NbOfTxs", f"Se declararon {expected} transacciones y se encontraron {total_tx}")


def _validate_pacs008(body: ET.Element, result: ValidationResult, *, international: bool = False) -> None:
    header = _validate_header(body, result)
    txs = _children(body, "CdtTrfTxInf")
    if not txs:
        result.add("TRANSACTION_REQUIRED", "CdtTrfTxInf", "Se requiere al menos una transacción")
    for index, tx in enumerate(txs, start=1):
        base = f"CdtTrfTxInf[{index}]"
        end_to_end = _text(tx, "PmtId", "EndToEndId")
        if not end_to_end:
            result.add("FIELD_REQUIRED", f"{base}.PmtId.EndToEndId", "Campo obligatorio ausente")
        else:
            result.merge(validate_reference(end_to_end, field=f"{base}.PmtId.EndToEndId"))
        _require_text(tx, ("PmtId", "InstrId"), f"{base}.PmtId.InstrId", result, max_length=35)
        uetr = _text(tx, "PmtId", "UETR")
        if uetr:
            result.merge(validate_uetr(uetr, field=f"{base}.PmtId.UETR"))
        amount_node = _child(tx, "IntrBkSttlmAmt")
        currency = _attr(amount_node, "Ccy")
        if amount_node is None or amount_node.text is None:
            result.add("AMOUNT_REQUIRED", f"{base}.IntrBkSttlmAmt", "El importe de liquidación es obligatorio")
        else:
            result.merge(
                validate_amount(
                    amount_node.text.strip(),
                    currency or "",
                    field=f"{base}.IntrBkSttlmAmt",
                )
            )
        _validate_date(_text(tx, "IntrBkSttlmDt"), f"{base}.IntrBkSttlmDt", result)
        charge = _text(tx, "ChrgBr")
        if charge and charge not in _CHARGE_BEARERS:
            result.add("CHARGE_BEARER", f"{base}.ChrgBr", "ChrgBr debe ser DEBT, CRED, SHAR o SLEV")
        _validate_party(
            _child(tx, "Dbtr"),
            f"{base}.Dbtr",
            result,
            require_iban=False,
        )
        _validate_party(
            _child(tx, "Cdtr"),
            f"{base}.Cdtr",
            result,
            require_iban=international,
        )
        if international:
            _validate_agent(_child(tx, "DbtrAgt"), f"{base}.DbtrAgt", result, required=True)
            _validate_agent(_child(tx, "CdtrAgt"), f"{base}.CdtrAgt", result, required=True)
    if header is not None:
        expected = _text(header, "NbOfTxs")
        if expected and expected.isdigit() and int(expected) != len(txs):
            result.add("COUNT_MISMATCH", "GrpHdr.NbOfTxs", f"Se declararon {expected} transacciones y se encontraron {len(txs)}")


def _validate_pacs002(body: ET.Element, result: ValidationResult) -> None:
    _validate_header(body, result)
    group = _child(body, "OrgnlGrpInfAndSts")
    if group is None:
        result.add("ORIGINAL_GROUP_REQUIRED", "OrgnlGrpInfAndSts", "Se requiere la referencia al grupo original")
    else:
        _require_text(group, ("OrgnlMsgId",), "OrgnlGrpInfAndSts.OrgnlMsgId", result)
        original_name = _text(group, "OrgnlMsgNmId")
        if not original_name:
            result.add("FIELD_REQUIRED", "OrgnlGrpInfAndSts.OrgnlMsgNmId", "Campo obligatorio ausente")
        elif not original_name.startswith("pacs.008."):
            result.add("ORIGINAL_MESSAGE", "OrgnlGrpInfAndSts.OrgnlMsgNmId", "El mensaje original debe ser pacs.008")
    txs = _children(body, "TxInfAndSts")
    if not txs:
        result.add("STATUS_REQUIRED", "TxInfAndSts", "Se requiere al menos un estado de transacción")
    for index, tx in enumerate(txs, start=1):
        base = f"TxInfAndSts[{index}]"
        end_to_end = _text(tx, "OrgnlEndToEndId")
        if not end_to_end:
            result.add("FIELD_REQUIRED", f"{base}.OrgnlEndToEndId", "Campo obligatorio ausente")
        else:
            result.merge(validate_reference(end_to_end, field=f"{base}.OrgnlEndToEndId"))
        uetr = _text(tx, "OrgnlUETR")
        if uetr:
            result.merge(validate_uetr(uetr, field=f"{base}.OrgnlUETR"))
        status = _text(tx, "TxSts")
        if status not in _PACS002_STATUSES:
            result.add("STATUS_INVALID", f"{base}.TxSts", "TxSts debe ser ACSC, ACSP, ACCP, RJCT, PDNG o RCVD")
        if status == "RJCT":
            reason_code = _text(tx, "StsRsnInf", "Rsn", "Cd")
            reason_proprietary = _text(tx, "StsRsnInf", "Rsn", "Prtry")
            if not reason_code and not reason_proprietary:
                result.add("REJECT_REASON_REQUIRED", f"{base}.StsRsnInf", "Un rechazo debe informar un motivo")
            elif reason_code and len(reason_code) > 4:
                result.add("REJECT_REASON_FORMAT", f"{base}.StsRsnInf", "El código de motivo debe tener hasta 4 caracteres")


def _validate_camt053(body: ET.Element, result: ValidationResult) -> None:
    _validate_header(body, result)
    statements = _children(body, "Stmt")
    if not statements:
        result.add("STATEMENT_REQUIRED", "Stmt", "Se requiere al menos un extracto")
    for index, statement in enumerate(statements, start=1):
        base = f"Stmt[{index}]"
        _require_text(statement, ("Id",), f"{base}.Id", result)
        account = _child(statement, "Acct")
        _validate_account(account, f"{base}.Acct", result)
        balances = _children(statement, "Bal")
        if not balances:
            result.add("BALANCE_REQUIRED", f"{base}.Bal", "Se requiere al menos un saldo")
        for bal_index, balance in enumerate(balances, start=1):
            amount_node = _child(balance, "Amt")
            currency = _attr(amount_node, "Ccy")
            if amount_node is None or amount_node.text is None:
                result.add("BALANCE_AMOUNT", f"{base}.Bal[{bal_index}].Amt", "El importe del saldo es obligatorio")
            else:
                try:
                    decimal_value(amount_node.text.strip())
                    if currency and not is_iso4217(currency):
                        result.add("CURRENCY_UNKNOWN", f"{base}.Bal[{bal_index}].Amt.Ccy", f"Código ISO 4217 desconocido: {currency}")
                except ValueError:
                    result.add("BALANCE_AMOUNT", f"{base}.Bal[{bal_index}].Amt", "El importe del saldo no es numérico")
            indicator = _text(balance, "CdtDbtInd")
            if indicator not in {"CRDT", "DBIT"}:
                result.add("BALANCE_INDICATOR", f"{base}.Bal[{bal_index}].CdtDbtInd", "CdtDbtInd debe ser CRDT o DBIT")
        entries = _children(statement, "Ntry")
        for entry_index, entry in enumerate(entries, start=1):
            entry_base = f"{base}.Ntry[{entry_index}]"
            amount_node = _child(entry, "Amt")
            currency = _attr(amount_node, "Ccy")
            if amount_node is None or amount_node.text is None:
                result.add("ENTRY_AMOUNT", f"{entry_base}.Amt", "El importe del asiento es obligatorio")
            else:
                result.merge(validate_amount(amount_node.text.strip(), currency or "", field=f"{entry_base}.Amt"))
            if _text(entry, "CdtDbtInd") not in {"CRDT", "DBIT"}:
                result.add("ENTRY_INDICATOR", f"{entry_base}.CdtDbtInd", "CdtDbtInd debe ser CRDT o DBIT")
            if _text(entry, "Sts") not in {"BOOK", "PDNG"}:
                result.add("ENTRY_STATUS", f"{entry_base}.Sts", "Sts debe ser BOOK o PDNG")
            _validate_date(_text(entry, "BookgDt", "Dt"), f"{entry_base}.BookgDt", result)


def validate_message(xml: str | bytes | Path, kind: str | None = None) -> ValidationResult:
    """Valida un mensaje ISO 20022 de los tipos cubiertos por el caso."""
    result = ValidationResult()
    try:
        root = _parse(xml)
    except (ET.ParseError, OSError) as exc:
        result.add("XML_PARSE", "document", f"No se pudo interpretar el XML: {exc}")
        return result
    if _local(root.tag) != "Document":
        result.add("XML_ROOT", "document", "La raíz debe ser Document")
        return result
    body = next(iter(list(root)), None)
    if body is None:
        result.add("XML_BODY", "document", "Document no contiene un mensaje")
        return result
    detected = {
        "CstmrCdtTrfInitn": "pain.001",
        "FIToFICstmrCdtTrf": "pacs.008",
        "FIToFIPmtStsRpt": "pacs.002",
        "BkToCstmrStmt": "camt.053",
    }.get(_local(body.tag))
    if detected is None:
        result.add("MESSAGE_TYPE", "document", f"Tipo de mensaje no soportado: {_local(body.tag)}")
        return result
    if kind is not None and kind != detected:
        result.add("MESSAGE_TYPE_MISMATCH", "document", f"Se esperaba {kind} y se recibió {detected}")
        return result
    if detected == "pain.001":
        _validate_pain001(body, result)
    elif detected == "pacs.008":
        _validate_pacs008(body, result)
    elif detected == "pacs.002":
        _validate_pacs002(body, result)
    else:
        _validate_camt053(body, result)
    return result


def validate_pacs008_international(xml: str | bytes | Path) -> ValidationResult:
    result = ValidationResult()
    try:
        root = _parse(xml)
    except (ET.ParseError, OSError) as exc:
        result.add("XML_PARSE", "document", f"No se pudo interpretar el XML: {exc}")
        return result
    body = next(iter(list(root)), None)
    if body is None or _local(body.tag) != "FIToFICstmrCdtTrf":
        result.add("MESSAGE_TYPE", "document", "Se esperaba un mensaje pacs.008")
        return result
    _validate_pacs008(body, result, international=True)
    return result


def extract_pacs008(xml: str | bytes | Path) -> dict[str, object]:
    """Extrae los campos usados por el mapeo y las pruebas."""
    root = _parse(xml)
    body = _child(root, "FIToFICstmrCdtTrf")
    if body is None:
        raise ValueError("El documento no contiene FIToFICstmrCdtTrf")
    header = _child(body, "GrpHdr")
    tx = _child(body, "CdtTrfTxInf")
    if tx is None:
        raise ValueError("El documento no contiene CdtTrfTxInf")
    amount_node = _child(tx, "IntrBkSttlmAmt")
    return {
        "message_id": _text(header, "MsgId"),
        "creation_datetime": _text(header, "CreDtTm"),
        "transaction_count": _text(header, "NbOfTxs"),
        "instruction_id": _text(tx, "PmtId", "InstrId"),
        "end_to_end_id": _text(tx, "PmtId", "EndToEndId"),
        "uetr": _text(tx, "PmtId", "UETR"),
        "currency": _attr(amount_node, "Ccy"),
        "amount": amount_node.text.strip() if amount_node is not None and amount_node.text else None,
        "settlement_date": _text(tx, "IntrBkSttlmDt"),
        "debtor_name": _text(tx, "Dbtr", "Nm"),
        "debtor_account": _text(tx, "Dbtr", "Acct", "Id", "IBAN")
        or _text(tx, "Dbtr", "Acct", "Id", "Othr", "Id"),
        "debtor_bic": _text(tx, "DbtrAgt", "FinInstnId", "BICFI"),
        "creditor_name": _text(tx, "Cdtr", "Nm"),
        "creditor_account": _text(tx, "Cdtr", "Acct", "Id", "IBAN")
        or _text(tx, "Cdtr", "Acct", "Id", "Othr", "Id"),
        "creditor_bic": _text(tx, "CdtrAgt", "FinInstnId", "BICFI"),
        "charge_bearer": _text(tx, "ChrgBr"),
        "remittance_information": _text(tx, "RmtInf", "Ustrd"),
    }


__all__ = [
    "extract_pacs008",
    "validate_message",
    "validate_pacs008_international",
]
