
import tkinter as tk
import sqlite3
from tkinter import *
import products.py
from tkinter import messagebox

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
root.geometry('700x400')
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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class OrdersList(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create the Listbox to display the orders
        self.orders_list = tk.Listbox(self)
        self.orders_list.grid(row=0, column=0, padx=5, pady=5)
        self.orders_list.configure(height=15, width=20)

        # Populate the Listbox with the existing orders
        cursor.execute('''
            SELECT products.name, orders.quantity, orders.total_price 
            FROM orders 
            INNER JOIN products ON products.id = orders.product_id
        ''')
        for row in cursor:
            self.orders_list.insert(tk.END, row[0] + ' x ' + str(row[1]) + ' = $' + str(row[2]))



# Create the OrderForm and OrdersList frames and add them to the main window

form = OrderForm(root)
form.pack()
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