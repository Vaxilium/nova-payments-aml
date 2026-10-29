-- Propósito de negocio: analizar corredores transfronterizos entre clientes
-- de distintos países, con concentración por país de origen. Insumo para
-- riesgo país, límites de corresponsalía y monitoreo AML.
WITH cross_border AS (
    SELECT sc.customer_id AS source_customer,
           sc.country_code AS source_country,
           dc.customer_id AS target_customer,
           dc.country_code AS target_country,
           t.currency,
           COUNT(*) AS tx_count,
           SUM(t.amount_minor) AS amount_minor
    FROM transactions t
    JOIN accounts sa ON sa.account_id = t.debit_account_id
    JOIN customers sc ON sc.customer_id = sa.customer_id
    JOIN accounts da ON da.account_id = t.credit_account_id
    JOIN customers dc ON dc.customer_id = da.customer_id
    WHERE t.transaction_type = 'TRANSFER'
      AND t.status = 'POSTED'
      AND sc.country_code <> dc.country_code
    GROUP BY sc.customer_id, sc.country_code, dc.customer_id, dc.country_code, t.currency
),
ranked AS (
    SELECT *,
           SUM(tx_count) OVER (PARTITION BY source_country) AS country_tx_total,
           ROUND(100.0 * tx_count / NULLIF(SUM(tx_count) OVER (PARTITION BY source_country), 0), 2) AS pct_country,
           RANK() OVER (
               PARTITION BY source_country ORDER BY tx_count DESC
           ) AS corridor_rank
    FROM cross_border
)
SELECT *
FROM ranked
ORDER BY source_country, corridor_rank;
