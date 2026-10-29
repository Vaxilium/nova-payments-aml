-- R02: velocidad por cantidad de transferencias en una ventana diaria.
WITH daily AS (
    SELECT t.debit_account_id AS account_id,
           a.customer_id,
           substr(t.created_at, 1, 10) AS day,
           COUNT(*) AS tx_count,
           SUM(t.amount_minor) AS total_amount
    FROM transactions t
    JOIN accounts a ON a.account_id = t.debit_account_id
    WHERE t.transaction_type = 'TRANSFER'
      AND t.status = 'POSTED'
      AND t.debit_account_id IS NOT NULL
    GROUP BY 1, 2, 3
    HAVING COUNT(*) >= :min_count
)
SELECT DISTINCT
    'R02' AS rule_id,
    d.customer_id,
    d.account_id,
    t.transaction_id,
    t.amount_minor,
    t.currency,
    t.created_at AS detected_at,
    printf('{"min_count":%d,"window_hours":%d,"tx_count":%d}', :min_count, :window_hours, d.tx_count) AS detail_json
FROM daily d
JOIN transactions t
  ON t.debit_account_id = d.account_id
 AND substr(t.created_at, 1, 10) = d.day
WHERE t.transaction_type = 'TRANSFER'
  AND t.status = 'POSTED';
