-- R11: concentración de transferencias salientes hacia una misma contraparte.
-- Se evalúa sobre el período completo disponible; la ventana queda documentada
-- como referencia del análisis operativo.
WITH outgoing AS (
    SELECT t.transaction_id,
           t.debit_account_id AS account_id,
           a.customer_id,
           t.credit_account_id AS counterparty_id,
           t.amount_minor,
           t.currency,
           t.created_at
    FROM transactions t
    JOIN accounts a ON a.account_id = t.debit_account_id
    WHERE t.transaction_type = 'TRANSFER'
      AND t.status = 'POSTED'
      AND t.debit_account_id IS NOT NULL
),
aggregated AS (
    SELECT account_id,
           customer_id,
           counterparty_id,
           COUNT(*) AS transfer_count,
           SUM(amount_minor) AS counterparty_total
    FROM outgoing
    GROUP BY 1, 2, 3
),
account_totals AS (
    SELECT account_id, SUM(amount_minor) AS account_total
    FROM outgoing
    GROUP BY 1
),
dominant AS (
    SELECT a.*,
           t.account_total,
           a.counterparty_total * 1.0 / NULLIF(t.account_total, 0) AS share
    FROM aggregated a
    JOIN account_totals t ON t.account_id = a.account_id
    WHERE a.transfer_count >= :min_count
      AND a.counterparty_total >= :min_total_minor
      AND a.counterparty_total * 1.0 / NULLIF(t.account_total, 0) >= :min_share
)
SELECT DISTINCT
    'R11' AS rule_id,
    d.customer_id,
    d.account_id,
    o.transaction_id,
    o.amount_minor,
    o.currency,
    o.created_at AS detected_at,
    printf('{"counterparty_account_id":"%s","counterparty_share":%.4f,"transfer_count":%d,"window_days":%d}', d.counterparty_id, d.share, d.transfer_count, :window_days) AS detail_json
FROM dominant d
JOIN outgoing o
  ON o.account_id = d.account_id
 AND o.counterparty_id = d.counterparty_id;
