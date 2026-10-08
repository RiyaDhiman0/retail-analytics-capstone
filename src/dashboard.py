import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import subprocess
import sys

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Retail Analytics Platform",
    page_icon="🛒",
    layout="wide"
)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🛒 Real-Time Retail Analytics Platform")
st.caption(
    "Self-serve BI demo — Bronze → Silver → Gold analytical view"
)

# ---------------------------------------------------------
# DATABASE PATH
# ---------------------------------------------------------

project_root = Path(__file__).resolve().parents[1]
db = project_root / "data" / "local_demo.db"

# ---------------------------------------------------------
# CREATE DEMO DATABASE IF IT DOES NOT EXIST
# ---------------------------------------------------------

if not db.exists():

    st.info("Preparing demo data...")

    demo_script = Path(__file__).resolve().parent / "local_demo.py"

    result = subprocess.run(
        [sys.executable, str(demo_script)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        st.error("Unable to create the demo database.")
        st.code(result.stderr)
        st.stop()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

try:

    conn = sqlite3.connect(db)

    df = pd.read_sql_query(
        "SELECT * FROM fact_sales",
        conn
    )

    conn.close()

except Exception as e:

    st.error("Unable to load sales data.")
    st.exception(e)
    st.stop()

# ---------------------------------------------------------
# DATA PREPARATION
# ---------------------------------------------------------

df["event_ts"] = pd.to_datetime(df["event_ts"])

df["date"] = df["event_ts"].dt.date

# Make sure region values are clean
valid_regions = [
    "North",
    "South",
    "East",
    "West"
]

df = df[df["region"].isin(valid_regions)].copy()

# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.subheader("Key Performance Indicators")

total_revenue = df["revenue"].sum()
total_orders = len(df)
total_units = df["quantity"].sum()

if total_orders > 0:
    average_order_value = total_revenue / total_orders
else:
    average_order_value = 0

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Revenue",
    f"₹{total_revenue:,.0f}"
)

c2.metric(
    "Orders",
    f"{total_orders:,}"
)

c3.metric(
    "Units",
    f"{total_units:,}"
)

c4.metric(
    "AOV",
    f"₹{average_order_value:,.0f}"
)

# ---------------------------------------------------------
# REGIONAL COMPARISON
# ---------------------------------------------------------

st.subheader("Regional comparison")

regional = (
    df.groupby("region")
    .agg(
        orders=("event_id", "count"),
        units=("quantity", "sum"),
        revenue=("revenue", "sum")
    )
    .reset_index()
)

# Sort regions consistently
region_order = ["North", "South", "East", "West"]

regional["region"] = pd.Categorical(
    regional["region"],
    categories=region_order,
    ordered=True
)

regional = regional.sort_values("region")

# Display a normal Streamlit table
st.table(regional)

# Regional revenue chart
st.subheader("Revenue by region")

regional_chart = regional.copy()

regional_chart["region"] = regional_chart["region"].astype(str)

st.bar_chart(
    regional_chart.set_index("region")["revenue"]
)

# ---------------------------------------------------------
# DAILY SALES TREND
# ---------------------------------------------------------

st.subheader("Daily sales trend")

daily = (
    df.groupby("date")["revenue"]
    .sum()
    .sort_index()
)

st.line_chart(daily)

# ---------------------------------------------------------
# TOP PRODUCTS
# ---------------------------------------------------------

st.subheader("Top products")

top_products = (
    df.groupby("product_id")
    .agg(
        units=("quantity", "sum"),
        revenue=("revenue", "sum")
    )
    .reset_index()
    .sort_values(
        "revenue",
        ascending=False
    )
    .head(10)
)

st.table(top_products)

# ---------------------------------------------------------
# DATA QUALITY SUMMARY
# ---------------------------------------------------------

st.subheader("Data quality summary")

q1, q2, q3 = st.columns(3)

q1.metric(
    "Valid regions",
    df["region"].nunique()
)

q2.metric(
    "Rows loaded",
    f"{len(df):,}"
)

q3.metric(
    "Missing values",
    f"{df.isna().sum().sum():,}"
)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Retail Analytics Capstone • Synthetic demonstration dataset • "
    "Bronze → Silver → Gold analytical architecture"
)