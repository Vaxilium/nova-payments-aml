-- =============================================================================
-- NovaBank — Esquema del core bancario simulado (SQLite)
-- Caso ficticio. Sin PII real. La base se regenera con scripts/seed.py.
--
-- Convención monetaria: todos los importes se guardan como enteros en la
-- unidad menor de la moneda (PYG: guaraníes; USD: centavos). Esto evita
-- errores de redondeo en la contabilidad por partida doble.
-- =============================================================================

PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------------
-- Catálogos
-- -----------------------------------------------------------------------------
CREATE TABLE currencies (
    code        TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    minor_unit  INTEGER NOT NULL CHECK (minor_unit BETWEEN 0 AND 4),
    symbol      TEXT NOT NULL
);

CREATE TABLE gl_accounts (
    gl_account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    code          TEXT NOT NULL UNIQUE,
    name          TEXT NOT NULL,
    account_class TEXT NOT NULL CHECK (account_class IN ('ASSET', 'LIABILITY', 'EQUITY', 'INCOME', 'EXPENSE')),
    normal_side   TEXT NOT NULL CHECK (normal_side IN ('DEBIT', 'CREDIT')),
    is_active     INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
);

CREATE TABLE fx_rates (
    rate_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    rate_date      TEXT NOT NULL,
    base_currency  TEXT NOT NULL REFERENCES currencies(code) ON DELETE RESTRICT,
    quote_currency TEXT NOT NULL REFERENCES currencies(code) ON DELETE RESTRICT,
    rate           REAL NOT NULL CHECK (rate > 0),
    source         TEXT NOT NULL DEFAULT 'NOVABANK',
    created_at     TEXT NOT NULL,
    UNIQUE (rate_date, base_currency, quote_currency),
    CHECK (base_currency <> quote_currency)
);

-- -----------------------------------------------------------------------------
-- Clientes y cuentas
-- -----------------------------------------------------------------------------
CREATE TABLE customers (
    customer_id     TEXT PRIMARY KEY,
    customer_type   TEXT NOT NULL CHECK (customer_type IN ('INDIVIDUAL', 'BUSINESS')),
    first_name      TEXT,
    last_name       TEXT,
    business_name   TEXT,
    document_type   TEXT NOT NULL CHECK (document_type IN ('CI', 'RUC', 'PASSPORT')),
    document_number TEXT NOT NULL UNIQUE,
    birth_date      TEXT,
    country_code    TEXT NOT NULL DEFAULT 'PRY' CHECK (length(country_code) = 3),
    city            TEXT,
    segment         TEXT NOT NULL CHECK (segment IN ('RETAIL', 'PREMIUM', 'SME', 'CORPORATE')),
    risk_rating     TEXT NOT NULL CHECK (risk_rating IN ('LOW', 'MEDIUM', 'HIGH')),
    kyc_status      TEXT NOT NULL CHECK (kyc_status IN ('PENDING', 'VERIFIED', 'REJECTED')),
    is_active       INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at      TEXT NOT NULL,
    CHECK (
        (customer_type = 'INDIVIDUAL' AND first_name IS NOT NULL AND last_name IS NOT NULL AND business_name IS NULL)
        OR
        (customer_type = 'BUSINESS' AND business_name IS NOT NULL)
    )
);

CREATE TABLE accounts (
    account_id           TEXT PRIMARY KEY,
    customer_id          TEXT NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,
    account_number       TEXT NOT NULL UNIQUE,
    account_type         TEXT NOT NULL CHECK (account_type IN ('SAVINGS', 'CHECKING')),
    currency             TEXT NOT NULL REFERENCES currencies(code) ON DELETE RESTRICT,
    status               TEXT NOT NULL CHECK (status IN ('ACTIVE', 'BLOCKED', 'CLOSED')),
    balance_minor        INTEGER NOT NULL DEFAULT 0,
    overdraft_limit_minor INTEGER NOT NULL DEFAULT 0 CHECK (overdraft_limit_minor >= 0),
    version              INTEGER NOT NULL DEFAULT 1 CHECK (version > 0),
    opened_at            TEXT NOT NULL,
    closed_at            TEXT,
    CHECK (balance_minor >= -overdraft_limit_minor),
    CHECK (closed_at IS NULL OR status = 'CLOSED')
);

