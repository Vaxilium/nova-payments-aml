-- R10: circularidad entre dos cuentas con retorno de monto similar.
WITH transfers AS (
    SELECT t.transaction_id,
           t.debit_account_id,
           t.credit_account_id,
           t.amount_minor,
           t.currency,
           t.created_at
    FROM transactions t
    WHERE t.transaction_type = 'TRANSFER'
      AND t.status = 'POSTED'
      AND t.debit_account_id IS NOT NULL
),
pairs AS (
    SELECT a.transaction_id AS out_id,
           a.debit_account_id AS account_id,
           da.customer_id,
           a.amount_minor AS out_amount,
           a.currency,
           a.created_at AS out_at,
           b.transaction_id AS return_id,
           b.amount_minor AS return_amount,
           b.created_at AS return_at,
           ROW_NUMBER() OVER (PARTITION BY a.transaction_id ORDER BY b.created_at) AS rn
    FROM transfers a
    JOIN accounts da ON da.account_id = a.debit_account_id
    JOIN transfers b
      ON b.debit_account_id = a.credit_account_id
     AND b.credit_account_id = a.debit_account_id
     AND b.created_at > a.created_at
     AND julianday(b.created_at) - julianday(a.created_at) <= :window_days
     AND b.amount_minor BETWEEN a.amount_minor * (1 - :tolerance)
                            AND a.amount_minor * (1 + :tolerance)
    WHERE a.amount_minor >= :min_amount_minor
)
SELECT 'R10' AS rule_id, customer_id, account_id, out_id AS transaction_id,
       out_amount AS amount_minor, currency, out_at AS detected_at,
       printf('{"out_transfer_id":"%s","return_transfer_id":"%s","out_amount_minor":%d,"return_amount_minor":%d}', out_id, return_id, out_amount, return_amount) AS detail_json
FROM pairs
WHERE rn = 1
UNION ALL
SELECT 'R10' AS rule_id, customer_id, account_id, return_id AS transaction_id,
       return_amount AS amount_minor, currency, return_at AS detected_at,
       printf('{"out_transfer_id":"%s","return_transfer_id":"%s","out_amount_minor":%d,"return_amount_minor":%d}', out_id, return_id, out_amount, return_amount) AS detail_json
FROM pairs
WHERE rn = 1;
