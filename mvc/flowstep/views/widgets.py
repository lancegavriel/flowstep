from tkinter import ttk


def make_card(parent, title):
    """A titled box with one big value label. Returns the label so it can be updated."""
    box = ttk.LabelFrame(parent, text=title, padding=10)
    box.pack(side="left", expand=True, fill="x", padx=4)
    label = ttk.Label(box, text="-", font=("Segoe UI", 16, "bold"))
    label.pack()
    return label
