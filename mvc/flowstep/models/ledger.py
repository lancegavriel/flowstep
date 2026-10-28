from models.customer import Customer


class CreditPolicy:
    def exceeds_limit(self, customer, amount):
        if customer.credit_limit <= 0:
            return False
        return customer.balance() + amount > customer.credit_limit + 0.005


class Ledger:
    def __init__(self, customers=None):
        self.customers = customers or []
        self.policy = CreditPolicy()

    def find(self, name):
        for customer in self.customers:
            if customer.name.lower() == name.lower():
                return customer
        return None

    def add_customer(self, name, contact="", credit_limit=0.0):
        if not name:
            raise ValueError("Customer name cannot be empty.")
        if self.find(name):
            raise ValueError(f"A customer named '{name}' already exists.")
        customer = Customer(name, contact, credit_limit)
        self.customers.append(customer)
        return customer

    def remove_customer(self, name):
        customer = self.find(name)
        if customer is None:
            raise ValueError(f"Customer '{name}' was not found.")
        self.customers.remove(customer)

    def total_outstanding(self):
        return round(sum(c.balance() for c in self.customers), 2)

    def overdue_customers(self, today):
        return [c for c in self.customers if c.is_overdue(today)]

    def to_dict(self):
        return [c.to_dict() for c in self.customers]
