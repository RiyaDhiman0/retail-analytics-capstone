INSERT INTO gold.daily_sales(sales_date,region,orders,units,revenue,avg_order_value)
SELECT event_ts::date, region, COUNT(*), SUM(quantity), SUM(revenue), ROUND(SUM(revenue)/NULLIF(COUNT(*),0),2)
FROM silver.fact_sales
GROUP BY event_ts::date, region
ON CONFLICT (sales_date,region) DO UPDATE SET orders=EXCLUDED.orders,units=EXCLUDED.units,revenue=EXCLUDED.revenue,avg_order_value=EXCLUDED.avg_order_value;

INSERT INTO gold.regional_kpis(region,orders,units,revenue,avg_order_value,return_rate)
SELECT region,COUNT(*),SUM(quantity),SUM(revenue),ROUND(SUM(revenue)/NULLIF(COUNT(*),0),2),0
FROM silver.fact_sales GROUP BY region
ON CONFLICT(region) DO UPDATE SET orders=EXCLUDED.orders,units=EXCLUDED.units,revenue=EXCLUDED.revenue,avg_order_value=EXCLUDED.avg_order_value,refreshed_at=NOW();
