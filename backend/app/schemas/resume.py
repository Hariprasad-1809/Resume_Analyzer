from datetime import datetime
from pydantic import BaseModel

class ResumeBase(BaseModel):
    filename: str

class ResumeCreate(ResumeBase):
    file_path: str
    raw_text: str

class Resume(ResumeBase):
    id: str
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True
