-- BEFORE: function on the timestamp prevents efficient index/partition pruning.
EXPLAIN ANALYZE
SELECT region, SUM(revenue)
FROM silver.fact_sales
WHERE DATE(event_ts) = CURRENT_DATE
GROUP BY region;

-- AFTER: sargable time range + supporting index.
CREATE INDEX IF NOT EXISTS ix_fact_sales_event_ts_region ON silver.fact_sales(event_ts, region);
EXPLAIN ANALYZE
SELECT region, SUM(revenue)
FROM silver.fact_sales
WHERE event_ts >= CURRENT_DATE
  AND event_ts < CURRENT_DATE + INTERVAL '1 day'
GROUP BY region;

-- Materialised aggregate for dashboard queries.
CREATE MATERIALIZED VIEW IF NOT EXISTS gold.mv_region_daily AS
SELECT event_ts::date AS sales_date, region, COUNT(*) orders, SUM(quantity) units, SUM(revenue) revenue
FROM silver.fact_sales GROUP BY event_ts::date, region;
