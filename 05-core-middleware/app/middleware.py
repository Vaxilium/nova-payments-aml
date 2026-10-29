"""Adaptador de middleware: interfaz estable entre la API y el core simulado.

En una arquitectura real esta capa representaría un ESB/orquestador de pagos:
recibe la petición del canal, valida el contrato, aplica idempotencia y
correlación, y delega en el core bancario. Aquí se resuelve en proceso para
mantener el caso reproducible y testeable.
"""

from __future__ import annotations

from typing import Any

from .service import BankingService


class PaymentMiddleware:
    """Fachada estable usada por la capa HTTP."""

    def __init__(self, service: BankingService) -> None:
        self.service = service

    def health(self) -> dict[str, Any]:
        return self.service.health()

    def list_customers(self, *, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        return self.service.list_customers(limit=limit, offset=offset)

    def get_customer(self, customer_id: str) -> dict[str, Any]:
        return self.service.get_customer(customer_id)

    def list_accounts(
        self, *, customer_id: str | None = None, limit: int = 50, offset: int = 0
    ) -> list[dict[str, Any]]:
        return self.service.list_accounts(customer_id=customer_id, limit=limit, offset=offset)

    def get_account(self, account_id: str) -> dict[str, Any]:
        return self.service.get_account(account_id)

    def get_balance(self, account_id: str) -> dict[str, Any]:
        return self.service.get_balance(account_id)

    def credit_account(self, **kwargs: Any) -> tuple[dict[str, Any], int, bool]:
        return self.service.credit_account(**kwargs)

    def debit_account(self, **kwargs: Any) -> tuple[dict[str, Any], int, bool]:
        return self.service.debit_account(**kwargs)

    def transfer(self, **kwargs: Any) -> tuple[dict[str, Any], int, bool]:
        return self.service.transfer(**kwargs)

    def get_operation(self, operation_id: str) -> dict[str, Any]:
        return self.service.get_operation(operation_id)


__all__ = ["PaymentMiddleware"]
