CREATE OR REPLACE VIEW security.national_sales AS
SELECT * FROM silver.fact_sales;

-- Example regional policy. In Superset, bind current_user_region to the logged-in user's region.
CREATE OR REPLACE VIEW security.regional_sales AS
SELECT * FROM silver.fact_sales
WHERE region = COALESCE(current_setting('app.user_region', true), 'UNKNOWN');

-- PII-safe view for non-production use.
CREATE OR REPLACE VIEW security.customer_masked AS
SELECT customer_id,
       'MASKED' AS customer_name,
       CASE WHEN email IS NULL THEN NULL ELSE CONCAT(LEFT(email,2),'***@***') END AS email,
       city
FROM silver.dim_customer_scd2;
