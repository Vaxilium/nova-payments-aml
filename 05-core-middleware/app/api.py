"""Aplicación FastAPI del core y del middleware de pagos."""

from __future__ import annotations

import logging
import time
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, FastAPI, Header, Query, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .config import API_DESCRIPTION, API_PREFIX, API_TITLE, API_VERSION
from .errors import DomainError
from .middleware import PaymentMiddleware
from .schemas import (
    AccountOut,
    BalanceOut,
    CreditRequest,
    CustomerOut,
    DebitRequest,
    ErrorResponse,
    HealthResponse,
    OperationOut,
    TransferRequest,
)
from .service import BankingService

logger = logging.getLogger("novabank.api")


def _correlation_id(request: Request) -> str:
    value = getattr(request.state, "correlation_id", None)
    if value:
        return str(value)
    return request.headers.get("X-Correlation-ID") or f"COR-{uuid.uuid4().hex[:16].upper()}"


def _error_body(request: Request, exc: DomainError) -> dict[str, Any]:
    return {"error": exc.to_dict(), "correlation_id": _correlation_id(request)}


def create_app(db_path: str | Path | None = None) -> FastAPI:
    """Construye la app con una base concreta (útil para tests)."""
    service = BankingService(db_path)
    middleware = PaymentMiddleware(service)

    app = FastAPI(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        contact={"name": "Franco Tillería Centurión", "url": "https://github.com/Vaxilium/nova-payments-aml"},
        license_info={"name": "Caso ficticio de portafolio"},
    )

    @app.middleware("http")
    async def request_context(request: Request, call_next):  # type: ignore[no-untyped-def]
        correlation = request.headers.get("X-Correlation-ID") or f"COR-{uuid.uuid4().hex[:16].upper()}"
        request.state.correlation_id = correlation
        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        response.headers["X-Correlation-ID"] = correlation
        logger.info(
            "%s %s -> %s (%.2f ms) corr=%s",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
            correlation,
        )
        return response

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=_error_body(request, exc))

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        details = [
            {
                "location": ".".join(str(part) for part in error.get("loc", [])),
                "message": error.get("msg", "Valor inválido"),
                "type": error.get("type", "validation_error"),
            }
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "La petición no cumple el contrato de la API",
                    "details": {"errors": details},
                },
                "correlation_id": _correlation_id(request),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Error no controlado en %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Error interno no controlado",
                    "details": {"type": type(exc).__name__},
                },
                "correlation_id": _correlation_id(request),
            },
        )

    router = APIRouter(prefix=API_PREFIX, tags=["core"])

    @router.get("/health", response_model=HealthResponse, summary="Estado del core")
    def health() -> dict[str, Any]:
        return middleware.health()

    @router.get("/customers", response_model=list[CustomerOut], summary="Listar clientes")
    def list_customers(
        limit: int = Query(50, ge=1, le=200),
        offset: int = Query(0, ge=0),
    ) -> list[dict[str, Any]]:
        return middleware.list_customers(limit=limit, offset=offset)

    @router.get("/customers/{customer_id}", response_model=CustomerOut, summary="Consultar cliente")
    def get_customer(customer_id: str) -> dict[str, Any]:
        return middleware.get_customer(customer_id)

    @router.get(
        "/customers/{customer_id}/accounts",
        response_model=list[AccountOut],
        summary="Listar cuentas del cliente",
    )
    def list_customer_accounts(
        customer_id: str,
        limit: int = Query(50, ge=1, le=200),
        offset: int = Query(0, ge=0),
    ) -> list[dict[str, Any]]:
        return middleware.list_accounts(customer_id=customer_id, limit=limit, offset=offset)

    @router.get("/accounts", response_model=list[AccountOut], summary="Listar cuentas")
    def list_accounts(
        customer_id: str | None = Query(None),
        limit: int = Query(50, ge=1, le=200),
        offset: int = Query(0, ge=0),
    ) -> list[dict[str, Any]]:
        return middleware.list_accounts(customer_id=customer_id, limit=limit, offset=offset)

    @router.get("/accounts/{account_id}", response_model=AccountOut, summary="Consultar cuenta")
    def get_account(account_id: str) -> dict[str, Any]:
        return middleware.get_account(account_id)

    @router.get(
        "/accounts/{account_id}/balance",
        response_model=BalanceOut,
        summary="Saldo contable y conciliación con el libro mayor",
    )
    def get_balance(account_id: str) -> dict[str, Any]:
        return middleware.get_balance(account_id)

    @router.post(
        "/accounts/{account_id}/credits",
        response_model=OperationOut,
        status_code=201,
        summary="Acreditar (depósito) en una cuenta",
    )
    def credit_account(
        account_id: str,
        body: CreditRequest,
        request: Request,
        response: Response,
        idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
        actor: str = Header("api-client", alias="X-Actor"),
    ) -> dict[str, Any]:
        result, status_code, replayed = middleware.credit_account(
            account_id=account_id,
            amount=body.amount,
            currency=body.currency,
            description=body.description,
            channel=body.channel,
            idempotency_key=idempotency_key,
            actor=actor,
            correlation_id=_correlation_id(request),
        )
        response.status_code = status_code
        response.headers["Idempotent-Replayed"] = "true" if replayed else "false"
        return result

    @router.post(
        "/accounts/{account_id}/debits",
        response_model=OperationOut,
        status_code=201,
        summary="Debitar (retiro) de una cuenta",
    )
    def debit_account(
        account_id: str,
        body: DebitRequest,
        request: Request,
        response: Response,
        idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
        actor: str = Header("api-client", alias="X-Actor"),
    ) -> dict[str, Any]:
        result, status_code, replayed = middleware.debit_account(
            account_id=account_id,
            amount=body.amount,
            currency=body.currency,
            description=body.description,
            channel=body.channel,
            idempotency_key=idempotency_key,
            actor=actor,
            correlation_id=_correlation_id(request),
        )
        response.status_code = status_code
        response.headers["Idempotent-Replayed"] = "true" if replayed else "false"
        return result

    @router.post(
        "/transfers",
        response_model=OperationOut,
        status_code=201,
        summary="Transferir entre cuentas de la misma moneda",
    )
    def transfer(
        body: TransferRequest,
        request: Request,
        response: Response,
        idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
        actor: str = Header("api-client", alias="X-Actor"),
    ) -> dict[str, Any]:
        result, status_code, replayed = middleware.transfer(
            from_account_id=body.from_account_id,
            to_account_id=body.to_account_id,
            amount=body.amount,
            currency=body.currency,
            description=body.description,
            channel=body.channel,
            idempotency_key=idempotency_key,
            actor=actor,
            correlation_id=_correlation_id(request),
        )
        response.status_code = status_code
        response.headers["Idempotent-Replayed"] = "true" if replayed else "false"
        return result

    @router.get(
        "/operations/{operation_id}",
        response_model=OperationOut,
        summary="Estado de una operación y sus asientos",
    )
    def get_operation(operation_id: str) -> dict[str, Any]:
        return middleware.get_operation(operation_id)

    app.include_router(router)

    app.state.service = service
    app.state.middleware = middleware
    return app
