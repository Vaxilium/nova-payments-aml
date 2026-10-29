-- R12: fan-in semanal. Múltiples remitentes distintos hacia una misma cuenta
-- dentro de la misma semana calendario (ventana de 7 días).
WITH incoming AS (
    SELECT t.transaction_id,
           t.credit_account_id AS account_id,
           a.customer_id,
           t.debit_account_id AS sender_account_id,
           t.amount_minor,
           t.currency,
           t.created_at,
           strftime('%Y-%W', t.created_at) AS week
    FROM transactions t
    JOIN accounts a ON a.account_id = t.credit_account_id
    WHERE t.transaction_type = 'TRANSFER'
      AND t.status = 'POSTED'
      AND t.debit_account_id IS NOT NULL
),
aggregated AS (
    SELECT account_id,
           customer_id,
           week,
           COUNT(DISTINCT sender_account_id) AS sender_count,
           COUNT(*) AS transfer_count,
           SUM(amount_minor) AS total_amount
    FROM incoming
    GROUP BY 1, 2, 3
)
SELECT DISTINCT
    'R12' AS rule_id,
    g.customer_id,
    g.account_id,
    i.transaction_id,
    i.amount_minor,
    i.currency,
    i.created_at AS detected_at,
    printf('{"week":"%s","sender_count":%d,"transfer_count":%d,"total_minor":%d,"window_days":%d}', g.week, g.sender_count, g.transfer_count, CAST(g.total_amount AS INTEGER), :window_days) AS detail_json
FROM aggregated g
JOIN incoming i ON i.account_id = g.account_id AND i.week = g.week
WHERE g.sender_count >= :min_senders
  AND g.total_amount >= :min_total_minor;
