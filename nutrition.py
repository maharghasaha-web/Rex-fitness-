from pydantic import BaseModel
from typing import List, Optional

class FoodItemScan(BaseModel):
    food_name: str
    estimated_portion: str
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    confidence_score: float = 0.9

class FoodScanRequest(BaseModel):
    image_base64: Optional[str] = None
    image_url: Optional[str] = None
    context_notes: Optional[str] = None

class FoodScanResponse(BaseModel):
    identified_meal_title: str
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    food_items: List[FoodItemScan]
    dietary_analysis_notes: str

class NutritionLogCreate(BaseModel):
    date: str
    meal_type: str
    image_url: Optional[str] = None
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    notes: Optional[str] = None
    food_items: List[FoodItemScan] = []

class FoodItemLogOut(FoodItemScan):
    id: int
    nutrition_log_id: int

    class Config:
        orm_mode = True

class NutritionLogOut(BaseModel):
    id: int
    user_id: int
    date: str
    meal_type: str
    image_url: Optional[str] = None
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    notes: Optional[str] = None
    food_items: List[FoodItemLogOut] = []
    created_at: Optional[str] = None

    class Config:
        orm_mode = True

class DailyNutritionSummary(BaseModel):
    date: str
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    calorie_target: float = 2400.0
    protein_target_g: float = 160.0
    carbs_target_g: float = 260.0
    fat_target_g: float = 70.0
    meals: List[NutritionLogOut] = []
