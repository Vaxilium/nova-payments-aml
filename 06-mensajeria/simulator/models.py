"""Modelos compartidos por los simuladores de pagos."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Callable, Iterable


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso_now(moment: datetime | None = None) -> str:
    current = moment or utcnow()
    return current.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class PaymentState(str, Enum):
    INITIATED = "INITIATED"
    VALIDATED = "VALIDATED"
    SENT = "SENT"
    SETTLED = "SETTLED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    HELD = "HELD"


ALLOWED_TRANSITIONS: dict[PaymentState, set[PaymentState]] = {
    PaymentState.INITIATED: {PaymentState.VALIDATED, PaymentState.REJECTED},
    PaymentState.VALIDATED: {PaymentState.SENT, PaymentState.HELD, PaymentState.REJECTED},
    PaymentState.SENT: {PaymentState.SENT, PaymentState.SETTLED, PaymentState.REJECTED, PaymentState.EXPIRED},
    PaymentState.HELD: {PaymentState.SENT, PaymentState.REJECTED, PaymentState.EXPIRED},
    PaymentState.SETTLED: set(),
    PaymentState.REJECTED: set(),
    PaymentState.EXPIRED: set(),
}


class SimulationError(RuntimeError):
    """Error base de simulación."""


class InvalidStateTransition(SimulationError):
    """Transición no permitida por la máquina de estados."""


class SimulationValidationError(SimulationError):
    """La solicitud no cumple las reglas de validación."""

    def __init__(self, message: str, *, issues: list[dict[str, str]] | None = None) -> None:
        self.issues = issues or []
        super().__init__(message)


class IdempotencyConflict(SimulationError):
    """La misma clave se reutilizó con un contenido distinto."""


class GatewayOutcome(str, Enum):
    ACCEPTED = "ACCEPTED"
    RETRYABLE = "RETRYABLE"
    REJECTED = "REJECTED"
    TIMEOUT = "TIMEOUT"


@dataclass(frozen=True)
class GatewayResult:
    outcome: GatewayOutcome
    reason_code: str | None = None
    reason: str | None = None
    detail: str | None = None


@dataclass(frozen=True)
class AmlResult:
    status: str = "ALLOW"
    reason: str | None = None


@dataclass(frozen=True)
class InstantPaymentRequest:
    instruction_id: str
    debtor_account_id: str
    creditor_name: str
    amount: Decimal
    currency: str = "PYG"
    debtor_name: str = "Cliente NovaBank"
    creditor_alias: str | None = None
    creditor_account_number: str | None = None
    creditor_account_id: str | None = None
    idempotency_key: str | None = None
    description: str | None = None


@dataclass(frozen=True)
class InternationalPaymentRequest:
    instruction_id: str
    debtor_account_id: str
    creditor_name: str
    creditor_iban: str
    creditor_bic: str
    amount: Decimal
    currency: str = "USD"
    debtor_name: str = "Cliente NovaBank"
    fee: Decimal = Decimal("25.00")
    charge_bearer: str = "SHA"
    remittance_information: str | None = None
    creditor_country: str | None = None
    idempotency_key: str | None = None


@dataclass
class SimulationRecord:
    request: object
    state: PaymentState
    history: list[PaymentState] = field(default_factory=list)
    pacs008: str | None = None
    pacs002: str | None = None
    attempts: int = 0
    operation_id: str | None = None
    reason_code: str | None = None
    reason: str | None = None
    aml_status: str | None = None

    def __post_init__(self) -> None:
        if not self.history:
            self.history.append(self.state)

    def transition(self, new_state: PaymentState) -> None:
        if new_state not in ALLOWED_TRANSITIONS[self.state]:
            raise InvalidStateTransition(f"Transición no permitida: {self.state.value} → {new_state.value}")
        self.state = new_state
        self.history.append(new_state)

    def as_dict(self) -> dict[str, object]:
        return {
            "instruction_id": getattr(self.request, "instruction_id", None),
            "state": self.state.value,
            "history": [state.value for state in self.history],
            "attempts": self.attempts,
            "operation_id": self.operation_id,
            "reason_code": self.reason_code,
            "reason": self.reason,
            "aml_status": self.aml_status,
            "pacs008": self.pacs008,
            "pacs002": self.pacs002,
        }


class SimulatedGateway:
    """Gateway determinista: consume una secuencia de resultados y luego usa el default."""

    def __init__(
        self,
        outcomes: Iterable[GatewayResult] | None = None,
        *,
        default: GatewayResult = GatewayResult(GatewayOutcome.ACCEPTED),
    ) -> None:
        self._outcomes = list(outcomes or [])
        self._default = default

    def send(self, attempt: int, request: object, message: str) -> GatewayResult:
        if attempt <= len(self._outcomes):
            return self._outcomes[attempt - 1]
        return self._default


AmlHook = Callable[[InternationalPaymentRequest], AmlResult]


def default_aml_hook(request: InternationalPaymentRequest) -> AmlResult:
    return AmlResult(status="ALLOW")


__all__ = [
    "ALLOWED_TRANSITIONS",
    "AmlHook",
    "AmlResult",
    "GatewayOutcome",
    "GatewayResult",
    "IdempotencyConflict",
    "InstantPaymentRequest",
    "InternationalPaymentRequest",
    "InvalidStateTransition",
    "PaymentState",
    "SimulatedGateway",
    "SimulationError",
    "SimulationRecord",
    "SimulationValidationError",
    "default_aml_hook",
    "iso_now",
    "utcnow",
]
