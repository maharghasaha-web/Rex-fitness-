import uuid
import datetime
import hashlib
from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserResponse, UserProfileUpdate
from app.db import database as db
from app.services.physique_engine import PhysiqueEngine
from app.services.workout_engine import WorkoutEngine

router = APIRouter(prefix="/auth", tags=["Authentication & User Profile"])

def calculate_initial_macros(weight_kg: float, height_cm: float, age: int, gender: str, goal: str):
    metrics = PhysiqueEngine.calculate_bmr_and_tdee(weight_kg, height_cm, age, gender)
    tdee = metrics["tdee"]
    
    # Adjust calories based on goal
    if goal == "hypertrophy":
        daily_cals = int(tdee + 300) # Lean surplus
        protein_g = round(weight_kg * 2.2, 1) # 2.2g per kg
        fat_g = round((daily_cals * 0.25) / 9, 1)
        carb_cals = daily_cals - (protein_g * 4) - (fat_g * 9)
        carb_g = max(50.0, round(carb_cals / 4, 1))
    elif goal == "fat_loss":
        daily_cals = int(tdee - 450) # Deficit
        protein_g = round(weight_kg * 2.4, 1) # High protein to preserve LBM
        fat_g = round((daily_cals * 0.25) / 9, 1)
        carb_cals = daily_cals - (protein_g * 4) - (fat_g * 9)
        carb_g = max(50.0, round(carb_cals / 4, 1))
    else: # Recomposition / balanced
        daily_cals = int(tdee)
        protein_g = round(weight_kg * 2.0, 1)
        fat_g = round((daily_cals * 0.25) / 9, 1)
        carb_cals = daily_cals - (protein_g * 4) - (fat_g * 9)
        carb_g = max(50.0, round(carb_cals / 4, 1))
        
    return daily_cals, protein_g, carb_g, fat_g

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate):
    existing = db.get_user_by_email(user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="A user with this email already exists.")
    
    user_id = str(uuid.uuid4())
    pw_hash = hashlib.sha256(user_in.password.encode()).hexdigest()
    created_at = datetime.datetime.utcnow().isoformat() + "Z"
    
    cals, protein, carbs, fat = calculate_initial_macros(
        user_in.weight_kg, user_in.height_cm, user_in.age, user_in.gender.value, user_in.fitness_goal.value
    )
    
    user_dict = {
        "id": user_id,
        "email": user_in.email,
        "full_name": user_in.full_name,
        "password_hash": pw_hash,
        "age": user_in.age,
        "gender": user_in.gender.value,
        "height_cm": user_in.height_cm,
        "weight_kg": user_in.weight_kg,
        "fitness_goal": user_in.fitness_goal.value,
        "experience_level": user_in.experience_level.value,
        "split_preference": user_in.split_preference.value,
        "days_per_week_available": user_in.days_per_week_available,
        "dietary_preference": user_in.dietary_preference,
        "daily_calorie_target": cals,
        "daily_protein_target_g": protein,
        "daily_carb_target_g": carbs,
        "daily_fat_target_g": fat,
        "created_at": created_at
    }
    
    db.save_user(user_dict)
    
    # Auto-generate initial workout split
    split_plan = WorkoutEngine.generate_split_for_user(user_dict)
    db.save_workout_split(split_plan.dict())
    
    return UserResponse(**user_dict)

@router.get("/profile/{user_id}", response_model=UserResponse)
async def get_profile(user_id: str):
    u = db.get_user(user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found.")
    return UserResponse(**u)
