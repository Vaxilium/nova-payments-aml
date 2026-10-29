-- Propósito de negocio: balance de comprobación contable por cuenta del plan
-- de cuentas. Permite validar que débitos y créditos totales coincidan y ver
-- la posición neta acumulada por naturaleza (activo, pasivo, patrimonio, etc.).
WITH movements AS (
    SELECT g.gl_account_id,
           g.code,
           g.name,
           g.account_class,
           g.normal_side,
           COALESCE(SUM(CASE WHEN je.status = 'POSTED' THEN jl.debit_minor END), 0) AS debits,
           COALESCE(SUM(CASE WHEN je.status = 'POSTED' THEN jl.credit_minor END), 0) AS credits,
           COUNT(CASE WHEN je.status = 'POSTED' THEN 1 END) AS line_count
    FROM gl_accounts g
    LEFT JOIN journal_lines jl ON jl.gl_account_id = g.gl_account_id
    LEFT JOIN journal_entries je ON je.entry_id = jl.entry_id
    GROUP BY g.gl_account_id, g.code, g.name, g.account_class, g.normal_side
),
balances AS (
    SELECT *,
           CASE WHEN normal_side = 'DEBIT' THEN debits - credits ELSE credits - debits END AS net_balance
    FROM movements
)
SELECT code,
       name,
       account_class,
       normal_side,
       debits,
       credits,
       net_balance,
       line_count,
       SUM(debits) OVER () AS total_debits,
       SUM(credits) OVER () AS total_credits,
       SUM(net_balance) OVER (ORDER BY code ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_net,
       RANK() OVER (ORDER BY ABS(net_balance) DESC) AS activity_rank
FROM balances
ORDER BY code;
