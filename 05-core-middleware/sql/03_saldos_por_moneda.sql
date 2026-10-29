-- Propósito de negocio: dimensionar el pasivo de clientes por moneda y tipo
-- de cuenta, con participación relativa y ranking dentro de cada moneda.
WITH base AS (
    SELECT currency,
           account_type,
           COUNT(*) AS accounts,
           SUM(CASE WHEN status = 'ACTIVE' THEN 1 ELSE 0 END) AS active_accounts,
           SUM(balance_minor) AS balance_minor
    FROM accounts
    GROUP BY currency, account_type
),
currency_totals AS (
    SELECT currency, SUM(balance_minor) AS total_minor
    FROM base
    GROUP BY currency
)
SELECT b.currency,
       b.account_type,
       b.accounts,
       b.active_accounts,
       b.balance_minor,
       ROUND(100.0 * b.balance_minor / NULLIF(t.total_minor, 0), 2) AS pct_currency,
       SUM(b.balance_minor) OVER (
           PARTITION BY b.currency
           ORDER BY b.balance_minor DESC
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS cumulative_minor,
       RANK() OVER (PARTITION BY b.currency ORDER BY b.balance_minor DESC) AS type_rank
FROM base b
JOIN currency_totals t ON t.currency = b.currency
ORDER BY b.currency, b.balance_minor DESC;
