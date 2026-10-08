CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS security;

CREATE TABLE IF NOT EXISTS raw.sales_events (
    event_id UUID PRIMARY KEY,
    event_ts TIMESTAMPTZ NOT NULL,
    store_id INT NOT NULL,
    region TEXT NOT NULL,
    product_id INT NOT NULL,
    customer_id INT,
    quantity INT NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    payment_method TEXT,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS raw.dead_letter_events (
    dlq_id BIGSERIAL PRIMARY KEY,
    raw_payload JSONB NOT NULL,
    error_reason TEXT NOT NULL,
    failed_at TIMESTAMPTZ DEFAULT NOW(),
    replayed BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS bronze.sales_events AS TABLE raw.sales_events WITH NO DATA;
CREATE TABLE IF NOT EXISTS silver.dim_store (
    store_sk BIGSERIAL PRIMARY KEY,
    store_id INT NOT NULL,
    store_name TEXT NOT NULL,
    region TEXT NOT NULL,
    manager_name TEXT,
    valid_from TIMESTAMPTZ NOT NULL,
    valid_to TIMESTAMPTZ,
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS silver.dim_product (
    product_sk BIGSERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    brand TEXT NOT NULL,
    unit_cost NUMERIC(12,2),
    valid_from TIMESTAMPTZ NOT NULL,
    valid_to TIMESTAMPTZ,
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS silver.dim_customer_scd2 (
    customer_sk BIGSERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    customer_name TEXT,
    email TEXT,
    city TEXT,
    valid_from TIMESTAMPTZ NOT NULL,
    valid_to TIMESTAMPTZ,
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS silver.fact_sales (
    sale_sk BIGSERIAL PRIMARY KEY,
    event_id UUID UNIQUE NOT NULL,
    event_ts TIMESTAMPTZ NOT NULL,
    store_id INT NOT NULL,
    product_id INT NOT NULL,
    customer_id INT,
    quantity INT NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    revenue NUMERIC(14,2) NOT NULL,
    region TEXT NOT NULL,
    loaded_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS silver.fact_returns (
    return_sk BIGSERIAL PRIMARY KEY,
    return_id UUID UNIQUE NOT NULL,
    event_ts TIMESTAMPTZ NOT NULL,
    store_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    return_value NUMERIC(14,2) NOT NULL,
    region TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS silver.fact_inventory (
    inventory_date DATE NOT NULL,
    store_id INT NOT NULL,
    product_id INT NOT NULL,
    stock_units INT NOT NULL,
    PRIMARY KEY (inventory_date, store_id, product_id)
);
CREATE TABLE IF NOT EXISTS gold.daily_sales (
    sales_date DATE NOT NULL,
    region TEXT NOT NULL,
    orders BIGINT NOT NULL,
    units BIGINT NOT NULL,
    revenue NUMERIC(18,2) NOT NULL,
    avg_order_value NUMERIC(18,2) NOT NULL,
    PRIMARY KEY (sales_date, region)
);
CREATE TABLE IF NOT EXISTS gold.product_performance (
    product_id INT NOT NULL,
    category TEXT NOT NULL,
    units BIGINT NOT NULL,
    revenue NUMERIC(18,2) NOT NULL,
    return_rate NUMERIC(8,4) NOT NULL,
    PRIMARY KEY (product_id, category)
);
CREATE TABLE IF NOT EXISTS gold.regional_kpis (
    region TEXT PRIMARY KEY,
    orders BIGINT,
    units BIGINT,
    revenue NUMERIC(18,2),
    avg_order_value NUMERIC(18,2),
    return_rate NUMERIC(8,4),
    refreshed_at TIMESTAMPTZ DEFAULT NOW()
);
