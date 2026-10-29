-- Propósito de negocio: seguir el volumen contable diario por moneda,
-- compararlo con el promedio móvil de 7 días y detectar picos o caídas
-- anómalas de actividad.
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
stats AS (
    SELECT *,
           (debits + credits) / 2.0 AS volume,
           AVG((debits + credits) / 2.0) OVER (
               PARTITION BY currency
               ORDER BY entry_date
               ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           ) AS moving_avg_7d,
           LAG((debits + credits) / 2.0) OVER (
               PARTITION BY currency ORDER BY entry_date
           ) AS previous_volume
    FROM daily
)
SELECT entry_date,
       currency,
       debits,
       credits,
       entries,
       ROUND(volume, 2) AS volume,
       ROUND(moving_avg_7d, 2) AS moving_avg_7d,
       ROUND(100.0 * (volume - previous_volume) / NULLIF(previous_volume, 0), 2) AS pct_change,
       RANK() OVER (PARTITION BY currency ORDER BY volume DESC) AS volume_rank
FROM stats
ORDER BY currency, entry_date;
