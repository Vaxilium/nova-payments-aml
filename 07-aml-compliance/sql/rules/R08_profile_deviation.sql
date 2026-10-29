-- R08: importe atípico respecto del historial disponible del cliente.
WITH customer_stats AS (
    SELECT a.customer_id,
           AVG(t.amount_minor) AS average_amount,
           COUNT(*) AS history_count
    FROM transactions t
    JOIN accounts a ON a.account_id = COALESCE(t.debit_account_id, t.credit_account_id)
    WHERE t.status = 'POSTED'
    GROUP BY 1
)
SELECT DISTINCT
    'R08' AS rule_id,
    a.customer_id,
    COALESCE(t.debit_account_id, t.credit_account_id) AS account_id,
    t.transaction_id,
    t.amount_minor,
    t.currency,
    t.created_at AS detected_at,
    printf('{"average_amount_minor":%d,"history_count":%d,"multiplier":%.2f}', CAST(s.average_amount AS INTEGER), s.history_count, :multiplier) AS detail_json
FROM transactions t
JOIN accounts a ON a.account_id = COALESCE(t.debit_account_id, t.credit_account_id)
JOIN customer_stats s ON s.customer_id = a.customer_id
WHERE t.status = 'POSTED'
  AND t.amount_minor >= :min_amount_minor
  AND s.history_count >= :min_history
  AND s.average_amount > 0
  AND t.amount_minor >= s.average_amount * :multiplier;
