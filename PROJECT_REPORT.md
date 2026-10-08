# REAL-TIME RETAIL ANALYTICS PLATFORM WITH SELF-SERVE BI

## 1. Introduction
Retail businesses generate large volumes of point-of-sale events. Traditional batch reporting delays visibility into sales, product performance, regional trends and anomalies. This project designs an end-to-end analytics platform that moves from event ingestion to governed self-serve BI.

## 2. Objectives
1. Simulate high-volume POS events.
2. Stream events through region-partitioned Kafka topics.
3. Store and transform data through Bronze, Silver and Gold layers.
4. Build a star schema for analytical queries.
5. Implement incremental processing and data-quality controls.
6. Provide semantic KPIs and self-serve dashboards.
7. Demonstrate security, lineage, PII masking and performance optimisation.

## 3. Technology Stack
Python, Kafka/Redpanda, PostgreSQL, Spark Structured Streaming template, dbt, Airflow, Great Expectations integration, Streamlit, Superset deployment plan, Docker and SQL.

## 4. Medallion Architecture
Raw events are first landed without changing their business meaning. Bronze preserves validated source records. Silver provides clean analytical facts and dimensions. Gold contains dashboard-ready aggregates.

## 5. Star Schema
The central fact is `fact_sales`. Dimensions include store, product and customer. Returns and inventory are represented as additional facts. SCD Type 2 keeps historical versions of changing customer attributes.

## 6. Streaming
The Python producer generates POS events and assigns them to region-specific topics. The consumer validates each event and writes valid events to the landing table. Invalid events are captured in a dead-letter table and can be replayed after correction.

## 7. Data Quality
Checks cover null keys, duplicate events, invalid regions, non-positive quantities and negative revenue. A production Great Expectations checkpoint can stop the pipeline before the BI layer refreshes.

## 8. Semantic Layer and BI
Canonical metrics are defined once: revenue, orders, units, AOV, return rate and growth. The BI layer visualises trends, regional comparisons, product performance and anomalies. Row-level access separates regional and national managers.

## 9. Performance
The project compares non-sargable timestamp filters with range predicates, adds supporting indexes, uses pre-aggregated gold tables and applies incremental watermarks. These techniques reduce repeated scanning and support dashboard responsiveness.

## 10. Governance
Customer name and email are masked in non-production views. Data lineage is documented from source event to final KPI. SLA monitoring tracks freshness and completeness.

## 11. Results
The platform demonstrates a complete analytical flow from synthetic POS event generation to interactive business KPIs. The local mode makes the project reproducible without requiring a cloud account, while the Docker/Kafka/dbt/Airflow/Spark templates provide a clear path to production deployment.

## 12. Conclusion
The project satisfies the major functional areas of the supplied capstone brief and demonstrates practical data-engineering and analytics skills: streaming, modelling, transformation, testing, governance, optimisation and self-service BI.
