# Real-Time Retail Analytics Platform

## Industry-Level Data Analytics Capstone

A practical, reproducible implementation of the supplied **Capstone Project 07 – Real-Time Retail Analytics Platform with Self-Serve BI**.

### What this project demonstrates
- Kafka-compatible event streaming with region-partitioned topics
- POS transaction simulation at a configurable high event rate
- Raw → Bronze → Silver → Gold medallion architecture
- Star-schema modelling for sales, returns and inventory
- SCD Type 2 customer dimension
- dbt transformations, tests and documentation structure
- Incremental watermark-based processing
- Data-quality validation and quarantine/dead-letter handling
- KPI/semantic metric definitions
- Regional row-level security examples
- Query optimisation evidence with before/after SQL and EXPLAIN workflow
- Self-serve dashboard using Streamlit for a laptop-friendly demo
- Superset SQL/dashboard configuration notes
- Airflow orchestration DAG
- Docker services for the local stack
- Mock embedded analytics portal

> **Academic honesty note:** this repository provides a complete educational implementation and local demonstration. The production technologies in the brief (Flink/Spark, Snowflake/BigQuery/Redshift, Superset, Kubernetes, Terraform) are represented with runnable local substitutes and integration-ready templates where a full cloud cluster would be impractical on a student machine.

## 1. Architecture

```text
                    +----------------------+
                    | POS Event Generator  |
                    | Python               |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Kafka / Redpanda      |
                    | topics by region      |
                    +----------+-----------+
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
        +----------------+          +----------------+
        | Stream Consumer|          | Dead Letter     |
        | exactly-once*  |          | malformed data  |
        +-------+--------+          +----------------+
                |
                v
        +----------------+
        | PostgreSQL     |
        | RAW / BRONZE   |
        +-------+--------+
                |
                v
        +----------------+
        | SILVER         |
        | cleaned facts  |
        +-------+--------+
                |
                v
        +----------------+
        | GOLD           |
        | KPI marts      |
        +-------+--------+
                |
        +-------+--------+
        |                |
        v                v
 +-------------+   +-------------+
 | dbt / tests |   | BI / RLS    |
 | docs / DAG  |   | Dashboard   |
 +-------------+   +-------------+
```

`*` The production brief calls for exactly-once semantics. The local Python consumer uses an event_id uniqueness constraint plus idempotent inserts to reproduce the important observable behaviour.

## 2. Requirement mapping

| Brief requirement | Implementation in this repository |
|---|---|
| Kafka topics by region | `src/producer.py` and Docker Redpanda |
| 50,000 events/hour simulation | Configurable producer; default 50,000/hour |
| Flink/Spark streaming | `streaming/spark_streaming.py` integration template |
| Schema Registry + Avro | `streaming/schema/sale_event.avsc` + compatibility notes |
| Dead-letter topic/replay | `src/consumer.py`, `src/replay_dlq.py` |
| Medallion architecture | `sql/01_bronze.sql`, `02_silver.sql`, `03_gold.sql` |
| Star schema | `sql/schema.sql` |
| SCD Type 2 | `sql/02_silver.sql` customer dimension logic |
| dbt transformations/tests | `dbt/` |
| Incremental watermark merge | `src/incremental_load.py` |
| Query optimisation | `docs/performance_report.md`, `sql/performance.sql` |
| Semantic layer | `docs/semantic_layer.md` |
| BI dashboards | `src/dashboard.py` + `superset/` |
| Row-level security | `sql/security.sql` |
| Data quality | `src/quality_checks.py` + `great_expectations/` |
| Data catalogue/lineage | `docs/data_catalog.md` |
| PII masking | `sql/security.sql` |
| SLA monitoring | `src/sla_monitor.py` |
| Orchestration | `dags/retail_pipeline.py` |
| Embedded analytics | `portal/app.py` |

The original brief explicitly asks for a live Kafka-to-dashboard flow, dbt DAG/tests/docs, Superset RLS, query-performance evidence and a Great Expectations validation report. See the supplied brief. fileciteturn0file0L86-L94

## 3. Fastest demo path

### Option A — laptop demo

1. Install Python 3.11+.
2. `pip install -r requirements.txt`
3. Start PostgreSQL and Kafka/Redpanda with Docker:
   `docker compose up -d postgres redpanda`
4. Create tables:
   `python src/bootstrap.py`
5. Generate master data:
   `python src/generate_master_data.py`
6. Start event producer:
   `python src/producer.py --events 1000 --interval 0.01`
7. Start consumer in another terminal:
   `python src/consumer.py --max-events 1000`
8. Run transformation:
   `python src/transform.py`
9. Run quality checks:
   `python src/quality_checks.py`
10. Start dashboard:
   `streamlit run src/dashboard.py`

### Option B — no Docker/Kafka available

Run:

```bash
python src/local_demo.py
streamlit run src/dashboard.py
```

This creates a realistic synthetic retail dataset locally and runs the same Bronze → Silver → Gold analytical logic.

## 4. Suggested presentation storyline

1. Business problem: retail managers cannot make fast decisions from delayed sales reports.
2. Solution: stream POS events into a governed analytical platform.
3. Data flow: POS → Kafka → landing → Bronze → Silver → Gold → BI.
4. Data quality: invalid records go to quarantine/DLQ instead of contaminating KPIs.
5. Analytics: revenue, orders, AOV, units, returns and regional performance.
6. Governance: SCD2, PII masking, lineage and regional access control.
7. Optimisation: partitioning, indexes, materialised aggregates and EXPLAIN comparison.
8. Outcome: self-serve, near-real-time decision support.

## 5. Important submission evidence

Before submission, capture screenshots of:
- Producer sending events
- Kafka/Redpanda topics
- Consumer inserting records
- Bronze/Silver/Gold row counts
- dbt model DAG and tests
- Data-quality validation output
- Dashboard KPI cards and charts
- Regional user showing only permitted stores
- National user showing all regions
- EXPLAIN before/after
- SLA freshness/completeness output

## 6. Production upgrade path

For a cloud deployment, replace local PostgreSQL with Snowflake/BigQuery/Redshift, replace the local consumer with Flink or Spark Structured Streaming, use managed Kafka + Schema Registry, run dbt and Airflow in managed infrastructure, and deploy Superset behind SSO. The conceptual architecture remains the same.
