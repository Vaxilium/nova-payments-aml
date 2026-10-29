-- Propósito de negocio: detectar operaciones potencialmente duplicadas por
-- misma cuenta, contraparte, moneda e importe dentro de una ventana corta.
-- Apoya el control de reintentos y la prevención de doble contabilización.
WITH ordered AS (
    SELECT t.transaction_id,
           t.transaction_type,
           t.currency,
           t.amount_minor,
           t.debit_account_id,
           t.credit_account_id,
           t.created_at,
           LAG(t.transaction_id) OVER (
               PARTITION BY t.debit_account_id, t.credit_account_id, t.amount_minor, t.currency
               ORDER BY t.created_at
           ) AS previous_id,
           LAG(t.created_at) OVER (
               PARTITION BY t.debit_account_id, t.credit_account_id, t.amount_minor, t.currency
               ORDER BY t.created_at
           ) AS previous_at,
           ROW_NUMBER() OVER (
               PARTITION BY t.debit_account_id, t.credit_account_id, t.amount_minor, t.currency
               ORDER BY t.created_at
           ) AS sequence_in_group
    FROM transactions t
    WHERE t.status = 'POSTED'
),
candidates AS (
    SELECT *,
           ROUND((julianday(created_at) - julianday(previous_at)) * 86400.0, 1) AS seconds_since_previous
    FROM ordered
    WHERE previous_id IS NOT NULL
)
SELECT transaction_id,
       previous_id,
       transaction_type,
       currency,
       amount_minor,
       debit_account_id,
       credit_account_id,
       created_at,
       previous_at,
       seconds_since_previous,
       sequence_in_group,
       CASE WHEN seconds_since_previous <= 300 THEN 'POSIBLE_DUPLICADO' ELSE 'FRECUENTE' END AS classification,
       RANK() OVER (ORDER BY seconds_since_previous) AS proximity_rank
FROM candidates
WHERE seconds_since_previous <= 3600
ORDER BY seconds_since_previous;
