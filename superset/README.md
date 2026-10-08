# Apache Superset Dashboard Plan

Create a PostgreSQL database connection and use `gold.regional_kpis` and `gold.daily_sales`.

Recommended dashboard tiles:
1. Total Revenue KPI
2. Orders KPI
3. Units KPI
4. Average Order Value KPI
5. Daily Revenue Line Chart
6. Regional Revenue Bar Chart
7. Product Performance Table
8. Anomaly/alert table

## Row-level security
Create two roles:
- `regional_manager`: dataset filter `region = <user_region>`
- `national_manager`: no region restriction

## Embedded analytics
Embed the Superset dashboard in an internal portal after enabling the deployment's SSO/authentication mechanism. For the student demo, `portal/app.py` is a local mock of this experience.
