import tkinter as tk
from tkinter import messagebox, ttk


class LoginView(ttk.Frame):
    def __init__(self, app):
        super().__init__(app.container, padding=40)
        self.app = app
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.confirm = tk.StringVar()
        self.registering = not app.auth.has_account()

        ttk.Label(self, text="FlowStep", font=("Segoe UI", 28, "bold")).pack(pady=(40, 0))
        ttk.Label(self, text="Sari-Sari Store Credit Tracker").pack(pady=(0, 24))

        form = ttk.Frame(self)
        form.pack()
        ttk.Label(form, text="Username").grid(row=0, column=0, sticky="w", pady=4)
        user_entry = ttk.Entry(form, textvariable=self.username, width=28)
        user_entry.grid(row=0, column=1, pady=4, padx=8)
        ttk.Label(form, text="Password").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(form, textvariable=self.password, show="•", width=28).grid(row=1, column=1, pady=4, padx=8)
        if self.registering:
            ttk.Label(form, text="Confirm password").grid(row=2, column=0, sticky="w", pady=4)
            ttk.Entry(form, textvariable=self.confirm, show="•", width=28).grid(row=2, column=1, pady=4, padx=8)
            ttk.Label(self, text="First time here? Create your store owner account.").pack(pady=(12, 0))

        ttk.Button(self, text="Create account" if self.registering else "Log in",
                   command=self.submit).pack(pady=16)
        user_entry.focus_set()
        app.bind("<Return>", lambda e: self.submit())

    def submit(self):
        try:
            if self.registering:
                self.app.auth.register(self.username.get(), self.password.get(), self.confirm.get())
            else:
                self.app.auth.login(self.username.get(), self.password.get())
        except ValueError as error:
            messagebox.showerror("Login", str(error))
            return
        self.app.show_dashboard()
