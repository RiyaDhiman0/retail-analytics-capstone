{{ config(materialized='incremental', unique_key='event_id') }}
select event_id,event_ts,store_id,region,product_id,customer_id,quantity,unit_price,quantity*unit_price as revenue
from {{ source('raw','sales_events') }}
{% if is_incremental() %}
where event_ts > (select coalesce(max(event_ts),'1970-01-01') from {{ this }})
{% endif %}
