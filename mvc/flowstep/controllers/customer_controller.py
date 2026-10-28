from datetime import date

from utils import parse_amount


class CustomerController:
    def __init__(self, ledger, owner, repository, today=date.today):
        self.ledger = ledger
        self.owner = owner
        self.repository = repository
        self.today = today

    def _save(self):
        self.repository.save(self.ledger, self.owner)

    def _get(self, name):
        customer = self.ledger.find(name)
        if customer is None:
            raise ValueError(f"Customer '{name}' was not found.")
        return customer

    def summary(self):
        today = self.today()
        return {
            "total_outstanding": self.ledger.total_outstanding(),
            "customer_count": len(self.ledger.customers),
            "overdue_count": len(self.ledger.overdue_customers(today)),
        }

    def list_customers(self, query="", overdue_only=False):
        today, query = self.today(), query.strip().lower()
        rows = []
        for customer in self.ledger.customers:
            overdue = customer.overdue_amount(today)
            if query and query not in customer.name.lower():
                continue
            if overdue_only and overdue == 0:
                continue
            rows.append({
                "name": customer.name,
                "balance": customer.balance(),
                "credit_limit": customer.credit_limit,
                "overdue": overdue,
            })
        return sorted(rows, key=lambda r: r["balance"], reverse=True)

    def add_customer(self, name, contact, limit_text):
        limit = parse_amount(limit_text, allow_zero=True) if limit_text else 0.0
        self.ledger.add_customer(name.strip(), contact.strip(), limit)
        self._save()

    def delete_customer(self, name):
        self.ledger.remove_customer(name)
        self._save()

    def details(self, name):
        customer = self._get(name)
        balance = customer.balance()
        limit = customer.credit_limit
        return {
            "name": customer.name,
            "contact": customer.contact,
            "credit_limit": limit,
            "balance": balance,
            "overdue": customer.overdue_amount(self.today()),
            "credit_left": max(limit - balance, 0) if limit else None,
        }

    def history(self, name):
        customer = self._get(name)
        rows, running = [], 0.0
        for index, transaction in enumerate(customer.sorted_transactions()):
            running = transaction.apply(running)
            rows.append({
                "index": index,  # position used by delete_transaction
                "date": transaction.on_date,
                "label": transaction.label,
                "details": transaction.describe(),
                "amount": transaction.amount,
                "balance_after": running,
                "is_payment": transaction.kind == "payment",
            })
        return rows
