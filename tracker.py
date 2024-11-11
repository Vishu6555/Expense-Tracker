# expense.py
class Expense:
    """Represents an individual expense entry with a name, category, and amount."""

    def __init__(self, name: str, category: str, amount: float) -> None:
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self) -> str:
        return f"<Expense: {self.name}, {self.category}, ${self.amount:.2f}>"

# tracker.py
from expense import Expense
import calendar
import datetime
import os

# Constants
EXPENSE_FILE_PATH = "expenses.csv"
INCOME_FILE_PATH = "income.txt"
BUDGET = 2000.0  # Default budget if income is not set

def main() -> None:
    """Main function to run the expense tracker."""
    print("🎯 Running Expense Tracker!")
    
    # Get monthly income
    income = get_monthly_income()

    # Get user input for expense
    expense = get_user_expense()

    # Write expense to a file
    save_expense_to_file(expense, EXPENSE_FILE_PATH)

    # Summarize expenses and show budget
    summarize_expenses(EXPENSE_FILE_PATH, income)


def get_monthly_income() -> float:
    """Prompts the user for monthly income if not set and saves it to a file."""
    if os.path.exists(INCOME_FILE_PATH):
        with open(INCOME_FILE_PATH, "r", encoding="utf-8") as f:
            try:
                income = float(f.read().strip())
                print(f"💰 Monthly Income: ${income:.2f}")
                return income
            except ValueError:
                print("⚠️ Invalid income data found. Please enter again.")
    
    # Get and save monthly income
    while True:
        try:
            income = float(input("Enter your monthly income: "))
            if income < 0:
                print("Income cannot be negative. Please try again.")
                continue
            with open(INCOME_FILE_PATH, "w", encoding="utf-8") as f:
                f.write(str(income))
            print(f"💰 Monthly Income saved: ${income:.2f}")
            return income
        except ValueError:
            print("Invalid income. Please enter a valid number.")

def get_user_expense() -> Expense:
    """Prompts the user for expense details and returns an Expense object."""
    print("🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    
    # Get and validate expense amount
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount < 0:
                print("Amount cannot be negative. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")

    # Display categories and get selection
    expense_categories = ["🍔 Food", "🏠 Home", "💼 Work", "🎉 Fun", "✨ Misc"]
    selected_category = select_category(expense_categories)
    
    return Expense(name=expense_name, category=selected_category, amount=expense_amount)


def select_category(categories: list[str]) -> str:
    """Displays a list of categories for the user to select from and returns the chosen category."""
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(categories, start=1):
            print(f"  {i}. {category_name}")

        try:
            selected_index = int(input(f"Enter a category number [1 - {len(categories)}]: ")) - 1
            if 0 <= selected_index < len(categories):
                return categories[selected_index]
            else:
                print("Invalid category. Please select from the given options.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def save_expense_to_file(expense: Expense, file_path: str) -> None:
    """Saves an Expense object to a file in CSV format."""
    print(f"🎯 Saving User Expense: {expense} to {file_path}")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses(file_path: str, income: float) -> None:
    """Reads expenses from a file, calculates total spending, and displays a summary with remaining budget."""
    expenses = load_expenses(file_path)

    amount_by_category = {}
    for expense in expenses:
        if expense.category in amount_by_category:
            amount_by_category[expense.category] += expense.amount
        else:
            amount_by_category[expense.category] = expense.amount

    print("Expenses By Category 📈:")
    for category, amount in amount_by_category.items():
        print(f"  {category}: ${amount:.2f}")

    total_spent = sum(expense.amount for expense in expenses)
    print(f"💵 Total Spent: ${total_spent:.2f}")

    remaining_budget = income - total_spent
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    daily_budget = calculate_daily_budget(remaining_budget)
    print(green_text(f"👉 Budget Per Day: ${daily_budget:.2f}"))


def load_expenses(file_path: str) -> list[Expense]:
    """Loads expenses from a CSV file and returns a list of Expense objects."""
    expenses = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                expense_name, expense_amount, expense_category = line.strip().split(",")
                expenses.append(Expense(expense_name, expense_category, float(expense_amount)))
    return expenses


def calculate_daily_budget(remaining_budget: float) -> float:
    """Calculates the budget per remaining day of the month."""
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    return remaining_budget / remaining_days if remaining_days > 0 else 0.0


def green_text(text: str) -> str:
    """Formats text with green color for console output."""
    return f"\033[92m{text}\033[0m"


if __name__ == "__main__":
    main()