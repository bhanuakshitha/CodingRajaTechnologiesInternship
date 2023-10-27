import os
import tkinter as tk
from tkinter import ttk
def add_Income():
    global Income
    Income=Income_entry.get()
    if Income:
        with open("Incom.csv", "a") as file:
            file.write(f"{Income}\n")
        status_label.config(text="Income added successfully!", fg="Blue")
    Income_entry.delete(0, tk.END)
def add_expense():
    Income=Income_entry.get()
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    if date and category and amount:
        with open("expenses.csv", "a") as file:
            file.write(f"{date},{category},{amount}\n")
        status_label.config(text="Expense added successfully!", fg="green")
        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        view_expenses()
    else:
        status_label.config(text="Please fill all the fields!", fg="red")

def delete_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        date, category, amount = item_text
        with open("expenses.csv", "r") as file:
            lines = file.readlines()
        with open("expenses.csv", "w") as file:
            for line in lines:
                if line.strip() != f"{date},{category},{amount}":
                    file.write(line)
        status_label.config(text="Expense deleted successfully!", fg="green")
        view_expenses()
    else:
        status_label.config(text="Please select an expense to delete!", fg="red")

def view_expenses():
    global expenses_tree
    if os.path.exists("expenses.csv"):
        total_expense = 0
        total_Income=1
        with open("Incom.csv", "r") as file:
            for line in file:
                Income = line.strip()
                total_Income += float(Income)
        Balance=0
        expenses_tree.delete(*expenses_tree.get_children())
        with open("expenses.csv", "r") as file:
            for line in file:
                date, category, amount = line.strip().split(",")
                expenses_tree.insert("", tk.END, values=(date, category, amount))
                total_expense += float(amount)
        total_label.config(text=f"Total Expense: {total_expense:.2f}")
        Balance=float(total_Income)-total_expense
        Balance_label.config(text=f"Balance:{Balance-1:.2f}")
    else:
        total_label.config(text="No expenses recorded.")
        expenses_tree.delete(*expenses_tree.get_children())

def View_Income(total_Income=1):
    with open("Incom.csv", "r") as file:
            for line in file:
                Income = line.strip()
                total_Income += float(Income)
    Income_label.config(text=f"Income:{ total_Income-1:.2f}")
    
# Create the main application window
root = tk.Tk()
root.title("Personal Budget Tracker")

# Create labels and entries for adding expenses
Income_label = tk.Label(root, text="Income")
Income_label.grid(row=0, column=0, padx=5, pady=5)
Income_entry = tk.Entry(root)
Income_entry.grid(row=0, column=1, padx=5, pady=5)

date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
date_label.grid(row=2, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=2, column=1, padx=5, pady=5)


category_label = tk.Label(root, text="Category:")
category_label.grid(row=3, column=0, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=3, column=1, padx=5, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=4, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=4, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

Income_button=tk.Button(root,text="Add Income", command=add_Income)
Income_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

# Create a treeview to display expenses
columns = ("Date", "Category", "Amount")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

# Create a label to display the total expense
total_label = tk.Label(root, text="")
total_label.grid(row=12, column=0, columnspan=2, padx=5, pady=5)
Balance_label = tk.Label(root, text="")
Balance_label.grid(row=10, column=0, columnspan=2, padx=5, pady=5)
Income_label= tk.Label(root, text="")
Income_label.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

# Create a label to show the status of expense addition and deletion
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
# Create buttons to view and delete expenses
view_button = tk.Button(root, text="View Expenses", command=view_expenses)
view_button.grid(row=7, column=0, padx=5, pady=10)

delete_button = tk.Button(root, text="Delete Expense", command=delete_expense)
delete_button.grid(row=7, column=1, padx=5, pady=10)
View_income_button=tk.Button(root,text='View Income',command=View_Income)
View_income_button.grid(row=7, column=2, padx=5, pady=10)
# Check if the 'expenses.txt' file exists; create it if it doesn't
if not os.path.exists("expenses.csv"):
    with open("expenses.csv", "w"):
        pass
if not os.path.exists("Incom.csv"):
    with open("Incom.csv", "w"):
        pass
# Display existing expenses on application start
view_expenses()

root.mainloop()