-- Propósito de negocio: detectar cuentas de paso donde un depósito se retira
-- o transfiere casi en su totalidad dentro de los 60 minutos siguientes.
-- Patrón típico de mulas de dinero o de uso transitorio de cuentas.
WITH inflows AS (
    SELECT t.transaction_id,
           t.credit_account_id AS account_id,
           t.amount_minor,
           t.created_at
    FROM transactions t
    WHERE t.status = 'POSTED'
      AND t.transaction_type = 'DEPOSIT'
      AND t.credit_account_id IS NOT NULL
),
outflows AS (
    SELECT t.transaction_id,
           t.debit_account_id AS account_id,
           t.amount_minor,
           t.created_at
    FROM transactions t
    WHERE t.status = 'POSTED'
      AND t.transaction_type IN ('TRANSFER', 'WITHDRAWAL')
      AND t.debit_account_id IS NOT NULL
),
paired AS (
    SELECT i.transaction_id AS deposit_id,
           o.transaction_id AS outflow_id,
           i.account_id,
           i.amount_minor AS deposit_minor,
           o.amount_minor AS outflow_minor,
           ROUND((julianday(o.created_at) - julianday(i.created_at)) * 1440, 2) AS minutes_to_outflow,
           ROW_NUMBER() OVER (
               PARTITION BY i.transaction_id
               ORDER BY o.created_at
           ) AS candidate_rank
    FROM inflows i
    JOIN outflows o
      ON o.account_id = i.account_id
     AND datetime(o.created_at) > datetime(i.created_at)
     AND datetime(o.created_at) <= datetime(i.created_at, '+60 minutes')
     AND o.amount_minor >= i.amount_minor * 0.8
)
SELECT deposit_id,
       outflow_id,
       account_id,
       deposit_minor,
       outflow_minor,
       minutes_to_outflow,
       ROUND(100.0 * outflow_minor / NULLIF(deposit_minor, 0), 2) AS pass_through_pct,
       RANK() OVER (ORDER BY minutes_to_outflow) AS speed_rank
FROM paired
WHERE candidate_rank = 1
ORDER BY minutes_to_outflow;
