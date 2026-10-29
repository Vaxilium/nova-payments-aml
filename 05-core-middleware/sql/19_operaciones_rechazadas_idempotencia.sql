-- Propósito de negocio: controlar reintentos y rechazos. Identifica operaciones
-- rechazadas repetidas y claves de idempotencia reutilizadas, señales de
-- problemas de integración o de abuso del canal.
WITH rejected AS (
    SELECT transaction_id,
           transaction_type,
           currency,
           amount_minor,
           debit_account_id,
           created_at,
           ROW_NUMBER() OVER (
               PARTITION BY debit_account_id, amount_minor, currency
               ORDER BY created_at
           ) AS attempt_sequence,
           COUNT(*) OVER (
               PARTITION BY debit_account_id, amount_minor, currency
           ) AS attempts
    FROM transactions
    WHERE status = 'REJECTED'
),
repeated AS (
    SELECT transaction_id,
           attempts AS occurrences,
           created_at
    FROM rejected
    WHERE attempts > 1
),
idempotency AS (
    SELECT idempotency_key,
           operation_id,
           COUNT(*) OVER (PARTITION BY request_hash) AS same_payload_count,
           ROW_NUMBER() OVER (
               PARTITION BY request_hash ORDER BY created_at
           ) AS payload_sequence,
           created_at
    FROM idempotency_keys
),
events AS (
    SELECT 'REJECTED_REPEATED' AS category,
           transaction_id AS entity_id,
           NULL AS idempotency_key,
           occurrences,
           created_at
    FROM repeated
    UNION ALL
    SELECT 'IDEMPOTENCY_REUSED' AS category,
           operation_id AS entity_id,
           idempotency_key,
           same_payload_count AS occurrences,
           created_at
    FROM idempotency
    WHERE same_payload_count > 1
)
SELECT category,
       entity_id,
       idempotency_key,
       occurrences,
       created_at,
       RANK() OVER (ORDER BY occurrences DESC) AS priority_rank
FROM events
ORDER BY priority_rank;
