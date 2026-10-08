select region,count(*) as orders,sum(quantity) as units,sum(revenue) as revenue,
round(sum(revenue)/nullif(count(*),0),2) as avg_order_value
from {{ ref('stg_sales') }} group by region
