INSERT INTO silver.fact_sales(event_id,event_ts,store_id,product_id,customer_id,quantity,unit_price,revenue,region)
SELECT event_id,event_ts,store_id,product_id,customer_id,quantity,unit_price,
       quantity*unit_price,region
FROM bronze.sales_events
WHERE quantity > 0 AND unit_price >= 0
ON CONFLICT (event_id) DO NOTHING;
