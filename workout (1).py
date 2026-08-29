from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class WorkoutSplit(Base):
    __tablename__ = "workout_splits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False) # e.g. "Custom Hypertrophy PPL"
    description = Column(Text, nullable=True)
    days_per_week = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WorkoutDay(Base):
    __tablename__ = "workout_days"

    id = Column(Integer, primary_key=True, index=True)
    split_id = Column(Integer, ForeignKey("workout_splits.id"), nullable=False, index=True)
    day_number = Column(Integer, nullable=False) # 1 to 7
    name = Column(String, nullable=False) # e.g. "Push Day A (Chest & Triceps Focus)"
    target_muscle_groups = Column(JSON, default=list)
    estimated_duration_minutes = Column(Integer, default=60)
    order_index = Column(Integer, default=0)

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_day_id = Column(Integer, ForeignKey("workout_days.id"), nullable=False, index=True)
    name = Column(String, nullable=False) # e.g. "Incline Dumbbell Press"
    target_muscle = Column(String, nullable=False) # e.g. "Upper Chest"
    sets = Column(Integer, default=3)
    rep_range = Column(String, default="8-12")
    rpe_target = Column(Float, default=8.0)
    rest_seconds = Column(Integer, default=90)
    notes = Column(Text, nullable=True)
    is_compound = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)

class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    workout_day_id = Column(Integer, ForeignKey("workout_days.id"), nullable=False)
    scheduled_date = Column(String, nullable=False) # YYYY-MM-DD
    completed_date = Column(String, nullable=True)  # YYYY-MM-DD
    status = Column(String, default="pending") # "pending", "completed", "missed", "rescheduled"
    duration_minutes = Column(Integer, nullable=True)
    total_volume_kg = Column(Float, nullable=True)
    calories_burned = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AdaptiveScheduleAction(Base):
    __tablename__ = "adaptive_schedule_actions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    missed_workout_day_id = Column(Integer, ForeignKey("workout_days.id"), nullable=False)
    missed_date = Column(String, nullable=False)
    strategy = Column(String, nullable=False) # "rollover", "hybrid_consolidation", "express_makeup"
    action_details = Column(JSON, nullable=False) # Modified exercises, new schedule, notes
    applied = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
