from typing import List, Dict, Any
import uuid
import datetime
from fastapi import APIRouter, HTTPException, status
from app.schemas.workout import (
    WorkoutSplitPlan,
    DayWorkoutPlan,
    WorkoutCompletionLog
)
from app.schemas.adaptive import (
    MissedWorkoutRequest,
    AdaptiveRecoveryResponse,
    ApplyAdaptivePlanRequest
)
from app.db import database as db
from app.services.adaptive_scheduler import AdaptiveScheduler

router = APIRouter(prefix="/workouts", tags=["Workouts & Adaptive Rescheduling"])

@router.get("/split/{user_id}", response_model=WorkoutSplitPlan)
async def get_active_split(user_id: str):
    split = db.get_active_workout_split(user_id)
    if not split:
        raise HTTPException(status_code=404, detail="No active workout split found for this user.")
    return WorkoutSplitPlan(**split)

@router.get("/daily/{user_id}/{day_number}", response_model=DayWorkoutPlan)
async def get_daily_workout(user_id: str, day_number: int):
    split = db.get_active_workout_split(user_id)
    if not split:
        raise HTTPException(status_code=404, detail="No active workout split found.")
    
    schedule = split.get("weekly_schedule", [])
    day_plan = next((d for d in schedule if d["day_number"] == day_number), None)
    if not day_plan:
        raise HTTPException(status_code=404, detail=f"Day {day_number} not found in schedule.")
    return DayWorkoutPlan(**day_plan)

@router.post("/log-completion", status_code=status.HTTP_201_CREATED)
async def log_workout_completion(log_in: WorkoutCompletionLog):
    user = db.get_user(log_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    db.save_workout_log(log_in.dict())
    return {"status": "success", "message": "Workout logged successfully!", "log_id": log_in.log_id}

@router.get("/history/{user_id}")
async def get_workout_history(user_id: str, limit: int = 15):
    return db.get_workout_logs(user_id, limit)

@router.post("/missed-workout/options", response_model=AdaptiveRecoveryResponse)
async def get_missed_workout_options(request: MissedWorkoutRequest):
    split = db.get_active_workout_split(request.user_id)
    if not split:
        raise HTTPException(status_code=404, detail="No active workout split found for this user.")
    
    recovery_options = AdaptiveScheduler.generate_backup_plans(request, split)
    return recovery_options

@router.post("/missed-workout/apply")
async def apply_missed_workout_plan(request: ApplyAdaptivePlanRequest):
    split = db.get_active_workout_split(request.user_id)
    if not split:
        raise HTTPException(status_code=404, detail="No active workout split found.")
    
    updated_schedule = AdaptiveScheduler.apply_strategy_to_split(
        split, request.selected_strategy, request.missed_day_number
    )
    db.update_workout_split_schedule(split["id"], updated_schedule)
    
    return {
        "status": "success",
        "message": f"Applied strategy {request.selected_strategy.value}. Workout split successfully updated.",
        "split_id": split["id"]
    }
