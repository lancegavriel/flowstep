class AuthController:
    def __init__(self, owner, ledger, repository):
        self.owner = owner
        self.ledger = ledger
        self.repository = repository

    def has_account(self):
        return self.owner.exists()

    def register(self, username, password, confirm):
        if password != confirm:
            raise ValueError("Passwords do not match.")
        self.owner.register(username.strip(), password)
        self.repository.save(self.ledger, self.owner)

    def login(self, username, password):
        if not self.owner.verify(username.strip(), password):
            raise ValueError("Wrong username or password.")
