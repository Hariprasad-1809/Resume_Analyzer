import uuid
from sqlalchemy import Column, String, Integer, JSON, Text
from app.core.database import Base

class JobProfile(Base):
    __tablename__ = "job_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, unique=True, nullable=False)
    required_skills = Column(JSON, nullable=False)
    preferred_skills = Column(JSON, nullable=False)
    description = Column(Text, nullable=False)
    min_experience_years = Column(Integer, default=0)
