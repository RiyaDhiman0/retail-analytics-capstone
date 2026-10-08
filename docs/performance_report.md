# Query Performance Report

## Optimisation 1 — Sargable timestamp predicate

**Before:** `WHERE DATE(event_ts) = CURRENT_DATE`

The function on `event_ts` can prevent the database from using an ordered timestamp index efficiently.

**After:** `event_ts >= CURRENT_DATE AND event_ts < CURRENT_DATE + INTERVAL '1 day'`

This allows an index/range scan and improves partition pruning in time-partitioned warehouses.

## Optimisation 2 — Aggregate reuse

A materialised daily-region view avoids repeatedly scanning the detailed fact table for dashboard tiles.

## Optimisation 3 — Composite index

`(event_ts, region)` supports common time-window + regional dashboard filters.

## Optimisation 4 — Incremental processing

The watermark table prevents reprocessing old events.

## Optimisation 5 — Gold-layer denormalisation

Frequently used dashboard metrics are pre-aggregated into `gold.regional_kpis`.

### Evidence to capture
Run `EXPLAIN ANALYZE` from `sql/performance.sql` before and after. Record execution time, scan type and rows processed in the final submission.
