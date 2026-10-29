-- Esquema AML de Fase 5. Se aplica sobre la base del core (Fase 3).
-- No elimina tablas del core. Los datos son ficticios.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS aml_rule_params (
    rule_id        TEXT NOT NULL,
    param_name     TEXT NOT NULL,
    param_value    TEXT NOT NULL,
    value_type     TEXT NOT NULL DEFAULT 'INTEGER'
                   CHECK (value_type IN ('INTEGER', 'REAL', 'TEXT')),
    description    TEXT NOT NULL,
    updated_at     TEXT NOT NULL,
    PRIMARY KEY (rule_id, param_name)
);

CREATE TABLE IF NOT EXISTS aml_high_risk_countries (
    country_code   TEXT PRIMARY KEY CHECK (length(country_code) = 3),
    country_name   TEXT NOT NULL,
    source         TEXT NOT NULL DEFAULT 'Lista interna ficticia NovaBank',
    is_active      INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
);

CREATE TABLE IF NOT EXISTS aml_watchlist (
    list_type      TEXT NOT NULL CHECK (list_type IN ('SANCTIONS', 'PEP', 'INTERNAL')),
    list_id        TEXT NOT NULL,
    name           TEXT NOT NULL,
    aliases        TEXT,
    country_code   TEXT,
    date_of_birth  TEXT,
    program        TEXT,
    is_active      INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    is_fictitious  INTEGER NOT NULL DEFAULT 1 CHECK (is_fictitious IN (0, 1)),
    PRIMARY KEY (list_type, list_id)
);

