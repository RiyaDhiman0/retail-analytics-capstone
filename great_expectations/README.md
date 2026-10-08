# Great Expectations integration

The capstone brief requires a Great Expectations checkpoint on every dbt run and pipeline halt/alert on a quality breach. fileciteturn0file0L78-L82

Use the following conceptual suites:
- `sales_event_id_not_null`
- `sales_event_id_unique`
- `quantity_positive`
- `unit_price_non_negative`
- `region_in_allowed_set`
- `freshness_under_sla`

The runnable local gate is `src/quality_checks.py`. In a managed deployment, connect these expectations to a Great Expectations checkpoint invoked after dbt and before BI refresh.
