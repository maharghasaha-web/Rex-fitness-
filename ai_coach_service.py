from typing import Dict, Any, List, Optional
import os
import json
import logging
from app.schemas.coach import (
    CoachChatRequest, 
    CoachChatResponse, 
    ExerciseSubstitutionRequest, 
    ExerciseSubstitutionResponse,
    ExerciseSubstitutionItem
)

logger = logging.getLogger(__name__)

# Comprehensive Exercise Database with Biomechanics & Substitutions
EXERCISE_SUBSTITUTION_MAP = {
    "barbell back squat": [
        {
            "exercise_name": "Leg Press",
            "target_muscle": "Quadriceps & Glutes",
            "equipment_needed": "Machine",
            "difficulty": "Intermediate",
            "mechanics": "compound",
            "reason_for_substitution": "Removes axial spinal loading while allowing high mechanical tension on quads and glutes.",
            "form_cue": "Keep lower back flat against pad, feet shoulder-width, lower until knees reach 90 degrees."
        },
        {
            "exercise_name": "Bulgarian Split Squat (Dumbbells)",
            "target_muscle": "Quadriceps, Glutes & Adductors",
            "equipment_needed": "Dumbbells & Bench",
            "difficulty": "Advanced",
            "mechanics": "compound",
            "reason_for_substitution": "Unilateral stimulus balances muscular asymmetries with minimal spinal compression.",
            "form_cue": "Slight forward torso lean for glute engagement or upright torso for quad isolation."
        },
        {
            "exercise_name": "Hack Squat Machine",
            "target_muscle": "Quadriceps",
            "equipment_needed": "Hack Squat Machine",
            "difficulty": "Intermediate",
            "mechanics": "compound",
            "reason_for_substitution": "Fixed path of motion provides exceptional knee-flexion quad overload safely.",
            "form_cue": "Place feet low on platform for maximum quad flexion, control the eccentric descent."
        }
    ],
    "barbell bench press": [
        {
            "exercise_name": "Incline Dumbbell Press",
            "target_muscle": "Clavicular Pectoralis (Upper Chest) & Anterior Deltoids",
            "equipment_needed": "Dumbbells & Incline Bench",
            "difficulty": "Intermediate",
            "mechanics": "compound",
            "reason_for_substitution": "Dumbbells allow natural convergent joint path and greater shoulder comfort.",
            "form_cue": "Retract scapulae, angle bench at 30 degrees, press dumbbells up in a gentle arc."
        },
        {
            "exercise_name": "Weighted Chest Dips",
            "target_muscle": "Sternal/Costal Pectoralis & Triceps",
            "equipment_needed": "Dip Station / Belt",
            "difficulty": "Intermediate",
            "mechanics": "compound",
            "reason_for_substitution": "Great multi-joint builder with intense pectoral stretch at the bottom.",
            "form_cue": "Lean torso forward 30 degrees, flare elbows slightly, lower until upper arms are parallel to floor."
        },
        {
            "exercise_name": "Converging Machine Chest Press",
            "target_muscle": "Pectoralis Major",
            "equipment_needed": "Chest Press Machine",
            "difficulty": "Beginner",
            "mechanics": "compound",
            "reason_for_substitution": "Safe to train to absolute muscular failure without needing a spotter.",
            "form_cue": "Keep shoulders pinned back and down, push through palms and contract chest at apex."
        }
    ],
    "barbell deadlift": [
        {
            "exercise_name": "Romanian Deadlift (RDL) with Dumbbells",
            "target_muscle": "Hamstrings & Gluteus Maximus",
            "equipment_needed": "Dumbbells",
            "difficulty": "Intermediate",
            "mechanics": "compound",
            "reason_for_substitution": "Focuses purely on the hip hinge and eccentric hamstring stretch with less systemic fatigue.",
            "form_cue": "Push hips back as if touching a wall behind you, keep soft knee bend, hinge until stretch is felt."
        },
        {
            "exercise_name": "Trap Bar (Hex Bar) Deadlift",
            "target_muscle": "Posterior Chain & Quadriceps",
            "equipment_needed": "Trap Bar",
            "difficulty": "Intermediate",
            "mechanics": "compound",
            "reason_for_substitution": "Neutral grip and centered load reduce lower back shear forces.",
            "form_cue": "Drive floor away with mid-foot, brace core, keep chest proud throughout pull."
        },
        {
            "exercise_name": "Seated Leg Curl + 45° Back Extension",
            "target_muscle": "Hamstrings & Spinal Erectors",
            "equipment_needed": "Machine & Hyperextension Bench",
            "difficulty": "Beginner",
            "mechanics": "isolation",
            "reason_for_substitution": "Completely isolates knee flexion hamstrings and lower back without heavy spinal compression.",
            "form_cue": "Squeeze glutes at top of extension, control leg curl with a 3-second negative."
        }
    ],
    "overhead barbell press": [
        {
            "exercise_name": "Seated Dumbbell Shoulder Press",
            "target_muscle": "Anterior & Lateral Deltoids",
            "equipment_needed": "Dumbbells & Bench",
            "difficulty": "Intermediate",
            "mechanics": "compound",
            "reason_for_substitution": "Back support minimizes lumbar hyperextension while independent dumbbells prevent dominant side takeover.",
            "form_cue": "Press dumbbells slightly in front of head in scapular plane (not flared out 90 degrees)."
        },
        {
            "exercise_name": "High Incline Machine Shoulder Press",
            "target_muscle": "Deltoids",
            "equipment_needed": "Shoulder Press Machine",
            "difficulty": "Beginner",
            "mechanics": "compound",
            "reason_for_substitution": "Stable guided path allows training to failure safely with lower injury risk.",
            "form_cue": "Adjust seat so handles start at ear level, drive upwards without locking out elbows aggressively."
        }
    ]
}

