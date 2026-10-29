-- Propósito de negocio: detectar estructuración de depósitos en PYG justo por
-- debajo del umbral de reporte de ₲10.000.000. Se agrupa por cliente y día
-- para distinguir operaciones aisladas de un patrón repetido.
WITH deposits AS (
    SELECT t.transaction_id,
           a.customer_id,
           substr(t.created_at, 1, 10) AS day,
           t.created_at,
           t.amount_minor,
           CASE WHEN t.amount_minor BETWEEN 8000000 AND 9999999 THEN 1 ELSE 0 END AS near_threshold
    FROM transactions t
    JOIN accounts a ON a.account_id = t.credit_account_id
    WHERE t.transaction_type = 'DEPOSIT'
      AND t.status = 'POSTED'
      AND t.currency = 'PYG'
),
daily AS (
    SELECT customer_id,
           day,
           COUNT(*) AS deposit_count,
           SUM(near_threshold) AS near_count,
           SUM(CASE WHEN near_threshold = 1 THEN amount_minor ELSE 0 END) AS near_total,
           SUM(amount_minor) AS total_deposits,
           MIN(created_at) AS first_at,
           MAX(created_at) AS last_at
    FROM deposits
    GROUP BY customer_id, day
),
ranked AS (
    SELECT *,
           ROUND(100.0 * near_count / NULLIF(deposit_count, 0), 2) AS near_pct,
           RANK() OVER (ORDER BY near_total DESC) AS exposure_rank,
           SUM(near_total) OVER () AS portfolio_near_total
    FROM daily
    WHERE near_count >= 2
)
SELECT customer_id,
       day,
       deposit_count,
       near_count,
       near_pct,
       near_total,
       total_deposits,
       first_at,
       last_at,
       exposure_rank,
       portfolio_near_total
FROM ranked
ORDER BY exposure_rank;
