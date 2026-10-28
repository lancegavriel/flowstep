import tkinter as tk
from tkinter import ttk

from views.customer_view import CustomerView
from views.dashboard_view import DashboardView
from views.login_view import LoginView


class FlowStepApp(tk.Tk):
    def __init__(self, auth, customers, transactions, reports):
        super().__init__()
        self.auth = auth
        self.customers = customers
        self.transactions = transactions
        self.reports = reports

        self.title("FlowStep - Sari-Sari Credit Tracker")
        self.geometry("820x580")
        self.minsize(720, 500)
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Treeview", rowheight=26)

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.current = None
        self.show_login()

    def _show(self, view):
        if self.current is not None:
            self.current.destroy()
        self.current = view
        view.pack(fill="both", expand=True)

    def show_login(self):
        self.unbind("<Return>")
        self._show(LoginView(self))

    def show_dashboard(self):
        self.unbind("<Return>")
        view = DashboardView(self)
        self._show(view)
        view.refresh()

    def show_customer(self, name):
        view = CustomerView(self, name)
        self._show(view)
        view.refresh()

    def logout(self):
        self.show_login()
