from pydantic import BaseModel
from typing import List, Optional

class PhysiqueScanRequest(BaseModel):
    image_base64: Optional[str] = None
    image_url: Optional[str] = None
    notes: Optional[str] = None

class PhysiqueScanResult(BaseModel):
    body_fat_estimate_range: str
    conditioning_summary: str
    muscular_strengths: List[str]
    focus_areas: List[str]
    recommended_split: str
    training_recommendations: List[str]

class PhysiqueScanOut(PhysiqueScanResult):
    id: int
    user_id: int
    image_url: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        orm_mode = True
