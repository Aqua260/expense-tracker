import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Global variable for file path
current_file = None

# Function to load existing CSV file
def load_csv():
    global current_file
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not file_path:
        return
    try:
        df = pd.read_csv(file_path)
        current_file = file_path
        messagebox.showinfo("Success", f"Loaded file:\n{os.path.basename(file_path)}")
        result_text.set("✅ File loaded successfully! You can now view summary or charts.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load file:\n{str(e)}")

# Function to add new expense
def add_expense():
    global current_file
    if not current_file:
        messagebox.showwarning("No File", "Please load or create a CSV file first!")
        return

    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()

    if not (date and category and amount):
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    try:
        amount = float(amount)
        df = pd.read_csv(current_file)
        df.loc[len(df)] = [date, category, amount]
        df.to_csv(current_file, index=False)
        messagebox.showinfo("Success", "Expense added successfully!")
        clear_fields()
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")

# Clear input fields
def clear_fields():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# Show summary
def show_summary():
    global current_file
    if not current_file:
        messagebox.showwarning("No File", "Please load a CSV file first!")
        return

    df = pd.read_csv(current_file)
    if df.empty:
        messagebox.showinfo("Info", "No expenses recorded yet!")
        return
    
    total = np.sum(df["Amount"])
    avg = np.mean(df["Amount"])
    max_expense = np.max(df["Amount"])
    
    result_text.set(f"Total Spent: ₹{total:.2f}\n"
                    f"Average Spending: ₹{avg:.2f}\n"
                    f"Highest Expense: ₹{max_expense:.2f}")

# Show pie chart
def show_chart():
    global current_file
    if not current_file:
        messagebox.showwarning("No File", "Please load a CSV file first!")
        return

    df = pd.read_csv(current_file)
    if df.empty:
        messagebox.showinfo("Info", "No data to show chart!")
        return
    
    category_sum = df.groupby("Category")["Amount"].sum()
    plt.figure(figsize=(6,6))
    plt.pie(category_sum, labels=category_sum.index, autopct="%1.1f%%", startangle=140)
    plt.title("Spending by Category")
    plt.show()

# Create new empty file
def create_new_file():
    global current_file
    file_path = filedialog.asksaveasfilename(
        title="Create New Expense File",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not file_path:
        return

    df = pd.DataFrame(columns=["Date", "Category", "Amount"])
    df.to_csv(file_path, index=False)
    current_file = file_path
    messagebox.showinfo("File Created", f"New file created:\n{os.path.basename(file_path)}")
    result_text.set("🆕 New file created! You can now add expenses.")

# GUI setup
root = tk.Tk()
root.title("Expense Tracker & Analyzer")
root.geometry("550x550")

title_label = tk.Label(root, text="💰 Personal Expense Tracker", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Buttons for file management
tk.Button(root, text="📂 Load CSV File", command=load_csv, bg="lightblue", width=20).pack(pady=5)
tk.Button(root, text="🆕 Create New File", command=create_new_file, bg="lightgreen", width=20).pack(pady=5)

# Input section
tk.Label(root, text="Date (YYYY-MM-DD):", font=("Arial", 12)).pack()
date_entry = tk.Entry(root, width=25)
date_entry.pack()

tk.Label(root, text="Category:", font=("Arial", 12)).pack()
category_entry = tk.Entry(root, width=25)
category_entry.pack()

tk.Label(root, text="Amount (₹):", font=("Arial", 12)).pack()
amount_entry = tk.Entry(root, width=25)
amount_entry.pack()

# Buttons for analysis
tk.Button(root, text="➕ Add Expense", command=add_expense, bg="lightyellow", width=20).pack(pady=10)
tk.Button(root, text="📊 Show Summary", command=show_summary, bg="lightgray", width=20).pack(pady=5)
tk.Button(root, text="🥧 Show Pie Chart", command=show_chart, bg="lightpink", width=20).pack(pady=5)

# Result Label
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Arial", 12), justify="left")
result_label.pack(pady=15)

root.mainloop()