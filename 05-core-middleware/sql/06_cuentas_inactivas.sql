-- Propósito de negocio: identificar cuentas sin actividad reciente para
-- campañas de reactivación, revisión de clientes dormidos y control AML de
-- activaciones repentinas.
WITH last_movement AS (
    SELECT jl.account_id,
           MAX(je.entry_date) AS last_entry_date,
           COUNT(*) AS line_count
    FROM journal_lines jl
    JOIN journal_entries je ON je.entry_id = jl.entry_id
    WHERE jl.account_id IS NOT NULL
      AND je.status = 'POSTED'
    GROUP BY jl.account_id
),
reference AS (
    SELECT MAX(entry_date) AS max_entry_date
    FROM journal_entries
    WHERE status = 'POSTED'
),
ranked AS (
    SELECT a.account_id,
           a.customer_id,
           a.account_type,
           a.currency,
           a.status,
           a.balance_minor,
           lm.last_entry_date,
           COALESCE(lm.line_count, 0) AS line_count,
           CAST(julianday(r.max_entry_date) - julianday(lm.last_entry_date) AS INTEGER) AS days_inactive,
           RANK() OVER (ORDER BY lm.last_entry_date) AS oldest_rank
    FROM accounts a
    LEFT JOIN last_movement lm ON lm.account_id = a.account_id
    CROSS JOIN reference r
)
SELECT account_id,
       customer_id,
       account_type,
       currency,
       status,
       balance_minor,
       last_entry_date,
       line_count,
       days_inactive,
       oldest_rank,
       CASE
           WHEN last_entry_date IS NULL THEN 'SIN_MOVIMIENTO'
           WHEN days_inactive >= 90 THEN 'DORMIDA'
           ELSE 'POCO_ACTIVA'
       END AS dormancy_band
FROM ranked
WHERE days_inactive IS NULL OR days_inactive >= 30
ORDER BY days_inactive DESC, balance_minor DESC;
