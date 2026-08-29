from typing import List, Dict, Any
from app.schemas.workout import (
    WorkoutSplitCreate, WorkoutDayCreate, ExerciseCreate,
    AdaptivePlanResponse, AdaptiveOption
)

class AdaptiveWorkoutService:
    @staticmethod
    def generate_initial_split(
        user_goal: str = "hypertrophy",
        days_per_week: int = 5,
        focus_areas: List[str] = None
    ) -> WorkoutSplitCreate:
        """
        Builds a comprehensive workout split tailored to user's schedule, goal, and focus areas.
        """
        focus_areas = focus_areas or ["Upper Chest", "Lateral Delts", "Lats"]

        if days_per_week == 3:
            # Full Body 3-Day Split
            days = [
                WorkoutDayCreate(
                    day_number=1,
                    name="Full Body A (Chest & Quad Focus)",
                    target_muscle_groups=["Chest", "Quadriceps", "Upper Back", "Triceps"],
                    estimated_duration_minutes=60,
                    exercises=[
                        ExerciseCreate(name="Incline Dumbbell Bench Press", target_muscle="Upper Chest", sets=4, rep_range="8-10", rpe_target=8.0, rest_seconds=120, is_compound=True, order_index=1),
                        ExerciseCreate(name="Barbell Back Squat", target_muscle="Quadriceps", sets=4, rep_range="6-8", rpe_target=8.0, rest_seconds=150, is_compound=True, order_index=2),
                        ExerciseCreate(name="Chest-Supported Neutral Row", target_muscle="Upper Back", sets=3, rep_range="10-12", rpe_target=8.5, rest_seconds=90, is_compound=True, order_index=3),
                        ExerciseCreate(name="Cable Lateral Raise", target_muscle="Lateral Deltoids", sets=4, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=4),
                        ExerciseCreate(name="Overhead Cable Triceps Extension", target_muscle="Triceps Long Head", sets=3, rep_range="10-12", rpe_target=8.5, rest_seconds=60, is_compound=False, order_index=5)
                    ]
                ),
                WorkoutDayCreate(
                    day_number=2,
                    name="Full Body B (Back & Hamstring Focus)",
                    target_muscle_groups=["Lats", "Hamstrings", "Shoulders", "Biceps"],
                    estimated_duration_minutes=60,
                    exercises=[
                        ExerciseCreate(name="Romanian Deadlift", target_muscle="Hamstrings & Glutes", sets=4, rep_range="8-10", rpe_target=8.0, rest_seconds=120, is_compound=True, order_index=1),
                        ExerciseCreate(name="Lat Pulldown (Close-Grip)", target_muscle="Lats", sets=4, rep_range="8-12", rpe_target=8.5, rest_seconds=90, is_compound=True, order_index=2),
                        ExerciseCreate(name="Standing Overhead Barbell Press", target_muscle="Anterior Deltoids", sets=3, rep_range="6-8", rpe_target=8.0, rest_seconds=120, is_compound=True, order_index=3),
                        ExerciseCreate(name="Incline Dumbbell Biceps Curl", target_muscle="Biceps", sets=3, rep_range="10-12", rpe_target=8.5, rest_seconds=60, is_compound=False, order_index=4),
                        ExerciseCreate(name="Hanging Leg Raises", target_muscle="Core / Abs", sets=3, rep_range="12-15", rpe_target=8.5, rest_seconds=60, is_compound=False, order_index=5)
                    ]
                ),
                WorkoutDayCreate(
                    day_number=3,
                    name="Full Body C (Shoulders & Arms Focus)",
                    target_muscle_groups=["Chest", "Lats", "Deltoids", "Arms"],
                    estimated_duration_minutes=60,
                    exercises=[
                        ExerciseCreate(name="Flat Dumbbell Bench Press", target_muscle="Mid Chest", sets=3, rep_range="8-10", rpe_target=8.0, rest_seconds=90, is_compound=True, order_index=1),
                        ExerciseCreate(name="Bulgarian Split Squat", target_muscle="Quadriceps & Glutes", sets=3, rep_range="10-12", rpe_target=8.5, rest_seconds=90, is_compound=True, order_index=2),
                        ExerciseCreate(name="Single-Arm Cable Lat Pulldown", target_muscle="Lats", sets=3, rep_range="10-12", rpe_target=8.5, rest_seconds=75, is_compound=True, order_index=3),
                        ExerciseCreate(name="Dumbbell Lateral Raise", target_muscle="Lateral Deltoids", sets=4, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=4),
                        ExerciseCreate(name="EZ Bar Preacher Curl superset with Skullcrushers", target_muscle="Arms", sets=3, rep_range="10-12", rpe_target=9.0, rest_seconds=75, is_compound=False, order_index=5)
                    ]
                )
            ]
            split_name = "3-Day Full Body Hypertrophy Split"

        elif days_per_week == 4:
            # 4-Day Upper / Lower Split
            days = [
                WorkoutDayCreate(
                    day_number=1,
                    name="Upper Body A (Chest & Lat Focus)",
                    target_muscle_groups=["Chest", "Lats", "Shoulders", "Triceps"],
                    estimated_duration_minutes=60,
                    exercises=[
                        ExerciseCreate(name="Incline Barbell Bench Press", target_muscle="Upper Chest", sets=4, rep_range="6-8", rpe_target=8.0, rest_seconds=120, is_compound=True, order_index=1),
                        ExerciseCreate(name="Chest Supported Row", target_muscle="Mid Back & Lats", sets=4, rep_range="8-10", rpe_target=8.5, rest_seconds=90, is_compound=True, order_index=2),
                        ExerciseCreate(name="Dumbbell Flat Bench Press", target_muscle="Mid Chest", sets=3, rep_range="8-10", rpe_target=8.0, rest_seconds=90, is_compound=True, order_index=3),
                        ExerciseCreate(name="Lat Pulldown (Neutral Grip)", target_muscle="Lats", sets=3, rep_range="10-12", rpe_target=8.5, rest_seconds=90, is_compound=True, order_index=4),
                        ExerciseCreate(name="Lateral Raise (Cable)", target_muscle="Lateral Delts", sets=4, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=5),
                        ExerciseCreate(name="Triceps Rope Pushdown", target_muscle="Triceps", sets=3, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=6)
                    ]
                ),
                WorkoutDayCreate(
                    day_number=2,
                    name="Lower Body A (Quad & Calf Focus)",
                    target_muscle_groups=["Quadriceps", "Hamstrings", "Calves", "Core"],
                    estimated_duration_minutes=60,
                    exercises=[
                        ExerciseCreate(name="Barbell Back Squat", target_muscle="Quadriceps", sets=4, rep_range="6-8", rpe_target=8.0, rest_seconds=150, is_compound=True, order_index=1),
                        ExerciseCreate(name="Romanian Deadlift", target_muscle="Hamstrings", sets=4, rep_range="8-10", rpe_target=8.0, rest_seconds=120, is_compound=True, order_index=2),
                        ExerciseCreate(name="Leg Press (Foot Placed Low)", target_muscle="Quadriceps", sets=3, rep_range="10-12", rpe_target=8.5, rest_seconds=90, is_compound=True, order_index=3),
                        ExerciseCreate(name="Lying Leg Curl", target_muscle="Hamstrings", sets=3, rep_range="10-12", rpe_target=8.5, rest_seconds=75, is_compound=False, order_index=4),
                        ExerciseCreate(name="Standing Calf Raise", target_muscle="Calves", sets=4, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=5)
                    ]
                ),
                WorkoutDayCreate(
                    day_number=3,
                    name="Upper Body B (Shoulders & Arms Focus)",
                    target_muscle_groups=["Shoulders", "Upper Back", "Biceps", "Triceps"],
                    estimated_duration_minutes=60,
                    exercises=[
                        ExerciseCreate(name="Standing Dumbbell Shoulder Press", target_muscle="Anterior Delts", sets=4, rep_range="8-10", rpe_target=8.0, rest_seconds=90, is_compound=True, order_index=1),
                        ExerciseCreate(name="Weighted Pull-ups / Lat Pulldown", target_muscle="Lats", sets=4, rep_range="6-8", rpe_target=8.5, rest_seconds=120, is_compound=True, order_index=2),
                        ExerciseCreate(name="Incline Dumbbell Fly / Cable Fly", target_muscle="Upper Chest", sets=3, rep_range="10-12", rpe_target=8.5, rest_seconds=75, is_compound=False, order_index=3),
                        ExerciseCreate(name="Face Pulls (Rear Delt focus)", target_muscle="Rear Delts", sets=4, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=4),
                        ExerciseCreate(name="Incline Dumbbell Curl", target_muscle="Biceps", sets=3, rep_range="10-12", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=5),
                        ExerciseCreate(name="Overhead Triceps Extension", target_muscle="Triceps", sets=3, rep_range="10-12", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=6)
                    ]
                ),
                WorkoutDayCreate(
                    day_number=4,
                    name="Lower Body B (Hamstring & Posterior Chain)",
                    target_muscle_groups=["Hamstrings", "Glutes", "Quadriceps", "Abs"],
                    estimated_duration_minutes=60,
                    exercises=[
                        ExerciseCreate(name="Barbell Deadlift / Trap Bar Deadlift", target_muscle="Posterior Chain", sets=3, rep_range="5-6", rpe_target=8.0, rest_seconds=180, is_compound=True, order_index=1),
                        ExerciseCreate(name="Bulgarian Split Squat", target_muscle="Glutes & Quads", sets=3, rep_range="8-10", rpe_target=8.5, rest_seconds=90, is_compound=True, order_index=2),
                        ExerciseCreate(name="Seated Leg Curl", target_muscle="Hamstrings", sets=3, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=3),
                        ExerciseCreate(name="Leg Extension", target_muscle="Quadriceps", sets=3, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=4),
                        ExerciseCreate(name="Cable Woodchoppers & Plank", target_muscle="Abs", sets=3, rep_range="12-15", rpe_target=8.5, rest_seconds=60, is_compound=False, order_index=5)
                    ]
                )
            ]
            split_name = "4-Day Upper / Lower Hypertrophy Split"

        else: # 5 or 6 Days (Default: 5-Day Push/Pull/Legs + Upper/Lower)
            days = [
                WorkoutDayCreate(
                    day_number=1,
                    name="Push Day (Chest, Shoulders, Triceps)",
                    target_muscle_groups=["Chest", "Lateral Delts", "Triceps"],
                    estimated_duration_minutes=60,
                    exercises=[
                        ExerciseCreate(name="Incline Dumbbell Press", target_muscle="Upper Chest", sets=4, rep_range="8-10", rpe_target=8.5, rest_seconds=120, is_compound=True, order_index=1),
                        ExerciseCreate(name="Flat Barbell Bench Press", target_muscle="Mid Chest", sets=3, rep_range="6-8", rpe_target=8.0, rest_seconds=120, is_compound=True, order_index=2),
                        ExerciseCreate(name="Seated Dumbbell Shoulder Press", target_muscle="Anterior Delts", sets=3, rep_range="8-10", rpe_target=8.0, rest_seconds=90, is_compound=True, order_index=3),
                        ExerciseCreate(name="Cable Lateral Raise", target_muscle="Lateral Delts", sets=4, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=4),
                        ExerciseCreate(name="Low-to-High Cable Crossover", target_muscle="Upper Chest", sets=3, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=5),
                        ExerciseCreate(name="Cross-Body Cable Triceps Extension", target_muscle="Triceps", sets=3, rep_range="10-12", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=6)
                    ]
                ),
                WorkoutDayCreate(
                    day_number=2,
                    name="Pull Day (Back, Rear Delts, Biceps)",
                    target_muscle_groups=["Lats", "Upper Back", "Rear Delts", "Biceps"],
                    estimated_duration_minutes=60,
                    exercises=[
                        ExerciseCreate(name="Chest-Supported T-Bar Row", target_muscle="Upper Back & Rhomboids", sets=4, rep_range="8-10", rpe_target=8.5, rest_seconds=120, is_compound=True, order_index=1),
                        ExerciseCreate(name="Neutral Grip Lat Pulldown", target_muscle="Lats", sets=4, rep_range="8-10", rpe_target=8.5, rest_seconds=90, is_compound=True, order_index=2),
                        ExerciseCreate(name="Single-Arm Cable Row (Lat bias)", target_muscle="Lats", sets=3, rep_range="10-12", rpe_target=8.5, rest_seconds=75, is_compound=True, order_index=3),
                        ExerciseCreate(name="Reverse Pec Deck / Rear Delt Fly", target_muscle="Rear Delts", sets=4, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=4),
                        ExerciseCreate(name="Incline Dumbbell Biceps Curl", target_muscle="Biceps Long Head", sets=3, rep_range="10-12", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=5),
                        ExerciseCreate(name="Hammer Curls with Rope", target_muscle="Brachialis & Forearms", sets=3, rep_range="10-12", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=6)
                    ]
                ),
                WorkoutDayCreate(
                    day_number=3,
                    name="Legs & Abs Day (Quad & Calves Focus)",
                    target_muscle_groups=["Quadriceps", "Hamstrings", "Calves", "Abs"],
                    estimated_duration_minutes=65,
                    exercises=[
                        ExerciseCreate(name="Barbell Back Squat / Hack Squat", target_muscle="Quadriceps", sets=4, rep_range="6-8", rpe_target=8.0, rest_seconds=150, is_compound=True, order_index=1),
                        ExerciseCreate(name="Romanian Deadlift", target_muscle="Hamstrings & Glutes", sets=4, rep_range="8-10", rpe_target=8.0, rest_seconds=120, is_compound=True, order_index=2),
                        ExerciseCreate(name="Leg Extension", target_muscle="Quadriceps", sets=3, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=3),
                        ExerciseCreate(name="Seated Hamstring Curl", target_muscle="Hamstrings", sets=3, rep_range="10-12", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=4),
                        ExerciseCreate(name="Standing Calf Raise", target_muscle="Calves", sets=4, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=5),
                        ExerciseCreate(name="Hanging Knee/Leg Raise", target_muscle="Lower Abs", sets=3, rep_range="12-15", rpe_target=8.5, rest_seconds=60, is_compound=False, order_index=6)
                    ]
                ),
                WorkoutDayCreate(
                    day_number=4,
                    name="Upper Body Dynamic (Power & Width)",
                    target_muscle_groups=["Upper Chest", "Lats", "Lateral Delts", "Arms"],
                    estimated_duration_minutes=60,
                    exercises=[
                        ExerciseCreate(name="Incline Smith Machine Press", target_muscle="Upper Chest", sets=3, rep_range="8-10", rpe_target=8.5, rest_seconds=90, is_compound=True, order_index=1),
                        ExerciseCreate(name="Weighted Pull-ups", target_muscle="Lats", sets=3, rep_range="6-8", rpe_target=8.5, rest_seconds=120, is_compound=True, order_index=2),
                        ExerciseCreate(name="Dumbbell Lateral Raise (Partials + Full ROM)", target_muscle="Lateral Delts", sets=4, rep_range="12-15", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=3),
                        ExerciseCreate(name="Cable Face Pulls", target_muscle="Rear Delts & Rotator Cuff", sets=3, rep_range="12-15", rpe_target=8.5, rest_seconds=60, is_compound=False, order_index=4),
                        ExerciseCreate(name="EZ Bar Skullcrushers superset with EZ Bar Curls", target_muscle="Arms", sets=3, rep_range="10-12", rpe_target=9.0, rest_seconds=75, is_compound=False, order_index=5)
                    ]
                ),
                WorkoutDayCreate(
                    day_number=5,
                    name="Lower Body & Conditioning (Hamstring & Posterior Focus)",
                    target_muscle_groups=["Hamstrings", "Glutes", "Quads", "Core"],
                    estimated_duration_minutes=55,
                    exercises=[
                        ExerciseCreate(name="Trap Bar Deadlift", target_muscle="Posterior Chain", sets=3, rep_range="5-7", rpe_target=8.0, rest_seconds=150, is_compound=True, order_index=1),
                        ExerciseCreate(name="Bulgarian Split Squat (Dumbbells)", target_muscle="Glutes & Quads", sets=3, rep_range="8-10", rpe_target=8.5, rest_seconds=90, is_compound=True, order_index=2),
                        ExerciseCreate(name="Lying Leg Curl (Slow Eccentric)", target_muscle="Hamstrings", sets=3, rep_range="10-12", rpe_target=9.0, rest_seconds=60, is_compound=False, order_index=3),
                        ExerciseCreate(name="Walking Lunges", target_muscle="Quadriceps & Glutes", sets=3, rep_range="12 steps/leg", rpe_target=8.5, rest_seconds=75, is_compound=True, order_index=4),
                        ExerciseCreate(name="Ab Wheel Rollouts", target_muscle="Core", sets=3, rep_range="10-12", rpe_target=8.5, rest_seconds=60, is_compound=False, order_index=5)
                    ]
                )
            ]
            split_name = "5-Day Push/Pull/Legs + Upper/Lower Advanced Split"

        return WorkoutSplitCreate(
            name=split_name,
            description=f"Personalized high-frequency programming targeting {', '.join(focus_areas)} with optimal recovery curves.",
            days_per_week=days_per_week,
            is_active=True,
            days=days
        )

    @staticmethod
    def calculate_missed_workout_options(
        missed_day_name: str,
        missed_exercises: List[Dict[str, Any]],
        next_day_name: str,
        next_day_exercises: List[Dict[str, Any]],
        missed_date: str
    ) -> AdaptivePlanResponse:
        """
        Calculates 3 intelligent adaptive recovery strategies when a client misses a session.
        """
        # 1. Rollover Strategy
        rollover_option = AdaptiveOption(
            strategy="rollover",
            title="Option 1: Calendar Push & Rollover (Recommended)",
            description="Shift the missed workout to the next available training day. Pushes subsequent workouts by 1 day without losing any prescribed volume.",
            recommended_action={
                "action_type": "calendar_shift",
                "shifted_workout": missed_day_name,
                "note": "Preserves total weekly volume and original recovery period between muscle groups."
            }
        )

        # 2. Hybrid Consolidation (Merge top compounds)
        missed_compounds = [e for e in missed_exercises if e.get("is_compound", True)][:2]
        next_compounds = [e for e in next_day_exercises if e.get("is_compound", True)][:2]
        hybrid_accessories = [e for e in next_day_exercises if not e.get("is_compound", True)][:2]

        combined_exercises = []
        for idx, ex in enumerate(missed_compounds + next_compounds + hybrid_accessories, start=1):
            ex_copy = dict(ex)
            # Reduce sets slightly to balance systemic fatigue in combined session
            if ex_copy.get("sets", 3) > 3:
                ex_copy["sets"] = 3
            ex_copy["order_index"] = idx
            combined_exercises.append(ex_copy)

        hybrid_option = AdaptiveOption(
            strategy="hybrid_consolidation",
            title="Option 2: Hybrid Compound Consolidation",
            description=f"Combines the top 2 priority lifts from '{missed_day_name}' with '{next_day_name}'. Trims lower-priority accessories to keep the session under 65 minutes.",
            recommended_action={
                "action_type": "consolidate_session",
                "target_date": "Next Training Session",
                "consolidated_workout_name": f"Hybrid: {missed_day_name.split('(')[0].strip()} + {next_day_name.split('(')[0].strip()}",
                "exercises": combined_exercises,
                "estimated_duration_minutes": 65
            }
        )

        # 3. 30-Minute Express Makeup Session
        express_exercises = []
        for idx, ex in enumerate(missed_exercises[:4], start=1):
            ex_copy = dict(ex)
            ex_copy["sets"] = 2
            ex_copy["rep_range"] = "10-12"
            ex_copy["rest_seconds"] = 45
            ex_copy["order_index"] = idx
            express_exercises.append(ex_copy)

        express_option = AdaptiveOption(
            strategy="express_makeup",
            title="Option 3: 30-Minute Express High-Density Session",
            description="Perform a quick 30-minute express session today or on your rest day with reduced sets and shorter rest intervals to maintain muscle stimulus.",
            recommended_action={
                "action_type": "express_session",
                "workout_name": f"Express {missed_day_name} (30 Min)",
                "exercises": express_exercises,
                "estimated_duration_minutes": 30
            }
        )

        return AdaptivePlanResponse(
            missed_date=missed_date,
            missed_workout_name=missed_day_name,
            options=[rollover_option, hybrid_option, express_option]
        )
