import streamlit as st
import sqlite3
import pandas as pd

st.title("Sawmill Stock & Sales Tracker")
st.write("Track timber stock, sales and revenue in real-time.")

conn = sqlite3.connect("stock.db")
stock_df = pd.read_sql("SELECT * FROM stock", conn)
sales_df = pd.read_sql("SELECT * FROM sales", conn)

col1, col2, col3 = st.columns(3)
col1.metric("Total Planks in Stock", int(stock_df["planks_in_stock"].sum()))
col2.metric("Total Sales", len(sales_df))
col3.metric("Total Revenue", f"R {sales_df['total_amount'].sum():,.2f}")

st.divider()

st.subheader("Low Stock Alert")
low = stock_df[stock_df["planks_in_stock"] < 50]
if len(low) > 0:
    st.warning(f"{len(low)} timber types are running LOW!")
    st.dataframe(low, use_container_width=True)
else:
    st.success("All stock levels are healthy!")

st.subheader("Current Stock")
st.dataframe(stock_df, use_container_width=True)

st.subheader("Recent Sales")
st.dataframe(sales_df, use_container_width=True)

st.divider()
st.subheader("Add New Sale")
with st.form("sale_form"):
    customer = st.text_input("Customer Name")
    timber = st.selectbox("Timber Type", stock_df["timber_type"].tolist())
    planks = st.number_input("Planks Sold", min_value=1, value=10)
    submitted = st.form_submit_button("Record Sale")
    if submitted and customer:
        price = float(stock_df[stock_df["timber_type"]==timber]["price_per_plank"].iloc[0])
        total = price * planks
        cur = conn.cursor()
        cur.execute("INSERT INTO sales VALUES (NULL,?,?,?,?,date('now'))", (customer, timber, planks, total))
        cur.execute("UPDATE stock SET planks_in_stock = planks_in_stock - ? WHERE timber_type = ?", (planks, timber))
        conn.commit()
        st.success(f"Sale recorded! R {total:,.2f}")
        st.rerun()