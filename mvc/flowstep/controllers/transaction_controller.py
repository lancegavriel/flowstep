from datetime import date, timedelta

from models.transaction import CreditPurchase, Payment
from utils import DATE_FMT, parse_amount, parse_date, peso


class CreditLimitExceeded(ValueError):
    """Raised when new utang would put a customer over their credit limit.

    The view can ask the owner to confirm and then retry with allow_over_limit=True.
    """

    def __init__(self, name, new_balance, limit):
        super().__init__(
            f"This utang would bring {name}'s balance to {peso(new_balance)}, "
            f"which is over the credit limit of {peso(limit)}."
        )


class TransactionController:
    def __init__(self, ledger, owner, repository, today=date.today):
        self.ledger = ledger
        self.owner = owner
        self.repository = repository
        self.today = today

    def default_dates(self):
        """Default form values: today, and a due date one week later."""
        today = self.today()
        return today.strftime(DATE_FMT), (today + timedelta(days=7)).strftime(DATE_FMT)

    def _customer(self, name):
        customer = self.ledger.find(name)
        if customer is None:
            raise ValueError(f"Customer '{name}' was not found.")
        return customer

    def record_purchase(self, name, items, amount_text, date_text, due_text, allow_over_limit=False):
        customer = self._customer(name)
        purchase = CreditPurchase(
            parse_amount(amount_text), parse_date(date_text), items.strip(), parse_date(due_text)
        )
        if not allow_over_limit and self.ledger.policy.exceeds_limit(customer, purchase.amount):
            raise CreditLimitExceeded(
                customer.name, customer.balance() + purchase.amount, customer.credit_limit
            )
        customer.add_transaction(purchase)
        self.repository.save(self.ledger, self.owner)

    def delete_transaction(self, name, index):
        customer = self._customer(name)
        records = customer.sorted_transactions()
        if not 0 <= index < len(records):
            raise ValueError("That record was not found.")
        customer.remove_transaction(records[index])  # raises ValueError if it would break the balance
        self.repository.save(self.ledger, self.owner)

    def record_payment(self, name, amount_text, date_text, note=""):
        customer = self._customer(name)
        payment = Payment(parse_amount(amount_text), parse_date(date_text), note.strip())
        customer.add_transaction(payment)  # raises ValueError if it exceeds the balance
        self.repository.save(self.ledger, self.owner)
