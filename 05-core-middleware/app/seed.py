"""Generador reproducible de datos sintéticos del core bancario.

Produce clientes, cuentas, movimientos, libro mayor y una tabla interna de
verdad con patrones sospechosos para validar las reglas AML de la Fase 5.
No usa PII real: nombres, documentos y cuentas son ficticios.
"""

from __future__ import annotations

import json
import random
import sqlite3
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any, Iterable

from .audit import utcnow, write_audit
from .closing import rebuild_daily_balances
from .config import DEFAULT_SEED, resolve_db_path
from .db import connect, init_schema
from .ledger import (
    CASH_BY_CURRENCY,
    CUSTOMER_DEPOSITS_BY_CURRENCY,
    FEE_INCOME_BY_CURRENCY,
    FX_POSITION_BY_CURRENCY,
    GL_ACCOUNTS,
    GL_BY_CONCEPT,
    LedgerLine,
    load_gl_map,
    post_entry,
)

FIRST_NAMES = [
    "Ana", "Carlos", "Lucía", "Miguel", "Sofía", "Diego", "María", "Jorge",
    "Camila", "Rodrigo", "Valeria", "Fernando", "Gabriela", "Andrés", "Patricia",
    "Nicolás", "Elena", "Sebastián", "Rocío", "Hugo", "Natalia", "Óscar",
    "Verónica", "Alejandro", "Cecilia", "Ramón", "Antonella", "Marcelo",
    "Fátima", "Gustavo", "Lorena", "Iván", "Daniela", "Rafael", "Mónica",
]
LAST_NAMES = [
    "González", "Benítez", "Martínez", "López", "Acosta", "Villalba", "Ramírez",
    "Cáceres", "Giménez", "Rojas", "Fernández", "Ortiz", "Bogado", "Amarilla",
    "Insfrán", "Ruiz Díaz", "Cardozo", "Franco", "Vega", "Cabrera", "Ayala",
    "Duarte", "Sosa", "Paredes", "Morel", "Ojeda", "Zárate", "Aguirre",
]
BUSINESS_NAMES = [
    "Comercial del Este", "Logística Guaraní", "Agro Sur", "Farmacias del Sol",
    "Tecnología Asunción", "Constructora Paraná", "Distribuidora Central",
    "Servicios Integrados", "Transporte Itapúa", "Alimentos del Chaco",
    "Importadora del Plata", "Talleres San Blas", "Consultora Aurora",
    "Hotel Río Verde", "Estación del Sur",
]
BUSINESS_SUFFIXES = ["S.A.", "S.R.L.", "E.A.S.", "S.A.C.I."]
CITIES = ["Asunción", "Ciudad del Este", "Encarnación", "San Lorenzo", "Luque", "Capiatá", "Fernando de la Mora"]
COUNTRIES = ["PRY", "ARG", "BRA", "URY", "USA", "ESP"]
COUNTRY_WEIGHTS = [90, 3, 2, 2, 2, 1]


@dataclass(frozen=True)
class SeedConfig:
    customers: int = 500
    accounts: int = 800
    transactions: int = 50_000
    months: int = 6
    seed: int = DEFAULT_SEED
    start_date: date = date(2026, 4, 1)


@dataclass
class PlannedEvent:
    when: datetime
    pattern_type: str | None = None
    kind: str | None = None
    debit_account_id: str | None = None
    credit_account_id: str | None = None
    amount_minor: int | None = None
    currency: str | None = None
    note: str | None = None


@dataclass
class AccountInfo:
    account_id: str
    customer_id: str
    currency: str
    status: str
    balance: int


@dataclass
class SeedSummary:
    customers: int = 0
    accounts: int = 0
    transactions: int = 0
    journal_entries: int = 0
    journal_lines: int = 0
    daily_balance_rows: int = 0
    suspicious_transactions: int = 0
    normal_sample: int = 0
    by_type: dict[str, int] = field(default_factory=dict)
    by_pattern: dict[str, int] = field(default_factory=dict)
    totals_by_currency: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "customers": self.customers,
            "accounts": self.accounts,
            "transactions": self.transactions,
            "journal_entries": self.journal_entries,
            "journal_lines": self.journal_lines,
            "daily_balance_rows": self.daily_balance_rows,
            "suspicious_transactions": self.suspicious_transactions,
            "normal_sample": self.normal_sample,
            "by_type": self.by_type,
            "by_pattern": self.by_pattern,
            "totals_by_currency": self.totals_by_currency,
        }


def _weighted_country(rng: random.Random) -> str:
    return rng.choices(COUNTRIES, weights=COUNTRY_WEIGHTS, k=1)[0]


def _random_datetime(rng: random.Random, start: datetime, days: int) -> datetime:
    moment = start + timedelta(days=rng.randrange(days))
    if rng.random() < 0.82:
        hour = rng.randint(7, 20)
    else:
        hour = rng.randint(0, 23)
    return moment.replace(hour=hour, minute=rng.randint(0, 59), second=rng.randint(0, 59))


