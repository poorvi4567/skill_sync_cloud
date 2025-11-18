from pydantic import BaseModel

class MentorshipCreate(BaseModel):
    mentor_name: str
    mentee_name: str
