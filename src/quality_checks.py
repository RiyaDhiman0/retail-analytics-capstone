import psycopg2
from config import POSTGRES
conn=psycopg2.connect(**POSTGRES); cur=conn.cursor()
checks=[
 ('fact_sales event_id not null','SELECT COUNT(*) FROM silver.fact_sales WHERE event_id IS NULL'),
 ('fact_sales positive quantity','SELECT COUNT(*) FROM silver.fact_sales WHERE quantity<=0'),
 ('fact_sales non-negative revenue','SELECT COUNT(*) FROM silver.fact_sales WHERE revenue<0'),
 ('valid regions','SELECT COUNT(*) FROM silver.fact_sales WHERE region NOT IN (\'North\',\'South\',\'East\',\'West\')'),
 ('duplicate events','SELECT COUNT(*) FROM (SELECT event_id,COUNT(*) c FROM silver.fact_sales GROUP BY event_id HAVING COUNT(*)>1) x')]
failed=0
for name,q in checks:
    cur.execute(q); bad=cur.fetchone()[0]; status='PASS' if bad==0 else 'FAIL'; print(f'{status:4} | {name:35} | bad_rows={bad}'); failed += bad>0
print('QUALITY GATE:', 'FAILED' if failed else 'PASSED')
raise SystemExit(1 if failed else 0)