-- -----------------------------------------------------------------------------
-- Libro mayor (partida doble)
-- -----------------------------------------------------------------------------
CREATE TABLE journal_entries (
    entry_id       TEXT PRIMARY KEY,
    entry_date     TEXT NOT NULL,
    description    TEXT NOT NULL,
    source_type    TEXT NOT NULL CHECK (source_type IN ('OPENING', 'DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'FEE', 'FX', 'ADJUSTMENT')),
    source_id      TEXT,
    status         TEXT NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'POSTED', 'REVERSED')),
    correlation_id TEXT,
    created_by     TEXT NOT NULL,
    created_at     TEXT NOT NULL,
    posted_at      TEXT
);

CREATE TABLE journal_lines (
    line_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id      TEXT NOT NULL REFERENCES journal_entries(entry_id) ON DELETE CASCADE,
    line_no       INTEGER NOT NULL CHECK (line_no > 0),
    gl_account_id INTEGER NOT NULL REFERENCES gl_accounts(gl_account_id) ON DELETE RESTRICT,
    account_id    TEXT REFERENCES accounts(account_id) ON DELETE RESTRICT,
    currency      TEXT NOT NULL REFERENCES currencies(code) ON DELETE RESTRICT,
    debit_minor   INTEGER NOT NULL DEFAULT 0 CHECK (debit_minor >= 0),
    credit_minor  INTEGER NOT NULL DEFAULT 0 CHECK (credit_minor >= 0),
    description   TEXT,
    UNIQUE (entry_id, line_no),
    CHECK ((debit_minor > 0 AND credit_minor = 0) OR (credit_minor > 0 AND debit_minor = 0))
);