class AICoachService:
    @staticmethod
    def get_exercise_substitutions(request: ExerciseSubstitutionRequest) -> ExerciseSubstitutionResponse:
        """Finds evidence-based exercise replacements based on muscle group, equipment, and constraints."""
        query_key = request.current_exercise.lower().strip()
        
        # Check direct lookup
        matches = None
        for key in EXERCISE_SUBSTITUTION_MAP:
            if key in query_key or query_key in key:
                matches = EXERCISE_SUBSTITUTION_MAP[key]
                break
                
        if not matches:
            # Fallback dynamic substitution generator
            target = request.target_muscle or "Target Muscle Group"
            matches = [
                {
                    "exercise_name": f"Dumbbell Variant for {request.current_exercise}",
                    "target_muscle": target,
                    "equipment_needed": "Dumbbells",
                    "difficulty": "Intermediate",
                    "mechanics": "compound",
                    "reason_for_substitution": f"Provides equal hypertrophy stimulus for {target} with independent unilateral load.",
                    "form_cue": "Focus on smooth eccentric contraction and full range of motion."
                },
                {
                    "exercise_name": f"Cable / Machine Equivalent for {request.current_exercise}",
                    "target_muscle": target,
                    "equipment_needed": "Cable Station / Machine",
                    "difficulty": "Beginner to Intermediate",
                    "mechanics": "isolation",
                    "reason_for_substitution": f"Maintains constant tension across the entire strength curve for {target}.",
                    "form_cue": "Hold peak contraction for 1 second and avoid momentum."
                }
            ]

        alternatives = [ExerciseSubstitutionItem(**item) for item in matches]
        
        advice = f"When substituting '{request.current_exercise}' due to {request.reason.replace('_', ' ')}, maintain progressive overload by recording your baseline weight and reps for the replacement movement."
        
        return ExerciseSubstitutionResponse(
            original_exercise=request.current_exercise,
            substitution_reason=request.reason,
            alternatives=alternatives,
            trainer_advice=advice
        )

    @staticmethod
    def chat_with_coach(request: CoachChatRequest, user_context: Optional[Dict[str, Any]] = None) -> CoachChatResponse:
        """Generates contextual personal trainer guidance."""
        user_msg = request.message.lower()
        context = user_context or {}
        user_name = context.get("full_name", "Athlete")
        goal = context.get("fitness_goal", "Hypertrophy")
        split = context.get("active_split_name", "Custom Split")

        # Intent detection
        if any(w in user_msg for w in ["replace", "substitute", "instead of", "alternative", "hurt", "pain"]):
            # Exercise substitution intent
            # Extract possible exercise
            for key in EXERCISE_SUBSTITUTION_MAP:
                if any(part in user_msg for part in key.split()):
                    sub_resp = AICoachService.get_exercise_substitutions(
                        ExerciseSubstitutionRequest(
                            user_id=request.user_id,
                            current_exercise=key.title(),
                            reason="joint_pain" if "pain" in user_msg or "hurt" in user_msg else "variety"
                        )
                    )
                    top_alt = sub_resp.alternatives[0]
                    reply = (
                        f"For **{key.title()}**, I recommend substituting with **{top_alt.exercise_name}**.\n\n"
                        f"**Why:** {top_alt.reason_for_substitution}\n"
                        f"**Key Form Cue:** {top_alt.form_cue}\n\n"
                        f"Would you like me to swap this into your active {split} workout routine?"
                    )
                    return CoachChatResponse(
                        reply=reply,
                        action_type="exercise_substitution",
                        structured_data=sub_resp.dict(),
                        suggested_quick_replies=["Swap into my routine", "Show more alternatives", "Ask form question"]
                    )

            # Generic substitution advice
            return CoachChatResponse(
                reply=f"To give you the exact replacement exercise, tell me which movement you'd like to substitute (e.g., Squat, Bench Press, Deadlift, Overhead Press) and what equipment you have on hand.",
                action_type="exercise_substitution",
                suggested_quick_replies=["Replace Barbell Bench Press", "Replace Barbell Squat", "Replace Deadlift"]
            )

        elif any(w in user_msg for w in ["protein", "macro", "diet", "vegetarian", "soya", "paneer", "meal", "calorie"]):
            # Nutrition & macro advice
            reply = (
                f"### High-Protein Nutrition Strategy for {goal.title()}\n\n"
                f"To maximize muscle protein synthesis, aim for **1.8g to 2.2g of protein per kg of body weight** distributed across 3 to 5 meals.\n\n"
                f"**Top High-Quality Protein Options:**\n"
                f"1. **Plant-Based & Vegetarian Powerhouses:**\n"
                f"   - **Soya Chunks / Meal:** ~52g protein per 100g dry weight (highest density plant source)\n"
                f"   - **Low-Fat Paneer / Tofu:** ~18–22g protein per 100g\n"
                f"   - **Pea & Soy Protein Isolate:** ~25–27g protein per scoop\n"
                f"   - **Sprouted Moong & Greek Yogurt / Hung Curd:** ~10–12g protein per 100g\n"
                f"2. **Lean Animal Sources:**\n"
                f"   - Chicken breast (31g/100g), Whole eggs & Egg whites (6g/egg), Fish (22g/100g)\n\n"
                f"*Pro Tip:* Pair legume proteins with grains (e.g., lentils + brown rice) to ensure a complete essential amino acid profile with optimal leucine content."
            )
            return CoachChatResponse(
                reply=reply,
                action_type="macro_adjustment",
                suggested_quick_replies=["Calculate my daily macros", "Scan my meal photo", "Pre-workout meal ideas"]
            )

        elif any(w in user_msg for w in ["overload", "progressive", "plateau", "increase weight", "1rm"]):
            # Progressive overload intent
            reply = (
                f"### Progressive Overload Execution Framework\n\n"
                f"Progressive overload isn't just about adding weight to the bar every session. Follow this 3-tier hierarchy:\n\n"
                f"1. **Double Progression Model (Recommended):**\n"
                f"   - Keep weight constant until you hit the top of your prescribed rep range (e.g. 3 sets of 12 reps @ RPE ≤ 8).\n"
                f"   - Next session: Increase weight by **2.5kg (5 lbs)** and aim for 8 reps. Work back up to 12 reps.\n"
                f"2. **Execution Quality & Tempo:** Slow the eccentric phase to 3 seconds before adding external load.\n"
                f"3. **Rest Intervals:** Standardize rest to 90–120s for compounds to ensure genuine muscular progression."
            )
            return CoachChatResponse(
                reply=reply,
                action_type="deload_recommendation",
                suggested_quick_replies=["View my 1RM calculator", "Check my active split progress", "Log a set"]
            )

        elif any(w in user_msg for w in ["sore", "recovery", "tired", "deload", "rest day"]):
            # Recovery & Deload advice
            reply = (
                f"### Recovery & Deload Management\n\n"
                f"Muscular adaptation happens during recovery, not in the gym.\n\n"
                f"- **Active Recovery:** 20–30 minutes of low-intensity steady-state walking (5,000–8,000 steps) improves blood flow and speeds up DOMS clearance.\n"
                f"- **Deload Signal:** If your lifts have stalled for 2+ weeks or resting heart rate is elevated, schedule a 1-week deload by reducing total volume by 40–50% while maintaining moderate intensity."
            )
            return CoachChatResponse(
                reply=reply,
                action_type="deload_recommendation",
                suggested_quick_replies=["Show missed day backup plan", "Log rest day activity", "Check sleep & hydration"]
            )

        else:
            # General AI Coach Response
            reply = (
                f"Hello {user_name}! As your dedicated AI Personal Trainer, I'm here to optimize your training and nutrition.\n\n"
                f"I can help you with:\n"
                f"• **Exercise Substitutions:** Swap out exercises due to equipment limitations or joint comfort.\n"
                f"• **Progressive Overload Tracking:** Calculate 1RM and target weights for your next session.\n"
                f"• **Nutritional & Macro Optimization:** Meal timing, protein targets, and food scanning.\n"
                f"• **Missed Workout Recovery:** Adaptive restructuring of your training split.\n\n"
                f"What would you like to work on right now?"
            )
            return CoachChatResponse(
                reply=reply,
                action_type="general_advice",
                suggested_quick_replies=["Replace an exercise", "Vegetarian high-protein diet", "Progressive overload guide", "Scan my meal"]
            )
