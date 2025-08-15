import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

# --- DB Lookup Function ---
def get_product_details(barcode):
    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, expiry FROM products WHERE barcode=?", (barcode,))
    result = cursor.fetchone()
    conn.close()
    return result

# --- Barcode Handler ---
def scan_barcode(event=None):
    barcode = barcode_entry.get().strip()
    if not barcode:
        return

    product = get_product_details(barcode)
    if product:
        name, price, expiry = product
        expiry_date = datetime.datetime.strptime(expiry, "%Y-%m-%d").date()
        today = datetime.date.today()

        if expiry_date < today:
            messagebox.showwarning("Expired", f"{name} has expired on {expiry}!")
        else:
            cart.insert("", tk.END, values=(barcode, name, price, expiry))
            global total
            total += float(price)
            total_label.config(text=f"Total: ₹{total:.2f}")
    else:
        messagebox.showerror("Not Found", f"Product with barcode {barcode} not found.")

    barcode_entry.delete(0, tk.END)

# --- Remove Selected Item ---
def remove_selected_item():
    selected_item = cart.selection()
    if selected_item:
        item_values = cart.item(selected_item, 'values')
        price_to_subtract = float(item_values[2])
        cart.delete(selected_item)

        global total
        total -= price_to_subtract
        total_label.config(text=f"Total: ₹{total:.2f}")
    else:
        messagebox.showwarning("No Selection", "Please select an item to remove.")

# --- GUI Setup ---
root = tk.Tk()
root.title("Smart Trolley Prediction System")
root.geometry("650x550")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Scan or Enter Barcode", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
barcode_entry = tk.Entry(root, font=("Arial", 14), width=40)
barcode_entry.pack()
barcode_entry.bind("<Return>", scan_barcode)

add_button = tk.Button(root, text="Add Item", command=scan_barcode, bg="green", fg="white", font=("Arial", 12))
add_button.pack(pady=5)

# --- Cart Table ---1
columns = ("Barcode", "Product", "Price", "Expiry")
cart = ttk.Treeview(root, columns=columns, show="headings", height=12)
for col in columns:
    cart.heading(col, text=col)
    cart.column(col, width=150)
cart.pack(pady=20)

# --- Remove Button ---
remove_button = tk.Button(root, text="Remove Selected", command=remove_selected_item, bg="orange", font=("Arial", 12))
remove_button.pack(pady=5)

# --- Total Label ---
total = 0.0
total_label = tk.Label(root, text="Total: ₹0.00", font=("Arial", 16, "bold"), bg="#f0f0f0")
total_label.pack(pady=10)

# --- Run App ---
root.mainloop()
