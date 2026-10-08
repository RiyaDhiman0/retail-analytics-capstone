from pathlib import Path
import psycopg2
from config import POSTGRES

root=Path(__file__).resolve().parents[1]
conn=psycopg2.connect(**POSTGRES)
conn.autocommit=True
cur=conn.cursor()
cur.execute((root/'sql/schema.sql').read_text())
print('Database schemas and tables created successfully.')
