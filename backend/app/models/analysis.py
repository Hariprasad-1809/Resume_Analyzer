import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    job_title = Column(String, nullable=False)
    role_match_percentage = Column(Float, nullable=False)
    existing_skills = Column(JSON, nullable=False)
    missing_skills = Column(JSON, nullable=False)
    relevant_projects = Column(JSON, nullable=False)
    relevant_experience = Column(JSON, nullable=False)
    strengths = Column(JSON, nullable=False)
    weaknesses = Column(JSON, nullable=False)
    structure_analysis = Column(JSON, nullable=False)
    formatting_analysis = Column(JSON, nullable=False)
    keyword_recommendations = Column(JSON, nullable=False)
    improvement_suggestions = Column(JSON, nullable=False)
    learning_recommendations = Column(JSON, nullable=False)
    suitable_job_roles = Column(JSON, nullable=False)
    explanations = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="analyses")
