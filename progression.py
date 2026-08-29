from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class OneRepMaxCalculateRequest(BaseModel):
    weight_kg: float = Field(..., gt=0, description="Weight lifted in kg")
    reps: int = Field(..., ge=1, le=30, description="Reps performed with good form")
    exercise_name: Optional[str] = "Compound Movement"

class OneRepMaxPercentage(BaseModel):
    percentage: int
    weight_kg: float
    estimated_reps: int

class OneRepMaxResponse(BaseModel):
    exercise_name: str
    input_weight_kg: float
    input_reps: int
    epley_1rm_kg: float
    brzycki_1rm_kg: float
    average_estimated_1rm_kg: float
    intensity_table: List[OneRepMaxPercentage]

class NextSessionRecommendationRequest(BaseModel):
    user_id: int
    exercise_name: str
    target_muscle_type: str = "upper" # 'upper' or 'lower'
    target_rep_range: str = "8-12"
    last_weight_kg: float
    last_reps_completed: int
    last_rpe: float = Field(8.0, ge=5.0, le=10.0)

class NextSessionRecommendationResponse(BaseModel):
    exercise_name: str
    recommended_action: str # "INCREASE_WEIGHT", "ADD_REPS", "MAINTAIN", "DELOAD_TECHNIQUE"
    recommended_weight_kg: float
    recommended_rep_target: str
    target_rpe: float
    coaching_logic: str
    estimated_1rm_kg: float
