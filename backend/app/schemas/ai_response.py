from pydantic import BaseModel, Field
from typing import List


class ProjectAnalysis(BaseModel):
    """Analysis of a project from resume."""

    project_name: str = Field(..., description="Name of the project")
    relevance: str = Field(
        ..., description="Relevance to target role (high/medium/low)"
    )
    impact: str = Field(..., description="Impact and achievements")
    skills_demonstrated: List[str] = Field(
        default_factory=list, description="Skills demonstrated in project"
    )
    improvement_suggestions: List[str] = Field(
        default_factory=list, description="Suggestions to improve project description"
    )


class ExperienceAnalysis(BaseModel):
    """Analysis of work experience."""

    company: str = Field(..., description="Company name")
    role: str = Field(..., description="Job role")
    duration: str = Field(..., description="Duration of employment")
    relevance: str = Field(
        ..., description="Relevance to target role (high/medium/low)"
    )
    key_achievements: List[str] = Field(
        default_factory=list, description="Key achievements highlighted"
    )
    transferable_skills: List[str] = Field(
        default_factory=list, description="Transferable skills to target role"
    )


class LearningRoadmapItem(BaseModel):
    """Learning roadmap item for skill development."""

    skill: str = Field(..., description="Skill to learn")
    priority: str = Field(..., description="Priority level (high/medium/low)")
    timeframe: str = Field(..., description="Suggested timeframe to learn")
    resources: List[str] = Field(
        default_factory=list, description="Suggested learning resources"
    )


class AIAnalysisResponse(BaseModel):
    """Response schema for AI resume analysis."""

    overall_match: int = Field(
        ..., ge=0, le=100, description="Overall match percentage (0-100)"
    )
    summary: str = Field(..., description="High-level summary of candidate fit")
    strengths: List[str] = Field(default_factory=list, description="Candidate strengths")
    weaknesses: List[str] = Field(
        default_factory=list, description="Areas for improvement"
    )
    missing_skills: List[str] = Field(
        default_factory=list, description="Critical missing skills"
    )
    recommended_skills: List[str] = Field(
        default_factory=list, description="Skills recommended to develop"
    )
    project_analysis: List[ProjectAnalysis] = Field(
        default_factory=list, description="Analysis of projects"
    )
    experience_analysis: List[ExperienceAnalysis] = Field(
        default_factory=list, description="Analysis of work experience"
    )
    resume_improvements: List[str] = Field(
        default_factory=list, description="Actionable improvements for resume"
    )
    learning_roadmap: List[LearningRoadmapItem] = Field(
        default_factory=list, description="Personalized learning roadmap"
    )
    interview_readiness: str = Field(
        ..., description="Assessment of interview readiness with recommendations"
    )
    suitable_roles: List[str] = Field(
        default_factory=list, description="Other suitable roles based on profile"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "overall_match": 85,
                "summary": "Strong full-stack developer with relevant experience",
                "strengths": ["Python expertise", "React proficiency"],
                "weaknesses": ["Limited DevOps experience"],
                "missing_skills": ["Kubernetes", "Docker"],
                "recommended_skills": ["AWS", "System Design"],
                "project_analysis": [],
                "experience_analysis": [],
                "resume_improvements": ["Add more metrics", "Highlight achievements"],
                "learning_roadmap": [],
                "interview_readiness": "Well-prepared",
                "suitable_roles": ["Backend Developer", "Senior Developer"],
            }
        }
