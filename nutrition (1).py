from fastapi import APIRouter, HTTPException, status
from typing import List
from app.db.database import db_session
from app.schemas.nutrition import (
    FoodScanRequest, FoodScanResponse,
    NutritionLogCreate, NutritionLogOut, FoodItemLogOut, DailyNutritionSummary
)
from app.services.ai_nutrition_service import AINutritionService

router = APIRouter(prefix="/nutrition", tags=["Nutrition & Macro Scanner"])

@router.post("/scan", response_model=FoodScanResponse)
async def scan_meal(req: FoodScanRequest):
    return await AINutritionService.scan_food_image(
        image_base64=req.image_base64,
        image_url=req.image_url,
        context_notes=req.context_notes
    )

@router.post("/log/{user_id}", response_model=NutritionLogOut, status_code=status.HTTP_201_CREATED)
def log_meal(user_id: int, meal_in: NutritionLogCreate):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO nutrition_logs (user_id, date, meal_type, image_url, total_calories, total_protein_g, total_carbs_g, total_fat_g, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            meal_in.date,
            meal_in.meal_type,
            meal_in.image_url,
            meal_in.total_calories,
            meal_in.total_protein_g,
            meal_in.total_carbs_g,
            meal_in.total_fat_g,
            meal_in.notes
        ))
        log_id = cursor.lastrowid

        food_items_out = []
        for item in meal_in.food_items:
            cursor.execute("""
            INSERT INTO food_item_logs (nutrition_log_id, food_name, estimated_portion, calories, protein_g, carbs_g, fat_g, confidence_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                log_id,
                item.food_name,
                item.estimated_portion,
                item.calories,
                item.protein_g,
                item.carbs_g,
                item.fat_g,
                item.confidence_score
            ))
            item_id = cursor.lastrowid
            food_items_out.append(FoodItemLogOut(
                id=item_id,
                nutrition_log_id=log_id,
                food_name=item.food_name,
                estimated_portion=item.estimated_portion,
                calories=item.calories,
                protein_g=item.protein_g,
                carbs_g=item.carbs_g,
                fat_g=item.fat_g,
                confidence_score=item.confidence_score
            ))

        cursor.execute("SELECT * FROM nutrition_logs WHERE id = ?", (log_id,))
        log_dict = dict(cursor.fetchone())
        log_dict["food_items"] = food_items_out
        return NutritionLogOut(**log_dict)

@router.get("/daily-summary/{user_id}/{date}", response_model=DailyNutritionSummary)
def get_daily_nutrition_summary(user_id: int, date: str):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nutrition_logs WHERE user_id = ? AND date = ?", (user_id, date))
        meals_rows = cursor.fetchall()

        meals_out = []
        tot_cal = 0.0
        tot_pro = 0.0
        tot_carb = 0.0
        tot_fat = 0.0

        for m_row in meals_rows:
            m_dict = dict(m_row)
            cursor.execute("SELECT * FROM food_item_logs WHERE nutrition_log_id = ?", (m_dict["id"],))
            items = [FoodItemLogOut(**dict(it)) for it in cursor.fetchall()]
            m_dict["food_items"] = items
            tot_cal += m_dict["total_calories"]
            tot_pro += m_dict["total_protein_g"]
            tot_carb += m_dict["total_carbs_g"]
            tot_fat += m_dict["total_fat_g"]
            meals_out.append(NutritionLogOut(**m_dict))

        return DailyNutritionSummary(
            date=date,
            total_calories=round(tot_cal, 1),
            total_protein_g=round(tot_pro, 1),
            total_carbs_g=round(tot_carb, 1),
            total_fat_g=round(tot_fat, 1),
            meals=meals_out
        )
