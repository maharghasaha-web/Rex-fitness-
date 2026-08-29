import sys
import os
sys.path.insert(0, "/working_dir/c_12bd1d258665ca82/fitness_backend")

if os.path.exists("/tmp/fitness_app.db"):
    os.remove("/tmp/fitness_app.db")

from fastapi.testclient import TestClient
from app.main import app
from app.db.database import init_db

init_db()
client = TestClient(app)

print("1. Testing Health Check...")
r = client.get("/")
assert r.status_code == 200, r.text
print("   [PASS] Health check:", r.json())

print("2. Testing User Registration...")
user_payload = {
    "email": "mahargha.client@example.com",
    "password": "SecurePassword123!",
    "full_name": "Mahargha Saha",
    "age": 28,
    "gender": "male",
    "height_cm": 178.0,
    "weight_kg": 77.0,
    "fitness_goal": "hypertrophy",
    "experience_level": "intermediate",
    "target_days_per_week": 5
}
r = client.post("/api/v1/users/register", json=user_payload)
assert r.status_code == 201, r.text
user_id = r.json()["id"]
print(f"   [PASS] Registered User ID: {user_id}")

print("3. Testing Physique Assessment Scan...")
scan_payload = {
    "image_url": "https://storage.googleapis.com/fitness-bucket/physique_front.jpg",
    "notes": "Focus on upper chest and lateral delts"
}
r = client.post(f"/api/v1/physique/scan/{user_id}", json=scan_payload)
assert r.status_code == 201, r.text
scan_res = r.json()
print("   [PASS] Physique conditioning estimated body fat:", scan_res["body_fat_estimate_range"])
print("   [PASS] Focus areas:", scan_res["focus_areas"])
print("   [PASS] Recommended split:", scan_res["recommended_split"])

print("4. Testing Workout Split Generation...")
r = client.post(f"/api/v1/workouts/generate-split/{user_id}")
assert r.status_code == 201, r.text
split_res = r.json()
print(f"   [PASS] Split '{split_res['name']}' with {len(split_res['days'])} workout days created.")
first_day = split_res["days"][0]
print(f"   [PASS] Day 1: {first_day['name']} has {len(first_day['exercises'])} exercises.")
first_day_id = first_day["id"]

print("5. Testing Logging Workout Session...")
log_payload = {
    "workout_day_id": first_day_id,
    "scheduled_date": "2026-08-28",
    "completed_date": "2026-08-28",
    "status": "completed",
    "duration_minutes": 58,
    "total_volume_kg": 4650.0,
    "calories_burned": 410.0,
    "notes": "Excellent intensity and pump on incline presses."
}
r = client.post(f"/api/v1/workouts/log/{user_id}", json=log_payload)
assert r.status_code == 200, r.text
print("   [PASS] Logged workout ID:", r.json()["id"])

print("6. Testing Missed Workout Adaptive Fallback Options...")
missed_req = {
    "missed_workout_day_id": first_day_id,
    "missed_date": "2026-08-29",
    "reason": "Heavy school schedule / urgent meeting"
}
r = client.post(f"/api/v1/workouts/adaptive/missed-workout/{user_id}", json=missed_req)
assert r.status_code == 200, r.text
adaptive_res = r.json()
print(f"   [PASS] Generated {len(adaptive_res['options'])} adaptive backup recovery options:")
for opt in adaptive_res["options"]:
    print(f"      - {opt['title']}: {opt['description']}")

print("7. Testing AI Nutrition & Macro Food Scanner...")
meal_scan_req = {
    "image_url": "https://storage.googleapis.com/fitness-bucket/meal_plate.jpg",
    "context_notes": "Post workout recovery shake with whey protein, oats, almond milk and banana"
}
r = client.post("/api/v1/nutrition/scan", json=meal_scan_req)
assert r.status_code == 200, r.text
meal_scan_res = r.json()
print(f"   [PASS] Meal Identified: {meal_scan_res['identified_meal_title']}")
print(f"   [PASS] Macros: {meal_scan_res['total_calories']} kcal | Protein: {meal_scan_res['total_protein_g']}g | Carbs: {meal_scan_res['total_carbs_g']}g | Fat: {meal_scan_res['total_fat_g']}g")

print("8. Testing Logging Meal to Daily Tracker...")
meal_log_payload = {
    "date": "2026-08-28",
    "meal_type": "post_workout",
    "image_url": meal_scan_req["image_url"],
    "total_calories": meal_scan_res["total_calories"],
    "total_protein_g": meal_scan_res["total_protein_g"],
    "total_carbs_g": meal_scan_res["total_carbs_g"],
    "total_fat_g": meal_scan_res["total_fat_g"],
    "notes": "Clean high-protein recovery shake",
    "food_items": meal_scan_res["food_items"]
}
r = client.post(f"/api/v1/nutrition/log/{user_id}", json=meal_log_payload)
assert r.status_code == 201, r.text
print("   [PASS] Meal log saved with ID:", r.json()["id"])

print("9. Testing Daily Nutrition & Calorie Summary...")
r = client.get(f"/api/v1/nutrition/daily-summary/{user_id}/2026-08-28")
assert r.status_code == 200, r.text
summary = r.json()
print(f"   [PASS] Total Daily Intake for {summary['date']}: {summary['total_calories']} kcal ({summary['total_protein_g']}g P / {summary['total_carbs_g']}g C / {summary['total_fat_g']}g F)")

print("\nALL PHASE 1 BACKEND & AI PIPELINE TESTS PASSED!")
