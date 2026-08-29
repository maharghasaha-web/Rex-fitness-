import uuid
import datetime
from typing import List, Dict, Any, Optional
from app.schemas.workout import (
    WorkoutSplitPlan,
    DayWorkoutPlan,
    ExerciseItem,
    ExerciseCategory
)

class WorkoutEngine:
    """
    Generates personalized weekly workout splits and daily exercise routines
    based on conditioning assessment, available days, and user preferences.
    """

    @staticmethod
    def _create_exercise(
        name: str,
        target_muscle: str,
        category: ExerciseCategory,
        sets: int,
        reps_range: str,
        target_rpe: float,
        rest_seconds: int,
        cues: List[str],
        priority: int
    ) -> ExerciseItem:
        return ExerciseItem(
            id=str(uuid.uuid4())[:8],
            name=name,
            target_muscle=target_muscle,
            category=category,
            sets=sets,
            reps_range=reps_range,
            target_rpe=target_rpe,
            rest_seconds=rest_seconds,
            execution_cues=cues,
            priority_order=priority
        )

    @classmethod
    def generate_ppl_4day_split(cls, user_id: str) -> WorkoutSplitPlan:
        """Push, Pull, Legs, Upper (4-Day Hybrid Split)."""
        split_id = str(uuid.uuid4())
        
        # Day 1: Push (Chest, Front/Side Delts, Triceps)
        day1_exercises = [
            cls._create_exercise(
                "Incline Barbell Bench Press (30°)", "Upper Pectorals",
                ExerciseCategory.COMPOUND, 4, "6-8", 8.5, 120,
                ["Slight arch in back", "Lower bar to clavicle level", "Drive through palms without flaring elbows"], 1
            ),
            cls._create_exercise(
                "Flat Dumbbell Press", "Mid & Lower Pectorals",
                ExerciseCategory.COMPOUND, 3, "8-10", 8.0, 90,
                ["Retract scapula into bench", "Deep stretch at bottom", "Smooth lockout"], 2
            ),
            cls._create_exercise(
                "Standing Cable Lateral Raises", "Lateral Deltoids",
                ExerciseCategory.ISOLATION, 4, "12-15", 8.5, 60,
                ["Set pulley at wrist height", "Slight forward torso lean", "Lead with elbows"], 2
            ),
            cls._create_exercise(
                "Overhead Rope Cable Tricep Extension", "Triceps Long Head",
                ExerciseCategory.ISOLATION, 3, "10-12", 8.0, 60,
                ["Keep elbows stationary", "Full stretch behind head", "Flare rope at full extension"], 3
            ),
            cls._create_exercise(
                "Cable Pec Flyes", "Inner/Lower Chest",
                ExerciseCategory.ISOLATION, 3, "12-15", 8.5, 60,
                ["Hugging a barrel cue", "2-second peak squeeze", "3-second eccentric"], 3
            )
        ]
        
        # Day 2: Pull (Back, Rear Delts, Biceps)
        day2_exercises = [
            cls._create_exercise(
                "Chest-Supported T-Bar / Machine Row", "Upper Back & Lat Thickness",
                ExerciseCategory.COMPOUND, 4, "6-8", 8.5, 120,
                ["Drive elbows back past torso", "Full stretch without rounding spine", "Pause at peak contraction"], 1
            ),
            cls._create_exercise(
                "Neutral Grip Lat Pulldown", "Latissimus Dorsi (Width)",
                ExerciseCategory.COMPOUND, 4, "8-10", 8.0, 90,
                ["Drive elbows straight down to hip pockets", "Avoid excessive momentum"], 2
            ),
            cls._create_exercise(
                "Face Pulls with External Rotation", "Rear Delts & Rotator Cuff",
                ExerciseCategory.ISOLATION, 4, "12-15", 8.0, 60,
                ["Pull rope towards forehead", "Rotate knuckles back", "Reinforces shoulder health"], 2
            ),
            cls._create_exercise(
                "Incline Dumbbell Bicep Curls", "Biceps Long Head",
                ExerciseCategory.ISOLATION, 3, "10-12", 8.5, 60,
                ["Bench at 45°", "Keep arms behind torso for deep stretch", "Supinate wrist at peak"], 3
            ),
            cls._create_exercise(
                "Standing Hammer Curls", "Brachialis & Forearms",
                ExerciseCategory.ISOLATION, 3, "10-12", 8.0, 60,
                ["Neutral grip", "Control swing", "Builds arm thickness"], 3
            )
        ]
        
        # Day 3: Legs & Core
        day3_exercises = [
            cls._create_exercise(
                "Barbell Back Squat / Hack Squat", "Quadriceps & Glutes",
                ExerciseCategory.COMPOUND, 4, "6-8", 8.5, 150,
                ["Brace core with Valsalva maneuver", "Break at hips and knees simultaneously", "Depth below parallel"], 1
            ),
            cls._create_exercise(
                "Romanian Deadlift (RDL)", "Hamstrings & Glutes",
                ExerciseCategory.COMPOUND, 3, "8-10", 8.0, 120,
                ["Push hips backwards towards wall", "Soft knee bend", "Feel deep hamstring stretch"], 1
            ),
            cls._create_exercise(
                "Leg Press (Narrow Stance)", "Quad Sweep / Vastus Lateralis",
                ExerciseCategory.ACCESSORY, 3, "10-12", 8.5, 90,
                ["Feet low on platform", "Do not allow lower back to lift off seat pad"], 2
            ),
            cls._create_exercise(
                "Seated Leg Curl", "Hamstring Hypertrophy",
                ExerciseCategory.ISOLATION, 3, "12-15", 9.0, 60,
                ["Lean slightly forward", "Control weight stack on return"], 3
            ),
            cls._create_exercise(
                "Hanging Leg Raises / Captains Chair", "Lower Rectus Abdominis",
                ExerciseCategory.ISOLATION, 3, "12-15", 8.0, 60,
                ["Curl pelvis upwards", "Avoid swinging momentum"], 3
            )
        ]
        
        # Day 4: Upper Body Hypertrophy Focus
        day4_exercises = [
            cls._create_exercise(
                "Incline Dumbbell Press (30°)", "Upper Pectorals",
                ExerciseCategory.COMPOUND, 4, "8-10", 8.5, 90,
                ["Deep range of motion", "Controlled 3-second descent"], 1
            ),
            cls._create_exercise(
                "Single-Arm Cable Lat Row", "Latissimus Dorsi",
                ExerciseCategory.COMPOUND, 3, "8-10", 8.0, 90,
                ["Pull elbow along torso", "Maintain strict hip stability"], 1
            ),
            cls._create_exercise(
                "Seated Dumbbell Overhead Shoulder Press", "Anterior & Lateral Delts",
                ExerciseCategory.COMPOUND, 3, "8-10", 8.5, 90,
                ["Keep dumbbells slightly in front in scapular plane"], 2
            ),
            cls._create_exercise(
                "Super-Set: Lateral Raises + Rear Delt Flyes", "Full Shoulder 3D Cap",
                ExerciseCategory.ISOLATION, 3, "15+15", 9.0, 60,
                ["High pump metabolic work", "Continuous tension"], 3
            ),
            cls._create_exercise(
                "Super-Set: EZ-Bar Skull Crushers + Preacher Curls", "Arms Hypertrophy",
                ExerciseCategory.ISOLATION, 3, "10-12", 8.5, 60,
                ["Strict form, peak contractions"], 3
            )
        ]

        weekly_schedule = [
            DayWorkoutPlan(
                day_number=1, day_name="Monday", session_title="Push Day (Upper Chest & Shoulder Focus)",
                target_muscle_groups=["Chest", "Shoulders", "Triceps"],
                estimated_duration_min=55, is_rest_day=False, exercises=day1_exercises
            ),
            DayWorkoutPlan(
                day_number=2, day_name="Tuesday", session_title="Pull Day (Back Density & Biceps)",
                target_muscle_groups=["Back", "Rear Delts", "Biceps"],
                estimated_duration_min=55, is_rest_day=False, exercises=day2_exercises
            ),
            DayWorkoutPlan(
                day_number=3, day_name="Wednesday", session_title="Active Recovery & Mobility Rest Day",
                target_muscle_groups=["Recovery", "Mobility"],
                estimated_duration_min=20, is_rest_day=True, exercises=[]
            ),
            DayWorkoutPlan(
                day_number=4, day_name="Thursday", session_title="Legs & Posterior Chain Power",
                target_muscle_groups=["Quadriceps", "Hamstrings", "Glutes", "Calves", "Core"],
                estimated_duration_min=60, is_rest_day=False, exercises=day3_exercises
            ),
            DayWorkoutPlan(
                day_number=5, day_name="Friday", session_title="Upper Body Specialization & Weak Point Hypertrophy",
                target_muscle_groups=["Chest", "Back", "Shoulders", "Arms"],
                estimated_duration_min=55, is_rest_day=False, exercises=day4_exercises
            ),
            DayWorkoutPlan(
                day_number=6, day_name="Saturday", session_title="Cardio & Core Conditioning / Rest Day",
                target_muscle_groups=["Cardio", "Core"],
                estimated_duration_min=30, is_rest_day=True, exercises=[]
            ),
            DayWorkoutPlan(
                day_number=7, day_name="Sunday", session_title="Full Rest & Systemic Recovery Day",
                target_muscle_groups=["Full Recovery"],
                estimated_duration_min=0, is_rest_day=True, exercises=[]
            ),
        ]

        return WorkoutSplitPlan(
            id=split_id,
            user_id=user_id,
            split_name="Push / Pull / Legs + Upper 4-Day Periodized Split",
            total_days_per_week=4,
            weekly_schedule=weekly_schedule,
            created_at=datetime.datetime.utcnow().isoformat() + "Z"
        )

    @classmethod
    def generate_split_for_user(cls, user_profile: Dict[str, Any]) -> WorkoutSplitPlan:
        # Default tailored to user profile
        user_id = user_profile.get("id", str(uuid.uuid4()))
        return cls.generate_ppl_4day_split(user_id=user_id)