-- -----------------------------------------------------------------------------
-- Operaciones, comisiones, cierre y control
-- -----------------------------------------------------------------------------
CREATE TABLE transactions (
    transaction_id        TEXT PRIMARY KEY,
    transaction_type      TEXT NOT NULL CHECK (transaction_type IN ('DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'FEE', 'FX')),
    status                TEXT NOT NULL CHECK (status IN ('PENDING', 'POSTED', 'REJECTED', 'REVERSED')),
    currency              TEXT NOT NULL REFERENCES currencies(code) ON DELETE RESTRICT,
    amount_minor          INTEGER NOT NULL CHECK (amount_minor > 0),
    counter_amount_minor  INTEGER CHECK (counter_amount_minor IS NULL OR counter_amount_minor > 0),
    debit_account_id      TEXT REFERENCES accounts(account_id) ON DELETE RESTRICT,
    credit_account_id     TEXT REFERENCES accounts(account_id) ON DELETE RESTRICT,
    fx_rate_id            INTEGER REFERENCES fx_rates(rate_id) ON DELETE RESTRICT,
    fee_minor             INTEGER NOT NULL DEFAULT 0 CHECK (fee_minor >= 0),
    description           TEXT,
    channel               TEXT NOT NULL CHECK (channel IN ('API', 'MOBILE', 'WEB', 'BRANCH', 'ATM', 'BATCH')),
    idempotency_key       TEXT UNIQUE,
    correlation_id        TEXT,
    external_ref          TEXT,
    created_at            TEXT NOT NULL,
    value_date            TEXT NOT NULL,
    posted_at             TEXT,
    CHECK (debit_account_id IS NOT NULL OR credit_account_id IS NOT NULL),
    CHECK (transaction_type <> 'FX' OR (counter_amount_minor IS NOT NULL AND fx_rate_id IS NOT NULL))
);

CREATE TABLE fees (
    fee_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT NOT NULL REFERENCES transactions(transaction_id) ON DELETE RESTRICT,
    fee_type       TEXT NOT NULL CHECK (fee_type IN ('TRANSFER', 'FX', 'MONTHLY', 'SERVICE')),
    currency       TEXT NOT NULL REFERENCES currencies(code) ON DELETE RESTRICT,
    amount_minor   INTEGER NOT NULL CHECK (amount_minor > 0),
    gl_account_id  INTEGER NOT NULL REFERENCES gl_accounts(gl_account_id) ON DELETE RESTRICT,
    created_at     TEXT NOT NULL
);

CREATE TABLE daily_balances (
    balance_date        TEXT NOT NULL,
    account_id          TEXT NOT NULL REFERENCES accounts(account_id) ON DELETE RESTRICT,
    currency            TEXT NOT NULL REFERENCES currencies(code) ON DELETE RESTRICT,
    opening_minor       INTEGER NOT NULL,
    debit_total_minor   INTEGER NOT NULL DEFAULT 0 CHECK (debit_total_minor >= 0),
    credit_total_minor  INTEGER NOT NULL DEFAULT 0 CHECK (credit_total_minor >= 0),
    closing_minor       INTEGER NOT NULL,
    created_at          TEXT NOT NULL,
    PRIMARY KEY (balance_date, account_id),
    CHECK (closing_minor = opening_minor + credit_total_minor - debit_total_minor)
);

CREATE TABLE idempotency_keys (
    idempotency_key TEXT PRIMARY KEY,
    request_hash    TEXT NOT NULL,
    operation_id    TEXT,
    status_code     INTEGER NOT NULL,
    response_json   TEXT NOT NULL,
    created_at      TEXT NOT NULL,
    expires_at      TEXT
);

CREATE TABLE audit_log (
    audit_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type   TEXT NOT NULL,
    entity_type  TEXT NOT NULL,
    entity_id    TEXT,
    actor        TEXT NOT NULL,
    correlation_id TEXT,
    payload_json TEXT NOT NULL,
    created_at   TEXT NOT NULL
);

-- Tabla interna de verdad sintética. No se expone por API: se usa para medir
-- cobertura y falsos positivos de las reglas AML de la Fase 5.
CREATE TABLE _aml_ground_truth (
    truth_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT NOT NULL UNIQUE REFERENCES transactions(transaction_id) ON DELETE CASCADE,
    customer_id    TEXT NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,
    pattern_type   TEXT CHECK (pattern_type IS NULL OR pattern_type IN (
                       'STRUCTURING', 'PASS_THROUGH', 'HIGH_VELOCITY',
                       'ROUND_MULE', 'DORMANT_ACTIVATION')),
    label          TEXT NOT NULL CHECK (label IN ('SUSPICIOUS', 'NORMAL')),
    notes          TEXT,
    generated_at   TEXT NOT NULL
);

-- -----------------------------------------------------------------------------
-- Índices operativos
-- -----------------------------------------------------------------------------
CREATE INDEX idx_accounts_customer ON accounts(customer_id);
CREATE INDEX idx_accounts_currency_status ON accounts(currency, status);
CREATE INDEX idx_accounts_balance ON accounts(balance_minor);
CREATE INDEX idx_journal_entries_date ON journal_entries(entry_date, status);
CREATE INDEX idx_journal_entries_source ON journal_entries(source_type, source_id);
CREATE INDEX idx_journal_lines_entry ON journal_lines(entry_id);
CREATE INDEX idx_journal_lines_account ON journal_lines(account_id, currency);
CREATE INDEX idx_journal_lines_gl ON journal_lines(gl_account_id);
CREATE INDEX idx_transactions_debit ON transactions(debit_account_id, created_at);
CREATE INDEX idx_transactions_credit ON transactions(credit_account_id, created_at);
CREATE INDEX idx_transactions_created ON transactions(created_at);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);
CREATE INDEX idx_fees_transaction ON fees(transaction_id);
CREATE INDEX idx_daily_balances_account ON daily_balances(account_id, balance_date);
CREATE INDEX idx_audit_created ON audit_log(created_at);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_truth_pattern ON _aml_ground_truth(pattern_type, label);

-- -----------------------------------------------------------------------------
-- Triggers de integridad contable
-- -----------------------------------------------------------------------------

-- Un asiento solo puede contabilizarse (POSTED) si tiene al menos dos líneas.
CREATE TRIGGER trg_journal_entries_min_lines_insert
BEFORE INSERT ON journal_entries
WHEN NEW.status = 'POSTED'
BEGIN
    SELECT RAISE(ABORT, 'Un asiento contabilizado requiere al menos dos líneas')
    WHERE (SELECT COUNT(*) FROM journal_lines WHERE entry_id = NEW.entry_id) < 2;
END;

CREATE TRIGGER trg_journal_entries_min_lines_update
BEFORE UPDATE OF status ON journal_entries
WHEN NEW.status = 'POSTED' AND OLD.status <> 'POSTED'
BEGIN
    SELECT RAISE(ABORT, 'Un asiento contabilizado requiere al menos dos líneas')
    WHERE (SELECT COUNT(*) FROM journal_lines WHERE entry_id = NEW.entry_id) < 2;
END;

-- Débitos y créditos deben coincidir por cada moneda del asiento.
CREATE TRIGGER trg_journal_entries_balanced_insert
BEFORE INSERT ON journal_entries
WHEN NEW.status = 'POSTED'
BEGIN
    SELECT RAISE(ABORT, 'Asiento desbalanceado por moneda')
    WHERE EXISTS (
        SELECT 1 FROM journal_lines
        WHERE entry_id = NEW.entry_id
        GROUP BY currency
        HAVING SUM(debit_minor) <> SUM(credit_minor)
    );
END;

CREATE TRIGGER trg_journal_entries_balanced_update
BEFORE UPDATE OF status ON journal_entries
WHEN NEW.status = 'POSTED' AND OLD.status <> 'POSTED'
BEGIN
    SELECT RAISE(ABORT, 'Asiento desbalanceado por moneda')
    WHERE EXISTS (
        SELECT 1 FROM journal_lines
        WHERE entry_id = NEW.entry_id
        GROUP BY currency
        HAVING SUM(debit_minor) <> SUM(credit_minor)
    );
END;

-- Un asiento contabilizado es inmutable.
CREATE TRIGGER trg_journal_entries_no_update_posted
BEFORE UPDATE ON journal_entries
WHEN OLD.status = 'POSTED'
BEGIN
    SELECT RAISE(ABORT, 'Un asiento contabilizado no puede modificarse');
END;

CREATE TRIGGER trg_journal_entries_no_delete_posted
BEFORE DELETE ON journal_entries
WHEN OLD.status = 'POSTED'
BEGIN
    SELECT RAISE(ABORT, 'Un asiento contabilizado no puede eliminarse');
END;

-- Las líneas de un asiento contabilizado no se insertan, modifican ni borran.
CREATE TRIGGER trg_journal_lines_no_insert_posted
BEFORE INSERT ON journal_lines
WHEN (SELECT status FROM journal_entries WHERE entry_id = NEW.entry_id) = 'POSTED'
BEGIN
    SELECT RAISE(ABORT, 'No se pueden agregar líneas a un asiento contabilizado');
END;

CREATE TRIGGER trg_journal_lines_no_update_posted
BEFORE UPDATE ON journal_lines
WHEN (SELECT status FROM journal_entries WHERE entry_id = OLD.entry_id) = 'POSTED'
BEGIN
    SELECT RAISE(ABORT, 'No se pueden modificar líneas de un asiento contabilizado');
END;

CREATE TRIGGER trg_journal_lines_no_delete_posted
BEFORE DELETE ON journal_lines
WHEN (SELECT status FROM journal_entries WHERE entry_id = OLD.entry_id) = 'POSTED'
BEGIN
    SELECT RAISE(ABORT, 'No se pueden eliminar líneas de un asiento contabilizado');
END;

-- La moneda de una línea debe coincidir con la moneda de la cuenta vinculada.
CREATE TRIGGER trg_journal_lines_account_currency_insert
BEFORE INSERT ON journal_lines
WHEN NEW.account_id IS NOT NULL
 AND NEW.currency <> (SELECT currency FROM accounts WHERE account_id = NEW.account_id)
BEGIN
    SELECT RAISE(ABORT, 'La moneda de la línea no coincide con la de la cuenta');
END;

CREATE TRIGGER trg_journal_lines_account_currency_update
BEFORE UPDATE ON journal_lines
WHEN NEW.account_id IS NOT NULL
 AND NEW.currency <> (SELECT currency FROM accounts WHERE account_id = NEW.account_id)
BEGIN
    SELECT RAISE(ABORT, 'La moneda de la línea no coincide con la de la cuenta');
END;

-- Una cuenta no puede quedar por debajo de su límite de sobregiro.
CREATE TRIGGER trg_accounts_non_negative_insert
BEFORE INSERT ON accounts
WHEN NEW.balance_minor < -NEW.overdraft_limit_minor
BEGIN
    SELECT RAISE(ABORT, 'Saldo insuficiente para abrir la cuenta');
END;

CREATE TRIGGER trg_accounts_non_negative_update
BEFORE UPDATE OF balance_minor ON accounts
WHEN NEW.balance_minor < -NEW.overdraft_limit_minor
BEGIN
    SELECT RAISE(ABORT, 'Saldo insuficiente');
END;

-- Una operación contabilizada no puede cambiar de importe, cuentas ni moneda.
CREATE TRIGGER trg_transactions_no_update_posted
BEFORE UPDATE ON transactions
WHEN OLD.status IN ('POSTED', 'REJECTED')
 AND (NEW.amount_minor <> OLD.amount_minor
      OR NEW.currency <> OLD.currency
      OR NEW.debit_account_id IS NOT OLD.debit_account_id
      OR NEW.credit_account_id IS NOT OLD.credit_account_id)
BEGIN
    SELECT RAISE(ABORT, 'Una operación contabilizada es inmutable');
END;

CREATE TRIGGER trg_transactions_no_delete_posted
BEFORE DELETE ON transactions
WHEN OLD.status IN ('POSTED', 'REJECTED')
BEGIN
    SELECT RAISE(ABORT, 'Una operación contabilizada no puede eliminarse');
END;
