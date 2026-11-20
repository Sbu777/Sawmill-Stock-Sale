import streamlit as st
import sqlite3
import pandas as pd
import os

# Create DB if it doesn't exist (for Streamlit Cloud)
if not os.path.exists("stock.db"):
    conn_init = sqlite3.connect("stock.db")
    cur_init = conn_init.cursor()
    cur_init.execute("CREATE TABLE stock (id INTEGER PRIMARY KEY, timber_type TEXT, planks_in_stock INTEGER, price_per_plank REAL)")
    cur_init.execute("CREATE TABLE sales (id INTEGER PRIMARY KEY, customer_name TEXT, timber_type TEXT, planks_sold INTEGER, total_amount REAL, sale_date TEXT)")
    cur_init.execute("INSERT INTO stock VALUES (1,'Pine',120,45.0)")
    cur_init.execute("INSERT INTO stock VALUES (2,'Oak',35,120.0)")
    cur_init.execute("INSERT INTO stock VALUES (3,'Mahogany',80,95.0)")
    cur_init.execute("INSERT INTO stock VALUES (4,'Eucalyptus',22,60.0)")
    cur_init.execute("INSERT INTO stock VALUES (5,'Teak',60,150.0)")
    cur_init.execute("INSERT INTO sales VALUES (1,'John Dube','Pine',20,900.0,'2026-11-18')")
    cur_init.execute("INSERT INTO sales VALUES (2,'Sarah Mokoena','Oak',5,600.0,'2026-11-19')")
    cur_init.execute("INSERT INTO sales VALUES (3,'Peter Nkosi','Mahogany',10,950.0,'2026-11-19')")
    cur_init.execute("INSERT INTO sales VALUES (4,'Lerato Khumalo','Pine',50,2250.0,'2026-11-20')")
    cur_init.execute("INSERT INTO sales VALUES (5,'Sipho Zulu','Teak',15,2250.0,'2026-11-20')")
    cur_init.execute("INSERT INTO sales VALUES (6,'Naledi Botha','Eucalyptus',30,1800.0,'2026-11-20')")
    cur_init.execute("INSERT INTO sales VALUES (7,'Thabo Maseko','Pine',40,1800.0,'2026-11-20')")
    cur_init.execute("INSERT INTO sales VALUES (8,'Ayesha Patel','Mahogany',8,760.0,'2026-11-20')")
    cur_init.execute("INSERT INTO sales VALUES (9,'Kabelo Radebe','Teak',4,600.0,'2026-11-20')")
    cur_init.execute("INSERT INTO sales VALUES (10,'Zanele Dlamini','Pine',10,450.0,'2026-11-20')")
    conn_init.commit()
    conn_init.close()

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
        cur.execute("INSERT INTO sales VALUES (NULL,?,?,?,?,date('now'))", (customer, timber, planks, total))
        cur.execute("UPDATE stock SET planks_in_stock = planks_in_stock - ? WHERE timber_type = ?", (planks, timber))
        conn.commit()
        st.success(f"Sale recorded! R {total:,.2f}")
        st.rerun()