def _money(rng: random.Random, currency: str, *, high: bool = False) -> int:
    if currency == "PYG":
        if high:
            return rng.randint(40_000, 120_000) * 1_000
        return rng.randint(2_000, 60_000) * 1_000
    if high:
        return rng.randint(20_000, 120_000) * 100
    return rng.randint(500, 40_000) * 100


def seed_database(
    db_path: str | Path | None = None,
    *,
    config: SeedConfig | None = None,
    reset: bool = True,
) -> SeedSummary:
    """Crea y puebla la base; devuelve métricas del dataset generado."""
    cfg = config or SeedConfig()
    rng = random.Random(cfg.seed)
    path = resolve_db_path(db_path)
    conn = connect(path)
    try:
        init_schema(conn, reset=reset)
        summary = _seed(conn, cfg, rng)
    except BaseException:
        conn.close()
        raise
    conn.close()
    return summary


def _seed(conn: sqlite3.Connection, cfg: SeedConfig, rng: random.Random) -> SeedSummary:
    start_dt = datetime.combine(cfg.start_date, time.min)
    end_dt = start_dt + timedelta(days=cfg.months * 30 + 3)
    total_days = (end_dt - start_dt).days
    timestamp_seed = utcnow()

    conn.execute("BEGIN")
    _insert_catalogs(conn)
    gl_map = load_gl_map(conn)

    customers = _build_customers(cfg, rng)
    conn.executemany(
        """
        INSERT INTO customers
            (customer_id, customer_type, first_name, last_name, business_name,
             document_type, document_number, birth_date, country_code, city,
             segment, risk_rating, kyc_status, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        customers,
    )

    accounts, account_index = _build_accounts(cfg, rng, customers)
    conn.executemany(
        """
        INSERT INTO accounts
            (account_id, customer_id, account_number, account_type, currency,
             status, balance_minor, overdraft_limit_minor, version, opened_at, closed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?, NULL)
        """,
        accounts,
    )

    rates, rates_by_date = _build_fx_rates(cfg, rng, start_dt, end_dt)
    conn.executemany(
        """
        INSERT INTO fx_rates
            (rate_id, rate_date, base_currency, quote_currency, rate, source, created_at)
        VALUES (?, ?, 'USD', 'PYG', ?, 'NOVABANK-SIM', ?)
        """,
        rates,
    )

    _insert_opening_entries(conn, account_index, cfg.start_date, gl_map)

    events, suspicious = _build_events(cfg, rng, start_dt, total_days, account_index)
    events.sort(key=lambda event: event.when)

    tx_rows: list[tuple[Any, ...]] = []
    entry_rows: list[tuple[Any, ...]] = []
    line_rows: list[tuple[Any, ...]] = []
    fee_rows: list[tuple[Any, ...]] = []
    truth_rows: list[tuple[Any, ...]] = []
    normal_ids: list[str] = []

    for event in events:
        record = _book_event(
            event=event,
            rng=rng,
            account_index=account_index,
            rates_by_date=rates_by_date,
            tx_rows=tx_rows,
            entry_rows=entry_rows,
            line_rows=line_rows,
            fee_rows=fee_rows,
            gl_map=gl_map,
        )
        if record is None:
            continue
        tx_id, width = record
        if event.pattern_type:
            truth_rows.append(
                (
                    tx_id,
                    account_index[event.debit_account_id or event.credit_account_id].customer_id,
                    event.pattern_type,
                    "SUSPICIOUS",
                    event.note,
                    timestamp_seed,
                )
            )
        else:
            normal_ids.append(tx_id)

    tx_customer: dict[str, str] = {}
    for row in tx_rows:
        account_id = row[6] or row[7]
        tx_customer[row[0]] = account_index[account_id].customer_id

    sample_size = max(1, len(normal_ids) // 100) if normal_ids else 0
    for tx_id in rng.sample(normal_ids, k=min(sample_size, len(normal_ids))):
        customer_id = tx_customer[tx_id]
        truth_rows.append(
            (
                tx_id,
                customer_id,
                None,
                "NORMAL",
                "Muestra aleatoria de operaciones normales",
                timestamp_seed,
            )
        )

    conn.executemany(
        """
        INSERT INTO transactions
            (transaction_id, transaction_type, status, currency, amount_minor,
             counter_amount_minor, debit_account_id, credit_account_id, fx_rate_id,
             fee_minor, description, channel, idempotency_key, correlation_id,
             external_ref, created_at, value_date, posted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, NULL, ?, ?, ?)
        """,
        tx_rows,
    )
    conn.executemany(
        """
        INSERT INTO journal_entries
            (entry_id, entry_date, description, source_type, source_id, status,
             correlation_id, created_by, created_at, posted_at)
        VALUES (?, ?, ?, ?, ?, 'DRAFT', ?, 'seed', ?, NULL)
        """,
        entry_rows,
    )
    conn.executemany(
        """
        INSERT INTO journal_lines
            (entry_id, line_no, gl_account_id, account_id, currency,
             debit_minor, credit_minor, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        line_rows,
    )
    conn.executemany(
        """
        INSERT INTO fees
            (transaction_id, fee_type, currency, amount_minor, gl_account_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        fee_rows,
    )
    conn.execute("UPDATE journal_entries SET status = 'POSTED', posted_at = created_at WHERE status = 'DRAFT'")
    conn.executemany(
        "UPDATE accounts SET balance_minor = ?, version = version + 1 WHERE account_id = ?",
        [(info.balance, info.account_id) for info in account_index.values()],
    )
    conn.executemany(
        """
        INSERT INTO _aml_ground_truth
            (transaction_id, customer_id, pattern_type, label, notes, generated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        truth_rows,
    )

    daily_rows = rebuild_daily_balances(conn)

    type_counter = Counter(row[1] for row in tx_rows)
    pattern_counter = Counter(row[2] for row in truth_rows if row[3] == "SUSPICIOUS")
    totals: dict[str, int] = {}
    for currency in ("PYG", "USD"):
        totals[currency] = sum(
            info.balance for info in account_index.values() if info.currency == currency
        )

    entry_count = int(conn.execute("SELECT COUNT(*) FROM journal_entries").fetchone()[0])
    line_count = int(conn.execute("SELECT COUNT(*) FROM journal_lines").fetchone()[0])
    summary = SeedSummary(
        customers=len(customers),
        accounts=len(accounts),
        transactions=len(tx_rows),
        journal_entries=entry_count,
        journal_lines=line_count,
        daily_balance_rows=daily_rows,
        suspicious_transactions=sum(pattern_counter.values()),
        normal_sample=sum(1 for row in truth_rows if row[3] == "NORMAL"),
        by_type=dict(sorted(type_counter.items())),
        by_pattern=dict(sorted(pattern_counter.items())),
        totals_by_currency=totals,
    )
    write_audit(
        conn,
        event_type="SEED_COMPLETED",
        entity_type="DATABASE",
        entity_id=str(path_of(conn)),
        actor="seed",
        payload=summary.to_dict(),
        created_at=timestamp_seed,
    )
    conn.execute("COMMIT")
    return summary


def path_of(conn: sqlite3.Connection) -> str:
    row = conn.execute("PRAGMA database_list").fetchone()
    return str(row[2]) if row else "memory"


def _insert_catalogs(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT INTO currencies (code, name, minor_unit, symbol) VALUES (?, ?, ?, ?)",
        [
            ("PYG", "Guaraní paraguayo", 0, "₲"),
            ("USD", "Dólar estadounidense", 2, "US$"),
        ],
    )
    conn.executemany(
        """
        INSERT INTO gl_accounts (code, name, account_class, normal_side, is_active)
        VALUES (?, ?, ?, ?, 1)
        """,
        [(gl["code"], gl["name"], gl["account_class"], gl["normal_side"]) for gl in GL_ACCOUNTS],
    )


def _build_customers(cfg: SeedConfig, rng: random.Random) -> list[tuple[Any, ...]]:
    rows: list[tuple[Any, ...]] = []
    pattern_pool = min(40, cfg.customers)
    earliest = datetime(2025, 1, 1)
    latest = datetime.combine(cfg.start_date, time.min) - timedelta(days=1)
    for index in range(1, cfg.customers + 1):
        customer_id = f"CUS-{index:06d}"
        is_business = rng.random() < 0.18
        country = _weighted_country(rng)
        created = earliest + timedelta(seconds=rng.randrange(int((latest - earliest).total_seconds())))
        is_pattern = index <= pattern_pool
        if is_business:
            first_name = None
            last_name = None
            business_name = f"{rng.choice(BUSINESS_NAMES)} {rng.choice(BUSINESS_SUFFIXES)}"
            document_type = "RUC"
            document_number = f"RUC-{rng.randint(10_000_000, 99_999_999)}-{rng.randint(0, 9)}"
            segment = rng.choices(["SME", "CORPORATE", "RETAIL"], weights=[55, 20, 25], k=1)[0]
            birth_date = None
        else:
            first_name = rng.choice(FIRST_NAMES)
            last_name = f"{rng.choice(LAST_NAMES)} {rng.choice(LAST_NAMES)}"
            business_name = None
            document_type = "CI"
            document_number = f"CI-{rng.randint(1_000_000, 9_999_999)}"
            segment = rng.choices(["RETAIL", "PREMIUM"], weights=[85, 15], k=1)[0]
            birth_date = (date(1955, 1, 1) + timedelta(days=rng.randint(0, 20_000))).isoformat()
        if is_pattern:
            risk = "HIGH"
            kyc = "VERIFIED"
        else:
            risk = rng.choices(["LOW", "MEDIUM", "HIGH"], weights=[78, 17, 5], k=1)[0]
            kyc = rng.choices(["VERIFIED", "PENDING", "REJECTED"], weights=[94, 5, 1], k=1)[0]
        rows.append(
            (
                customer_id,
                "BUSINESS" if is_business else "INDIVIDUAL",
                first_name,
                last_name,
                business_name,
                document_type,
                document_number,
                birth_date,
                country,
                rng.choice(CITIES),
                segment,
                risk,
                kyc,
                int(kyc != "REJECTED"),
                created.replace(microsecond=0).isoformat(),
            )
        )
    return rows


def _build_accounts(
    cfg: SeedConfig, rng: random.Random, customers: list[tuple[Any, ...]]
) -> tuple[list[tuple[Any, ...]], dict[str, AccountInfo]]:
    rows: list[tuple[Any, ...]] = []
    index: dict[str, AccountInfo] = {}
    by_customer: dict[str, list[str]] = {}
    pattern_pool = min(40, cfg.customers)
    account_number = 0
    customer_created = {row[0]: row[14] for row in customers}

    def add_account(customer_id: str, currency: str, *, high_balance: bool) -> None:
        nonlocal account_number
        account_number += 1
        account_id = f"ACC-{account_number:06d}"
        account_type = rng.choices(["SAVINGS", "CHECKING"], weights=[62, 38], k=1)[0]
        balance = _money(rng, currency, high=high_balance)
        overdraft = 0
        if rng.random() < 0.04:
            overdraft = 1_000_000 if currency == "PYG" else 50_000
        status = "ACTIVE"
        if rng.random() < 0.008:
            status = "BLOCKED"
        opened = datetime.fromisoformat(customer_created[customer_id]) + timedelta(days=rng.randint(0, 60))
        max_open = datetime.combine(cfg.start_date, time.min) - timedelta(days=1)
        if opened > max_open:
            opened = max_open
        rows.append(
            (
                account_id,
                customer_id,
                f"{account_number:014d}",
                account_type,
                currency,
                status,
                balance,
                overdraft,
                opened.replace(microsecond=0).isoformat(),
            )
        )
        index[account_id] = AccountInfo(account_id, customer_id, currency, status, balance)
        by_customer.setdefault(customer_id, []).append(account_id)

    customer_ids = [row[0] for row in customers]
    for offset, customer_id in enumerate(customer_ids, start=1):
        currency = "PYG" if offset <= pattern_pool else rng.choices(["PYG", "USD"], weights=[72, 28], k=1)[0]
        add_account(customer_id, currency, high_balance=offset <= pattern_pool)

    extra = max(0, cfg.accounts - cfg.customers)
    for _ in range(extra):
        customer_id = rng.choice(customer_ids)
        existing = {index[account_id].currency for account_id in by_customer[customer_id]}
        if len(existing) == 1:
            currency = "USD" if "USD" not in existing else "PYG"
        else:
            currency = rng.choice(["PYG", "USD"])
        add_account(customer_id, currency, high_balance=False)

    return rows, index


def _build_fx_rates(
    cfg: SeedConfig, rng: random.Random, start_dt: datetime, end_dt: datetime
) -> tuple[list[tuple[Any, ...]], dict[str, tuple[int, float]]]:
    rows: list[tuple[Any, ...]] = []
    by_date: dict[str, tuple[int, float]] = {}
    rate_id = 0
    first = start_dt.date() - timedelta(days=35)
    last = end_dt.date()
    total = (last - first).days + 1
    for day_offset in range(total):
        day = first + timedelta(days=day_offset)
        rate = 7_180 + day_offset * 0.55 + rng.uniform(-32, 32)
        rate = round(rate, 4)
        rate_id += 1
        rows.append((rate_id, day.isoformat(), rate, f"{day.isoformat()}T00:00:00"))
        by_date[day.isoformat()] = (rate_id, rate)
    return rows, by_date


def _insert_opening_entries(
    conn: sqlite3.Connection,
    account_index: dict[str, AccountInfo],
    start_date: date,
    gl_map: dict[str, int],
) -> None:
    opening_date = (start_date - timedelta(days=1)).isoformat()
    for currency in ("PYG", "USD"):
        accounts = [info for info in account_index.values() if info.currency == currency and info.balance > 0]
        if not accounts:
            continue
        total = sum(info.balance for info in accounts)
        lines = [
            LedgerLine(
                CASH_BY_CURRENCY[currency],
                currency,
                debit_minor=total,
                description="Saldo inicial de caja",
            )
        ]
        lines.extend(
            LedgerLine(
                CUSTOMER_DEPOSITS_BY_CURRENCY[currency],
                currency,
                credit_minor=info.balance,
                account_id=info.account_id,
                description="Saldo inicial de cliente",
            )
            for info in accounts
        )
        post_entry(
            conn,
            entry_id=f"JE-OPEN-{currency}",
            entry_date=opening_date,
            description="Apertura contable del core simulado",
            source_type="OPENING",
            created_by="seed",
            created_at=f"{opening_date}T00:00:00",
            gl_map=gl_map,
            lines=lines,
        )


def _build_events(
    cfg: SeedConfig,
    rng: random.Random,
    start_dt: datetime,
    total_days: int,
    account_index: dict[str, AccountInfo],
) -> tuple[list[PlannedEvent], int]:
    by_customer: dict[str, list[str]] = {}
    for info in account_index.values():
        by_customer.setdefault(info.customer_id, []).append(info.account_id)

    pattern_pool = sorted({info.customer_id for info in account_index.values()})[: min(40, cfg.customers)]
    cursor = 0

    def take(count: int) -> list[str]:
        nonlocal cursor
        selected = pattern_pool[cursor: cursor + count]
        cursor += max(count, 0)
        return selected

    structuring = take(max(1, len(pattern_pool) // 4))
    pass_through = take(max(1, len(pattern_pool) // 5))
    velocity = take(max(1, len(pattern_pool) // 8))
    mules = take(max(1, len(pattern_pool) // 8))
    dormant = take(max(1, len(pattern_pool) // 13))

    def pyg_account(customer_id: str) -> str | None:
        for account_id in by_customer.get(customer_id, []):
            if account_index[account_id].currency == "PYG" and account_index[account_id].status == "ACTIVE":
                return account_id
        return None

    suspicious: list[PlannedEvent] = []

    for customer_id in structuring:
        account_id = pyg_account(customer_id)
        if not account_id:
            continue
        base_day = start_dt + timedelta(days=rng.randint(30, max(31, total_days - 40)))
        for n in range(10):
            moment = (base_day + timedelta(days=n % 3)).replace(
                hour=rng.randint(9, 17), minute=rng.randint(0, 59), second=rng.randint(0, 59)
            )
            suspicious.append(
                PlannedEvent(
                    when=moment,
                    pattern_type="STRUCTURING",
                    kind="DEPOSIT",
                    credit_account_id=account_id,
                    amount_minor=rng.randint(9_000, 9_900) * 1_000,
                    currency="PYG",
                    note="Depósito repetido justo por debajo del umbral de ₲10.000.000",
                )
            )

    mule_accounts = [pyg_account(customer_id) for customer_id in mules]
    mule_accounts = [account_id for account_id in mule_accounts if account_id]
    for customer_id in pass_through:
        account_id = pyg_account(customer_id)
        if not account_id:
            continue
        for _ in range(6):
            day = start_dt + timedelta(days=rng.randint(40, max(41, total_days - 30)))
            source_moment = day.replace(
                hour=rng.randint(8, 16), minute=rng.randint(0, 59), second=rng.randint(0, 59)
            )
            amount = rng.randint(5_000, 8_900) * 1_000
            target = rng.choice(mule_accounts) if mule_accounts else account_id
            if target == account_id:
                continue
            suspicious.append(
                PlannedEvent(
                    when=source_moment,
                    pattern_type="PASS_THROUGH",
                    kind="DEPOSIT",
                    credit_account_id=account_id,
                    amount_minor=amount,
                    currency="PYG",
                    note="Ingreso seguido de transferencia de salida en menos de una hora",
                )
            )
            suspicious.append(
                PlannedEvent(
                    when=source_moment + timedelta(minutes=rng.randint(5, 50)),
                    pattern_type="PASS_THROUGH",
                    kind="TRANSFER",
                    debit_account_id=account_id,
                    credit_account_id=target,
                    amount_minor=int(amount * rng.uniform(0.9, 1.0)),
                    currency="PYG",
                    note="Salida rápida hacia cuenta receptora de bajo perfil",
                )
            )

    for customer_id in velocity:
        account_id = pyg_account(customer_id)
        if not account_id:
            continue
        day = start_dt + timedelta(days=rng.randint(40, max(41, total_days - 20)))
        for n in range(25):
            moment = day.replace(hour=8, minute=0, second=0) + timedelta(minutes=n * 18)
            target = rng.choice(list(account_index))
            if account_index[target].currency != "PYG" or target == account_id:
                continue
            suspicious.append(
                PlannedEvent(
                    when=moment,
                    pattern_type="HIGH_VELOCITY",
                    kind="TRANSFER",
                    debit_account_id=account_id,
                    credit_account_id=target,
                    amount_minor=rng.randint(100, 450) * 1_000,
                    currency="PYG",
                    note="Alta velocidad de transferencias en una sola jornada",
                )
            )

    for account_id in mule_accounts:
        for n in range(15):
            moment = (start_dt + timedelta(days=rng.randint(20, max(21, total_days - 10)))).replace(
                hour=rng.randint(8, 18), minute=rng.randint(0, 59), second=0
            )
            suspicious.append(
                PlannedEvent(
                    when=moment,
                    pattern_type="ROUND_MULE",
                    kind="DEPOSIT",
                    credit_account_id=account_id,
                    amount_minor=rng.choice([1_000, 2_000, 5_000, 10_000]) * 1_000,
                    currency="PYG",
                    note="Depósitos en montos redondos hacia cuenta mula",
                )
            )

    for customer_id in dormant:
        account_id = pyg_account(customer_id)
        if not account_id:
            continue
        moment = (start_dt + timedelta(days=max(1, total_days - 20))).replace(
            hour=rng.randint(9, 17), minute=rng.randint(0, 59), second=0
        )
        suspicious.append(
            PlannedEvent(
                when=moment,
                pattern_type="DORMANT_ACTIVATION",
                kind="DEPOSIT",
                credit_account_id=account_id,
                amount_minor=rng.randint(7_000, 8_500) * 1_000,
                currency="PYG",
                note="Reactivación de cuenta inactiva con ingreso alto",
            )
        )

    normal_count = max(0, cfg.transactions - len(suspicious))
    events: list[PlannedEvent] = [
        PlannedEvent(when=_random_datetime(rng, start_dt, total_days)) for _ in range(normal_count)
    ]
    events.extend(suspicious)
    return events, len(suspicious)


def _book_event(
    *,
    event: PlannedEvent,
    rng: random.Random,
    account_index: dict[str, AccountInfo],
    rates_by_date: dict[str, tuple[int, float]],
    tx_rows: list[tuple[Any, ...]],
    entry_rows: list[tuple[Any, ...]],
    line_rows: list[tuple[Any, ...]],
    fee_rows: list[tuple[Any, ...]],
    gl_map: dict[str, int],
) -> tuple[str, int] | None:
    if event.pattern_type:
        return _book_pattern_event(
            event=event,
            account_index=account_index,
            rates_by_date=rates_by_date,
            tx_rows=tx_rows,
            entry_rows=entry_rows,
            line_rows=line_rows,
            fee_rows=fee_rows,
            gl_map=gl_map,
        )
    return _book_normal_event(
        event=event,
        rng=rng,
        account_index=account_index,
        rates_by_date=rates_by_date,
        tx_rows=tx_rows,
        entry_rows=entry_rows,
        line_rows=line_rows,
        fee_rows=fee_rows,
        gl_map=gl_map,
    )


def _book_pattern_event(
    *,
    event: PlannedEvent,
    account_index: dict[str, AccountInfo],
    rates_by_date: dict[str, tuple[int, float]],
    tx_rows: list[tuple[Any, ...]],
    entry_rows: list[tuple[Any, ...]],
    line_rows: list[tuple[Any, ...]],
    fee_rows: list[tuple[Any, ...]],
    gl_map: dict[str, int],
) -> tuple[str, int] | None:
    kind = event.kind or "DEPOSIT"
    currency = event.currency or "PYG"
    amount = event.amount_minor or 0
    credit_id = event.credit_account_id
    debit_id = event.debit_account_id

    if kind in {"WITHDRAWAL", "TRANSFER", "FEE"} and debit_id:
        available = account_index[debit_id].balance
        if available <= 10_000:
            return None
        amount = min(amount, max(10_000, int(available * 0.5)))
    if kind == "TRANSFER" and (not debit_id or not credit_id or debit_id == credit_id):
        return None
    if kind == "DEPOSIT" and not credit_id:
        return None

    return _append_transaction(
        when=event.when,
        kind=kind,
        currency=currency,
        amount=amount,
        debit_id=debit_id,
        credit_id=credit_id,
        account_index=account_index,
        rates_by_date=rates_by_date,
        tx_rows=tx_rows,
        entry_rows=entry_rows,
        line_rows=line_rows,
        fee_rows=fee_rows,
        gl_map=gl_map,
        description=event.note,
    )


def _book_normal_event(
    *,
    event: PlannedEvent,
    rng: random.Random,
    account_index: dict[str, AccountInfo],
    rates_by_date: dict[str, tuple[int, float]],
    tx_rows: list[tuple[Any, ...]],
    entry_rows: list[tuple[Any, ...]],
    line_rows: list[tuple[Any, ...]],
    fee_rows: list[tuple[Any, ...]],
    gl_map: dict[str, int],
) -> tuple[str, int] | None:
    candidate = rng.choice(list(account_index.values()))
    if candidate.status != "ACTIVE":
        return None
    currency = candidate.currency
    kind = rng.choices(
        ["DEPOSIT", "WITHDRAWAL", "TRANSFER", "FEE", "FX"],
        weights=[30, 18, 37, 10, 5],
        k=1,
    )[0]

    if kind == "FX":
        pair = _fx_pair(rng, account_index)
        if pair is None:
            kind = "TRANSFER"
        else:
            source_id, target_id = pair
            source_balance = account_index[source_id].balance
            if source_balance < 100_000:
                kind = "DEPOSIT"
                currency = "PYG"
            else:
                amount = min(rng.randint(500, 5_000) * 1_000, int(source_balance * 0.20))
                return _append_transaction(
                    when=event.when,
                    kind="FX",
                    currency="PYG",
                    amount=amount,
                    debit_id=source_id,
                    credit_id=target_id,
                    account_index=account_index,
                    rates_by_date=rates_by_date,
                    tx_rows=tx_rows,
                    entry_rows=entry_rows,
                    line_rows=line_rows,
                    fee_rows=fee_rows,
                    gl_map=gl_map,
                    description="Conversión de moneda del cliente",
                )

    if kind == "DEPOSIT":
        target = rng.choice(list(account_index.values()))
        while target.status != "ACTIVE":
            target = rng.choice(list(account_index.values()))
        amount = _movement_amount(rng, target.balance, target.currency)
        if amount <= 0:
            return None
        return _append_transaction(
            when=event.when,
            kind="DEPOSIT",
            currency=target.currency,
            amount=amount,
            debit_id=None,
            credit_id=target.account_id,
            account_index=account_index,
            rates_by_date=rates_by_date,
            tx_rows=tx_rows,
            entry_rows=entry_rows,
            line_rows=line_rows,
            fee_rows=fee_rows,
            gl_map=gl_map,
            description="Depósito de cliente",
        )

    if kind == "TRANSFER":
        target = rng.choice(list(account_index.values()))
        attempts = 0
        while (
            target.status != "ACTIVE"
            or target.currency != candidate.currency
            or target.account_id == candidate.account_id
        ):
            target = rng.choice(list(account_index.values()))
            attempts += 1
            if attempts > 20:
                return None
        amount = _movement_amount(rng, candidate.balance, candidate.currency, max_pct=0.06)
        if amount <= 0 or candidate.balance - amount < 0:
            return None
        return _append_transaction(
            when=event.when,
            kind="TRANSFER",
            currency=candidate.currency,
            amount=amount,
            debit_id=candidate.account_id,
            credit_id=target.account_id,
            account_index=account_index,
            rates_by_date=rates_by_date,
            tx_rows=tx_rows,
            entry_rows=entry_rows,
            line_rows=line_rows,
            fee_rows=fee_rows,
            gl_map=gl_map,
            description="Transferencia entre clientes",
        )

    if kind == "WITHDRAWAL":
        amount = _movement_amount(rng, candidate.balance, candidate.currency, max_pct=0.05)
        if amount <= 0 or candidate.balance - amount < 0:
            return None
        return _append_transaction(
            when=event.when,
            kind="WITHDRAWAL",
            currency=candidate.currency,
            amount=amount,
            debit_id=candidate.account_id,
            credit_id=None,
            account_index=account_index,
            rates_by_date=rates_by_date,
            tx_rows=tx_rows,
            entry_rows=entry_rows,
            line_rows=line_rows,
            fee_rows=fee_rows,
            gl_map=gl_map,
            description="Retiro de cliente",
        )

    amount = 5_000 if candidate.currency == "PYG" else 500
    if candidate.balance < amount * 2:
        return None
    return _append_transaction(
        when=event.when,
        kind="FEE",
        currency=candidate.currency,
        amount=amount,
        debit_id=candidate.account_id,
        credit_id=None,
        account_index=account_index,
        rates_by_date=rates_by_date,
        tx_rows=tx_rows,
        entry_rows=entry_rows,
        line_rows=line_rows,
        fee_rows=fee_rows,
        gl_map=gl_map,
        description="Comisión de servicio",
    )


def _fx_pair(rng: random.Random, account_index: dict[str, AccountInfo]) -> tuple[str, str] | None:
    by_customer: dict[str, dict[str, str]] = {}
    for info in account_index.values():
        if info.status != "ACTIVE":
            continue
        by_customer.setdefault(info.customer_id, {})[info.currency] = info.account_id
    candidates = [
        (currencies["PYG"], currencies["USD"])
        for currencies in by_customer.values()
        if "PYG" in currencies and "USD" in currencies
    ]
    return rng.choice(candidates) if candidates else None


def _movement_amount(rng: random.Random, balance: int, currency: str, *, max_pct: float = 0.10) -> int:
    if currency == "PYG":
        base = rng.randint(30, 4_000) * 1_000
    else:
        base = rng.randint(1_000, 200_000)
    cap = int(balance * max_pct)
    return max(0, min(base, cap))


def _append_transaction(
    *,
    when: datetime,
    kind: str,
    currency: str,
    amount: int,
    debit_id: str | None,
    credit_id: str | None,
    account_index: dict[str, AccountInfo],
    rates_by_date: dict[str, tuple[int, float]],
    tx_rows: list[tuple[Any, ...]],
    entry_rows: list[tuple[Any, ...]],
    line_rows: list[tuple[Any, ...]],
    fee_rows: list[tuple[Any, ...]],
    gl_map: dict[str, int],
    description: str | None,
) -> tuple[str, int] | None:
    if amount <= 0:
        return None
    if kind in {"WITHDRAWAL", "TRANSFER", "FEE"} and debit_id:
        if account_index[debit_id].balance < amount:
            return None
    if kind == "FX" and (not debit_id or not credit_id):
        return None

    tx_id = f"TX-{len(tx_rows) + 1:09d}"
    timestamp = when.replace(microsecond=0).isoformat()
    day = when.date().isoformat()
    counter_amount: int | None = None
    fx_rate_id: int | None = None
    fee_minor = 0
    entry_specs: list[tuple[str, str, list[LedgerLine]]] = []

    if kind == "DEPOSIT":
        entry_specs.append(
            (
                f"JE-{tx_id}",
                "Depósito de cliente",
                [
                    LedgerLine(CASH_BY_CURRENCY[currency], currency, debit_minor=amount),
                    LedgerLine(
                        CUSTOMER_DEPOSITS_BY_CURRENCY[currency],
                        currency,
                        credit_minor=amount,
                        account_id=credit_id,
                    ),
                ],
            )
        )
        account_index[credit_id].balance += amount
    elif kind == "WITHDRAWAL":
        entry_specs.append(
            (
                f"JE-{tx_id}",
                "Retiro de cliente",
                [
                    LedgerLine(
                        CUSTOMER_DEPOSITS_BY_CURRENCY[currency],
                        currency,
                        debit_minor=amount,
                        account_id=debit_id,
                    ),
                    LedgerLine(CASH_BY_CURRENCY[currency], currency, credit_minor=amount),
                ],
            )
        )
        account_index[debit_id].balance -= amount
    elif kind == "TRANSFER":
        entry_specs.append(
            (
                f"JE-{tx_id}",
                "Transferencia entre cuentas",
                [
                    LedgerLine(
                        CUSTOMER_DEPOSITS_BY_CURRENCY[currency],
                        currency,
                        debit_minor=amount,
                        account_id=debit_id,
                    ),
                    LedgerLine(
                        CUSTOMER_DEPOSITS_BY_CURRENCY[currency],
                        currency,
                        credit_minor=amount,
                        account_id=credit_id,
                    ),
                ],
            )
        )
        account_index[debit_id].balance -= amount
        account_index[credit_id].balance += amount
    elif kind == "FEE":
        fee_minor = amount
        gl_code = FEE_INCOME_BY_CURRENCY[currency]
        entry_specs.append(
            (
                f"JE-{tx_id}",
                "Comisión de servicio",
                [
                    LedgerLine(
                        CUSTOMER_DEPOSITS_BY_CURRENCY[currency],
                        currency,
                        debit_minor=amount,
                        account_id=debit_id,
                    ),
                    LedgerLine(gl_code, currency, credit_minor=amount),
                ],
            )
        )
        account_index[debit_id].balance -= amount
        fee_rows.append(
            (
                tx_id,
                "SERVICE",
                currency,
                amount,
                gl_map[gl_code],
                timestamp,
            )
        )
    elif kind == "FX":
        rate_id, rate = rates_by_date[day]
        counter_amount = max(1, int(round(amount / rate * 100)))
        fx_rate_id = rate_id
        entry_specs.append(
            (
                f"JE-{tx_id}-1",
                "Conversión PYG: origen",
                [
                    LedgerLine(
                        CUSTOMER_DEPOSITS_BY_CURRENCY["PYG"],
                        "PYG",
                        debit_minor=amount,
                        account_id=debit_id,
                    ),
                    LedgerLine(FX_POSITION_BY_CURRENCY["PYG"], "PYG", credit_minor=amount),
                ],
            )
        )
        entry_specs.append(
            (
                f"JE-{tx_id}-2",
                "Conversión USD: destino",
                [
                    LedgerLine(FX_POSITION_BY_CURRENCY["USD"], "USD", debit_minor=counter_amount),
                    LedgerLine(
                        CUSTOMER_DEPOSITS_BY_CURRENCY["USD"],
                        "USD",
                        credit_minor=counter_amount,
                        account_id=credit_id,
                    ),
                ],
            )
        )
        account_index[debit_id].balance -= amount
        account_index[credit_id].balance += counter_amount
    else:
        return None

    tx_rows.append(
        (
            tx_id,
            kind,
            "POSTED",
            currency,
            amount,
            counter_amount,
            debit_id,
            credit_id,
            fx_rate_id,
            fee_minor,
            description,
            "BATCH",
            f"SEED-{day}",
            timestamp,
            day,
            timestamp,
        )
    )
    for entry_id, entry_description, lines in entry_specs:
        entry_rows.append(
            (
                entry_id,
                day,
                entry_description,
                kind,
                tx_id,
                f"SEED-{day}",
                timestamp,
            )
        )
        for line_no, line in enumerate(lines, start=1):
            line_rows.append(
                (
                    entry_id,
                    line_no,
                    gl_map[line.gl_code],
                    line.account_id,
                    line.currency,
                    line.debit_minor,
                    line.credit_minor,
                    line.description,
                )
            )
    return tx_id, sum(len(lines) for _, _, lines in entry_specs)


def write_seed_report(summary: SeedSummary, output: str | Path) -> Path:
    """Escribe el resumen del seed en JSON para revisión manual."""
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(summary.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return destination
