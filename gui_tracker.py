import tkinter as tk
from tkinter import messagebox
from expense import Expense
import csv

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("500x400")
        self.root.configure(bg="#282C34")

        # Fonts and styles
        self.default_font = ("Arial", 10)
        
        # Frame for inputs
        frame = tk.Frame(self.root, bg="#282C34")
        frame.pack(pady=20)

        # Label and Entry for Expense Name
        tk.Label(frame, text="Expense Name:", bg="#282C34", fg="#ABB2BF", font=self.default_font).grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(frame, font=self.default_font, width=25)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Label and Entry for Expense Amount
        tk.Label(frame, text="Amount:", bg="#282C34", fg="#ABB2BF", font=self.default_font).grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(frame, font=self.default_font, width=25)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5)

        # Label and Listbox for Category Selection
        tk.Label(frame, text="Category:", bg="#282C34", fg="#ABB2BF", font=self.default_font).grid(row=2, column=0, sticky="w")
        self.category_listbox = tk.Listbox(frame, selectmode="single", bg="#353A42", fg="#ABB2BF", font=self.default_font, relief="sunken", height=5, width=23)
        category_options = ["🍔 Food", "🏠 Home", "💼 Work", "🎉 Fun", "✨ Misc"]
        for option in category_options:
            self.category_listbox.insert(tk.END, option)
        self.category_listbox.grid(row=2, column=1, padx=10, pady=5)

        # Button to add the expense
        self.add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense, font=self.default_font, bg="#61AFEF", fg="white")
        self.add_button.pack(pady=10)

        # Label to display the most recent expense
        self.recent_expense_label = tk.Label(self.root, text="", bg="#282C34", fg="#ABB2BF", font=self.default_font)
        self.recent_expense_label.pack(pady=5)

    def add_expense(self):
        name = self.name_entry.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number for amount.")
            return

        try:
            category = self.category_listbox.get(self.category_listbox.curselection())
        except tk.TclError:
            messagebox.showerror("No selection", "Please select a category.")
            return

        expense = Expense(name=name, amount=amount, category=category)
        
        with open("expenses.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([expense.name, expense.amount, expense.category])

        # Update the recent expense label to show the added expense
        self.recent_expense_label.config(text=f"Added Expense: {expense.name} - ${expense.amount} in {expense.category}")

        # Clear the fields after adding
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_listbox.selection_clear(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()
