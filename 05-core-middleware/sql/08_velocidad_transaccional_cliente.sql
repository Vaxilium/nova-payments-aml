-- Propósito de negocio: medir la intensidad transaccional diaria por cliente
-- y su acumulado de 7 días, insumo directo para reglas AML de velocidad.
WITH tx_customer AS (
    SELECT t.transaction_id,
           t.created_at,
           substr(t.created_at, 1, 10) AS day,
           t.amount_minor,
           t.currency,
           COALESCE(da.customer_id, ca.customer_id) AS customer_id
    FROM transactions t
    LEFT JOIN accounts da ON da.account_id = t.debit_account_id
    LEFT JOIN accounts ca ON ca.account_id = t.credit_account_id
    WHERE t.status = 'POSTED'
),
daily AS (
    SELECT customer_id,
           day,
           COUNT(*) AS tx_count,
           SUM(amount_minor) AS amount_minor,
           COUNT(DISTINCT currency) AS currencies
    FROM tx_customer
    GROUP BY customer_id, day
),
rolling AS (
    SELECT *,
           SUM(tx_count) OVER (
               PARTITION BY customer_id
               ORDER BY day
               ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           ) AS tx_7d,
           AVG(tx_count) OVER (
               PARTITION BY customer_id
               ORDER BY day
               ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           ) AS avg_7d,
           RANK() OVER (PARTITION BY day ORDER BY tx_count DESC) AS daily_rank
    FROM daily
)
SELECT customer_id,
       day,
       tx_count,
       amount_minor,
       currencies,
       tx_7d,
       ROUND(avg_7d, 2) AS avg_7d,
       daily_rank,
       CASE
           WHEN tx_count >= 20 THEN 'ALTA'
           WHEN tx_count >= 10 THEN 'MEDIA'
           ELSE 'NORMAL'
       END AS velocity_band
FROM rolling
ORDER BY day, tx_count DESC;
