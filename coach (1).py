from fastapi import APIRouter, HTTPException
from app.db.database import db_session
from app.schemas.coach import (
    CoachChatRequest,
    CoachChatResponse,
    ExerciseSubstitutionRequest,
    ExerciseSubstitutionResponse
)
from app.services.ai_coach_service import AICoachService

router = APIRouter(prefix="/coach", tags=["AI Personal Coach"])

@router.post("/chat", response_model=CoachChatResponse)
def chat_with_coach(request: CoachChatRequest):
    """Interactive conversational fitness coaching with user context awareness."""
    user_context = {}
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT full_name, fitness_goal, experience_level FROM users WHERE id = ?", (request.user_id,))
        user_row = cursor.fetchone()
        if user_row:
            user_context = {
                "full_name": user_row["full_name"],
                "fitness_goal": user_row["fitness_goal"],
                "experience_level": user_row["experience_level"]
            }
            cursor.execute("SELECT name FROM workout_splits WHERE user_id = ? AND is_active = 1", (request.user_id,))
            split_row = cursor.fetchone()
            user_context["active_split_name"] = split_row["name"] if split_row else "Custom Routine"
    
    if request.context_override:
        user_context.update(request.context_override)
        
    return AICoachService.chat_with_coach(request, user_context)

@router.post("/substitute", response_model=ExerciseSubstitutionResponse)
def get_exercise_substitutions(request: ExerciseSubstitutionRequest):
    """Finds biomechanically sound exercise replacements based on equipment, pain, or variety."""
    return AICoachService.get_exercise_substitutions(request)
