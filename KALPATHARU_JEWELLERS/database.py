import sqlite3

connection = sqlite3.connect("jewellery.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
category TEXT,
type TEXT,
weight TEXT,
price TEXT,
image TEXT
)
""")

connection.commit()
connection.close()

print("Database created successfully!")