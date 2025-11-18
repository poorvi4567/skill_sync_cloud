from pydantic import BaseModel
from typing import Optional

class SkillCreate(BaseModel):
    name: str
    category: int
    skill_description: Optional[str] = None
