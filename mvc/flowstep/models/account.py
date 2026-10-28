import hashlib
import secrets


class OwnerAccount:
    def __init__(self, username="", salt="", password_hash=""):
        self.username = username
        self.salt = salt
        self.password_hash = password_hash

    def exists(self):
        return bool(self.username)

    @staticmethod
    def _hash(password, salt):
        return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 100_000).hex()

    def register(self, username, password):
        if not username or len(password) < 4:
            raise ValueError("Enter a username and a password of at least 4 characters.")
        self.username = username
        self.salt = secrets.token_hex(16)
        self.password_hash = self._hash(password, self.salt)

    def verify(self, username, password):
        if not self.exists():
            return False
        return (
            username == self.username
            and secrets.compare_digest(self._hash(password, self.salt), self.password_hash)
        )

    def to_dict(self):
        return {"username": self.username, "salt": self.salt, "password_hash": self.password_hash}
