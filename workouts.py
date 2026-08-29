from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
import json
from app.db.database import db_session
from app.schemas.workout import (
    WorkoutSplitOut, WorkoutDayOut, ExerciseOut,
    WorkoutLogCreate, WorkoutLogOut, MissedWorkoutRequest, AdaptivePlanResponse
)
from app.services.adaptive_workout_service import AdaptiveWorkoutService

router = APIRouter(prefix="/workouts", tags=["Workouts & Adaptive Training"])

def _fetch_full_split(split_id: int, conn) -> WorkoutSplitOut:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workout_splits WHERE id = ?", (split_id,))
    split_row = cursor.fetchone()
    if not split_row:
        raise HTTPException(status_code=404, detail="Split not found")
    
    split_dict = dict(split_row)
    cursor.execute("SELECT * FROM workout_days WHERE split_id = ? ORDER BY day_number ASC", (split_id,))
    day_rows = cursor.fetchall()
    
    days_out = []
    for day_r in day_rows:
        day_d = dict(day_r)
        day_d["target_muscle_groups"] = json.loads(day_d["target_muscle_groups"]) if day_d["target_muscle_groups"] else []
        cursor.execute("SELECT * FROM exercises WHERE workout_day_id = ? ORDER BY order_index ASC", (day_d["id"],))
        ex_rows = cursor.fetchall()
        day_d["exercises"] = [ExerciseOut(**dict(e)) for e in ex_rows]
        days_out.append(WorkoutDayOut(**day_d))
    
    split_dict["days"] = days_out
    return WorkoutSplitOut(**split_dict)

@router.post("/generate-split/{user_id}", response_model=WorkoutSplitOut, status_code=status.HTTP_201_CREATED)
def generate_user_split(user_id: int, custom_days_per_week: Optional[int] = None):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_row = cursor.fetchone()
        if not user_row:
            raise HTTPException(status_code=404, detail="User not found")

        days_per_week = custom_days_per_week or user_row["target_days_per_week"] or 5
        generated = AdaptiveWorkoutService.generate_initial_split(
            user_goal=user_row["fitness_goal"] or "hypertrophy",
            days_per_week=days_per_week
        )

        cursor.execute("UPDATE workout_splits SET is_active = 0 WHERE user_id = ?", (user_id,))
        cursor.execute("""
        INSERT INTO workout_splits (user_id, name, description, days_per_week, is_active)
        VALUES (?, ?, ?, ?, 1)
        """, (user_id, generated.name, generated.description, generated.days_per_week))
        new_split_id = cursor.lastrowid

        for day in generated.days:
            cursor.execute("""
            INSERT INTO workout_days (split_id, day_number, name, target_muscle_groups, estimated_duration_minutes, order_index)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                new_split_id,
                day.day_number,
                day.name,
                json.dumps(day.target_muscle_groups),
                day.estimated_duration_minutes,
                day.order_index
            ))
            day_id = cursor.lastrowid

            for ex in day.exercises:
                cursor.execute("""
                INSERT INTO exercises (workout_day_id, name, target_muscle, sets, rep_range, rpe_target, rest_seconds, notes, is_compound, order_index)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    day_id,
                    ex.name,
                    ex.target_muscle,
                    ex.sets,
                    ex.rep_range,
                    ex.rpe_target,
                    ex.rest_seconds,
                    ex.notes,
                    1 if ex.is_compound else 0,
                    ex.order_index
                ))

        return _fetch_full_split(new_split_id, conn)

@router.get("/active-split/{user_id}", response_model=WorkoutSplitOut)
def get_active_split(user_id: int):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM workout_splits WHERE user_id = ? AND is_active = 1", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="No active workout split found for user")
        return _fetch_full_split(row["id"], conn)

@router.post("/log/{user_id}", response_model=WorkoutLogOut)
def log_workout(user_id: int, log_in: WorkoutLogCreate):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO workout_logs (user_id, workout_day_id, scheduled_date, completed_date, status, duration_minutes, total_volume_kg, calories_burned, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            log_in.workout_day_id,
            log_in.scheduled_date,
            log_in.completed_date,
            log_in.status,
            log_in.duration_minutes,
            log_in.total_volume_kg,
            log_in.calories_burned,
            log_in.notes
        ))
        log_id = cursor.lastrowid
        cursor.execute("SELECT * FROM workout_logs WHERE id = ?", (log_id,))
        return WorkoutLogOut(**dict(cursor.fetchone()))

@router.post("/adaptive/missed-workout/{user_id}", response_model=AdaptivePlanResponse)
def handle_missed_workout(user_id: int, req: MissedWorkoutRequest):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workout_days WHERE id = ?", (req.missed_workout_day_id,))
        missed_day = cursor.fetchone()
        if not missed_day:
            raise HTTPException(status_code=404, detail="Workout day not found")

        cursor.execute("SELECT * FROM exercises WHERE workout_day_id = ?", (req.missed_workout_day_id,))
        missed_exercises = [dict(r) for r in cursor.fetchall()]

        cursor.execute("""
        SELECT * FROM workout_days 
        WHERE split_id = ? AND day_number > ? 
        ORDER BY day_number ASC LIMIT 1
        """, (missed_day["split_id"], missed_day["day_number"]))
        next_day = cursor.fetchone()
        if not next_day:
            cursor.execute("SELECT * FROM workout_days WHERE split_id = ? ORDER BY day_number ASC LIMIT 1", (missed_day["split_id"],))
            next_day = cursor.fetchone()

        next_exercises = []
        if next_day:
            cursor.execute("SELECT * FROM exercises WHERE workout_day_id = ?", (next_day["id"],))
            next_exercises = [dict(r) for r in cursor.fetchall()]

        return AdaptiveWorkoutService.calculate_missed_workout_options(
            missed_day_name=missed_day["name"],
            missed_exercises=missed_exercises,
            next_day_name=next_day["name"] if next_day else "Next Scheduled Workout",
            next_day_exercises=next_exercises,
            missed_date=req.missed_date
        )
