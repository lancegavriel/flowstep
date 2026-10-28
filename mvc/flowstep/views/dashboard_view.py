import tkinter as tk
from tkinter import messagebox, ttk

from utils import peso
from views.form_dialog import FormDialog
from views.widgets import make_card


class DashboardView(ttk.Frame):
    def __init__(self, app):
        super().__init__(app.container, padding=16)
        self.app = app
        self.search = tk.StringVar()
        self.overdue_only = tk.BooleanVar(value=False)

        header = ttk.Frame(self)
        header.pack(fill="x")
        ttk.Label(header, text="Dashboard", font=("Segoe UI", 18, "bold")).pack(side="left")
        ttk.Button(header, text="Log out", command=app.logout).pack(side="right")

        cards = ttk.Frame(self)
        cards.pack(fill="x", pady=12)
        self.total_label = make_card(cards, "Total outstanding utang")
        self.customers_label = make_card(cards, "Customers")
        self.overdue_label = make_card(cards, "Overdue customers")

        controls = ttk.Frame(self)
        controls.pack(fill="x", pady=(0, 8))
        ttk.Label(controls, text="Search:").pack(side="left")
        ttk.Entry(controls, textvariable=self.search, width=24).pack(side="left", padx=6)
        self.search.trace_add("write", lambda *_: self.refresh())
        ttk.Checkbutton(controls, text="Show overdue only", variable=self.overdue_only,
                        command=self.refresh).pack(side="left", padx=12)
        ttk.Button(controls, text="Add customer", command=self.add_customer).pack(side="right")
        ttk.Button(controls, text="Open selected", command=self.open_selected).pack(side="right", padx=8)
        ttk.Button(controls, text="Delete selected", command=self.delete_selected).pack(side="right")

        columns = ("name", "balance", "limit", "overdue")
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=14)
        for col, title, width, anchor in [
            ("name", "Customer", 260, "w"), ("balance", "Balance", 140, "e"),
            ("limit", "Credit limit", 140, "e"), ("overdue", "Overdue", 140, "e"),
        ]:
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor=anchor)
        self.table.tag_configure("overdue", foreground="#b00020")
        self.table.pack(fill="both", expand=True)
        self.table.bind("<Double-1>", lambda e: self.open_selected())

    def refresh(self):
        summary = self.app.customers.summary()
        self.total_label.config(text=peso(summary["total_outstanding"]))
        self.customers_label.config(text=str(summary["customer_count"]))
        self.overdue_label.config(text=str(summary["overdue_count"]))

        self.table.delete(*self.table.get_children())
        rows = self.app.customers.list_customers(self.search.get(), self.overdue_only.get())
        for row in rows:
            self.table.insert(
                "", "end", iid=row["name"],
                values=(row["name"], peso(row["balance"]),
                        peso(row["credit_limit"]) if row["credit_limit"] else "None",
                        peso(row["overdue"]) if row["overdue"] else "-"),
                tags=("overdue",) if row["overdue"] else (),
            )

    def add_customer(self):
        def submit(values):
            self.app.customers.add_customer(values["name"], values["contact"], values["limit"])
            self.refresh()

        FormDialog(self.app, "Add customer", [
            ("name", "Name", ""),
            ("contact", "Contact (optional)", ""),
            ("limit", "Credit limit (0 = none)", "0"),
        ], submit)

    def delete_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Delete customer", "Select a customer first.")
            return
        name = selected[0]
        balance = self.app.customers.details(name)["balance"]
        warning = f"\n\nThey still owe {peso(balance)}." if balance > 0 else ""
        if not messagebox.askyesno(
            "Delete customer",
            f"Delete {name} and all of their records? This cannot be undone.{warning}",
            icon="warning",
        ):
            return
        try:
            self.app.customers.delete_customer(name)
        except ValueError as error:
            messagebox.showerror("Delete customer", str(error))
        self.refresh()

    def open_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Open customer", "Select a customer first.")
            return
        self.app.show_customer(selected[0])
