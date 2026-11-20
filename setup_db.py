import sqlite3

conn = sqlite3.connect("stock.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS stock")
cur.execute("DROP TABLE IF EXISTS sales")

cur.execute("""
CREATE TABLE stock (
    id INTEGER PRIMARY KEY,
    timber_type TEXT,
    planks_in_stock INTEGER,
    price_per_plank REAL
)
""")

cur.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    customer TEXT,
    timber_type TEXT,
    planks_sold INTEGER,
    total_amount REAL,
    sale_date TEXT
)
""")

stock_data = [
    ("Pine", 120, 85.00),
    ("Eucalyptus", 45, 120.00),
    ("Oak", 18, 250.00),
    ("Meranti", 65, 180.00),
    ("Saligna", 90, 95.00),
]
cur.executemany("INSERT INTO stock VALUES (NULL,?,?,?)", stock_data)

sales_data = [
    ("Builders Warehouse", "Pine", 40, 3400.00, "2026-11-18"),
    ("Mkhonto Timber", "Eucalyptus", 20, 2400.00, "2026-11-19"),
    ("Local Furniture", "Oak", 10, 2500.00, "2026-11-19"),
    ("Builders Warehouse", "Saligna", 30, 2850.00, "2026-11-20"),
]
cur.executemany("INSERT INTO sales VALUES (NULL,?,?,?,?,?)", sales_data)

conn.commit()
conn.close()
print("Stock DB Created!")