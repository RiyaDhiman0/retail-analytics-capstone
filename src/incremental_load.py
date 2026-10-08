"""Watermark-based incremental loader demonstration."""
import psycopg2
from config import POSTGRES
conn=psycopg2.connect(**POSTGRES); conn.autocommit=True; cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS raw.pipeline_watermark (pipeline_name text primary key, last_event_ts timestamptz)")
cur.execute("SELECT last_event_ts FROM raw.pipeline_watermark WHERE pipeline_name='sales'")
row=cur.fetchone(); watermark=row[0] if row else '1970-01-01'
cur.execute("SELECT COALESCE(MAX(event_ts),'1970-01-01') FROM raw.sales_events WHERE event_ts>%s",(watermark,))
new_watermark=cur.fetchone()[0]
cur.execute("INSERT INTO raw.pipeline_watermark VALUES ('sales',%s) ON CONFLICT(pipeline_name) DO UPDATE SET last_event_ts=EXCLUDED.last_event_ts",(new_watermark,))
print('Previous watermark:',watermark); print('New watermark:',new_watermark)
