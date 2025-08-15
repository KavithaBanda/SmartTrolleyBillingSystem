import sqlite3

conn = sqlite3.connect("items.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        barcode TEXT PRIMARY KEY,
        name TEXT,
        price REAL,
        expiry TEXT
    )
''')

# Insert some sample items (you can modify or extend)
products = [
    ("8901234567890", "Milk", 45.00, "2025-01-12"),
    ("8901234567891", "Bread", 30.00, "2025-01-10"),
    ("8901234567892", "Chips", 20.00, "2025-02-01"),
    ("8906001050490", "Colgate", 55.00, "2025-06-01"),
]

cursor.executemany("INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?)", products)
conn.commit()
conn.close()

print("items.db created with expiry column.")

