from models.transaction import CreditPurchase, Payment, Transaction
from utils import peso


class Customer:
    def __init__(self, name, contact="", credit_limit=0.0, transactions=None):
        self.name = name
        self.contact = contact
        self.credit_limit = credit_limit  # 0 means "no limit"
        self.transactions = transactions or []

    def add_transaction(self, transaction):
        if isinstance(transaction, Payment) and transaction.amount > self.balance() + 0.005:
            raise ValueError(
                f"Payment ({peso(transaction.amount)}) is more than the "
                f"balance ({peso(self.balance())})."
            )
        self.transactions.append(transaction)

    def remove_transaction(self, transaction):
        remaining = [t for t in self.transactions if t is not transaction]
        if len(remaining) == len(self.transactions):
            raise ValueError("That record was not found.")
        total = 0.0
        for t in sorted(remaining, key=lambda t: t.on_date):
            total = t.apply(total)
        if total < -0.005:
            raise ValueError(
                "This credit can't be deleted because the payments already recorded "
                "would be more than what is left owed. Delete the related payments first."
            )
        self.transactions = remaining

    def sorted_transactions(self):
        return sorted(self.transactions, key=lambda t: t.on_date)

    def balance(self):
        total = 0.0
        for transaction in self.sorted_transactions():
            total = transaction.apply(total)  # polymorphism: each type applies itself
        return round(total, 2)

    def purchases(self):
        return [t for t in self.transactions if isinstance(t, CreditPurchase)]

    def unpaid_purchases(self):
        """Payments are applied to the oldest purchases first."""
        paid = sum(t.amount for t in self.transactions if isinstance(t, Payment))
        result = []
        for purchase in sorted(self.purchases(), key=lambda p: p.on_date):
            if paid >= purchase.amount - 0.005:
                paid -= purchase.amount
            else:
                result.append((purchase, round(purchase.amount - paid, 2)))
                paid = 0
        return result

    def overdue_amount(self, today):
        return round(sum(unpaid for p, unpaid in self.unpaid_purchases() if p.due_date < today), 2)

    def is_overdue(self, today):
        return self.overdue_amount(today) > 0

    def to_dict(self):
        return {
            "name": self.name,
            "contact": self.contact,
            "credit_limit": self.credit_limit,
            "transactions": [t.to_dict() for t in self.transactions],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"], data.get("contact", ""), data.get("credit_limit", 0.0),
            [Transaction.from_dict(t) for t in data.get("transactions", [])],
        )
