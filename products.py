import sqlite3

# Connect to the database
conn = sqlite3.connect('coffee_shop.db')

# Create a cursor
cursor = conn.cursor()

# Create the products table if it doesn't exist
cursor.execute('''
    SELECT name FROM sqlite_master WHERE type='table' AND name='products'
''')
if cursor.fetchone() is None:
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')

# Insert some sample products
cursor.execute ('''
    INSERT INTO products (name, price) VALUES
    ('Coffee', 3.00),
    ('Tea', 2.50),
    ('Hot Chocolate', 3.00),
    ('Americano', 2.50),
    ('Iced Coffee', 3.00),
    ('Cappuccino', 4.00),
    ('Latte', 4.00),
    ('Croissant', 3.50),
    ('Muffin', 2.75),
    ('Scone', 2.00),
    ('Coffee Cake', 3.50),
    ('Cheesecake', 4.50),
    ('All Bagels', 2.00),
    ('Club Sandwich', 10.00),
    ('Veggie Sandwich', 6.50);
''')

# Save changes
conn.commit()

# Close the connection
conn.close()