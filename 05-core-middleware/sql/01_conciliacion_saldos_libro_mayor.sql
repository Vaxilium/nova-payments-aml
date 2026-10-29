-- Propósito de negocio: verificar que el saldo operativo de cada cuenta
-- coincida con la suma de sus líneas en el libro mayor. Es el control diario
-- que evita diferencias entre el core y contabilidad.
WITH ledger AS (
    SELECT jl.account_id,
           jl.currency,
           SUM(jl.credit_minor - jl.debit_minor) AS ledger_minor,
           COUNT(*) AS line_count,
           MAX(je.entry_date) AS last_entry_date
    FROM journal_lines jl
    JOIN journal_entries je ON je.entry_id = jl.entry_id
    WHERE jl.account_id IS NOT NULL
      AND je.status = 'POSTED'
    GROUP BY jl.account_id, jl.currency
),
comparison AS (
    SELECT a.account_id,
           a.customer_id,
           a.account_type,
           a.currency,
           a.status,
           a.balance_minor,
           COALESCE(l.ledger_minor, 0) AS ledger_minor,
           a.balance_minor - COALESCE(l.ledger_minor, 0) AS difference_minor,
           COALESCE(l.line_count, 0) AS line_count,
           l.last_entry_date
    FROM accounts a
    LEFT JOIN ledger l
      ON l.account_id = a.account_id
     AND l.currency = a.currency
)
SELECT account_id,
       customer_id,
       account_type,
       currency,
       status,
       balance_minor,
       ledger_minor,
       difference_minor,
       CASE WHEN difference_minor = 0 THEN 'OK' ELSE 'REVISAR' END AS reconciliation_status,
       ROW_NUMBER() OVER (ORDER BY ABS(difference_minor) DESC, account_id) AS risk_rank,
       SUM(difference_minor) OVER () AS total_difference_minor,
       SUM(CASE WHEN difference_minor <> 0 THEN 1 ELSE 0 END) OVER () AS accounts_with_difference
FROM comparison
ORDER BY risk_rank;
