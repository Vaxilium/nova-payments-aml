-- R05: depósitos redondos de monto relevante, repetidos en una ventana.
WITH round_deposits AS (
    SELECT t.transaction_id,
           t.credit_account_id AS account_id,
           a.customer_id,
           t.amount_minor,
           t.currency,
           t.created_at
    FROM transactions t
    JOIN accounts a ON a.account_id = t.credit_account_id
    WHERE t.transaction_type = 'DEPOSIT'
      AND t.status = 'POSTED'
      AND t.amount_minor >= :min_amount_minor
      AND t.amount_minor % :round_unit = 0
),
anchors AS (
    SELECT x.account_id, x.customer_id, x.created_at AS anchor_at
    FROM round_deposits x
    JOIN round_deposits y
      ON y.account_id = x.account_id
     AND julianday(y.created_at) <= julianday(x.created_at)
     AND julianday(x.created_at) - julianday(y.created_at) <= :window_days
    GROUP BY x.transaction_id
    HAVING COUNT(*) >= :min_count
),
windows AS (
    SELECT DISTINCT account_id, customer_id, anchor_at FROM anchors
)
SELECT DISTINCT
    'R05' AS rule_id,
    w.customer_id,
    w.account_id,
    t.transaction_id,
    t.amount_minor,
    t.currency,
    t.created_at AS detected_at,
    printf('{"round_unit_minor":%d,"min_count":%d,"window_days":%d}', :round_unit, :min_count, :window_days) AS detail_json
FROM windows w
JOIN round_deposits t
  ON t.account_id = w.account_id
 AND julianday(t.created_at) <= julianday(w.anchor_at)
 AND julianday(w.anchor_at) - julianday(t.created_at) <= :window_days;

