from fastapi import APIRouter
from app.api.v1.endpoints import resume, history, ai_analysis

router = APIRouter()
router.include_router(resume.router, prefix="/resume", tags=["Resume"])
router.include_router(history.router, prefix="/history", tags=["History"])
router.include_router(ai_analysis.router, prefix="/ai", tags=["AI Analysis"])
