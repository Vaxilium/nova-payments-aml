-- Elimina los objetos del core simulado en orden inverso a sus dependencias.
PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS _aml_ground_truth;
DROP TABLE IF EXISTS audit_log;
DROP TABLE IF EXISTS idempotency_keys;
DROP TABLE IF EXISTS daily_balances;
DROP TABLE IF EXISTS fees;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS journal_lines;
DROP TABLE IF EXISTS journal_entries;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS fx_rates;
DROP TABLE IF EXISTS gl_accounts;
DROP TABLE IF EXISTS currencies;

PRAGMA foreign_keys = ON;
