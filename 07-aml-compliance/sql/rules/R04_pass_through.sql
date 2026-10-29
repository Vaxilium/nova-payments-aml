-- R04: cuenta de paso. Entrada seguida de salida rápida y proporcional.
WITH pairs AS (
    SELECT d.transaction_id AS deposit_id,
           d.credit_account_id AS account_id,
           a.customer_id,
           d.amount_minor AS deposit_amount,
           d.currency,
           d.created_at AS deposit_at,
           t.transaction_id AS transfer_id,
           t.amount_minor AS transfer_amount,
           t.created_at AS transfer_at,
           ROW_NUMBER() OVER (PARTITION BY d.transaction_id ORDER BY t.created_at) AS rn
    FROM transactions d
    JOIN accounts a ON a.account_id = d.credit_account_id
    JOIN transactions t
      ON t.debit_account_id = d.credit_account_id
     AND t.transaction_type = 'TRANSFER'
     AND t.status = 'POSTED'
     AND t.created_at > d.created_at
     AND (julianday(t.created_at) - julianday(d.created_at)) * 24 * 60 <= :window_minutes
    WHERE d.transaction_type = 'DEPOSIT'
      AND d.status = 'POSTED'
      AND d.amount_minor >= :min_amount_minor
      AND t.amount_minor >= d.amount_minor * :min_ratio
),
selected AS (
    SELECT * FROM pairs WHERE rn = 1
)
SELECT 'R04' AS rule_id, customer_id, account_id, deposit_id AS transaction_id,
       deposit_amount AS amount_minor, currency, deposit_at AS detected_at,
       printf('{"deposit_id":"%s","transfer_id":"%s","window_minutes":%d}', deposit_id, transfer_id, :window_minutes) AS detail_json
FROM selected
UNION ALL
SELECT 'R04' AS rule_id, customer_id, account_id, transfer_id AS transaction_id,
       transfer_amount AS amount_minor, currency, transfer_at AS detected_at,
       printf('{"deposit_id":"%s","transfer_id":"%s","window_minutes":%d}', deposit_id, transfer_id, :window_minutes) AS detail_json
FROM selected;
