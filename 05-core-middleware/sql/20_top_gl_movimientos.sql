-- Propósito de negocio: identificar las cuentas contables con mayor volumen
-- de movimiento y su participación en el total. Ayuda a priorizar controles
-- y a entender el peso relativo de cada proceso en el libro mayor.
WITH activity AS (
    SELECT g.gl_account_id,
           g.code,
           g.name,
           g.account_class,
           g.normal_side,
           SUM(
               CASE WHEN je.status = 'POSTED' THEN jl.debit_minor + jl.credit_minor ELSE 0 END
           ) AS volume_minor,
           COUNT(CASE WHEN je.status = 'POSTED' THEN 1 END) AS line_count,
           COUNT(DISTINCT jl.entry_id) AS entry_count
    FROM gl_accounts g
    LEFT JOIN journal_lines jl ON jl.gl_account_id = g.gl_account_id
    LEFT JOIN journal_entries je ON je.entry_id = jl.entry_id
    GROUP BY g.gl_account_id, g.code, g.name, g.account_class, g.normal_side
),
ranked AS (
    SELECT *,
           ROUND(100.0 * volume_minor / NULLIF(SUM(volume_minor) OVER (), 0), 4) AS pct_volume,
           RANK() OVER (ORDER BY volume_minor DESC) AS volume_rank,
           LAG(volume_minor) OVER (ORDER BY volume_minor DESC) AS next_lower_volume
    FROM activity
)
SELECT *
FROM ranked
ORDER BY volume_rank;
