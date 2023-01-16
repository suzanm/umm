import tkinter as tk
import sqlite3
from tkinter import *
import products
from tkinter import messagebox

#ummm i'll add a header when i feel like it
#and i'll also make the cover page and a product description  eventually so ya
#still working on stopping the repeating part for the products but its a pain...
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Connect to the database
conn = sqlite3.connect('coffee_shop.db')

# Create a cursor
cursor = conn.cursor()

def initialize_database():
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='orders'
    ''')
    if cursor.fetchone() is None:
        cursor.execute('''
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
    conn.commit()

initialize_database()

root = tk.Tk()


class OrderForm(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args,**kwargs)

        # Product list
        self.product_list = tk.Listbox(self)
        cursor.execute('''
            SELECT name FROM products
        ''')
        for row in cursor:
            self.product_list.insert(tk.END, row[0])
        self.product_list.grid(row=0, column=0, padx=5, pady=5)
        self.product_list.configure(height=15, width=20)

        # Quantity entry
        self.quantity_label = tk.Label(self, text="Quantity")
        self.quantity_entry = tk.Entry(self)

        # Create a button to submit the order
        self.submit = tk.Button(self, text="Submit", command=self.place_order)

        # Lay out the widgets in a grid
        self.product_list.grid(row=0, column=0)
        self.quantity_label.grid(row=5, column=1)
        self.quantity_entry.grid(row=5, column=2)
        self.submit.grid(row=5, column=3, columnspan=2)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def place_order(self):
        # Check if a product is selected
        if self.product_list.curselection():
            product = self.product_list.get(self.product_list.curselection())
        else:
            # Inform the user that no product is selected
            messagebox.showerror("Error", "No product selected.")
            return
        # Check if the quantity is valid
        try:
            quantity = int(self.quantity_entry.get())
        except ValueError:
            # Inform the user that the entered value is not valid
            messagebox.showerror("Error", "Invalid Quantity.")
            return
        # Retrieve the product_id and price for the given product
        cursor.execute('''
            SELECT id, price FROM products WHERE name=?
        ''', (product,))
        product_id, price = cursor.fetchone()

        # Calculate the total price for the order
        total_price = quantity * price

        # Add the order to the database
        cursor.execute(''' 
            INSERT INTO orders (product_id, quantity, total_price) VALUES (?, ?, ?)
        ''', (product_id, quantity, total_price))
        conn.commit()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class OrdersList(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create the Listbox to display the orders
        self.orders_list = tk.Listbox(self)
        self.orders_list.grid(row=0, column=0, padx=5, pady=5)
        self.load_orders()

        # Create the delete button
        self.delete_button = tk.Button(self, text="Delete Order", command=self.delete_order)
        self.delete_button.grid(row=1, column=0, pady=5)

    def load_orders(self):
        # Clear the Listbox
        self.orders_list.delete(0, tk.END)

        # Retrieve all the orders from the database
        cursor.execute('''
            SELECT name, quantity, total_price FROM orders
            JOIN products ON orders.product_id = products.id
        ''')

        # Insert the orders into the Listbox
        for row in cursor:
            self.orders_list.insert(tk.END, row)

    def delete_order(self):
        # Check if an order is selected
        if self.orders_list.curselection():
            # Retrieve the selected order's id
            selected_order = self.orders_list.get(self.orders_list.curselection())
            order_id = selected_order[0]

            # Delete the order from the database
            cursor.execute('''
                DELETE FROM orders WHERE id=?
            ''', (order_id,))
            conn.commit()

            # Reload the orders list
            self.load_orders()
        else:
            # Inform the user that no order is selected
            messagebox.showerror("Error", "No order selected.")

#-------------------------------------------------------------------------
      
    def update_list(self):
        self.populate_list()
        self.after(1000, self.update_list)

#-------------------------------------------------------------------------
      
# Create the Order Form and Orders List frames
order_form = OrderForm(root)
order_form.grid(row=0, column=0, padx=5, pady=5)

order_list = OrdersList(root)
order_list.grid(row=0, column=1, padx=5, pady=5)

root.mainloop()

#-------------------------------------------------------------------------

# Create the OrderForm and OrdersList frames and add them to the main window

form = OrderForm(root)
form.pack()
root.mainloop()

orders_list = OrdersList(root)
form = OrderForm(root, orders_list)
orders_list.grid(row=0, column=1)
form.grid(row=0, column=0)
root.mainloop()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
order_form = OrderForm(frame1)
orders_list = OrdersList(frame2)
frame1.grid(row=0, column=0, padx=5, pady=5)
frame2.grid(row=0, column=1, padx=5, pady=5)
order_form.grid(row=0, column=0)
orders_list.grid(row=0, column=0)
root.mainloop()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Close the database connection
conn.close()
  
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

root.title("Coffee Shop Order Form")

# Main Frame
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True)

# Create the OrderForm and OrdersList frames as children of the main frame
order_form = OrderForm(main_frame)
orders_list = OrdersList(main_frame)

# Pack the OrderForm and OrdersList frames side by side
order_form.pack(side='left', fill='both', expand=True)
orders_list.pack(side='right', fill='both', expand=True)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------