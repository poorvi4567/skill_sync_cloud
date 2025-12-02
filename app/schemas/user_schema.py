from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    name: str
    password: str        # ✔ user sends raw password
    role: str
    phone_number: Optional[str] = None
    experience_level: Optional[str] = None
    profile_summary: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str