import math
from typing import List
from app.schemas.progression import (
    OneRepMaxCalculateRequest,
    OneRepMaxResponse,
    OneRepMaxPercentage,
    NextSessionRecommendationRequest,
    NextSessionRecommendationResponse
)

class ProgressiveOverloadService:
    @staticmethod
    def calculate_1rm(request: OneRepMaxCalculateRequest) -> OneRepMaxResponse:
        """Calculates 1RM using Epley and Brzycki scientific formulas and generates intensity charts."""
        w = request.weight_kg
        r = request.reps
        
        if r == 1:
            epley_1rm = w
            brzycki_1rm = w
        else:
            epley_1rm = w * (1 + (r / 30.0))
            brzycki_1rm = w * (36.0 / (37.0 - r)) if r < 37 else epley_1rm
            
        avg_1rm = round((epley_1rm + brzycki_1rm) / 2.0, 2)
        
        # Standard intensity table
        percentages = [
            (100, 1),
            (95, 2),
            (90, 4),
            (85, 6),
            (80, 8),
            (75, 10),
            (70, 12),
            (65, 15)
        ]
        
        intensity_table = [
            OneRepMaxPercentage(
                percentage=pct,
                weight_kg=round(avg_1rm * (pct / 100.0), 1),
                estimated_reps=estimated_reps
            )
            for pct, estimated_reps in percentages
        ]
        
        return OneRepMaxResponse(
            exercise_name=request.exercise_name or "Compound Movement",
            input_weight_kg=w,
            input_reps=r,
            epley_1rm_kg=round(epley_1rm, 2),
            brzycki_1rm_kg=round(brzycki_1rm, 2),
            average_estimated_1rm_kg=avg_1rm,
            intensity_table=intensity_table
        )

    @staticmethod
    def recommend_next_session(request: NextSessionRecommendationRequest) -> NextSessionRecommendationResponse:
        """Applies double progression algorithm to prescribe next session's target weights and reps."""
        # Parse rep range e.g. "8-12"
        parts = request.target_rep_range.split("-")
        try:
            min_reps = int(parts[0].strip())
            max_reps = int(parts[1].strip())
        except Exception:
            min_reps, max_reps = 8, 12
            
        current_w = request.last_weight_kg
        completed_r = request.last_reps_completed
        rpe = request.last_rpe
        
        # Increment step: upper body +2.5kg, lower body +5.0kg
        step = 5.0 if request.target_muscle_type.lower() == "lower" else 2.5
        
        # Calculate 1RM estimate
        est_1rm = round(current_w * (1 + (completed_r / 30.0)), 2)
        
        if completed_r >= max_reps and rpe <= 8.5:
            # Hit max reps with reserve -> Increase weight, drop to min reps
            rec_action = "INCREASE_WEIGHT"
            rec_weight = current_w + step
            rec_rep_target = f"{min_reps} reps"
            target_rpe = 8.0
            logic = f"Target achieved ({completed_r} reps @ RPE {rpe}). Increase load by +{step}kg and build back up from {min_reps} reps."
        elif completed_r >= min_reps and rpe <= 8.5:
            # In target rep range with gas in the tank -> Add +1 rep next session
            rec_action = "ADD_REPS"
            rec_weight = current_w
            target_next_reps = min(completed_r + 1, max_reps)
            rec_rep_target = f"{target_next_reps} reps"
            target_rpe = 8.0
            logic = f"Good execution. Maintain {current_w}kg and aim for {target_next_reps} reps next session to satisfy double progression."
        elif completed_r < min_reps or rpe >= 9.5:
            # Struggled or form breakdown -> Technique / Maintain
            rec_action = "MAINTAIN_AND_REFINE_TEMPO"
            rec_weight = current_w
            rec_rep_target = f"{min_reps} reps"
            target_rpe = 7.5
            logic = f"High mechanical fatigue detected (RPE {rpe}). Maintain {current_w}kg, focus on 3-second eccentric tempo and clean form."
        else:
            rec_action = "MAINTAIN"
            rec_weight = current_w
            rec_rep_target = f"{completed_r} reps"
            target_rpe = 8.0
            logic = f"Maintain {current_w}kg and stabilize reps across all working sets."
            
        return NextSessionRecommendationResponse(
            exercise_name=request.exercise_name,
            recommended_action=rec_action,
            recommended_weight_kg=rec_weight,
            recommended_rep_target=rec_rep_target,
            target_rpe=target_rpe,
            coaching_logic=logic,
            estimated_1rm_kg=est_1rm
        )
