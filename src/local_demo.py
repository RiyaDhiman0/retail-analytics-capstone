"""No-Docker demo: creates synthetic data in SQLite for a quick dashboard."""
from pathlib import Path
import sqlite3, random, uuid
from datetime import datetime, timedelta
import pandas as pd
root=Path(__file__).resolve().parents[1]
db=root/'data/local_demo.db'
conn=sqlite3.connect(db)
rows=[]; start=datetime.now()-timedelta(days=7)
regions=['North','South','East','West']
for i in range(5000):
    ts=start+timedelta(seconds=random.randint(0,7*86400))
    rows.append([str(uuid.uuid4()),ts.isoformat(),random.randint(1,20),random.choice(regions),random.randint(1,100),random.randint(1,5),round(random.uniform(50,5000),2)])
df=pd.DataFrame(rows,columns=['event_id','event_ts','store_id','region','product_id','quantity','unit_price'])
df['revenue']=df.quantity*df.unit_price
df.to_sql('fact_sales',conn,if_exists='replace',index=False)
print(f'Created {len(df):,} synthetic sales events at {db}')
