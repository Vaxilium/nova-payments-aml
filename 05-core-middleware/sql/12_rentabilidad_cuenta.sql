-- Propósito de negocio: estimar el rendimiento por comisiones de cada cuenta
-- respecto de su saldo y compararlo por deciles dentro de la moneda. Orienta
-- acciones de pricing y de gestión de cuentas de bajo valor.
WITH fee_by_account AS (
    SELECT t.debit_account_id AS account_id,
           SUM(f.amount_minor) AS fee_minor,
           COUNT(*) AS fee_count
    FROM fees f
    JOIN transactions t ON t.transaction_id = f.transaction_id
    WHERE t.debit_account_id IS NOT NULL
    GROUP BY t.debit_account_id
),
activity AS (
    SELECT t.debit_account_id AS account_id,
           COUNT(*) AS debit_tx,
           SUM(t.amount_minor) AS debit_amount
    FROM transactions t
    WHERE t.status = 'POSTED'
      AND t.debit_account_id IS NOT NULL
    GROUP BY t.debit_account_id
),
ranked AS (
    SELECT a.account_id,
           a.customer_id,
           a.currency,
           a.balance_minor,
           COALESCE(f.fee_minor, 0) AS fee_minor,
           COALESCE(f.fee_count, 0) AS fee_count,
           COALESCE(ac.debit_tx, 0) AS debit_tx,
           COALESCE(ac.debit_amount, 0) AS debit_amount,
           ROUND(100.0 * COALESCE(f.fee_minor, 0) / NULLIF(a.balance_minor, 0), 4) AS fee_yield_pct,
           NTILE(10) OVER (
               PARTITION BY a.currency
               ORDER BY COALESCE(f.fee_minor, 0) DESC
           ) AS fee_decile
    FROM accounts a
    LEFT JOIN fee_by_account f ON f.account_id = a.account_id
    LEFT JOIN activity ac ON ac.account_id = a.account_id
)
SELECT *
FROM ranked
ORDER BY currency, fee_decile, account_id;
