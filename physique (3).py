from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class PhysiqueScan(Base):
    __tablename__ = "physique_scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    image_url = Column(String, nullable=True)
    body_fat_estimate_range = Column(String, nullable=True) # e.g. "13-15%"
    conditioning_summary = Column(Text, nullable=False)
    muscular_strengths = Column(JSON, default=list) # e.g. ["Deltoids", "Upper Chest"]
    focus_areas = Column(JSON, default=list) # e.g. ["Lats width", "Hamstring sweep"]
    recommended_split = Column(String, nullable=False) # e.g. "Push/Pull/Legs 5-Day"
    training_recommendations = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
