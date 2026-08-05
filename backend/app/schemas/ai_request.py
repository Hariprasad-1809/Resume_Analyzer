from pydantic import BaseModel, Field, field_validator


class AIAnalysisRequest(BaseModel):
    """Request schema for AI resume analysis."""

    job_title: str = Field(
        ..., min_length=1, max_length=200, description="Target job title for analysis"
    )
    resume_data: dict = Field(
        ..., description="Structured resume data from parser"
    )

    @field_validator("job_title")
    @classmethod
    def validate_job_title(cls, value: str) -> str:
        """Validate and normalize job title."""
        if not value or not value.strip():
            raise ValueError("job_title cannot be empty")
        return value.strip()

    @field_validator("resume_data")
    @classmethod
    def validate_resume_data(cls, value: dict) -> dict:
        """Validate that resume data is not empty."""
        if not value:
            raise ValueError("resume_data cannot be empty")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "job_title": "Full Stack Developer",
                "resume_data": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "experience": [],
                    "skills": [],
                    "education": [],
                },
            }
        }
