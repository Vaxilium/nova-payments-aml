-- Propósito de negocio: monitorear el uso del sobregiro autorizado por cuenta
-- y detectar cuentas cercanas al límite. Insumo para gestión de liquidez y
-- para revisar la calidad de la cartera.
WITH usage AS (
    SELECT a.account_id,
           a.customer_id,
           a.currency,
           a.status,
           a.balance_minor,
           a.overdraft_limit_minor,
           a.balance_minor + a.overdraft_limit_minor AS available_minor,
           CASE
               WHEN a.overdraft_limit_minor = 0 THEN 0
               WHEN a.balance_minor >= a.overdraft_limit_minor THEN 0
               ELSE ROUND(
                   100.0 * (a.overdraft_limit_minor - a.balance_minor) / a.overdraft_limit_minor,
                   2
               )
           END AS overdraft_used_pct
    FROM accounts a
    WHERE a.status = 'ACTIVE'
)
SELECT account_id,
       customer_id,
       currency,
       balance_minor,
       overdraft_limit_minor,
       available_minor,
       overdraft_used_pct,
       RANK() OVER (PARTITION BY currency ORDER BY overdraft_used_pct DESC) AS risk_rank,
       CASE
           WHEN available_minor < 0 THEN 'EXCEDIDO'
           WHEN overdraft_used_pct >= 80 THEN 'ALTO'
           WHEN overdraft_used_pct > 0 THEN 'MEDIO'
           ELSE 'SIN_SOBREGIRO'
       END AS risk_band
FROM usage
ORDER BY currency, risk_rank;
