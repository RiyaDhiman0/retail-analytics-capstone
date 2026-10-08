# Semantic Layer

## Canonical metrics
- **Revenue** = SUM(fact_sales.revenue)
- **Orders** = COUNT(DISTINCT fact_sales.event_id)
- **Units** = SUM(fact_sales.quantity)
- **Average Order Value** = Revenue / Orders
- **Return Rate** = Returned Units / Sold Units
- **Sales Growth %** = (Current Revenue - Prior Revenue) / Prior Revenue × 100

Dimensions: date, region, store, product, category, brand.

Access policy: national managers can query all regions; regional managers are restricted to their assigned region.
