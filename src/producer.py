import argparse, json, random, time, uuid
from datetime import datetime, timezone
from kafka import KafkaProducer
from config import KAFKA

REGIONS=['North','South','East','West']
def make_event():
    region=random.choice(REGIONS)
    return {
      'event_id':str(uuid.uuid4()), 'event_ts':datetime.now(timezone.utc).isoformat(),
      'store_id':random.randint(1,20), 'region':region, 'product_id':random.randint(1,100),
      'customer_id':random.randint(1,1000), 'quantity':random.randint(1,5),
      'unit_price':round(random.uniform(50,5000),2),
      'payment_method':random.choice(['UPI','CARD','CASH','WALLET'])
    }

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--events',type=int,default=1000); p.add_argument('--interval',type=float,default=0.072)
    a=p.parse_args()
    producer=KafkaProducer(bootstrap_servers=KAFKA, value_serializer=lambda x: json.dumps(x).encode())
    for i in range(a.events):
        e=make_event(); topic=f"sales-{e['region'].lower()}"
        producer.send(topic,key=e['event_id'].encode(),value=e)
        if (i+1)%100==0: producer.flush(); print(f'Sent {i+1}/{a.events} events')
        time.sleep(a.interval)
    producer.flush(); producer.close(); print('Producer completed.')
