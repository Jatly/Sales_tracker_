import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar  # For date selection

# Database setup
conn = sqlite3.connect("sales_tracker.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    sales_amount REAL,
    cost REAL,
    profit_loss REAL
)
""")
conn.commit()

# Functions
def add_sale():
    try:
        date = date_entry.get()
        if not date:
            raise ValueError("Please select a valid date.")

        sales_amount = float(sales_entry.get())
        cost = float(cost_entry.get())
        profit_loss = sales_amount - cost

        cursor.execute("INSERT INTO sales (date, sales_amount, cost, profit_loss) VALUES (?, ?, ?, ?)",
                       (date, sales_amount, cost, profit_loss))
        conn.commit()
        messagebox.showinfo("Success", "Sale added successfully!")
        clear_entries()
        fetch_data()
        calculate_totals()
    except ValueError as ve:
        messagebox.showerror("Error", f"Input Error: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add sale: {e}")

def edit_sale():
    try:
        selected_item = tree.selection()
        if not selected_item:
            raise ValueError("No sale selected. Please select a sale to edit.")

        item_values = tree.item(selected_item, "values")
        sale_id = item_values[0]

        date = date_entry.get()
        if not date:
            raise ValueError("Please select a valid date.")

        sales_amount = float(sales_entry.get())
        cost = float(cost_entry.get())
        profit_loss = sales_amount - cost

        cursor.execute("""
            UPDATE sales
            SET date = ?, sales_amount = ?, cost = ?, profit_loss = ?
            WHERE id = ?
        """, (date, sales_amount, cost, profit_loss, sale_id))
        conn.commit()
        messagebox.showinfo("Success", "Sale updated successfully!")
        clear_entries()
        fetch_data()
        calculate_totals()
    except ValueError as ve:
        messagebox.showerror("Error", f"Input Error: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to edit sale: {e}")

def populate_entries(event):
    selected_item = tree.selection()
    if not selected_item:
        return

    item_values = tree.item(selected_item, "values")
    date_entry.delete(0, END)
    date_entry.insert(0, item_values[1])
    sales_entry.delete(0, END)
    sales_entry.insert(0, item_values[2])
    cost_entry.delete(0, END)
    cost_entry.insert(0, item_values[3])

def clear_entries():
    sales_entry.delete(0, END)
    cost_entry.delete(0, END)
    date_entry.delete(0, END)

def fetch_data(filter_by=None, profit_filter=None):
    tree.delete(*tree.get_children())

    query = "SELECT * FROM sales"
    params = []

    if filter_by:
        query += f" WHERE strftime('%Y', date) = ?" if len(filter_by) == 4 else f" WHERE strftime('%m', date) = ?"
        params.append(filter_by)

    if profit_filter == "Profit":
        query += " AND profit_loss > 0" if filter_by else " WHERE profit_loss > 0"
    elif profit_filter == "Loss":
        query += " AND profit_loss <= 0" if filter_by else " WHERE profit_loss <= 0"
    

    cursor.execute(query, params)
    rows = cursor.fetchall()
    for row in rows:
        profit_loss_type = "Profit" if row[4] > 0 else "Loss"
        tree.insert("", END, values=(row[0], row[1], row[2], row[3], row[4], profit_loss_type))

def calculate_totals():
    cursor.execute("SELECT SUM(sales_amount), SUM(cost), SUM(profit_loss) FROM sales")
    totals = cursor.fetchone()

    total_sales = totals[0] if totals[0] is not None else 0
    total_cost = totals[1] if totals[1] is not None else 0
    total_profit_loss = totals[2] if totals[2] is not None else 0

    profit_percent = (total_profit_loss / total_cost) * 100 if total_cost != 0 else 0
    overall_status = "Profit" if total_profit_loss > 0 else "Loss" if total_profit_loss < 0 else "Break-Even"

    totals_label.config(text=f"Total Sales: ₹{total_sales:.2f} | Total Cost: ₹{total_cost:.2f} | "
                             f"Profit/Loss: ₹{total_profit_loss:.2f} ({profit_percent:.2f}%) | Overall: {overall_status}")

def filter_data():
    filter_value = filter_entry.get()
    if filter_value.isdigit() and len(filter_value) == 4:  # Year filter
        fetch_data(filter_by=filter_value)
    elif filter_value.isdigit() and len(filter_value) == 2:  # Month filter
        fetch_data(filter_by=filter_value)
    else:
        messagebox.showerror("Error", "Enter a valid year (YYYY) or month (MM)")

def reset_filter():
    fetch_data()  # Fetch all data
    filter_entry.delete(0, END)

def filter_profit_loss(profit_type):
    fetch_data(profit_filter=profit_type)

# GUI Setup
root = Tk()
root.title("Sales Tracker")
root.geometry("750x650")
root.configure(bg="#f5f5f5")

# Title Label
title_label = Label(root, text="Sales Tracker Application", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333")
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# Input Fields
input_frame = Frame(root, bg="#f5f5f5")
input_frame.grid(row=1, column=0, columnspan=4, pady=10, sticky=W+E)

Label(input_frame, text="Date:", bg="#f5f5f5", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky=W)
date_entry = Entry(input_frame, width=15, font=("Arial", 12))
date_entry.grid(row=0, column=1, padx=10, pady=5)

Label(input_frame, text="Sales Amount (₹):", bg="#f5f5f5", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky=W)
sales_entry = Entry(input_frame, font=("Arial", 12))
sales_entry.grid(row=1, column=1, padx=10, pady=5)

Label(input_frame, text="Cost (₹):", bg="#f5f5f5", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky=W)
cost_entry = Entry(input_frame, font=("Arial", 12))
cost_entry.grid(row=2, column=1, padx=10, pady=5)

add_button = Button(input_frame, text="Add Sale", command=add_sale, font=("Arial", 12), bg="#4CAF50", fg="white", width=12)
add_button.grid(row=3, column=0, padx=10, pady=10)

edit_button = Button(input_frame, text="Edit Sale", command=edit_sale, font=("Arial", 12), bg="#2196F3", fg="white", width=12)
edit_button.grid(row=3, column=1, padx=10, pady=10)

# Filter Section
filter_frame = Frame(root, bg="#f5f5f5")
filter_frame.grid(row=2, column=0, columnspan=4, pady=10, sticky=W+E)

Label(filter_frame, text="Filter (Year YYYY / Month MM):", bg="#f5f5f5", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky=W)
filter_entry = Entry(filter_frame, font=("Arial", 12))
filter_entry.grid(row=0, column=1, padx=10, pady=5)

filter_button = Button(filter_frame, text="Apply Filter", command=filter_data, font=("Arial", 12), bg="#ff9800", fg="white", width=12)
filter_button.grid(row=0, column=2, padx=10, pady=5)

reset_button = Button(filter_frame, text="Reset Filter", command=reset_filter, font=("Arial", 12), bg="#607D8B", fg="white", width=12)
reset_button.grid(row=0, column=3, padx=10, pady=5)

profit_filter_button = Button(filter_frame, text="Filter Profit", command=lambda: filter_profit_loss("Profit"), font=("Arial", 12), bg="#8BC34A", fg="white", width=12)
profit_filter_button.grid(row=1, column=0, padx=10, pady=5)

loss_filter_button = Button(filter_frame, text="Filter Loss", command=lambda: filter_profit_loss("Loss"), font=("Arial", 12), bg="#F44336", fg="white", width=12)
loss_filter_button.grid(row=1, column=1, padx=10, pady=5)

reset_profit_loss_button = Button(filter_frame, text="Show All", command=lambda: filter_profit_loss(None), font=("Arial", 12), bg="#9E9E9E", fg="white", width=12)
reset_profit_loss_button.grid(row=1, column=2, padx=10, pady=5)

# Data Table
data_frame = Frame(root, bg="#f5f5f5")
data_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky=W+E)

columns = ("ID", "Date", "Sales Amount", "Cost", "Profit/Loss", "Type")
tree = ttk.Treeview(data_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill=BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", populate_entries)

# Totals
status_frame = Frame(root, bg="#f5f5f5")
status_frame.grid(row=4, column=0,columnspan=4, pady=10, sticky=W+E)

totals_label = Label(status_frame, text="Total Sales: ₹0.00 | Total Cost: ₹0.00 | Profit/Loss: ₹0.00 (0.00%) | Overall: Break-Even", 
                     font=("Arial", 12), bg="#f5f5f5", fg="#333")
totals_label.pack(fill=BOTH, expand=True, padx=10, pady=5)

# Fetch and display initial data
fetch_data()
calculate_totals()

# Run the GUI application
root.mainloop()

# Close the database connection when the application exits
conn.close()

