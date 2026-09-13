import os

from dotenv import load_dotenv
from pwdlib import PasswordHash


load_dotenv()


password_hash = PasswordHash.recommended()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not configured")

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return password_hash.hash(password)