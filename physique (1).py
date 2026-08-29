from fastapi import APIRouter, HTTPException, status
from typing import List
import json
from app.db.database import db_session
from app.schemas.physique import PhysiqueScanRequest, PhysiqueScanOut
from app.services.ai_physique_service import AIPhysiqueService

router = APIRouter(prefix="/physique", tags=["Physique Analysis & Conditioning"])

@router.post("/scan/{user_id}", response_model=PhysiqueScanOut, status_code=status.HTTP_201_CREATED)
async def scan_physique(user_id: int, request: PhysiqueScanRequest):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_row = cursor.fetchone()
        if not user_row:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_context = {
            "fitness_goal": user_row["fitness_goal"],
            "experience_level": user_row["experience_level"],
            "target_days_per_week": user_row["target_days_per_week"]
        }

    ai_result = await AIPhysiqueService.analyze_physique(
        image_base64=request.image_base64,
        image_url=request.image_url,
        user_context=user_context
    )

    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO physique_scans (
            user_id, image_url, body_fat_estimate_range, conditioning_summary,
            muscular_strengths, focus_areas, recommended_split, training_recommendations
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            request.image_url or "uploaded_media_scan.jpg",
            ai_result.body_fat_estimate_range,
            ai_result.conditioning_summary,
            json.dumps(ai_result.muscular_strengths),
            json.dumps(ai_result.focus_areas),
            ai_result.recommended_split,
            json.dumps(ai_result.training_recommendations)
        ))
        scan_id = cursor.lastrowid
        cursor.execute("SELECT * FROM physique_scans WHERE id = ?", (scan_id,))
        row = dict(cursor.fetchone())
        row["muscular_strengths"] = json.loads(row["muscular_strengths"])
        row["focus_areas"] = json.loads(row["focus_areas"])
        row["training_recommendations"] = json.loads(row["training_recommendations"])
        return PhysiqueScanOut(**row)

@router.get("/history/{user_id}", response_model=List[PhysiqueScanOut])
def get_physique_history(user_id: int):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM physique_scans WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        rows = cursor.fetchall()
        scans = []
        for r in rows:
            d = dict(r)
            d["muscular_strengths"] = json.loads(d["muscular_strengths"])
            d["focus_areas"] = json.loads(d["focus_areas"])
            d["training_recommendations"] = json.loads(d["training_recommendations"])
            scans.append(PhysiqueScanOut(**d))
        return scans
