-- Propósito de negocio: auditar las conversiones de moneda aplicadas,
-- comparar el tipo usado con el de mercado del día y priorizar desvíos.
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
    )
    WHERE rn = 1
),
fx_transactions AS (
    SELECT t.transaction_id,
           t.currency,
           t.amount_minor,
           t.counter_amount_minor,
           t.created_at,
           t.fx_rate_id,
           r.rate AS applied_rate,
           r.rate_date
    FROM transactions t
    LEFT JOIN fx_rates r ON r.rate_id = t.fx_rate_id
    WHERE t.transaction_type = 'FX'
      AND t.status = 'POSTED'
),
calculated AS (
    SELECT *,
           ROUND(amount_minor / NULLIF(counter_amount_minor / 100.0, 0), 6) AS effective_rate
    FROM fx_transactions
)
SELECT transaction_id,
       created_at,
       rate_date,
       applied_rate,
       effective_rate,
       ROUND(100.0 * (effective_rate - applied_rate) / NULLIF(applied_rate, 0), 4) AS deviation_pct,
       RANK() OVER (ORDER BY ABS(effective_rate - applied_rate) DESC) AS deviation_rank,
       (SELECT rate FROM latest_rate WHERE base_currency = 'USD' AND quote_currency = 'PYG') AS current_market_rate
FROM calculated
ORDER BY deviation_rank;
