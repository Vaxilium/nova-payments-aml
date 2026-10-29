"""Contratos Pydantic de la API /v1."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Channel = Literal["API", "MOBILE", "WEB", "BRANCH", "ATM", "BATCH"]
Currency = Literal["PYG", "USD"]


class HealthResponse(BaseModel):
    status: str
    database: str
    accounts: int
    journal_entries: int


class CustomerOut(BaseModel):
    model_config = ConfigDict(extra="ignore")

    customer_id: str
    customer_type: str
    first_name: str | None = None
    last_name: str | None = None
    business_name: str | None = None
    document_type: str
    document_number: str
    birth_date: str | None = None
    country_code: str
    city: str | None = None
    segment: str
    risk_rating: str
    kyc_status: str
    is_active: bool
    created_at: str
    account_count: int = 0


class AccountOut(BaseModel):
    account_id: str
    customer_id: str
    account_number: str
    account_type: str
    currency: str
    status: str
    balance: str
    balance_minor: int
    overdraft_limit: str
    overdraft_limit_minor: int
    available_balance: str
    version: int
    opened_at: str
    closed_at: str | None = None


class BalanceOut(AccountOut):
    ledger_balance: str
    ledger_balance_minor: int
    reconciled: bool


class CreditRequest(BaseModel):
    amount: Decimal = Field(gt=0, description="Importe mayor que cero en la moneda indicada")
    currency: Currency
    description: str | None = Field(default=None, max_length=280)
    channel: Channel = "API"


class DebitRequest(CreditRequest):
    pass


class TransferRequest(BaseModel):
    from_account_id: str = Field(min_length=3, max_length=40)
    to_account_id: str = Field(min_length=3, max_length=40)
    amount: Decimal = Field(gt=0)
    currency: Currency
    description: str | None = Field(default=None, max_length=280)
    channel: Channel = "API"


class JournalLineOut(BaseModel):
    line_no: int
    gl_account_id: int
    account_id: str | None = None
    currency: str
    debit: str
    credit: str
    debit_minor: int
    credit_minor: int
    description: str | None = None


class JournalEntryOut(BaseModel):
    entry_id: str
    status: str
    entry_date: str
    description: str
    lines: list[JournalLineOut]


class OperationOut(BaseModel):
    operation_id: str
    type: str
    status: str
    currency: str
    amount: str
    amount_minor: int
    counter_amount: str | None = None
    counter_amount_minor: int | None = None
    fee: str
    fee_minor: int
    debit_account_id: str | None = None
    credit_account_id: str | None = None
    debit_account_number: str | None = None
    credit_account_number: str | None = None
    description: str | None = None
    channel: str
    created_at: str
    value_date: str
    posted_at: str | None = None
    entries: list[JournalEntryOut]


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
    correlation_id: str | None = None
