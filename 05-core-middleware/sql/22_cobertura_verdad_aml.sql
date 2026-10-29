-- Propósito de negocio: medir el volumen y la distribución de los patrones
-- etiquetados en la tabla interna de verdad sintética. Se usa para validar
-- cobertura de reglas y falsos positivos en la Fase 5. No es una consulta
-- operativa ni se expone por la API.
WITH truth AS (
    SELECT g.pattern_type,
           g.label,
           COUNT(*) AS tx_count,
           COUNT(DISTINCT g.customer_id) AS customers,
           SUM(t.amount_minor) AS amount_minor,
           MIN(t.created_at) AS first_at,
           MAX(t.created_at) AS last_at
    FROM _aml_ground_truth g
    JOIN transactions t ON t.transaction_id = g.transaction_id
    GROUP BY g.pattern_type, g.label
),
totals AS (
    SELECT SUM(tx_count) AS total_tx FROM truth
),
ranked AS (
    SELECT *,
           ROUND(100.0 * tx_count / NULLIF((SELECT total_tx FROM totals), 0), 2) AS pct_of_truth,
           RANK() OVER (ORDER BY tx_count DESC) AS volume_rank
    FROM truth
)
SELECT *
FROM ranked
ORDER BY volume_rank;
