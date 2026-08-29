import uuid
from fastapi import APIRouter, HTTPException, status
from app.schemas.activity import HealthSyncRequest, DailyActivitySummary
from app.db import database as db
from app.services.physique_engine import PhysiqueEngine

router = APIRouter(prefix="/activity", tags=["Activity & HealthKit / Health Connect Tracking"])

@router.post("/sync-health", status_code=status.HTTP_200_OK)
async def sync_health_data(request: HealthSyncRequest):
    user = db.get_user(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    activity_dict = {
        "id": str(uuid.uuid4()),
        "user_id": request.user_id,
        "date": request.date,
        "step_count": request.step_count,
        "active_energy_burned_kcal": request.active_energy_burned_kcal,
        "resting_energy_burned_kcal": request.resting_energy_burned_kcal,
        "source": request.source
    }
    db.save_activity_log(activity_dict)
    return {"status": "success", "message": "Health metrics synced successfully"}

@router.get("/summary/{user_id}/{date_str}", response_model=DailyActivitySummary)
async def get_activity_summary(user_id: str, date_str: str):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    activity = db.get_activity_log(user_id, date_str)
    steps = activity["step_count"] if activity else 0
    active_cals = activity["active_energy_burned_kcal"] if activity else 0.0
    
    # Workout calories from logged workouts on that day
    workout_logs = db.get_workout_logs(user_id, 100)
    day_workout_cals = sum(w["calories_burned_estimated"] for w in workout_logs if w["date"] == date_str)
    
    bmr_data = PhysiqueEngine.calculate_bmr_and_tdee(
        user["weight_kg"], user["height_cm"], user["age"], user["gender"]
    )
    bmr = bmr_data["bmr"]
    
    # Meals consumed for net balance
    meal_logs = db.get_meal_logs(user_id, date_str)
    consumed_cals = sum(m["total_calories"] for m in meal_logs)
    
    total_burned = bmr + active_cals + day_workout_cals
    net_balance = consumed_cals - total_burned
    
    step_goal = 10000
    progress_pct = min(100.0, round((steps / step_goal) * 100, 1))
    
    return DailyActivitySummary(
        user_id=user_id,
        date=date_str,
        step_count=steps,
        active_calories_burned=round(active_cals, 1),
        workout_calories_burned=float(day_workout_cals),
        bmr_calories=round(bmr, 1),
        total_calories_burned=round(total_burned, 1),
        net_calorie_balance=round(net_balance, 1),
        daily_step_goal=step_goal,
        step_goal_progress_percent=progress_pct
    )
