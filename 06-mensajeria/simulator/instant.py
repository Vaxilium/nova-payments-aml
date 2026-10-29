"""Simulador de pago instantáneo local inspirado en el SPI del BCP."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import asdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Callable

try:
    from app.errors import (
        AccountBlockedError,
        AccountNotFoundError,
        ConcurrentModificationError,
        CurrencyMismatchError,
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
        ConcurrentModificationError,
        CurrencyMismatchError,
        InsufficientFundsError,
    )
    from app.service import BankingService

from validator.amounts import to_minor, validate_amount
from validator.identifiers import validate_reference
from validator.iso4217 import normalize_currency
from validator.validation import ValidationResult

from .messages import build_pacs002, build_pacs008
from .models import (
    GatewayOutcome,
    GatewayResult,
    IdempotencyConflict,
    InstantPaymentRequest,
    PaymentState,
    SimulatedGateway,
    SimulationRecord,
    SimulationValidationError,
    iso_now,
    utcnow,
)

_IDEMPOTENCY_RE = re.compile(r"^[A-Za-z0-9._:-]{8,128}$")
_LOCAL_LIMIT_MINOR = 10_000_000


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


class InstantPaymentSimulator:
    """Máquina de estados con idempotencia, reintentos y posteo contable."""

    MAX_ATTEMPTS = 3
    MAX_AMOUNT_MINOR = _LOCAL_LIMIT_MINOR

    def __init__(
        self,
        service: BankingService,
        *,
        gateway: SimulatedGateway | None = None,
        clock: Callable[[], datetime] | None = None,
        max_attempts: int = MAX_ATTEMPTS,
    ) -> None:
        self.service = service
        self.gateway = gateway or SimulatedGateway()
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

    def submit(self, request: InstantPaymentRequest) -> SimulationRecord:
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
                reason_proprietary=None,
                original_message_id=_message_id("MSG", request.instruction_id),
            )
            raise SimulationValidationError(record.reason, issues=[issue.as_dict() for issue in issues.issues])

        record.transition(PaymentState.VALIDATED)
        record.pacs008 = self._pacs008(request)
        current_time = self.clock()
        creation = iso_now(current_time)
        settlement_date = current_time.date().isoformat()

        for attempt in range(1, self.max_attempts + 1):
            record.transition(PaymentState.SENT)
            record.attempts = attempt
            outcome = self.gateway.send(attempt, request, record.pacs008)
            if outcome.outcome == GatewayOutcome.ACCEPTED:
                try:
                    operation_id = self._settle(request)
                except InsufficientFundsError:
                    return self._reject(record, request, "AM04", "Saldo insuficiente")
                except (AccountNotFoundError, AccountBlockedError):
                    return self._reject(record, request, "AC01", "Cuenta inexistente o bloqueada")
                except CurrencyMismatchError:
                    return self._reject(record, request, "AM04", "Moneda incompatible con la cuenta")
                except (ConcurrentModificationError, ValueError) as exc:
                    return self._reject(record, request, "FF01", str(exc))
                record.operation_id = operation_id
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
                record.reason = outcome.detail or "El PSP no respondió dentro del plazo"
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
                    outcome.detail or outcome.reason or "Rechazo del PSP",
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

    def _validate(self, request: InstantPaymentRequest) -> ValidationResult:
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
        if not request.creditor_account_id and not request.creditor_alias and not request.creditor_account_number:
            result.add(
                "CREDITOR_ACCOUNT_REQUIRED",
                "creditor",
                "Se requiere creditor_account_id, alias o número de cuenta",
            )
        if request.creditor_alias:
            result.merge(validate_reference(request.creditor_alias, field="creditor_alias", max_length=64))
        if request.creditor_account_number:
            result.merge(
                validate_reference(
                    request.creditor_account_number,
                    field="creditor_account_number",
                    max_length=34,
                )
            )
        result.merge(validate_amount(request.amount, request.currency, field="amount"))
        if result.valid:
            try:
                amount_minor = to_minor(request.amount, request.currency)
            except ValueError as exc:
                result.add("AMOUNT_INVALID", "amount", str(exc))
                return result
            if normalize_currency(request.currency) != "PYG":
                result.add("CURRENCY_NOT_LOCAL", "currency", "El tramo instantáneo local opera en PYG")
            if amount_minor > self.MAX_AMOUNT_MINOR:
                result.add(
                    "AMOUNT_LIMIT",
                    "amount",
                    f"El tope local es ₲{self.MAX_AMOUNT_MINOR:,}",
                )
        try:
            account = self.service.get_account(request.debtor_account_id)
        except (AccountNotFoundError, KeyError):
            result.add("DEBTOR_ACCOUNT_NOT_FOUND", "debtor_account_id", "La cuenta de origen no existe")
        else:
            if account["status"] != "ACTIVE":
                result.add("DEBTOR_ACCOUNT_BLOCKED", "debtor_account_id", "La cuenta de origen no está activa")
            if account["currency"] != normalize_currency(request.currency):
                result.add("DEBTOR_CURRENCY", "currency", "La cuenta de origen no opera en la moneda indicada")
        if request.creditor_account_id:
            if request.creditor_account_id == request.debtor_account_id:
                result.add("SAME_ACCOUNT", "creditor_account_id", "La cuenta destino debe ser distinta")
            else:
                try:
                    target = self.service.get_account(request.creditor_account_id)
                except (AccountNotFoundError, KeyError):
                    result.add("CREDITOR_ACCOUNT_NOT_FOUND", "creditor_account_id", "La cuenta destino no existe")
                else:
                    if target["status"] != "ACTIVE":
                        result.add("CREDITOR_ACCOUNT_BLOCKED", "creditor_account_id", "La cuenta destino no está activa")
                    if target["currency"] != normalize_currency(request.currency):
                        result.add("CREDITOR_CURRENCY", "currency", "La cuenta destino no opera en la moneda indicada")
        return result

    def _pacs008(self, request: InstantPaymentRequest) -> str:
        account = self.service.get_account(request.debtor_account_id)
        creditor_account = (
            request.creditor_account_id
            or request.creditor_account_number
            or request.creditor_alias
            or ""
        )
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
            creditor_name=request.creditor_name,
            creditor_account=creditor_account,
            charge_bearer="SLEV",
            remittance_information=request.description,
        )

    def _settle(self, request: InstantPaymentRequest) -> str:
        if request.creditor_account_id:
            response, _, _ = self.service.transfer(
                from_account_id=request.debtor_account_id,
                to_account_id=request.creditor_account_id,
                amount=request.amount,
                currency=normalize_currency(request.currency),
                idempotency_key=_core_key("instant", request.instruction_id),
                description=request.description or f"Pago instantáneo {request.instruction_id}",
                channel="API",
                actor="simulator",
                correlation_id=request.instruction_id,
            )
        else:
            response, _, _ = self.service.debit_account(
                account_id=request.debtor_account_id,
                amount=request.amount,
                currency=normalize_currency(request.currency),
                idempotency_key=_core_key("instant", request.instruction_id),
                description=request.description or f"Pago instantáneo a {request.creditor_name}",
                channel="API",
                actor="simulator",
                correlation_id=request.instruction_id,
            )
        return str(response["operation_id"])

    def _reject(
        self,
        record: SimulationRecord,
        request: InstantPaymentRequest,
        reason_code: str,
        reason: str,
    ) -> SimulationRecord:
        record.transition(PaymentState.REJECTED)
        record.reason_code = reason_code
        record.reason = reason
        record.pacs002 = self._status_message(
            request,
            status="RJCT",
            reason_code=reason_code,
            reason_proprietary=None,
            original_message_id=_message_id("MSG", request.instruction_id),
        )
        return record

    def _status_message(
        self,
        request: InstantPaymentRequest,
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


__all__ = ["InstantPaymentSimulator"]
