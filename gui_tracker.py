import tkinter as tk
from tkinter import messagebox
from expense import Expense
import csv
import os
# Path to the budget file
BUDGET_FILE = "budget.txt"

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x600")
        self.root.configure(bg="#2E2E2E")

        # Initialize budget
        self.budget = self.load_budget()

        # Fonts and styles
        self.default_font = ("Arial", 10)
        
        # Frame for inputs
        frame = tk.Frame(self.root, bg="#2E2E2E")
        frame.pack(pady=20)

        # Label and Entry for Expense Name
        tk.Label(frame, text="Expense Name:", bg="#2E2E2E", fg="#D1D1D1", font=self.default_font).grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(frame, font=self.default_font, width=25)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Label and Entry for Expense Amount
        tk.Label(frame, text="Amount:", bg="#2E2E2E", fg="#D1D1D1", font=self.default_font).grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(frame, font=self.default_font, width=25)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5)

        # Label and Listbox for Category Selection
        tk.Label(frame, text="Category:", bg="#2E2E2E", fg="#D1D1D1", font=self.default_font).grid(row=2, column=0, sticky="w")
        self.category_listbox = tk.Listbox(frame, selectmode="single", bg="#3A3A3A", fg="#D1D1D1", font=self.default_font, relief="sunken", height=5, width=23)
        category_options = ["🍔 Food", "🏠 Home", "💼 Work", "🎉 Fun", "✨ Misc"]
        for option in category_options:
            self.category_listbox.insert(tk.END, option)
        self.category_listbox.grid(row=2, column=1, padx=10, pady=5)

        # Button to add the expense
        self.add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense, font=self.default_font, bg="#4C8CFF", fg="white")
        self.add_button.pack(pady=10)

        # Label to display the most recent expense
        self.recent_expense_label = tk.Label(self.root, text="", bg="#2E2E2E", fg="#D1D1D1", font=self.default_font)
        self.recent_expense_label.pack(pady=5)

        # Button to track budget
        self.track_budget_button = tk.Button(self.root, text="Track Budget", command=self.open_budget_window, font=self.default_font, bg="#FF7F50", fg="white")
        self.track_budget_button.pack(pady=10)

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

    def load_budget(self):
        """Loads the budget from the file or initializes it to 0 if not found."""
        if os.path.exists(BUDGET_FILE):
            with open(BUDGET_FILE, "r") as file:
                try:
                    return float(file.read().strip())
                except ValueError:
                    messagebox.showerror("File Error", "Budget file is corrupted. Resetting to 0.")
                    return 0.0
        else:
            # Create file with initial budget value of 0.0
            with open(BUDGET_FILE, "w") as file:
                file.write("0")
            return 0.0

    def save_budget(self):
        """Saves the budget to a file."""
        with open(BUDGET_FILE, "w") as file:
            file.write(str(self.budget))

    def open_budget_window(self):
        """Opens the budget tracking window."""
        total_expenses = self.calculate_total_expenses()

        # Ensure budget is a valid float
        if self.budget is None:
            self.budget = 0.0

        remaining_budget = self.budget - total_expenses
        budget_window = tk.Toplevel(self.root)
        budget_window.title("Budget Tracking")
        budget_window.geometry("400x300")
        budget_window.configure(bg="#2E2E2E")

        # Labels to show the budget details
        tk.Label(budget_window, text=f"Total Expenses: ${total_expenses:.2f}", bg="#2E2E2E", fg="#D1D1D1", font=self.default_font).pack(pady=10)
        tk.Label(budget_window, text=f"Remaining Budget: ${remaining_budget:.2f}", bg="#2E2E2E", fg="#D1D1D1", font=self.default_font).pack(pady=10)

        tk.Label(budget_window, text=f"Budget: ${self.budget:.2f}", bg="#2E2E2E", fg="#D1D1D1", font=self.default_font).pack(pady=10)

        tk.Button(budget_window, text="Close", command=budget_window.destroy, font=self.default_font, bg="#FF6347", fg="white").pack(pady=10)

    def calculate_total_expenses(self):
        """Calculates the total expenses from the saved expenses."""
        try:
            with open("expenses.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                total_expenses = sum(float(row[1]) for row in reader if row)
                return total_expenses
        except FileNotFoundError:
            return 0.0


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()
