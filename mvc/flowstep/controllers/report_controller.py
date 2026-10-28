from datetime import date

from utils import DATE_FMT, peso


class ReportController:
    def __init__(self, ledger, today=date.today):
        self.ledger = ledger
        self.today = today

    def suggested_filename(self, name):
        return f"statement_{name.replace(' ', '_')}.txt"

    def statement(self, name):
        customer = self.ledger.find(name)
        if customer is None:
            raise ValueError(f"Customer '{name}' was not found.")
        today = self.today()
        lines = [
            "FLOWSTEP - CUSTOMER STATEMENT",
            f"Customer: {customer.name}",
            f"Contact: {customer.contact or '-'}",
            f"Credit limit: {peso(customer.credit_limit) if customer.credit_limit else 'None'}",
            f"As of: {today.strftime(DATE_FMT)}",
            "-" * 64,
            f"{'Date':<12}{'Type':<8}{'Amount':>12}{'Balance':>14}  Details",
        ]
        running = 0.0
        for t in customer.sorted_transactions():
            running = t.apply(running)
            lines.append(
                f"{t.on_date.strftime(DATE_FMT):<12}{t.label:<8}"
                f"{peso(t.amount):>12}{peso(running):>14}  {t.describe()}"
            )
        lines.append("-" * 64)
        lines.append(f"Current balance: {peso(customer.balance())}")
        overdue = customer.overdue_amount(today)
        if overdue:
            lines.append(f"Overdue amount:  {peso(overdue)}")
        return "\n".join(lines)

    def export_statement(self, name, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.statement(name))
