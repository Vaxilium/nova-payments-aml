-- Propósito de negocio: identificar clientes con mayor exposición depositada,
-- normalizando USD a PYG con el último tipo de cambio disponible. Sirve para
-- priorización comercial y para segmentar revisiones de riesgo.
WITH latest_rate AS (
    SELECT base_currency, quote_currency, rate
    FROM (
        SELECT base_currency,
               quote_currency,
               rate,
               ROW_NUMBER() OVER (
                   PARTITION BY base_currency, quote_currency
                   ORDER BY rate_date DESC
               ) AS rn
        FROM fx_rates
        WHERE base_currency = 'USD' AND quote_currency = 'PYG'
    )
    WHERE rn = 1
),
normalized AS (
    SELECT c.customer_id,
           c.customer_type,
           COALESCE(c.business_name, c.first_name || ' ' || c.last_name) AS customer_name,
           c.segment,
           c.risk_rating,
           a.currency,
           SUM(a.balance_minor) AS balance_minor,
           SUM(
               CASE
                   WHEN a.currency = 'PYG' THEN a.balance_minor * 1.0
                   ELSE a.balance_minor * (SELECT rate FROM latest_rate) / 100.0
               END
           ) AS pyg_equivalent
    FROM customers c
    JOIN accounts a ON a.customer_id = c.customer_id
    GROUP BY c.customer_id, c.customer_type, c.business_name, c.first_name,
             c.last_name, c.segment, c.risk_rating, a.currency
),
customer_totals AS (
    SELECT customer_id, SUM(pyg_equivalent) AS pyg_total
    FROM normalized
    GROUP BY customer_id
),
portfolio AS (
    SELECT SUM(pyg_total) AS portfolio_total FROM customer_totals
)
SELECT n.customer_id,
       n.customer_type,
       n.customer_name,
       n.segment,
       n.risk_rating,
       n.currency,
       n.balance_minor,
       ROUND(n.pyg_equivalent, 2) AS pyg_equivalent,
       ROUND(t.pyg_total, 2) AS customer_pyg_total,
       RANK() OVER (ORDER BY t.pyg_total DESC) AS customer_rank,
       ROUND(100.0 * t.pyg_total / NULLIF(p.portfolio_total, 0), 4) AS pct_of_portfolio
FROM normalized n
JOIN customer_totals t ON t.customer_id = n.customer_id
CROSS JOIN portfolio p
ORDER BY customer_rank, n.currency;
