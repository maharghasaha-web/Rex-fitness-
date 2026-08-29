from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from app.schemas.workout import DayWorkoutPlan, ExerciseItem

class MissedReason(str, Enum):
    TIME_CONSTRAINT = "time_constraint"
    FATIGUE_OR_SORE = "fatigue_or_sore"
    ILLNESS = "illness"
    TRAVEL_OR_EQUIPMENT = "travel_or_equipment"
    FORGOT_OR_BUSY = "forgot_or_busy"

class MissedWorkoutRequest(BaseModel):
    user_id: str
    split_id: str
    missed_day_number: int
    missed_date: str
    reason: MissedReason = MissedReason.TIME_CONSTRAINT
    available_days_remaining_in_week: int = Field(default=3, ge=1, le=6)

class AdaptiveStrategyType(str, Enum):
    ROLLOVER = "rollover"                       # Push split by 1 day, shifting rest day
    HYBRID_CONSOLIDATION = "hybrid_consolidation" # Combine key compounds of missed day with next day
    EXPRESS_MICRO_SESSION = "express_micro"     # Short 20-25 min high-intensity workout for missed volume
    SKIP_WITH_VOLUME_SPREAD = "volume_spread"   # Skip session but add 1-2 key sets into subsequent workouts

class AdaptiveOption(BaseModel):
    strategy: AdaptiveStrategyType
    title: str
    description: str
    pros: List[str]
    adjusted_routine: Optional[DayWorkoutPlan] = None
    new_weekly_schedule_overview: List[str]

class AdaptiveRecoveryResponse(BaseModel):
    missed_day_number: int
    missed_day_name: str
    missed_muscles: List[str]
    ai_coach_advice: str
    recommended_options: List[AdaptiveOption]

class ApplyAdaptivePlanRequest(BaseModel):
    user_id: str
    split_id: str
    selected_strategy: AdaptiveStrategyType
    missed_day_number: int
