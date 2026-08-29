from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class CoachMessage(BaseModel):
    role: str = Field(..., description="'user', 'assistant', or 'system'")
    content: str

class CoachChatRequest(BaseModel):
    user_id: int
    message: str
    conversation_history: Optional[List[CoachMessage]] = []
    context_override: Optional[Dict[str, Any]] = None

class ExerciseSubstitutionRequest(BaseModel):
    user_id: int
    current_exercise: str
    target_muscle: Optional[str] = None
    reason: str = Field("equipment_unavailable", description="'equipment_unavailable', 'joint_pain', 'variety', 'injury'")
    equipment_available: Optional[List[str]] = ["barbell", "dumbbell", "cables", "machines", "bodyweight"]

class ExerciseSubstitutionItem(BaseModel):
    exercise_name: str
    target_muscle: str
    equipment_needed: str
    difficulty: str
    mechanics: str # 'compound' or 'isolation'
    reason_for_substitution: str
    form_cue: str

class ExerciseSubstitutionResponse(BaseModel):
    original_exercise: str
    substitution_reason: str
    alternatives: List[ExerciseSubstitutionItem]
    trainer_advice: str

class CoachChatResponse(BaseModel):
    reply: str
    action_type: Optional[str] = "general_advice" # 'general_advice', 'exercise_substitution', 'macro_adjustment', 'deload_recommendation'
    structured_data: Optional[Dict[str, Any]] = None
    suggested_quick_replies: List[str] = []
