from abc import ABC, abstractmethod

from utils import DATE_FMT, parse_date


class Transaction(ABC):
    """Base class for anything that changes a customer's balance."""

    kind = "transaction"
    label = "Transaction"

    def __init__(self, amount, on_date, note=""):
        amount = round(float(amount), 2)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.amount = amount
        self.on_date = on_date
        self.note = note

    @abstractmethod
    def apply(self, balance):
        """Return the new balance after this transaction."""

    @abstractmethod
    def describe(self):
        """Return a short description for tables and statements."""

    def to_dict(self):
        return {
            "kind": self.kind,
            "amount": self.amount,
            "date": self.on_date.strftime(DATE_FMT),
            "note": self.note,
        }

    @staticmethod
    def from_dict(data):
        on_date = parse_date(data["date"])
        if data["kind"] == "purchase":
            return CreditPurchase(
                data["amount"], on_date, data.get("items", ""),
                parse_date(data["due_date"]), data.get("note", ""),
            )
        return Payment(data["amount"], on_date, data.get("note", ""))


class CreditPurchase(Transaction):
    """Goods taken on credit. Increases the balance."""

    kind = "purchase"
    label = "Utang"

    def __init__(self, amount, on_date, items, due_date, note=""):
        super().__init__(amount, on_date, note)
        if due_date < on_date:
            raise ValueError("Due date cannot be earlier than the purchase date.")
        self.items = items
        self.due_date = due_date

    def apply(self, balance):
        return round(balance + self.amount, 2)

    def describe(self):
        text = self.items or "Credit purchase"
        return f"{text} (due {self.due_date.strftime(DATE_FMT)})"

    def to_dict(self):
        data = super().to_dict()
        data["items"] = self.items
        data["due_date"] = self.due_date.strftime(DATE_FMT)
        return data


class Payment(Transaction):
    """Money received from the customer. Decreases the balance."""

    kind = "payment"
    label = "Bayad"

    def apply(self, balance):
        return round(balance - self.amount, 2)

    def describe(self):
        return self.note or "Payment received"
