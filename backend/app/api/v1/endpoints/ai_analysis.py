from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
import uuid

from app.schemas.ai_request import AIAnalysisRequest
from app.schemas.ai_response import AIAnalysisResponse
from app.services.openrouter_service import (
    OpenRouterService,
    OpenRouterAuthError,
    OpenRouterForbiddenError,
    OpenRouterRateLimitError,
    OpenRouterServerError,
    OpenRouterTimeoutError,
    OpenRouterParseError,
    OpenRouterException,
)


router = APIRouter()


def get_openrouter_service() -> OpenRouterService:
    """Dependency injection for OpenRouter service."""
    return OpenRouterService()


@router.post(
    "/analyze",
    response_model=AIAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze Resume Against Job Title",
    description="Analyze a structured resume against a target job title using AI",
    responses={
        200: {
            "description": "Analysis completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "overall_match": 85,
                        "summary": "Strong candidate with relevant experience",
                        "strengths": ["Python", "React"],
                        "weaknesses": ["DevOps"],
                        "missing_skills": ["Docker"],
                        "recommended_skills": ["Kubernetes"],
                        "project_analysis": [],
                        "experience_analysis": [],
                        "resume_improvements": ["Add metrics"],
                        "learning_roadmap": [],
                        "interview_readiness": "Well prepared",
                        "suitable_roles": ["Backend Developer"],
                    }
                }
            },
        },
        400: {
            "description": "Invalid request payload",
            "content": {
                "application/json": {"example": {"detail": "Validation error"}}
            },
        },
        401: {
            "description": "Authentication failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid or expired API key"}
                }
            },
        },
        429: {
            "description": "Rate limit exceeded",
            "content": {
                "application/json": {"example": {"detail": "Rate limit exceeded"}}
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {"example": {"detail": "Internal server error"}}
            },
        },
    },
)
async def analyze_resume(
    request: AIAnalysisRequest,
    service: OpenRouterService = Depends(get_openrouter_service),
) -> AIAnalysisResponse:
    """
    Analyze a resume against a target job title.

    This endpoint accepts a structured resume (from the parser) and a job title,
    then uses AI to provide comprehensive analysis including match score, strengths,
    weaknesses, missing skills, and personalized recommendations.

    Args:
        request: AIAnalysisRequest containing job_title and resume_data
        service: OpenRouter service instance (injected)

    Returns:
        AIAnalysisResponse with detailed analysis

    Raises:
        HTTPException: For various error conditions
    """
    try:
        analysis = await service.analyze_resume(
            job_title=request.job_title, resume_data=request.resume_data
        )
        return analysis

    except OpenRouterAuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API authentication failed. Please check your API key.",
        ) from e

    except OpenRouterForbiddenError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden. Please check your API permissions.",
        ) from e

    except OpenRouterRateLimitError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        ) from e

    except OpenRouterTimeoutError as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request timeout. The analysis took too long. Please try again.",
        ) from e

    except OpenRouterParseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to parse AI response. Please try again.",
        ) from e

    except OpenRouterServerError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="External API server error. Please try again later.",
        ) from e

    except OpenRouterException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during analysis. Please try again.",
        ) from e

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Service initialization error: {str(e)}",
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from e

    finally:
        await service.close()
