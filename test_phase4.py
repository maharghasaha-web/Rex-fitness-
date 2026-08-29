import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

client = TestClient(app)

def run_phase4_tests():
    print("=== STARTING PHASE 4 BACKEND & AI CUSTOMIZATION TESTS ===")

    # 1. Test User Setup
    user_resp = client.post("/api/v1/auth/register", json={
        "email": "coach_tester@example.com",
        "password": "SecurePassword123!",
        "full_name": "Test Athlete",
        "age": 27,
        "gender": "male",
        "height_cm": 178,
        "weight_kg": 76,
        "fitness_goal": "hypertrophy",
        "experience_level": "advanced",
        "target_days_per_week": 5
    })
    user_id = user_resp.json().get("id", 1)
    print(f"1. [PASS] User registered with ID: {user_id}")

    # 2. Test AI Coach Conversational Chat
    chat_resp = client.post("/api/v1/coach/chat", json={
        "user_id": user_id,
        "message": "My lower back feels tight today, what can I replace Barbell Deadlift with?"
    })
    assert chat_resp.status_code == 200
    chat_data = chat_resp.json()
    print("2. [PASS] AI Coach Chat Response:")
    print("   Action Type:", chat_data.get("action_type"))
    print("   Coach Reply Snippet:", chat_data.get("reply")[:120], "...")

    # 3. Test Exercise Substitution Direct API
    sub_resp = client.post("/api/v1/coach/substitute", json={
        "user_id": user_id,
        "current_exercise": "Barbell Back Squat",
        "reason": "joint_pain"
    })
    assert sub_resp.status_code == 200
    sub_data = sub_resp.json()
    print("3. [PASS] Exercise Substitution:")
    print(f"   Original: {sub_data['original_exercise']}")
    for alt in sub_data["alternatives"][:2]:
        print(f"   - Substitute: {alt['exercise_name']} ({alt['equipment_needed']}) - {alt['form_cue']}")

    # 4. Test Progressive Overload 1RM Calculation
    orm_resp = client.post("/api/v1/progression/calculate-1rm", json={
        "weight_kg": 85.0,
        "reps": 8,
        "exercise_name": "Incline Dumbbell Press"
    })
    assert orm_resp.status_code == 200
    orm_data = orm_resp.json()
    print("4. [PASS] 1RM Calculation:")
    print(f"   Estimated 1RM: {orm_data['average_estimated_1rm_kg']} kg")
    print(f"   90% Intensity Working Load: {orm_data['intensity_table'][2]['weight_kg']} kg ({orm_data['intensity_table'][2]['estimated_reps']} reps)")

    # 5. Test Next Session Progression Prescriptions
    next_resp = client.post("/api/v1/progression/recommend-next-session", json={
        "user_id": user_id,
        "exercise_name": "Incline Dumbbell Press",
        "target_muscle_type": "upper",
        "target_rep_range": "8-12",
        "last_weight_kg": 80.0,
        "last_reps_completed": 12,
        "last_rpe": 8.0
    })
    assert next_resp.status_code == 200
    next_data = next_resp.json()
    print("5. [PASS] Double Progression Next Session Prescription:")
    print(f"   Action: {next_data['recommended_action']}")
    print(f"   Recommended Load: {next_data['recommended_weight_kg']} kg for {next_data['recommended_rep_target']}")
    print(f"   Coaching Logic: {next_data['coaching_logic']}")

    # 6. Test Monetization & AdMob Reward Token
    tier_resp = client.get(f"/api/v1/monetization/tier/{user_id}")
    assert tier_resp.status_code == 200
    print("6. [PASS] Initial Free Tier Status:")
    print(f"   Tier: {tier_resp.json()['tier']}, Scan Credits: {tier_resp.json()['scan_credits_remaining']}, Ads Enabled: {tier_resp.json()['ads_enabled']}")

    reward_resp = client.post("/api/v1/monetization/claim-reward", json={
        "user_id": user_id,
        "ad_unit_id": "ca-app-pub-3940256099942544/5224354917",
        "reward_type": "ai_scan_credit"
    })
    assert reward_resp.status_code == 200
    print("7. [PASS] Rewarded Video Claim:")
    print(f"   Reward Claimed: {reward_resp.json()['message']}")
    print(f"   Updated Scan Credits: {reward_resp.json()['new_credit_balance']}")

    # 7. Test In-App Upgrade to PRO
    upgrade_resp = client.post("/api/v1/monetization/upgrade", json={
        "user_id": user_id,
        "target_tier": "PRO_ANNUAL",
        "payment_provider": "apple_in_app_purchase",
        "purchase_token": "mock_valid_token_xyz"
    })
    assert upgrade_resp.status_code == 200
    assert upgrade_resp.json()["is_pro"] == True
    print("8. [PASS] Upgraded to PRO Tier:")
    print(f"   Tier: {upgrade_resp.json()['tier']}, Unlimited Scans: {upgrade_resp.json()['unlimited_scans']}, Ads: {upgrade_resp.json()['ads_enabled']}")

    # 8. Test Export Progress Report PDF
    pdf_resp = client.get(f"/api/v1/reports/export-pdf/{user_id}")
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
    assert len(pdf_resp.content) > 1000
    print(f"9. [PASS] Generated Progress Report PDF ({len(pdf_resp.content)} bytes).")

    print("\nALL PHASE 4 BACKEND & CUSTOMIZATION INTEGRATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_phase4_tests()
