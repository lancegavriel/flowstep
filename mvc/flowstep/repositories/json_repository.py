import json
import os

from models.account import OwnerAccount
from models.customer import Customer
from models.ledger import Ledger

DEFAULT_PATH = os.environ.get("FLOWSTEP_DATA", "flowstep_data.json")


class JsonRepository:
    def __init__(self, path=DEFAULT_PATH):
        self.path = path

    def load(self):
        if not os.path.exists(self.path):
            return Ledger(), OwnerAccount()
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        owner = OwnerAccount(**data.get("owner", {}))
        ledger = Ledger([Customer.from_dict(c) for c in data.get("customers", [])])
        return ledger, owner

    def save(self, ledger, owner):
        temp_path = self.path + ".tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump({"owner": owner.to_dict(), "customers": ledger.to_dict()}, f, indent=2)
        os.replace(temp_path, self.path)  # avoids a half-written data file
