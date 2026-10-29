"""Simulador de transferencia internacional saliente (SWIFT/ISO 20022)."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Callable

try:
    from app.errors import (
        AccountBlockedError,
        AccountNotFoundError,
        InsufficientFundsError,
    )
    from app.service import BankingService
except ImportError:  # pragma: no cover - CLI desde 06-mensajeria
    CORE_DIR = Path(__file__).resolve().parents[2] / "05-core-middleware"
    if str(CORE_DIR) not in sys.path:
        sys.path.insert(0, str(CORE_DIR))
    from app.errors import (
        AccountBlockedError,
        AccountNotFoundError,
        InsufficientFundsError,
    )
    from app.service import BankingService

from validator.amounts import to_minor, validate_amount
from validator.identifiers import validate_bic, validate_iban, validate_reference
from validator.iso4217 import normalize_currency
from validator.mapping import CHARGE_TO_ISO
from validator.validation import ValidationResult

from .core_bridge import CoreLedgerBridge, CorePostingError
from .messages import build_pacs002, build_pacs008
from .models import (
    AmlHook,
    GatewayOutcome,
    IdempotencyConflict,
    InternationalPaymentRequest,
    PaymentState,
    SimulatedGateway,
    SimulationRecord,
    SimulationValidationError,
    default_aml_hook,
    iso_now,
    utcnow,
)

_IDEMPOTENCY_RE = re.compile(r"^[A-Za-z0-9._:-]{8,128}$")
_SETTLEMENT_CURRENCIES = {"USD"}


def _fingerprint(request: object) -> str:
    return json.dumps(asdict(request), sort_keys=True, separators=(",", ":"), default=str)


def _message_id(prefix: str, instruction_id: str) -> str:
    return f"{prefix}-{instruction_id}"[:35]


def _core_key(prefix: str, instruction_id: str) -> str:
    raw = f"sim-{prefix}-{instruction_id}"
    safe = re.sub(r"[^A-Za-z0-9._:-]", "-", raw)
    if len(safe) < 8:
        safe = f"{safe}-{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:8]}"
    return safe[:128]


class InternationalPaymentSimulator:
    """Orquesta validación, screening simulado, mensajes y asiento contable."""

    MAX_ATTEMPTS = 3

    def __init__(
        self,
        service: BankingService,
        *,
        gateway: SimulatedGateway | None = None,
        aml_hook: AmlHook | None = None,
        clock: Callable[[], datetime] | None = None,
        max_attempts: int = MAX_ATTEMPTS,
    ) -> None:
        self.service = service
        self.bridge = CoreLedgerBridge(service.db_path)
        self.gateway = gateway or SimulatedGateway()
        self.aml_hook = aml_hook or default_aml_hook
        self.clock = clock or utcnow
        self.max_attempts = max(1, int(max_attempts))
        self._records: dict[str, SimulationRecord] = {}
        self._idempotency: dict[str, tuple[str, str]] = {}

    @property
    def records(self) -> dict[str, SimulationRecord]:
        return dict(self._records)

    def get(self, instruction_id: str) -> SimulationRecord:
        try:
            return self._records[instruction_id]
        except KeyError as exc:
            raise KeyError(f"Instrucción no encontrada: {instruction_id}") from exc

    def submit(self, request: InternationalPaymentRequest) -> SimulationRecord:
        fingerprint = _fingerprint(request)
        if request.idempotency_key:
            existing = self._idempotency.get(request.idempotency_key)
            if existing is not None:
                existing_fingerprint, existing_instruction = existing
                if existing_fingerprint != fingerprint:
                    raise IdempotencyConflict(
                        "La idempotency-key ya se usó con una solicitud diferente"
                    )
                return self._records[existing_instruction]
        if request.instruction_id in self._records:
            raise ValueError(f"Instrucción duplicada: {request.instruction_id}")

        record = SimulationRecord(request=request, state=PaymentState.INITIATED)
        self._records[request.instruction_id] = record
        if request.idempotency_key:
            self._idempotency[request.idempotency_key] = (fingerprint, request.instruction_id)

        issues = self._validate(request)
        if issues.issues:
            record.transition(PaymentState.REJECTED)
            record.reason_code = issues.issues[0].code
            record.reason = "; ".join(issue.message for issue in issues.issues)
            record.pacs002 = self._status_message(
                request,
                status="RJCT",
                reason_code="FF01",
                original_message_id=_message_id("MSG", request.instruction_id),
            )
            raise SimulationValidationError(record.reason, issues=[issue.as_dict() for issue in issues.issues])

        record.transition(PaymentState.VALIDATED)
        aml = self.aml_hook(request)
        record.aml_status = aml.status
        if aml.status == "HOLD":
            record.transition(PaymentState.HELD)
            record.reason_code = "AMLHOLD"
            record.reason = aml.reason or "Retenido por screening AML simulado"
            record.pacs002 = self._status_message(
                request,
                status="PDNG",
                reason_proprietary="AMLHOLD",
                original_message_id=_message_id("MSG", request.instruction_id),
            )
            return record
        if aml.status == "REJECT":
            return self._reject(record, request, "FF01", aml.reason or "Rechazado por screening AML simulado", proprietary="AMLREJECT")

        record.pacs008 = self._pacs008(request)
        creation = iso_now(self.clock())
        for attempt in range(1, self.max_attempts + 1):
            record.transition(PaymentState.SENT)
            record.attempts = attempt
            outcome = self.gateway.send(attempt, request, record.pacs008)
            if outcome.outcome == GatewayOutcome.ACCEPTED:
                try:
                    posting = self.bridge.post_outbound(
                        account_id=request.debtor_account_id,
                        amount_minor=to_minor(request.amount, normalize_currency(request.currency)),
                        fee_minor=to_minor(request.fee, normalize_currency(request.currency)) if request.fee else 0,
                        currency=normalize_currency(request.currency),
                        external_ref=request.creditor_iban,
                        instruction_id=request.instruction_id,
                        idempotency_key=_core_key("intl", request.instruction_id),
                        created_at=iso_now(self.clock()),
                        value_date=self.clock().date().isoformat(),
                        description=request.remittance_information or f"Pago internacional {request.instruction_id}",
                    )
                except InsufficientFundsError:
                    return self._reject(record, request, "AM04", "Saldo insuficiente para importe y comisión")
                except (AccountNotFoundError, AccountBlockedError):
                    return self._reject(record, request, "AC01", "Cuenta de origen inexistente o bloqueada")
                except CorePostingError as exc:
                    return self._reject(record, request, "FF01", str(exc))
                record.operation_id = str(posting["operation_id"])
                record.transition(PaymentState.SETTLED)
                record.pacs002 = self._status_message(
                    request,
                    status="ACSC",
                    original_message_id=_message_id("MSG", request.instruction_id),
                    creation=creation,
                )
                return record
            if outcome.outcome == GatewayOutcome.RETRYABLE and attempt < self.max_attempts:
                continue
            if outcome.outcome == GatewayOutcome.TIMEOUT:
                record.transition(PaymentState.EXPIRED)
                record.reason_code = "TIMEOUT"
                record.reason = outcome.detail or "El corresponsal no respondió dentro del plazo"
                record.pacs002 = self._status_message(
                    request,
                    status="RJCT",
                    reason_proprietary="TIMEOUT",
                    original_message_id=_message_id("MSG", request.instruction_id),
                    creation=creation,
                )
                return record
            if outcome.outcome == GatewayOutcome.REJECTED:
                return self._reject(
                    record,
                    request,
                    outcome.reason_code or "FF01",
                    outcome.detail or outcome.reason or "Rechazo del corresponsal",
                )
            if outcome.outcome == GatewayOutcome.RETRYABLE:
                continue

        record.transition(PaymentState.EXPIRED)
        record.reason_code = "TIMEOUT"
        record.reason = "Se agotaron los reintentos"
        record.pacs002 = self._status_message(
            request,
            status="RJCT",
            reason_proprietary="TIMEOUT",
            original_message_id=_message_id("MSG", request.instruction_id),
            creation=creation,
        )
        return record

    def _validate(self, request: InternationalPaymentRequest) -> ValidationResult:
        result = ValidationResult()
        result.merge(validate_reference(request.instruction_id, field="instruction_id"))
        if not request.idempotency_key:
            result.add("IDEMPOTENCY_REQUIRED", "idempotency_key", "La idempotency-key es obligatoria")
        elif not _IDEMPOTENCY_RE.fullmatch(request.idempotency_key.strip()):
            result.add(
                "IDEMPOTENCY_FORMAT",
                "idempotency_key",
                "Use entre 8 y 128 caracteres [A-Za-z0-9._:-]",
            )
        if not request.creditor_name or not request.creditor_name.strip():
            result.add("CREDITOR_NAME_REQUIRED", "creditor_name", "El nombre del beneficiario es obligatorio")
        elif len(request.creditor_name) > 140:
            result.add("CREDITOR_NAME_LENGTH", "creditor_name", "El nombre del beneficiario supera 140 caracteres")
        result.merge(validate_iban(request.creditor_iban, field="creditor_iban"))
        result.merge(validate_bic(request.creditor_bic, field="creditor_bic"))
        currency = normalize_currency(request.currency)
        result.merge(validate_amount(request.amount, currency, field="amount"))
        if request.fee < 0:
            result.add("FEE_NEGATIVE", "fee", "La comisión no puede ser negativa")
        else:
            try:
                to_minor(request.fee, currency)
            except ValueError as exc:
                if request.fee != 0:
                    result.add("FEE_INVALID", "fee", str(exc))
        result.merge(validate_reference(request.remittance_information or "", field="remittance_information", max_length=140, required=False))
        if currency not in _SETTLEMENT_CURRENCIES:
            result.add(
                "CURRENCY_NOT_SETTLEABLE",
                "currency",
                "El core de Fase 3 solo liquida internacionales en USD; EUR queda para mensajería/validación",
            )
        if request.charge_bearer not in CHARGE_TO_ISO:
            result.add("CHARGE_BEARER", "charge_bearer", "charge_bearer debe ser OUR, SHA o BEN")
        if request.creditor_country and request.creditor_iban:
            iban_country = request.creditor_iban.strip().replace(" ", "")[:2].upper()
            if request.creditor_country.strip().upper() != iban_country:
                result.add(
                    "IBAN_COUNTRY_MISMATCH",
                    "creditor_country",
                    "El país del beneficiario no coincide con el país del IBAN",
                )
        try:
            account = self.service.get_account(request.debtor_account_id)
        except (AccountNotFoundError, KeyError):
            result.add("DEBTOR_ACCOUNT_NOT_FOUND", "debtor_account_id", "La cuenta de origen no existe")
        else:
            if account["status"] != "ACTIVE":
                result.add("DEBTOR_ACCOUNT_BLOCKED", "debtor_account_id", "La cuenta de origen no está activa")
            if account["currency"] != currency:
                result.add("DEBTOR_CURRENCY", "currency", "La cuenta de origen no opera en la moneda indicada")
        return result

    def _pacs008(self, request: InternationalPaymentRequest) -> str:
        account = self.service.get_account(request.debtor_account_id)
        return build_pacs008(
            message_id=_message_id("MSG", request.instruction_id),
            creation_datetime=iso_now(self.clock()),
            instruction_id=request.instruction_id,
            end_to_end_id=request.instruction_id,
            amount=request.amount,
            currency=normalize_currency(request.currency),
            settlement_date=self.clock().date().isoformat(),
            debtor_name=request.debtor_name,
            debtor_account=account["account_number"],
            debtor_agent_bic="NOVAPYPA",
            creditor_name=request.creditor_name,
            creditor_account=request.creditor_iban,
            creditor_account_is_iban=True,
            creditor_agent_bic=request.creditor_bic,
            charge_bearer=CHARGE_TO_ISO[request.charge_bearer],
            remittance_information=request.remittance_information,
        )

    def _reject(
        self,
        record: SimulationRecord,
        request: InternationalPaymentRequest,
        reason_code: str,
        reason: str,
        *,
        proprietary: str | None = None,
    ) -> SimulationRecord:
        record.transition(PaymentState.REJECTED)
        record.reason_code = reason_code
        record.reason = reason
        record.pacs002 = self._status_message(
            request,
            status="RJCT",
            reason_code=None if proprietary else reason_code,
            reason_proprietary=proprietary,
            original_message_id=_message_id("MSG", request.instruction_id),
        )
        return record

    def _status_message(
        self,
        request: InternationalPaymentRequest,
        *,
        status: str,
        original_message_id: str,
        reason_code: str | None = None,
        reason_proprietary: str | None = None,
        creation: str | None = None,
    ) -> str:
        return build_pacs002(
            message_id=_message_id("STS", request.instruction_id),
            creation_datetime=creation or iso_now(self.clock()),
            original_message_id=original_message_id,
            original_instruction_id=request.instruction_id,
            original_end_to_end_id=request.instruction_id,
            status=status,
            reason_code=reason_code,
            reason_proprietary=reason_proprietary,
        )


__all__ = ["InternationalPaymentSimulator"]
