-- 03_customer_risk.sql
-- High-Risk Business Segment Query (Rule-Based, NOT ML)

-- This query identifies customers who match the high-risk business rules:
-- - Month-to-month contract
-- - 5 or more support calls
-- - Tenure of 12 months or less
--
-- NOTE: This is a rule-based segment, not a model output.
-- The ML-based risk scoring will be done in Python (Phase 2 Notebook).

SELECT
    customer_id,
    age,
    tenure,
    monthly_charges,
    contract_type,
    support_calls,
    churn
FROM customers
WHERE contract_type = 'Month-to-month'
  AND support_calls >= 5
  AND tenure <= 12
ORDER BY monthly_charges DESC;
