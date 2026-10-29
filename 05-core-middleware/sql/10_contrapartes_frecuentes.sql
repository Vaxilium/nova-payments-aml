-- Propósito de negocio: conocer las principales contrapartes de cada cliente
-- y su concentración. Es insumo para límites operativos y para revisiones AML
-- de relaciones atípicas.
WITH pairs AS (
    SELECT da.customer_id AS source_customer,
           ca.customer_id AS target_customer,
           t.currency,
           COUNT(*) AS tx_count,
           SUM(t.amount_minor) AS amount_minor,
           MAX(t.created_at) AS last_at
    FROM transactions t
    JOIN accounts da ON da.account_id = t.debit_account_id
    JOIN accounts ca ON ca.account_id = t.credit_account_id
    WHERE t.transaction_type = 'TRANSFER'
      AND t.status = 'POSTED'
    GROUP BY da.customer_id, ca.customer_id, t.currency
),
ranked AS (
    SELECT *,
           RANK() OVER (PARTITION BY source_customer ORDER BY tx_count DESC) AS counterparty_rank,
           SUM(tx_count) OVER (PARTITION BY source_customer) AS customer_tx_total,
           ROUND(100.0 * tx_count / NULLIF(SUM(tx_count) OVER (PARTITION BY source_customer), 0), 2) AS pct_customer
    FROM pairs
)
SELECT source_customer,
       target_customer,
       currency,
       tx_count,
       amount_minor,
       last_at,
       counterparty_rank,
       customer_tx_total,
       pct_customer
FROM ranked
WHERE counterparty_rank <= 3
ORDER BY source_customer, counterparty_rank;
