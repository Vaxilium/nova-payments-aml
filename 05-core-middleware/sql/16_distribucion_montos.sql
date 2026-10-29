-- Propósito de negocio: entender la distribución de importes operados por
-- moneda y rango, información útil para calibrar umbrales y diseñar reglas
-- de monitoreo proporcionadas al tamaño típico de las operaciones.
WITH bucketed AS (
    SELECT currency,
           amount_minor,
           CASE
               WHEN currency = 'PYG' THEN
                   CASE
                       WHEN amount_minor < 100000 THEN '0-100k'
                       WHEN amount_minor < 1000000 THEN '100k-1M'
                       WHEN amount_minor < 10000000 THEN '1M-10M'
                       ELSE '>=10M'
                   END
               ELSE
                   CASE
                       WHEN amount_minor < 10000 THEN '0-100'
                       WHEN amount_minor < 100000 THEN '100-1k'
                       WHEN amount_minor < 1000000 THEN '1k-10k'
                       ELSE '>=10k'
                   END
           END AS amount_bucket
    FROM transactions
    WHERE status = 'POSTED'
),
aggregated AS (
    SELECT currency,
           amount_bucket,
           COUNT(*) AS tx_count,
           SUM(amount_minor) AS total_minor,
           MIN(amount_minor) AS min_minor,
           MAX(amount_minor) AS max_minor,
           AVG(amount_minor) AS avg_minor
    FROM bucketed
    GROUP BY currency, amount_bucket
),
ranked AS (
    SELECT *,
           ROUND(100.0 * tx_count / NULLIF(SUM(tx_count) OVER (PARTITION BY currency), 0), 2) AS pct_transactions,
           RANK() OVER (PARTITION BY currency ORDER BY total_minor DESC) AS bucket_rank
    FROM aggregated
)
SELECT *
FROM ranked
ORDER BY currency, bucket_rank;
