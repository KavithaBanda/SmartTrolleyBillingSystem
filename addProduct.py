import tkinter as tk
from tkinter import messagebox
import sqlite3

def focus_name(event):
    name_entry.focus_set()

def add_product():
    barcode = barcode_entry.get().strip()
    name = name_entry.get().strip()
    price = price_entry.get().strip()
    expiry = expiry_entry.get().strip()

    if not barcode or not name or not price or not expiry:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    try:
        conn = sqlite3.connect("items.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO products (barcode, name, price, expiry) VALUES (?, ?, ?, ?)",
                       (barcode, name, float(price), expiry))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Product '{name}' added successfully!")

        # Clear fields and focus back to barcode
        barcode_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        expiry_entry.delete(0, tk.END)
        barcode_entry.focus_set()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# --- GUI Layout ---
root = tk.Tk()
root.title("Add Product")
root.geometry("350x300")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Scan/Enter Barcode", bg="#f0f0f0").pack()
barcode_entry = tk.Entry(root, width=30)
barcode_entry.pack()
barcode_entry.focus_set()
barcode_entry.bind("<Return>", focus_name)  # When Enter is pressed, go to name

tk.Label(root, text="Product Name", bg="#f0f0f0").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack()

tk.Label(root, text="Price (in ₹)", bg="#f0f0f0").pack()
price_entry = tk.Entry(root, width=30)
price_entry.pack()

tk.Label(root, text="Expiry Date (YYYY-MM-DD)", bg="#f0f0f0").pack()
expiry_entry = tk.Entry(root, width=30)
expiry_entry.pack()

tk.Button(root, text="Add Product", command=add_product, bg="blue", fg="white").pack(pady=15)

root.mainloop()
