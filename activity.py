from typing import List, Optional
from pydantic import BaseModel, Field

class HealthSyncRequest(BaseModel):
    user_id: str
    date: str                      # YYYY-MM-DD
    step_count: int = Field(default=0, ge=0)
    active_energy_burned_kcal: float = Field(default=0.0, ge=0)
    resting_energy_burned_kcal: Optional[float] = None
    distance_meters: Optional[float] = None
    active_minutes: Optional[int] = None
    source: str = "AppleHealthKit" # "AppleHealthKit" or "GoogleHealthConnect"

class DailyActivitySummary(BaseModel):
    user_id: str
    date: str
    step_count: int
    active_calories_burned: float
    workout_calories_burned: float
    bmr_calories: float
    total_calories_burned: float
    net_calorie_balance: float      # Consumed - Burned
    daily_step_goal: int = 10000
    step_goal_progress_percent: float
