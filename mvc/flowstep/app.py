"""FlowStep: Sari-Sari Store Credit (Utang) Tracking System.

You may start the application with:  python app.py
"""

from controllers.auth_controller import AuthController
from controllers.customer_controller import CustomerController
from controllers.report_controller import ReportController
from controllers.transaction_controller import TransactionController
from repositories.json_repository import JsonRepository


def main():
    try:
        from views.main_window import FlowStepApp
    except ImportError as error:
        print(f"Could not start the interface: {error}")
        print("Tkinter is required. On Linux, install it with: sudo apt install python3-tk")
        return

    repository = JsonRepository()
    ledger, owner = repository.load()

    app = FlowStepApp(
        auth=AuthController(owner, ledger, repository),
        customers=CustomerController(ledger, owner, repository),
        transactions=TransactionController(ledger, owner, repository),
        reports=ReportController(ledger),
    )
    app.mainloop()


if __name__ == "__main__":
    main()
