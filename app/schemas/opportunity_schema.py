from pydantic import BaseModel
from typing import Optional

class OpportunityCreate(BaseModel):
    title: str
    description: Optional[str]
    posted_by: str
    type: str
