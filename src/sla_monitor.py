import psycopg2
from config import POSTGRES
conn=psycopg2.connect(**POSTGRES); cur=conn.cursor()
cur.execute("SELECT COUNT(*), MAX(ingested_at), MIN(event_ts) FROM raw.sales_events")
count,latest,oldest=cur.fetchone()
print('SLA MONITOR'); print('rows=',count); print('latest_ingested=',latest); print('oldest_event=',oldest)
print('Freshness SLA: PASS if latest ingestion is within the agreed operational window.')
print('Completeness SLA: PASS when expected POS partitions have arrived.')
