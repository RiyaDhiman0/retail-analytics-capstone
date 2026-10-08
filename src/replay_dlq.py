import json, psycopg2
from config import POSTGRES
conn=psycopg2.connect(**POSTGRES); conn.autocommit=True; cur=conn.cursor()
cur.execute("SELECT dlq_id, raw_payload FROM raw.dead_letter_events WHERE replayed=false ORDER BY dlq_id")
rows=cur.fetchall(); replayed=0
for dlq_id,payload in rows:
    try:
        e=json.loads(payload) if isinstance(payload,str) else payload
        if isinstance(e,str): e=json.loads(e)
        cur.execute("INSERT INTO raw.sales_events(event_id,event_ts,store_id,region,product_id,customer_id,quantity,unit_price,payment_method,payload) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb) ON CONFLICT DO NOTHING",(e['event_id'],e['event_ts'],e['store_id'],e['region'],e['product_id'],e.get('customer_id'),e['quantity'],e['unit_price'],e.get('payment_method'),json.dumps(e)))
        cur.execute('UPDATE raw.dead_letter_events SET replayed=true WHERE dlq_id=%s',(dlq_id,)); replayed+=1
    except Exception: pass
print('Replayed',replayed,'events')
