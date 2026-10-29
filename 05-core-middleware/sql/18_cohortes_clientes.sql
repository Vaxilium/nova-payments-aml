-- Propósito de negocio: analizar la evolución de altas y saldos por mes de
-- creación de cliente (cohorte), para medir captación y maduración de la base.
WITH cohorts AS (
    SELECT customer_id,
           substr(created_at, 1, 7) AS cohort_month
    FROM customers
),
accounts_by_cohort AS (
    SELECT c.cohort_month,
           a.currency,
           COUNT(*) AS account_count,
           SUM(a.balance_minor) AS balance_minor
    FROM cohorts c
    JOIN accounts a ON a.customer_id = c.customer_id
    GROUP BY c.cohort_month, a.currency
),
ranked AS (
    SELECT *,
           SUM(account_count) OVER (
               PARTITION BY currency ORDER BY cohort_month
           ) AS cumulative_accounts,
           LAG(account_count) OVER (
               PARTITION BY currency ORDER BY cohort_month
           ) AS previous_accounts,
           RANK() OVER (
               PARTITION BY currency ORDER BY balance_minor DESC
           ) AS cohort_balance_rank
    FROM accounts_by_cohort
)
SELECT *
FROM ranked
ORDER BY currency, cohort_month;
