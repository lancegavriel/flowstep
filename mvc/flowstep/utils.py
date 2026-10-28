from datetime import datetime

DATE_FMT = "%Y-%m-%d"


def parse_date(text):
    try:
        return datetime.strptime(text.strip(), DATE_FMT).date()
    except ValueError:
        raise ValueError(f"'{text}' is not a valid date. Use YYYY-MM-DD (e.g. 2026-11-05).")


def parse_amount(text, allow_zero=False):
    cleaned = text.replace("₱", "").replace(",", "").strip()
    try:
        value = round(float(cleaned), 2)
    except ValueError:
        raise ValueError(f"'{text}' is not a valid amount.")
    if value < 0 or (value == 0 and not allow_zero):
        raise ValueError("Amount must be greater than zero.")
    return value


def peso(amount):
    return f"₱{amount:,.2f}"
