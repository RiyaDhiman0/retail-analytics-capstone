import argparse, json
from kafka import KafkaConsumer
import psycopg2
from config import KAFKA, POSTGRES

TOPICS=[f'sales-{r}' for r in ['north','south','east','west']]
SQL='''INSERT INTO raw.sales_events(event_id,event_ts,store_id,region,product_id,customer_id,quantity,unit_price,payment_method,payload)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb) ON CONFLICT(event_id) DO NOTHING'''

def valid(e):
    required=['event_id','event_ts','store_id','region','product_id','quantity','unit_price']
    return all(k in e for k in required) and e['quantity']>0 and e['unit_price']>=0 and e['region'] in ['North','South','East','West']

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--max-events',type=int,default=1000); a=p.parse_args()
    conn=psycopg2.connect(**POSTGRES); conn.autocommit=True
    cur=conn.cursor()
    c=KafkaConsumer(*TOPICS,bootstrap_servers=KAFKA,group_id='retail-analytics-consumer',auto_offset_reset='earliest',enable_auto_commit=False)
    n=0
    for msg in c:
        try:
            e=json.loads(msg.value)
            if not valid(e): raise ValueError('schema/business validation failed')
            cur.execute(SQL,(e['event_id'],e['event_ts'],e['store_id'],e['region'],e['product_id'],e.get('customer_id'),e['quantity'],e['unit_price'],e.get('payment_method'),json.dumps(e)))
        except Exception as ex:
            cur.execute('INSERT INTO raw.dead_letter_events(raw_payload,error_reason) VALUES (%s::jsonb,%s)',(json.dumps(msg.value.decode(errors='replace')),str(ex)))
        n+=1; c.commit();
        if n%100==0: print(f'Consumed {n} events')
        if n>=a.max_events: break
    c.commit(); c.close(); conn.close(); print('Consumer completed.')
