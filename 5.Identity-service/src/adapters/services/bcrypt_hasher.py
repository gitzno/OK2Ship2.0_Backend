import bcrypt

from src.use_cases.ports.services import PasswordHasherService


class BcryptHasher(PasswordHasherService):

    def hash_password(self, password: str) -> str:
        password = password.encode("utf-8")

        salt = bcrypt.gensalt()

        hashed_bytes = bcrypt.hashpw(password, salt)

        return hashed_bytes.decode("utf-8")

    def verify_password(self, password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
        except Exception:
            return False

