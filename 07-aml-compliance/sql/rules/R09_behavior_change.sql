-- R09: cambio abrupto de comportamiento transaccional mensual.
WITH monthly AS (
    SELECT a.customer_id,
           substr(t.created_at, 1, 7) AS month,
           SUM(t.amount_minor) AS total_amount,
           COUNT(*) AS tx_count
    FROM transactions t
    JOIN accounts a ON a.account_id = COALESCE(t.debit_account_id, t.credit_account_id)
    WHERE t.status = 'POSTED'
    GROUP BY 1, 2
),
baseline AS (
    SELECT m.customer_id,
           m.month,
           m.total_amount,
           m.tx_count,
           (
               SELECT AVG(b.total_amount)
               FROM monthly b
               WHERE b.customer_id = m.customer_id
                 AND b.month < m.month
                 AND b.month >= strftime('%Y-%m', date(m.month || '-01', '-3 months'))
           ) AS average_previous,
           (
               SELECT COUNT(*)
               FROM monthly b
               WHERE b.customer_id = m.customer_id
                 AND b.month < m.month
                 AND b.month >= strftime('%Y-%m', date(m.month || '-01', '-3 months'))
           ) AS previous_months
    FROM monthly m
),
spikes AS (
    SELECT * FROM baseline
    WHERE total_amount >= :min_total_minor
      AND average_previous > 0
      AND previous_months >= 1
      AND total_amount >= average_previous * :multiplier
)
SELECT DISTINCT
    'R09' AS rule_id,
    s.customer_id,
    COALESCE(t.debit_account_id, t.credit_account_id) AS account_id,
    t.transaction_id,
    t.amount_minor,
    t.currency,
    t.created_at AS detected_at,
    printf('{"month":"%s","month_total_minor":%d,"baseline_minor":%d,"multiplier":%.2f}', s.month, CAST(s.total_amount AS INTEGER), CAST(s.average_previous AS INTEGER), :multiplier) AS detail_json
FROM spikes s
JOIN transactions t
  ON substr(t.created_at, 1, 7) = s.month
JOIN accounts a
  ON a.customer_id = s.customer_id
 AND a.account_id = COALESCE(t.debit_account_id, t.credit_account_id)
WHERE t.status = 'POSTED';
