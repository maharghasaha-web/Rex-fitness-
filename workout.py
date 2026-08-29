from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ExerciseBase(BaseModel):
    name: str
    target_muscle: str
    sets: int = 3
    rep_range: str = "8-12"
    rpe_target: float = 8.0
    rest_seconds: int = 90
    notes: Optional[str] = None
    is_compound: bool = True
    order_index: int = 0

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseOut(ExerciseBase):
    id: int
    workout_day_id: int

    class Config:
        orm_mode = True

class WorkoutDayBase(BaseModel):
    day_number: int
    name: str
    target_muscle_groups: List[str] = []
    estimated_duration_minutes: int = 60
    order_index: int = 0

class WorkoutDayCreate(WorkoutDayBase):
    exercises: List[ExerciseCreate] = []

class WorkoutDayOut(WorkoutDayBase):
    id: int
    split_id: int
    exercises: List[ExerciseOut] = []

    class Config:
        orm_mode = True

class WorkoutSplitBase(BaseModel):
    name: str
    description: Optional[str] = None
    days_per_week: int = 5
    is_active: bool = True

class WorkoutSplitCreate(WorkoutSplitBase):
    days: List[WorkoutDayCreate] = []

class WorkoutSplitOut(WorkoutSplitBase):
    id: int
    user_id: int
    days: List[WorkoutDayOut] = []
    created_at: Optional[str] = None

    class Config:
        orm_mode = True

class WorkoutLogCreate(BaseModel):
    workout_day_id: int
    scheduled_date: str
    completed_date: Optional[str] = None
    status: str = "completed"
    duration_minutes: Optional[int] = 60
    total_volume_kg: Optional[float] = None
    calories_burned: Optional[float] = None
    notes: Optional[str] = None

class WorkoutLogOut(WorkoutLogCreate):
    id: int
    user_id: int
    created_at: Optional[str] = None

    class Config:
        orm_mode = True

class MissedWorkoutRequest(BaseModel):
    missed_workout_day_id: int
    missed_date: str
    reason: Optional[str] = None

class AdaptiveOption(BaseModel):
    strategy: str
    title: str
    description: str
    recommended_action: Dict[str, Any]

class AdaptivePlanResponse(BaseModel):
    missed_date: str
    missed_workout_name: str
    options: List[AdaptiveOption]
