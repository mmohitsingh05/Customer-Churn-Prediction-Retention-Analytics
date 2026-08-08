-- 01_create_tables.sql
-- Create customers table for churn analytics

DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    age INTEGER,
    gender VARCHAR(20),
    tenure INTEGER,
    monthly_charges NUMERIC(10,2),
    contract_type VARCHAR(50),
    support_calls INTEGER,
    internet_service VARCHAR(50),
    payment_method VARCHAR(50),
    total_charges NUMERIC(12,2),
    churn VARCHAR(10)
);

-- Verify table creation
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'customers'
ORDER BY ordinal_position;
