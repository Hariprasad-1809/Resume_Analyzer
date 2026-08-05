from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ProjectMatch(BaseModel):
    title: str
    relevance: str
    score: float
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    business_impact: Optional[str] = None
    deployment: Optional[str] = None
    github: Optional[str] = None
    live_demo: Optional[str] = None

class ExperienceMatch(BaseModel):
    title: str
    company: str
    years: float
    alignment: str
    relevance: float
    duration: Optional[str] = None
    responsibilities: Optional[List[str]] = None
    technologies: Optional[List[str]] = None
    achievements: Optional[List[str]] = None

class StructureAnalysis(BaseModel):
    sections_found: List[str]
    missing_sections: List[str]
    score: int
    feedback: str

class FormattingAnalysis(BaseModel):
    issues: List[str]
    score: int
    feedback: str
    rating: Optional[str] = None

class LearningResource(BaseModel):
    skill: str
    resource_name: str
    resource_url: str

class AnalysisCreate(BaseModel):
    resume_id: str
    job_title: str
    role_match_percentage: float
    existing_skills: List[str]
    missing_skills: List[str]
    relevant_projects: List[ProjectMatch]
    relevant_experience: List[ExperienceMatch]
    strengths: List[str]
    weaknesses: List[str]
    structure_analysis: StructureAnalysis
    formatting_analysis: FormattingAnalysis
    keyword_recommendations: List[str]
    improvement_suggestions: List[str]
    learning_recommendations: List[LearningResource]
    suitable_job_roles: List[str]
    explanations: Optional[Dict[str, Any]] = None

class AnalysisResponse(AnalysisCreate):
    id: str
    created_at: datetime
    resume_raw_text: Optional[str] = None

    class Config:
        from_attributes = True

class AnalysisBrief(BaseModel):
    id: str
    resume_id: str
    job_title: str
    role_match_percentage: float
    created_at: datetime
    filename: str

    class Config:
        from_attributes = True
