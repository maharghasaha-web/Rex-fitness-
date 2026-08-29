import pytest
from httpx import AsyncClient, ASGITransport
import sys
import os
sys.path.insert(0, "/working_dir/c_12bd1d258665ca82/fitness_backend")

from app.main import app
from app.db.base import Base
from app.db.session import engine

@pytest.mark.asyncio
async def test_full_pipeline():
    # 1. Initialize DB tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Health check
        resp = await client.get("/")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

        # 2. Register user
        user_payload = {
            "email": "trainer_client@example.com",
            "password": "SecurePassword123!",
            "full_name": "Alex Mercer",
            "age": 27,
            "gender": "male",
            "height_cm": 178.0,
            "weight_kg": 76.5,
            "fitness_goal": "hypertrophy",
            "experience_level": "intermediate",
            "target_days_per_week": 5
        }
        resp = await client.post("/api/v1/users/register", json=user_payload)
        assert resp.status_code == 201, resp.text
        user_data = resp.json()
        user_id = user_data["id"]
        assert user_data["email"] == "trainer_client@example.com"

        # 3. Physique Scan & Conditioning Assessment
        scan_payload = {
            "image_url": "https://storage.googleapis.com/fitness-bucket/physique_front.jpg",
            "notes": "Looking to build upper chest and wider lats"
        }
        resp = await client.post(f"/api/v1/physique/scan/{user_id}", json=scan_payload)
        assert resp.status_code == 201, resp.text
        physique_data = resp.json()
        assert "body_fat_estimate_range" in physique_data
        assert "conditioning_summary" in physique_data
        assert len(physique_data["focus_areas"]) > 0

        # 4. Generate Personalized Workout Split
        resp = await client.post(f"/api/v1/workouts/generate-split/{user_id}")
        assert resp.status_code == 201, resp.text
        split_data = resp.json()
        assert split_data["days_per_week"] == 5
        assert len(split_data["days"]) == 5
        first_day = split_data["days"][0]
        assert len(first_day["exercises"]) > 0
        first_day_id = first_day["id"]

        # 5. Log a completed workout
        log_payload = {
            "workout_day_id": first_day_id,
            "scheduled_date": "2026-08-28",
            "completed_date": "2026-08-28",
            "status": "completed",
            "duration_minutes": 55,
            "total_volume_kg": 4200.0,
            "calories_burned": 380.0,
            "notes": "Great pump on incline press"
        }
        resp = await client.post(f"/api/v1/workouts/log/{user_id}", json=log_payload)
        assert resp.status_code == 200, resp.text
        log_data = resp.json()
        assert log_data["status"] == "completed"

        # 6. Trigger Missed Workout Adaptive Recovery Strategy
        missed_payload = {
            "missed_workout_day_id": first_day_id,
            "missed_date": "2026-08-29",
            "reason": "Traveled for work"
        }
        resp = await client.post(f"/api/v1/workouts/adaptive/missed-workout/{user_id}", json=missed_payload)
        assert resp.status_code == 200, resp.text
        adaptive_data = resp.json()
        assert len(adaptive_data["options"]) == 3
        strategies = [opt["strategy"] for opt in adaptive_data["options"]]
        assert "rollover" in strategies
        assert "hybrid_consolidation" in strategies
        assert "express_makeup" in strategies

        # 7. AI Food Scanning (Multimodal Meal Recognition & Macro Breakdown)
        food_scan_payload = {
            "image_url": "https://storage.googleapis.com/fitness-bucket/meal_lunch.jpg",
            "context_notes": "High protein post-workout shake with whey, oats and banana"
        }
        resp = await client.post("/api/v1/nutrition/scan", json=food_scan_payload)
        assert resp.status_code == 200, resp.text
        nutrition_scan = resp.json()
        assert nutrition_scan["total_calories"] > 0
        assert nutrition_scan["total_protein_g"] > 0
        assert len(nutrition_scan["food_items"]) > 0

        # 8. Log Meal to Daily Nutrition
        meal_log_payload = {
            "date": "2026-08-28",
            "meal_type": "post_workout",
            "image_url": "https://storage.googleapis.com/fitness-bucket/meal_lunch.jpg",
            "total_calories": nutrition_scan["total_calories"],
            "total_protein_g": nutrition_scan["total_protein_g"],
            "total_carbs_g": nutrition_scan["total_carbs_g"],
            "total_fat_g": nutrition_scan["total_fat_g"],
            "notes": "Post workout refuel",
            "food_items": nutrition_scan["food_items"]
        }
        resp = await client.post(f"/api/v1/nutrition/log/{user_id}", json=meal_log_payload)
        assert resp.status_code == 201, resp.text
        saved_meal = resp.json()
        assert len(saved_meal["food_items"]) > 0

        # 9. Get Daily Nutrition & Macro Summary
        resp = await client.get(f"/api/v1/nutrition/daily-summary/{user_id}/2026-08-28")
        assert resp.status_code == 200, resp.text
        daily_summary = resp.json()
        assert daily_summary["total_calories"] == nutrition_scan["total_calories"]
        assert daily_summary["total_protein_g"] == nutrition_scan["total_protein_g"]
        assert len(daily_summary["meals"]) == 1
