from pathlib import Path
import psycopg2
from config import POSTGRES
root=Path(__file__).resolve().parents[1]
conn=psycopg2.connect(**POSTGRES); conn.autocommit=True; cur=conn.cursor()
for name in ['01_bronze.sql','02_silver.sql','03_gold.sql']:
    cur.execute((root/'sql'/name).read_text())
print('Bronze → Silver → Gold transformation completed.')
