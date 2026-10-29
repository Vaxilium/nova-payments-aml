-- R07: jurisdicción de alto riesgo según el país declarado del cliente.
SELECT DISTINCT
    'R07' AS rule_id,
    a.customer_id,
    a.account_id,
    t.transaction_id,
    t.amount_minor,
    t.currency,
    t.created_at AS detected_at,
    printf('{"country_code":"%s","list_source":"aml_high_risk_countries"}', c.country_code) AS detail_json
FROM transactions t
JOIN accounts a ON a.account_id = COALESCE(t.debit_account_id, t.credit_account_id)
JOIN customers c ON c.customer_id = a.customer_id
JOIN aml_high_risk_countries h
  ON h.country_code = c.country_code
 AND h.is_active = 1
WHERE t.status = 'POSTED';
