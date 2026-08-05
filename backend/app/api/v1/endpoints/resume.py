import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import validate_uploaded_file
from app.schemas.analysis import AnalysisResponse
from app.services.analysis_service import AnalysisService
from app.models.job_profile import JobProfile
from typing import List

router = APIRouter()
analysis_service = AnalysisService()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze", response_model=AnalysisResponse)
def analyze_resume(
    file: UploadFile = File(...),
    job_title: str = Form(...),
    db: Session = Depends(get_db)
):
    validate_uploaded_file(file)
    
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
        
    try:
        analysis = analysis_service.run_analysis(
            db=db,
            file_path=file_path,
            filename=file.filename or "resume.pdf",
            target_title=job_title
        )
        return analysis
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise e

@router.get("/roles", response_model=List[str])
def get_available_roles(db: Session = Depends(get_db)):
    profiles = db.query(JobProfile).all()
    return [p.title for p in profiles]
