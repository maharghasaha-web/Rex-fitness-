from typing import List
import uuid
import datetime
from fastapi import APIRouter, HTTPException, status
from app.schemas.nutrition import (
    FoodScanRequest,
    FoodScanResponse,
    MealLogEntry,
    DailyNutritionSummary
)
from app.db import database as db
from app.services.nutrition_engine import NutritionEngine

router = APIRouter(prefix="/nutrition", tags=["Food Recognition & Macro Tracking"])

@router.post("/scan-meal", response_model=FoodScanResponse)
async def scan_meal(request: FoodScanRequest):
    user = db.get_user(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    scan_result = await NutritionEngine.scan_food_image(request)
    return scan_result

@router.post("/log-meal", response_model=MealLogEntry, status_code=status.HTTP_201_CREATED)
async def log_meal(meal: MealLogEntry):
    user = db.get_user(meal.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    db.save_meal_log(meal.dict())
    return meal

@router.get("/daily-summary/{user_id}/{date_str}", response_model=DailyNutritionSummary)
async def get_daily_nutrition_summary(user_id: str, date_str: str):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    meal_logs = db.get_meal_logs(user_id, date_str)
    summary = NutritionEngine.calculate_daily_summary(user, meal_logs, date_str)
    return summary
