-- Propósito de negocio: control global de partida doble por día y moneda.
-- Débitos y créditos deben coincidir siempre; cualquier desvío indica un
-- asiento inconsistente o una intervención manual no autorizada.
WITH daily AS (
    SELECT je.entry_date,
           jl.currency,
           SUM(jl.debit_minor) AS debits,
           SUM(jl.credit_minor) AS credits,
           COUNT(DISTINCT je.entry_id) AS entries
    FROM journal_entries je
    JOIN journal_lines jl ON jl.entry_id = je.entry_id
    WHERE je.status = 'POSTED'
    GROUP BY je.entry_date, jl.currency
),
checks AS (
    SELECT *,
           debits - credits AS imbalance,
           SUM(debits - credits) OVER (
               PARTITION BY currency ORDER BY entry_date
           ) AS cumulative_imbalance,
           RANK() OVER (
               PARTITION BY currency ORDER BY ABS(debits - credits) DESC
           ) AS imbalance_rank
    FROM daily
)
SELECT *
FROM checks
ORDER BY currency, entry_date;