CREATE TABLE IF NOT EXISTS aml_customer_profile (
    customer_id                    TEXT PRIMARY KEY REFERENCES customers(customer_id) ON DELETE CASCADE,
    occupation                     TEXT,
    activity_risk                  TEXT NOT NULL DEFAULT 'LOW'
                                   CHECK (activity_risk IN ('LOW', 'MEDIUM', 'HIGH')),
    is_pep                         INTEGER NOT NULL DEFAULT 0 CHECK (is_pep IN (0, 1)),
    pep_type                       TEXT,
    beneficial_owner_identified    INTEGER NOT NULL DEFAULT 1
                                   CHECK (beneficial_owner_identified IN (0, 1)),
    source_of_funds_verified       INTEGER NOT NULL DEFAULT 1
                                   CHECK (source_of_funds_verified IN (0, 1)),
    negative_news                  INTEGER NOT NULL DEFAULT 0 CHECK (negative_news IN (0, 1)),
    onboarding_channel             TEXT NOT NULL DEFAULT 'BRANCH'
                                   CHECK (onboarding_channel IN ('BRANCH', 'WEB', 'MOBILE', 'API')),
    product_complexity             TEXT NOT NULL DEFAULT 'BASIC'
                                   CHECK (product_complexity IN ('BASIC', 'MEDIUM', 'COMPLEX')),
    expected_monthly_volume_minor  INTEGER NOT NULL DEFAULT 0 CHECK (expected_monthly_volume_minor >= 0),
    updated_at                     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS aml_kyc_scores (
    customer_id       TEXT PRIMARY KEY REFERENCES customers(customer_id) ON DELETE CASCADE,
    score             INTEGER NOT NULL CHECK (score BETWEEN 0 AND 100),
    risk_category     TEXT NOT NULL CHECK (risk_category IN ('LOW', 'MEDIUM', 'HIGH')),
    requires_edd      INTEGER NOT NULL DEFAULT 0 CHECK (requires_edd IN (0, 1)),
    factors_json      TEXT NOT NULL,
    calculated_at     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS aml_payment_context (
    payment_id           TEXT PRIMARY KEY,
    customer_id          TEXT REFERENCES customers(customer_id) ON DELETE SET NULL,
    account_id           TEXT REFERENCES accounts(account_id) ON DELETE SET NULL,
    direction            TEXT NOT NULL CHECK (direction IN ('INBOUND', 'OUTBOUND')),
    counterparty_name    TEXT,
    counterparty_country TEXT,
    amount_minor         INTEGER NOT NULL CHECK (amount_minor > 0),
    currency             TEXT NOT NULL,
    source               TEXT NOT NULL DEFAULT 'SIMULATOR',
    created_at           TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS aml_screening_results (
    screening_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name    TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    list_type       TEXT,
    list_id         TEXT,
    matched_name    TEXT,
    score           REAL NOT NULL CHECK (score BETWEEN 0 AND 1),
    threshold       REAL NOT NULL CHECK (threshold BETWEEN 0 AND 1),
    decision        TEXT NOT NULL CHECK (decision IN ('NO_MATCH', 'REVIEW', 'BLOCK')),
    payment_ref     TEXT,
    created_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS aml_alerts (
    alert_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    dedup_key         TEXT NOT NULL UNIQUE,
    alert_type        TEXT NOT NULL,
    rule_id           TEXT NOT NULL,
    customer_id       TEXT REFERENCES customers(customer_id) ON DELETE SET NULL,
    account_id        TEXT REFERENCES accounts(account_id) ON DELETE SET NULL,
    transaction_id    TEXT REFERENCES transactions(transaction_id) ON DELETE SET NULL,
    severity          TEXT NOT NULL CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    risk_score        INTEGER NOT NULL CHECK (risk_score BETWEEN 0 AND 100),
    priority          TEXT NOT NULL CHECK (priority IN ('P1', 'P2', 'P3')),
    status            TEXT NOT NULL DEFAULT 'NUEVA'
                      CHECK (status IN ('NUEVA', 'EN_ANALISIS', 'ESCALADA', 'CERRADA_FALSO_POSITIVO', 'REPORTADA')),
    transaction_count INTEGER NOT NULL DEFAULT 1,
    case_id           INTEGER REFERENCES aml_cases(case_id) ON DELETE SET NULL,
    created_at        TEXT NOT NULL,
    updated_at        TEXT NOT NULL,
    last_seen_at      TEXT NOT NULL,
    assigned_to       TEXT,
    assigned_at       TEXT,
    due_at            TEXT,
    closed_at         TEXT,
    closure_notes     TEXT,
    detail_json       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS aml_cases (
    case_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id    TEXT REFERENCES customers(customer_id) ON DELETE SET NULL,
    title          TEXT NOT NULL,
    status         TEXT NOT NULL DEFAULT 'ABIERTO'
                   CHECK (status IN ('ABIERTO', 'EN_ANALISIS', 'ESCALADO', 'CERRADO', 'REPORTADO')),
    priority       TEXT NOT NULL CHECK (priority IN ('P1', 'P2', 'P3')),
    risk_score     INTEGER NOT NULL DEFAULT 0 CHECK (risk_score BETWEEN 0 AND 100),
    opened_at      TEXT NOT NULL,
    assigned_to    TEXT,
    due_at         TEXT,
    closed_at      TEXT,
    closure_notes  TEXT,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL,
    ros_reported   INTEGER NOT NULL DEFAULT 0 CHECK (ros_reported IN (0, 1))
);

CREATE TABLE IF NOT EXISTS aml_case_alerts (
    case_id   INTEGER NOT NULL REFERENCES aml_cases(case_id) ON DELETE CASCADE,
    alert_id  INTEGER NOT NULL REFERENCES aml_alerts(alert_id) ON DELETE CASCADE,
    PRIMARY KEY (case_id, alert_id)
);

CREATE TABLE IF NOT EXISTS aml_workflow_transitions (
    transition_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type    TEXT NOT NULL CHECK (entity_type IN ('ALERT', 'CASE', 'ROS')),
    entity_id      INTEGER NOT NULL,
    from_status    TEXT,
    to_status      TEXT NOT NULL,
    analyst        TEXT NOT NULL,
    reason         TEXT,
    created_at     TEXT NOT NULL,
    sla_due_at     TEXT
);

CREATE TABLE IF NOT EXISTS aml_ros (
    ros_id           TEXT PRIMARY KEY,
    case_id          INTEGER REFERENCES aml_cases(case_id) ON DELETE SET NULL,
    customer_id      TEXT REFERENCES customers(customer_id) ON DELETE SET NULL,
    created_at       TEXT NOT NULL,
    status           TEXT NOT NULL DEFAULT 'BORRADOR'
                     CHECK (status IN ('BORRADOR', 'REVISADO', 'ENVIADO')),
    narrative        TEXT NOT NULL,
    operations_json  TEXT NOT NULL,
    submitted_at     TEXT
);

CREATE INDEX IF NOT EXISTS idx_aml_alerts_customer ON aml_alerts(customer_id, status);
CREATE INDEX IF NOT EXISTS idx_aml_alerts_rule ON aml_alerts(rule_id);
CREATE INDEX IF NOT EXISTS idx_aml_alerts_created ON aml_alerts(created_at);
CREATE INDEX IF NOT EXISTS idx_aml_cases_customer ON aml_cases(customer_id, status);
CREATE INDEX IF NOT EXISTS idx_aml_screening_decision ON aml_screening_results(decision);
CREATE INDEX IF NOT EXISTS idx_aml_payment_country ON aml_payment_context(counterparty_country);
CREATE INDEX IF NOT EXISTS idx_tx_debit_created ON transactions(debit_account_id, created_at);
CREATE INDEX IF NOT EXISTS idx_tx_credit_created ON transactions(credit_account_id, created_at);
CREATE INDEX IF NOT EXISTS idx_tx_created ON transactions(created_at);
