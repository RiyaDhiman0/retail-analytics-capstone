import sys
sys.path.insert(0, "src")

import psycopg2
from config import POSTGRES

conn = psycopg2.connect(**POSTGRES)
cur = conn.cursor()

cur.execute("""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_schema = 'gold'
    ORDER BY table_name
""")

print("Gold tables:")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()