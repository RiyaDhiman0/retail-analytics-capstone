DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'bronze_sales_events_event_id_unique'
    ) THEN
        ALTER TABLE bronze.sales_events
        ADD CONSTRAINT bronze_sales_events_event_id_unique UNIQUE (event_id);
    END IF;
END $$;

INSERT INTO bronze.sales_events
SELECT r.* FROM raw.sales_events r
ON CONFLICT (event_id) DO NOTHING;