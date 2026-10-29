"""Errores de dominio con códigos estables para la API."""

from __future__ import annotations

from typing import Any


class DomainError(Exception):
    """Error de negocio con traducción HTTP y código estable."""

    status_code = 400
    code = "DOMAIN_ERROR"

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.details:
            payload["details"] = self.details
        return payload


class NotFoundError(DomainError):
    status_code = 404
    code = "NOT_FOUND"


class CustomerNotFoundError(NotFoundError):
    code = "CUSTOMER_NOT_FOUND"


class AccountNotFoundError(NotFoundError):
    code = "ACCOUNT_NOT_FOUND"


class OperationNotFoundError(NotFoundError):
    code = "OPERATION_NOT_FOUND"


class AccountBlockedError(DomainError):
    status_code = 409
    code = "ACCOUNT_NOT_ACTIVE"


class InsufficientFundsError(DomainError):
    status_code = 422
    code = "INSUFFICIENT_FUNDS"


class CurrencyMismatchError(DomainError):
    status_code = 422
    code = "CURRENCY_MISMATCH"


class InvalidOperationError(DomainError):
    status_code = 422
    code = "INVALID_OPERATION"


class IdempotencyKeyRequiredError(DomainError):
    status_code = 400
    code = "IDEMPOTENCY_KEY_REQUIRED"


class IdempotencyConflictError(DomainError):
    status_code = 409
    code = "IDEMPOTENCY_CONFLICT"


class ConcurrentModificationError(DomainError):
    status_code = 409
    code = "CONCURRENT_MODIFICATION"
