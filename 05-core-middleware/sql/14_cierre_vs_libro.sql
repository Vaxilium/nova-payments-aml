-- Propósito de negocio: comparar el último cierre diario de cada cuenta con
-- el saldo actual y con el libro mayor. Detecta cierres desactualizados o
-- diferencias de integración entre el core y contabilidad.
WITH latest_close AS (
    SELECT db.*,
           ROW_NUMBER() OVER (
               PARTITION BY db.account_id
               ORDER BY db.balance_date DESC
           ) AS rn
    FROM daily_balances db
),
ledger AS (
    SELECT account_id,
           SUM(credit_minor - debit_minor) AS ledger_minor
    FROM journal_lines
    WHERE account_id IS NOT NULL
    GROUP BY account_id
)
SELECT lc.balance_date,
       lc.account_id,
       a.currency,
       lc.opening_minor,
       lc.debit_total_minor,
       lc.credit_total_minor,
       lc.closing_minor,
       a.balance_minor AS current_balance_minor,
       COALESCE(l.ledger_minor, 0) AS ledger_minor,
       lc.closing_minor - COALESCE(l.ledger_minor, 0) AS close_vs_ledger_diff,
       a.balance_minor - lc.closing_minor AS current_vs_last_close_diff,
       RANK() OVER (ORDER BY ABS(a.balance_minor - lc.closing_minor) DESC) AS discrepancy_rank
FROM latest_close lc
JOIN accounts a ON a.account_id = lc.account_id
LEFT JOIN ledger l ON l.account_id = lc.account_id
WHERE lc.rn = 1
ORDER BY discrepancy_rank;
