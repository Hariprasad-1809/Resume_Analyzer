from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.analysis import Analysis
from app.models.resume import Resume
from app.schemas.analysis import AnalysisBrief, AnalysisResponse
from app.core.exceptions import NotFoundException
from typing import List

router = APIRouter()

@router.get("", response_model=List[AnalysisBrief])
def get_history(db: Session = Depends(get_db)):
    results = db.query(
        Analysis.id,
        Analysis.resume_id,
        Analysis.job_title,
        Analysis.role_match_percentage,
        Analysis.created_at,
        Resume.filename
    ).join(Resume, Analysis.resume_id == Resume.id).order_by(Analysis.created_at.desc()).all()
    
    return [
        AnalysisBrief(
            id=r.id,
            resume_id=r.resume_id,
            job_title=r.job_title,
            role_match_percentage=r.role_match_percentage,
            created_at=r.created_at,
            filename=r.filename
        ) for r in results
    ]

@router.get("/{id}", response_model=AnalysisResponse)
def get_analysis_detail(id: str, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.id == id).first()
    if not analysis:
        raise NotFoundException("Analysis record not found.")
    
    response_data = AnalysisResponse.model_validate(analysis)
    if analysis.resume:
        response_data.resume_raw_text = analysis.resume.raw_text
    return response_data
