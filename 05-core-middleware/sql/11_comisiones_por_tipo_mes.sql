-- Propósito de negocio: analizar la evolución mensual de comisiones por tipo
-- y moneda, con variación mes a mes y acumulado. Apoya la proyección de
-- ingresos por servicios.
WITH monthly AS (
    SELECT substr(f.created_at, 1, 7) AS month,
           f.fee_type,
           f.currency,
           COUNT(*) AS fee_count,
           COUNT(DISTINCT f.transaction_id) AS tx_count,
           SUM(f.amount_minor) AS fee_minor
    FROM fees f
    GROUP BY substr(f.created_at, 1, 7), f.fee_type, f.currency
),
changes AS (
    SELECT *,
           LAG(fee_minor) OVER (
               PARTITION BY fee_type, currency ORDER BY month
           ) AS previous_fee,
           SUM(fee_minor) OVER (
               PARTITION BY currency ORDER BY month
           ) AS cumulative_fee
    FROM monthly
)
SELECT month,
       fee_type,
       currency,
       fee_count,
       tx_count,
       fee_minor,
       ROUND(100.0 * (fee_minor - previous_fee) / NULLIF(previous_fee, 0), 2) AS month_over_month_pct,
       cumulative_fee,
       RANK() OVER (PARTITION BY month ORDER BY fee_minor DESC) AS type_rank
FROM changes
ORDER BY month, type_rank;
