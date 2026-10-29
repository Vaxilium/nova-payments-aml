-- R06: activación de cuenta inactiva. Proxy operativo ante la ausencia de un
-- indicador de dormancia en el core; ver docs/PENDIENTES.md (P-015).
WITH candidates AS (
    SELECT t.transaction_id,
           t.credit_account_id AS account_id,
           a.customer_id,
           a.opened_at,
           t.amount_minor,
           t.currency,
           t.created_at,
           NULLIF(
               MAX(
                   COALESCE((
                       SELECT MAX(p.created_at)
                       FROM transactions p
                       WHERE p.credit_account_id = t.credit_account_id
                         AND p.created_at < t.created_at
                   ), ''),
                   COALESCE((
                       SELECT MAX(p.created_at)
                       FROM transactions p
                       WHERE p.debit_account_id = t.credit_account_id
                         AND p.created_at < t.created_at
                   ), '')
               ),
               ''
           ) AS previous_at
    FROM transactions t
    JOIN accounts a ON a.account_id = t.credit_account_id
    WHERE t.transaction_type = 'DEPOSIT'
      AND t.status = 'POSTED'
      AND t.amount_minor >= :min_amount_minor
      AND julianday(t.created_at) - julianday(a.opened_at) >= :min_account_age_days
    GROUP BY t.transaction_id
)
SELECT DISTINCT
    'R06' AS rule_id,
    customer_id,
    account_id,
    transaction_id,
    amount_minor,
    currency,
    created_at AS detected_at,
    printf('{"min_amount_minor":%d,"inactive_days":%.1f,"min_account_age_days":%d}', :min_amount_minor, :inactive_days, :min_account_age_days) AS detail_json
FROM candidates
WHERE previous_at IS NOT NULL
  AND julianday(created_at) - julianday(previous_at) >= :inactive_days;
