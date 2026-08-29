from typing import List
from fastapi import APIRouter, HTTPException, status
from app.schemas.physique import PhysiqueScanRequest, PhysiqueAssessmentResponse
from app.db import database as db
from app.services.physique_engine import PhysiqueEngine

router = APIRouter(prefix="/physique", tags=["Physique Assessment & Conditioning"])

@router.post("/scan", response_model=PhysiqueAssessmentResponse, status_code=status.HTTP_200_OK)
async def scan_physique(request: PhysiqueScanRequest):
    user = db.get_user(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    assessment = await PhysiqueEngine.analyze_physique(request, user)
    db.save_physique_assessment(assessment.dict())
    
    return assessment

@router.get("/history/{user_id}", response_model=List[PhysiqueAssessmentResponse])
async def get_physique_history(user_id: str):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    assessments = db.get_physique_assessments(user_id)
    return [PhysiqueAssessmentResponse(**a) for a in assessments]
