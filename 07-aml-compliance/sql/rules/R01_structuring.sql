-- R01: estructuración por debajo del umbral de reporte interno.
-- Devuelve las operaciones que integran una ventana con suficientes depósitos
-- cercanos al umbral y un monto acumulado relevante.
WITH near_threshold AS (
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
      AND t.amount_minor >= CAST(:threshold_minor * :min_ratio AS INTEGER)
      AND t.amount_minor < :threshold_minor
),
anchors AS (
    SELECT n.account_id, n.customer_id, n.created_at AS anchor_at
    FROM near_threshold n
    JOIN near_threshold p
      ON p.account_id = n.account_id
     AND julianday(p.created_at) <= julianday(n.created_at)
     AND julianday(n.created_at) - julianday(p.created_at) <= :window_days
    GROUP BY n.transaction_id
    HAVING COUNT(*) >= :min_count
       AND SUM(p.amount_minor) >= :min_total_minor
),
windows AS (
    SELECT DISTINCT account_id, customer_id, anchor_at FROM anchors
)
SELECT DISTINCT
    'R01' AS rule_id,
    w.customer_id,
    w.account_id,
    n.transaction_id,
    n.amount_minor,
    n.currency,
    n.created_at AS detected_at,
    printf('{"threshold_minor":%d,"min_count":%d,"window_days":%d}', :threshold_minor, :min_count, :window_days) AS detail_json
FROM windows w
JOIN near_threshold n
  ON n.account_id = w.account_id
 AND julianday(n.created_at) <= julianday(w.anchor_at)
 AND julianday(w.anchor_at) - julianday(n.created_at) <= :window_days;
