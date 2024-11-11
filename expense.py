class Expense:
    """Represents an individual expense entry with a name, category, and amount."""

    def __init__(self, name: str, category: str, amount: float) -> None:
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self) -> str:
        return f"<Expense: {self.name}, {self.category}, ${self.amount:.2f}>"
