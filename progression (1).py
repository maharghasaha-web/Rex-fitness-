from fastapi import APIRouter
from app.schemas.progression import (
    OneRepMaxCalculateRequest,
    OneRepMaxResponse,
    NextSessionRecommendationRequest,
    NextSessionRecommendationResponse
)
from app.services.progressive_overload_service import ProgressiveOverloadService

router = APIRouter(prefix="/progression", tags=["Progressive Overload & 1RM"])

@router.post("/calculate-1rm", response_model=OneRepMaxResponse)
def calculate_1rm(request: OneRepMaxCalculateRequest):
    """Calculates estimated 1RM using Epley/Brzycki formulas and returns percentage intensity tables."""
    return ProgressiveOverloadService.calculate_1rm(request)

@router.post("/recommend-next-session", response_model=NextSessionRecommendationResponse)
def recommend_next_session(request: NextSessionRecommendationRequest):
    """Prescribes double progression targets (weight, reps, RPE) for the upcoming workout session."""
    return ProgressiveOverloadService.recommend_next_session(request)
