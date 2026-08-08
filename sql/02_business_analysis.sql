-- 02_business_analysis.sql
-- 12 Business Analysis Queries for Customer Churn

-- ============================================
-- Q1: Total Customers
-- ============================================
SELECT COUNT(*) AS total_customers
FROM customers;

-- ============================================
-- Q2: Churned Customers Count
-- ============================================
SELECT COUNT(*) AS churned_customers
FROM customers
WHERE churn = 'Yes';

-- ============================================
-- Q3: Churn Rate (%)
-- ============================================
SELECT
    ROUND(COUNT(*) FILTER (WHERE churn = 'Yes') * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers;

-- ============================================
-- Q4: Retention Rate (%)
-- ============================================
SELECT
    ROUND(COUNT(*) FILTER (WHERE churn = 'No') * 100.0 / COUNT(*), 2) AS retention_rate_pct
FROM customers;

-- ============================================
-- Q5: Revenue Lost Due to Churn
-- ============================================
SELECT
    ROUND(SUM(monthly_charges), 2) AS monthly_revenue_lost
FROM customers
WHERE churn = 'Yes';

-- ============================================
-- Q6: Average Monthly Charges
-- ============================================
SELECT
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM customers;

-- ============================================
-- Q7: Churn by Contract Type (count + rate)
-- ============================================
SELECT
    contract_type,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    ROUND(COUNT(*) FILTER (WHERE churn = 'Yes') * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY contract_type
ORDER BY churn_rate_pct DESC;

-- ============================================
-- Q8: Churn by Gender
-- ============================================
SELECT
    gender,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    ROUND(COUNT(*) FILTER (WHERE churn = 'Yes') * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY gender
ORDER BY churn_rate_pct DESC;

-- ============================================
-- Q9: Churn by Support Calls
-- ============================================
SELECT
    support_calls,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    ROUND(COUNT(*) FILTER (WHERE churn = 'Yes') * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY support_calls
ORDER BY support_calls;

-- ============================================
-- Q10: Churn by Tenure Group (matches Python bins)
-- ============================================
SELECT
    CASE
        WHEN tenure <= 6 THEN '0-6 Months'
        WHEN tenure <= 12 THEN '7-12 Months'
        WHEN tenure <= 24 THEN '13-24 Months'
        WHEN tenure <= 48 THEN '25-48 Months'
        ELSE '49-72 Months'
    END AS tenure_group,
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned_customers,
    ROUND(COUNT(*) FILTER (WHERE churn = 'Yes') * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY tenure_group
ORDER BY MIN(tenure);

-- ============================================
-- Q11: Top 20 High-Value Churned Customers
-- ============================================
SELECT
    customer_id,
    age,
    tenure,
    monthly_charges,
    contract_type,
    support_calls,
    churn
FROM customers
WHERE churn = 'Yes'
ORDER BY monthly_charges DESC
LIMIT 20;

-- ============================================
-- Q12: Revenue at Risk by Contract Type
-- ============================================
SELECT
    contract_type,
    COUNT(*) AS churned_customers,
    ROUND(SUM(monthly_charges), 2) AS monthly_revenue_at_risk,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charge_at_risk
FROM customers
WHERE churn = 'Yes'
GROUP BY contract_type
ORDER BY monthly_revenue_at_risk DESC;
