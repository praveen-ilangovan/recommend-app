""" """

# Builtin imports
import logging

# Project specific imports
from passlib.context import CryptContext

# [ISSUE]: AttributeError: module 'bcrypt' has no attribute '__about__'
# [LINK]: https://github.com/pyca/bcrypt/issues/684
logging.getLogger("passlib").setLevel(logging.ERROR)


# -----------------------------------------------------------------------------#
# Class
# -----------------------------------------------------------------------------#
class Hasher:
    CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return Hasher.CONTEXT.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return Hasher.CONTEXT.hash(password)
