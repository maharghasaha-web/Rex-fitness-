from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class NutritionLog(Base):
    __tablename__ = "nutrition_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(String, nullable=False, index=True) # YYYY-MM-DD
    meal_type = Column(String, nullable=False) # "breakfast", "lunch", "dinner", "snack", "post_workout"
    image_url = Column(String, nullable=True)
    total_calories = Column(Float, default=0.0)
    total_protein_g = Column(Float, default=0.0)
    total_carbs_g = Column(Float, default=0.0)
    total_fat_g = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FoodItemLog(Base):
    __tablename__ = "food_item_logs"

    id = Column(Integer, primary_key=True, index=True)
    nutrition_log_id = Column(Integer, ForeignKey("nutrition_logs.id"), nullable=False, index=True)
    food_name = Column(String, nullable=False)
    estimated_portion = Column(String, nullable=True) # e.g. "150g", "1 cup"
    calories = Column(Float, default=0.0)
    protein_g = Column(Float, default=0.0)
    carbs_g = Column(Float, default=0.0)
    fat_g = Column(Float, default=0.0)
    confidence_score = Column(Float, default=0.9)
