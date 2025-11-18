from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGO = os.getenv("JWT_ALGORITHM")

def create_access_token(data: dict):
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)
