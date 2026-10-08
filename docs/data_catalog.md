# Data Catalogue & Lineage

| Layer | Table | Grain | Key | PII |
|---|---|---|---|---|
| Raw | raw.sales_events | one POS event | event_id | possible customer_id |
| Bronze | bronze.sales_events | one validated event | event_id | possible customer_id |
| Silver | silver.fact_sales | one sale | event_id | customer_id |
| Silver | silver.dim_customer_scd2 | customer version | customer_sk | name/email |
| Gold | gold.daily_sales | day + region | sales_date, region | no |
| Gold | gold.regional_kpis | region | region | no |

Lineage: Kafka sale event → raw.sales_events → bronze.sales_events → silver.fact_sales → gold.daily_sales / gold.regional_kpis → BI metric.
