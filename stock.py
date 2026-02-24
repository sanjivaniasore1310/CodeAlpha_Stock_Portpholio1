import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
import csv

portfolio = {}
total_investment = 0

# ---------------- FUNCTIONS ---------------- #

def add_stock():
    global total_investment
    
    stock = stock_entry.get().upper()
    qty = qty_entry.get()

    if stock == "" or qty == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        qty = int(qty)
        data = yf.Ticker(stock)
        price = data.info['currentPrice']
        investment = price * qty

        portfolio[stock] = (qty, price, investment)
        total_investment += investment

        tree.insert("", "end", values=(stock, qty, round(price,2), round(investment,2)))
        total_label.config(text=f"Total Investment: ${round(total_investment,2)}")

        stock_entry.delete(0, tk.END)
        qty_entry.delete(0, tk.END)

    except:
        messagebox.showerror("Error", "Invalid Stock Symbol")

def delete_stock():
    global total_investment

    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a stock to delete")
        return

    for item in selected:
        values = tree.item(item, "values")
        stock = values[0]
        investment = float(values[3])

        total_investment -= investment
        total_label.config(text=f"Total Investment: ${round(total_investment,2)}")

        del portfolio[stock]
        tree.delete(item)

def save_csv():
    if not portfolio:
        messagebox.showinfo("Info", "No data to save")
        return

    with open("portfolio.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Stock", "Quantity", "Price", "Investment"])

        for stock, data in portfolio.items():
            writer.writerow([stock, data[0], data[1], data[2]])

        writer.writerow(["", "", "Total", total_investment])

    messagebox.showinfo("Success", "Portfolio saved to portfolio.csv")

def show_pie_chart():
    if not portfolio:
        messagebox.showinfo("Info", "No data to display")
        return

    stocks = []
    investments = []

    for stock, data in portfolio.items():
        stocks.append(stock)
        investments.append(data[2])

    plt.figure()
    plt.pie(investments, labels=stocks, autopct="%1.1f%%")
    plt.title("Portfolio Distribution")
    plt.show()

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Stock Portfolio Tracker Pro")
root.geometry("800x550")
root.config(bg="#0f172a")

title = tk.Label(root, text="Stock Portfolio Tracker",
                 font=("Arial", 20, "bold"),
                 bg="#0f172a", fg="white")
title.pack(pady=10)

frame = tk.Frame(root, bg="#0f172a")
frame.pack(pady=10)

tk.Label(frame, text="Stock Symbol", bg="#0f172a", fg="white").grid(row=0, column=0, padx=10)
stock_entry = tk.Entry(frame)
stock_entry.grid(row=0, column=1, padx=10)

tk.Label(frame, text="Quantity", bg="#0f172a", fg="white").grid(row=0, column=2, padx=10)
qty_entry = tk.Entry(frame)
qty_entry.grid(row=0, column=3, padx=10)

tk.Button(frame, text="Add Stock", bg="#22c55e", fg="white",
          command=add_stock).grid(row=0, column=4, padx=10)

columns = ("Stock", "Quantity", "Price", "Investment")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(pady=20)

total_label = tk.Label(root, text="Total Investment: $0",
                       font=("Arial", 14, "bold"),
                       bg="#0f172a", fg="#22c55e")
total_label.pack(pady=10)

button_frame = tk.Frame(root, bg="#0f172a")
button_frame.pack(pady=10)

tk.Button(button_frame, text="📊 Show Pie Chart",
          bg="#3b82f6", fg="white",
          command=show_pie_chart).grid(row=0, column=0, padx=10)

tk.Button(button_frame, text="💾 Save to CSV",
          bg="#f59e0b", fg="white",
          command=save_csv).grid(row=0, column=1, padx=10)

tk.Button(button_frame, text="🗑 Delete Selected",
          bg="#ef4444", fg="white",
          command=delete_stock).grid(row=0, column=2, padx=10)

root.mainloop()