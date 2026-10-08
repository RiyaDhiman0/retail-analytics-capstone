import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

st.set_page_config(page_title='Retail Analytics Platform',layout='wide')
st.title('🛒 Real-Time Retail Analytics Platform')
st.caption('Self-serve BI demo — Bronze → Silver → Gold analytical view')

db=Path(__file__).resolve().parents[1]/'data/local_demo.db'
if not db.exists():
    st.warning('Run: python src/local_demo.py first.')
    st.stop()
conn=sqlite3.connect(db); df=pd.read_sql_query('SELECT * FROM fact_sales',conn); conn.close()
df['event_ts']=pd.to_datetime(df.event_ts); df['date']=df.event_ts.dt.date

c1,c2,c3,c4=st.columns(4)
c1.metric('Revenue',f'₹{df.revenue.sum():,.0f}')
c2.metric('Orders',f'{len(df):,}')
c3.metric('Units',f'{df.quantity.sum():,}')
c4.metric('AOV',f'₹{df.revenue.sum()/len(df):,.0f}')

st.subheader('Regional comparison')
regional=df.groupby('region',as_index=False).agg(orders=('event_id','count'),units=('quantity','sum'),revenue=('revenue','sum'))
st.dataframe(regional,use_container_width=True)
st.bar_chart(regional.set_index('region')['revenue'])

st.subheader('Daily sales trend')
daily=df.groupby('date',as_index=False)['revenue'].sum().set_index('date')
st.line_chart(daily)

st.subheader('Top products')
top=df.groupby('product_id',as_index=False).agg(units=('quantity','sum'),revenue=('revenue','sum')).sort_values('revenue',ascending=False).head(10)
st.dataframe(top,use_container_width=True)
