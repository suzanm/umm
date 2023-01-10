import tkinter
import sqlite3
import tkinter as tk



# Connect to the database
conn = sqlite3.connect('coffee_shop.db')

# Create a cursor
cursor = conn.cursor()

# Checks if the products table exists
cursor.execute('''
    SELECT name FROM sqlite_master WHERE type='table' AND name='products'
''')

# If the table does not exist, creates it
if not cursor.fetchone():
  cursor.execute('''
      CREATE TABLE products (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          price REAL NOT NULL
      )
  ''')

# Inserts some products
cursor.execute('''
    INSERT INTO products (name, price) VALUES
    ('Coffee', 3.50),
    ('Tea', 2.50),
    ('Hot Chocolate', 3.00)
''')

root = tk.Tk()

# Checks if the orders table exists
cursor.execute('''
    SELECT name FROM sqlite_master WHERE type='table' AND name='orders'
''')

#Table with orders
if not cursor.fetchone():
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

# Orders
cursor.execute('''
    INSERT INTO orders (product_id, quantity, total_price) VALUES
    (1, 2, 7.00),
    (2, 3, 7.50),
    (3, 1, 3.00)
''')

  
class OrderForm(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a Listbox for selecting the product
        self.product_list = tk.Listbox(self)

        # Populate the Listbox with the available products
        cursor.execute('''
            SELECT name FROM products  
        ''')
        for row in cursor:
            self.product_list.insert(tk.END, row[0])

        # Create a widget for entering the quantity
        self.quantity_label = tk.Label(self, text="Quantity")
        self.quantity_entry = tk.Entry(self)

        # Create a button to submit the order
        self.submit_button = tk.Button(self, text="Submit", command=self.place_order)

        # Lay out the widgets in a grid
        self.product_list.grid(row=0, column=0)
        self.quantity_label.grid(row=1, column=0)
        self.quantity_entry.grid(row=1, column=1)
        self.submit_button.grid(row=2, column=0, columnspan=2)

    def place_order(self):
      # Get the selected product and quantity from the form
      product = self.product_list.get(self.product_list.curselection())
      quantity = int(self.quantity_entry.get())
  
      # Retrive product id
      cursor.execute('''
          SELECT id, price FROM products WHERE name=?
      ''', (product,))
      product_id, price = cursor.fetchone()

      # Total Price
      total_price = quantity * price

      # Add order to database
      cursor.execute('''
        INSERT INTO orders (product_id, quantity, total_price) VALUES (?, ?, ?)
      ''', (product_id, quantity, total_price))
      conn.commit()


if not hasattr(root, 'form'): root.form = OrderForm(root)
form = OrderForm(root)
form.pack()
root.mainloop()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Commit changes
conn.commit()

# Select all products
cursor.execute('''
    SELECT * FROM products
''')

# Print the products
print('PRODUCTS:')
print('----------')
products = cursor.fetchall()
for row in products:
    print(f'ID: {row[0]} | Name: {row[1]} | Price: ${row[2]:.2f}')

# Create a new cursor for the orders
cursor = conn.cursor()

# Select all orders
cursor.execute('''
    SELECT * FROM orders
''')

# Print the orders
print('\nORDERS:')
print('----------')
orders = cursor.fetchall()
for row in orders:
    print(f'ID: {row[0]} | Product ID: {row[1]} | Quantity: {row[2]} | Total Price: ${row[3]:.2f}')

  
# Close the connection
conn.close()
