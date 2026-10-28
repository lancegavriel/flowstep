import tkinter as tk
from tkinter import messagebox, ttk


class FormDialog(tk.Toplevel):
    """fields is a list of (key, label, default).

    on_submit(values) is called with a dict of the entered text. It may raise
    ValueError (shown to the user, dialog stays open) or return False (dialog stays open).
    """

    def __init__(self, parent, title, fields, on_submit):
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.resizable(False, False)
        self.on_submit = on_submit
        self.vars = {}

        body = ttk.Frame(self, padding=16)
        body.pack()
        for row, (key, label, default) in enumerate(fields):
            ttk.Label(body, text=label).grid(row=row, column=0, sticky="w", pady=4, padx=(0, 12))
            var = tk.StringVar(value=default)
            entry = ttk.Entry(body, textvariable=var, width=32)
            entry.grid(row=row, column=1, pady=4)
            self.vars[key] = var
            if row == 0:
                entry.focus_set()

        buttons = ttk.Frame(body)
        buttons.grid(row=len(fields), column=0, columnspan=2, pady=(12, 0), sticky="e")
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(buttons, text="Save", command=self.submit).pack(side="right")

        self.bind("<Return>", self.submit)
        self.bind("<Escape>", lambda e: self.destroy())
        self.wait_visibility()
        self.grab_set()

    def submit(self, event=None):
        values = {key: var.get().strip() for key, var in self.vars.items()}
        try:
            result = self.on_submit(values)
        except ValueError as error:
            messagebox.showerror("Please check your input", str(error), parent=self)
            return
        if result is not False:
            self.destroy()
