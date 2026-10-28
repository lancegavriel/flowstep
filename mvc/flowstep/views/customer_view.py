from tkinter import filedialog, messagebox, ttk

from controllers.transaction_controller import CreditLimitExceeded
from utils import DATE_FMT, peso
from views.form_dialog import FormDialog
from views.widgets import make_card


class CustomerView(ttk.Frame):
    def __init__(self, app, customer_name):
        super().__init__(app.container, padding=16)
        self.app = app
        self.name = customer_name

        header = ttk.Frame(self)
        header.pack(fill="x")
        ttk.Button(header, text="← Back", command=app.show_dashboard).pack(side="left")
        ttk.Label(header, text=customer_name, font=("Segoe UI", 18, "bold")).pack(side="left", padx=12)

        self.info_label = ttk.Label(self)
        self.info_label.pack(anchor="w", pady=(8, 0))

        cards = ttk.Frame(self)
        cards.pack(fill="x", pady=10)
        self.balance_label = make_card(cards, "Current balance")
        self.overdue_label = make_card(cards, "Overdue amount")
        self.remaining_label = make_card(cards, "Credit left")

        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=(0, 8))
        ttk.Button(actions, text="Record credit", command=self.record_purchase).pack(side="left")
        ttk.Button(actions, text="Record payment", command=self.record_payment).pack(side="left", padx=8)
        ttk.Button(actions, text="Export statement", command=self.export_statement).pack(side="right")
        ttk.Button(actions, text="Delete selected record", command=self.delete_selected).pack(side="right", padx=8)

        columns = ("date", "type", "details", "amount", "balance")
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=12)
        for col, title, width, anchor in [
            ("date", "Date", 100, "w"), ("type", "Type", 80, "w"), ("details", "Details", 330, "w"),
            ("amount", "Amount", 110, "e"), ("balance", "Balance after", 120, "e"),
        ]:
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor=anchor)
        self.table.tag_configure("payment", foreground="#1b7a3d")
        self.table.pack(fill="both", expand=True)

    def refresh(self):
        d = self.app.customers.details(self.name)
        limit_text = peso(d["credit_limit"]) if d["credit_limit"] else "No limit"
        self.info_label.config(text=f"Contact: {d['contact'] or '-'}    Credit limit: {limit_text}")
        self.balance_label.config(text=peso(d["balance"]))
        self.overdue_label.config(text=peso(d["overdue"]) if d["overdue"] else "None")
        self.remaining_label.config(text=peso(d["credit_left"]) if d["credit_left"] is not None else "-")

        self.table.delete(*self.table.get_children())
        for row in self.app.customers.history(self.name):
            self.table.insert(
                "", "end", iid=str(row["index"]),
                values=(row["date"].strftime(DATE_FMT), row["label"], row["details"],
                        peso(row["amount"]), peso(row["balance_after"])),
                tags=("payment",) if row["is_payment"] else (),
            )

    def record_purchase(self):
        today, due = self.app.transactions.default_dates()

        def submit(values):
            args = (self.name, values["items"], values["amount"], values["date"], values["due"])
            try:
                self.app.transactions.record_purchase(*args)
            except CreditLimitExceeded as warning:
                if not messagebox.askyesno("Credit limit warning",
                                           f"{warning}\n\nRecord it anyway?", parent=self.app):
                    return False
                self.app.transactions.record_purchase(*args, allow_over_limit=True)
            self.refresh()

        FormDialog(self.app, "Record credit", [
            ("items", "Items bought", ""),
            ("amount", "Amount (₱)", ""),
            ("date", "Date (YYYY-MM-DD)", today),
            ("due", "Due date (YYYY-MM-DD)", due),
        ], submit)

    def record_payment(self):
        today, _ = self.app.transactions.default_dates()

        def submit(values):
            self.app.transactions.record_payment(self.name, values["amount"], values["date"], values["note"])
            self.refresh()

        FormDialog(self.app, "Record payment", [
            ("amount", "Amount paid (₱)", ""),
            ("date", "Date (YYYY-MM-DD)", today),
            ("note", "Note (optional)", ""),
        ], submit)

    def delete_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Delete record", "Select a record first.")
            return
        values = self.table.item(selected[0], "values")
        description = f"{values[1]} of {values[3]} on {values[0]}"
        if not messagebox.askyesno("Delete record",
                                   f"Delete this record?\n\n{description}\n\nThis cannot be undone."):
            return
        try:
            self.app.transactions.delete_transaction(self.name, int(selected[0]))
        except ValueError as error:
            messagebox.showerror("Delete record", str(error))
        self.refresh()

    def export_statement(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=self.app.reports.suggested_filename(self.name),
            filetypes=[("Text file", "*.txt")],
        )
        if path:
            self.app.reports.export_statement(self.name, path)
            messagebox.showinfo("Export statement", "Statement saved.")
