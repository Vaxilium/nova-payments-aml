"""Pruebas de validación estructural de mensajes ISO 20022."""

from __future__ import annotations

from decimal import Decimal

from simulator.messages import build_pacs002, build_pacs008, build_pain001
from validator.xml_messages import (
    extract_pacs008,
    validate_message,
    validate_pacs008_international,
)

PACS008_KWARGS = {
    "message_id": "MSG-NOVA-0001",
    "creation_datetime": "2026-10-28T12:00:00Z",
    "instruction_id": "NOVA-2026-0001",
    "end_to_end_id": "NOVA-2026-0001",
    "amount": Decimal("1250.00"),
    "currency": "USD",
    "settlement_date": "2026-10-28",
    "debtor_name": "ANA DEMO",
    "debtor_account": "00000000000001",
    "debtor_agent_bic": "NOVAPYPA",
    "creditor_name": "JOHN DEMO",
    "creditor_account": "GB29NWBK60161331926819",
    "creditor_account_is_iban": True,
    "creditor_agent_bic": "NOVBGB2L",
    "charge_bearer": "SHAR",
    "remittance_information": "INVOICE 2026-001",
}


def test_pacs008_valido() -> None:
    xml = build_pacs008(**PACS008_KWARGS)
    assert validate_message(xml, "pacs.008").valid
    assert validate_pacs008_international(xml).valid


def test_extract_pacs008() -> None:
    payload = extract_pacs008(build_pacs008(**PACS008_KWARGS))
    assert payload["message_id"] == "MSG-NOVA-0001"
    assert payload["currency"] == "USD"
    assert payload["amount"] == "1250.00"
    assert payload["creditor_account"] == "GB29NWBK60161331926819"


def test_pacs008_importe_con_exceso_decimales() -> None:
    xml = build_pacs008(**PACS008_KWARGS).replace(">1250.00<", ">1250.555<")
    result = validate_message(xml)
    assert not result.valid
    assert "AMOUNT_PRECISION" in {issue.code for issue in result.issues}


def test_pacs008_iban_invalido() -> None:
    xml = build_pacs008(**{**PACS008_KWARGS, "creditor_account": "GB28NWBK60161331926819"})
    result = validate_message(xml)
    assert not result.valid
    assert "IBAN_CHECKSUM" in {issue.code for issue in result.issues}


def test_pacs008_internacional_exige_agente() -> None:
    xml = build_pacs008(**{**PACS008_KWARGS, "creditor_agent_bic": None})
    result = validate_pacs008_international(xml)
    assert not result.valid
    assert "AGENT_BIC_REQUIRED" in {issue.code for issue in result.issues}


def test_pacs002_aceptado() -> None:
    xml = build_pacs002(
        message_id="STS-NOVA-0001",
        creation_datetime="2026-10-28T12:00:01Z",
        original_message_id="MSG-NOVA-0001",
        original_instruction_id="NOVA-2026-0001",
        original_end_to_end_id="NOVA-2026-0001",
        status="ACSC",
    )
    assert validate_message(xml, "pacs.002").valid


def test_pacs002_rechazado_sin_motivo() -> None:
    xml = build_pacs002(
        message_id="STS-NOVA-0001",
        creation_datetime="2026-10-28T12:00:01Z",
        original_message_id="MSG-NOVA-0001",
        original_end_to_end_id="NOVA-2026-0001",
        status="RJCT",
    )
    result = validate_message(xml)
    assert not result.valid
    assert "REJECT_REASON_REQUIRED" in {issue.code for issue in result.issues}


def test_pain001_valido() -> None:
    xml = build_pain001(
        message_id="PAIN-NOVA-0001",
        creation_datetime="2026-10-28T12:00:00Z",
        payment_info_id="PMT-NOVA-0001",
        requested_execution_date="2026-10-28",
        debtor_name="ANA DEMO",
        debtor_account="00000000000001",
        creditor_name="JOHN DEMO",
        creditor_iban="GB29NWBK60161331926819",
        amount=Decimal("1250.00"),
        currency="USD",
        end_to_end_id="NOVA-2026-0001",
        creditor_bic="NOVBGB2L",
    )
    assert validate_message(xml, "pain.001").valid


def test_camt053_valido() -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.053.001.08">
  <BkToCstmrStmt>
    <GrpHdr>
      <MsgId>STMT-NOVA-0001</MsgId>
      <CreDtTm>2026-10-28T12:00:00Z</CreDtTm>
      <NbOfTxs>1</NbOfTxs>
    </GrpHdr>
    <Stmt>
      <Id>STMT-2026-10-28</Id>
      <Acct><Id><IBAN>DE89370400440532013000</IBAN></Id></Acct>
      <Bal>
        <Amt Ccy="EUR">1000.00</Amt>
        <CdtDbtInd>CRDT</CdtDbtInd>
      </Bal>
      <Ntry>
        <Amt Ccy="EUR">250.00</Amt>
        <CdtDbtInd>CRDT</CdtDbtInd>
        <Sts>BOOK</Sts>
        <BookgDt><Dt>2026-10-28</Dt></BookgDt>
      </Ntry>
    </Stmt>
  </BkToCstmrStmt>
</Document>"""
    assert validate_message(xml, "camt.053").valid


def test_camt053_estado_invalido() -> None:
    xml = """<Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.053.001.08">
  <BkToCstmrStmt><GrpHdr><MsgId>M</MsgId><CreDtTm>2026-10-28T12:00:00Z</CreDtTm><NbOfTxs>1</NbOfTxs></GrpHdr>
  <Stmt><Id>S</Id><Acct><Id><IBAN>DE89370400440532013000</IBAN></Id></Acct>
  <Bal><Amt Ccy="EUR">1.00</Amt><CdtDbtInd>CRDT</CdtDbtInd></Bal>
  <Ntry><Amt Ccy="EUR">1.00</Amt><CdtDbtInd>CRDT</CdtDbtInd><Sts>XXXX</Sts><BookgDt><Dt>2026-10-28</Dt></BookgDt></Ntry>
  </Stmt></BkToCstmrStmt></Document>"""
    result = validate_message(xml)
    assert not result.valid
    assert "ENTRY_STATUS" in {issue.code for issue in result.issues}


def test_xml_mal_formado() -> None:
    result = validate_message("<Document>")
    assert not result.valid
    assert result.issues[0].code == "XML_PARSE"
