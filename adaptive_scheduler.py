from typing import List, Dict, Any, Optional
import copy
import uuid
from app.schemas.adaptive import (
    MissedWorkoutRequest,
    AdaptiveRecoveryResponse,
    AdaptiveOption,
    AdaptiveStrategyType
)
from app.schemas.workout import DayWorkoutPlan, ExerciseItem, ExerciseCategory

class AdaptiveScheduler:
    """
    Intelligent dynamic rescheduling engine that automatically calculates backup plans
    and volume rebalancing whenever a client misses a training session.
    """

    @classmethod
    def generate_backup_plans(
        cls,
        missed_request: MissedWorkoutRequest,
        current_split: Dict[str, Any]
    ) -> AdaptiveRecoveryResponse:
        schedule: List[Dict[str, Any]] = current_split.get("weekly_schedule", [])
        missed_day_num = missed_request.missed_day_number
        
        # Find missed day details
        missed_day = next((d for d in schedule if d["day_number"] == missed_day_num), None)
        if not missed_day or missed_day.get("is_rest_day"):
            # Default fallback if non-training day or not found
            missed_day = schedule[0]
            
        missed_muscles = missed_day.get("target_muscle_groups", ["Chest", "Shoulders", "Triceps"])
        missed_exercises = missed_day.get("exercises", [])
        
        # Find next scheduled workout day
        next_day = None
        for d in schedule:
            if d["day_number"] > missed_day_num and not d.get("is_rest_day"):
                next_day = d
                break
        if not next_day:
            next_day = next((d for d in schedule if not d.get("is_rest_day")), schedule[0])

        options: List[AdaptiveOption] = []

        # -------------------------------------------------------------
        # OPTION 1: Split Roll-Over (Shift schedule forward, absorb rest day)
        # -------------------------------------------------------------
        rollover_overview = [
            f"Day {missed_day_num + 1}: Perform Missed [{missed_day['session_title']}]",
            f"Day {missed_day_num + 2}: Perform Next [{next_day['session_title']}]",
            "Shifts upcoming rest day to end of the week to maintain 100% weekly training volume."
        ]
        options.append(AdaptiveOption(
            strategy=AdaptiveStrategyType.ROLLOVER,
            title="Option 1: Schedule Roll-Over (Recommended for Maximum Hypertrophy)",
            description="Shifts the missed workout into your next available session. Your rest day moves to the weekend, ensuring zero loss of total muscle volume.",
            pros=[
                "Preserves 100% of your programmed weekly sets and muscle stimulus",
                "No exercises need to be cut or rushed",
                "Maintains progressive overload tracking on all lifts"
            ],
            adjusted_routine=DayWorkoutPlan(**missed_day),
            new_weekly_schedule_overview=rollover_overview
        ))

        # -------------------------------------------------------------
        # OPTION 2: Hybrid Compound Consolidation (Merge Key Compounds)
        # -------------------------------------------------------------
        # Extract top 2 priority exercises from missed day
        missed_compounds = [
            e for e in missed_exercises if e.get("priority_order", 3) <= 2
        ][:2]
        
        # Extract top 3 exercises from next day
        next_day_exercises = next_day.get("exercises", [])
        next_compounds = [
            e for e in next_day_exercises if e.get("priority_order", 3) <= 2
        ][:3]

        hybrid_exercises: List[ExerciseItem] = []
        # Add missed compounds first
        for ec in missed_compounds:
            h_item = ExerciseItem(**ec)
            h_item.sets = min(h_item.sets, 3) # capped to 3 sets for efficiency
            hybrid_exercises.append(h_item)
        for nc in next_compounds:
            h_item = ExerciseItem(**nc)
            h_item.sets = min(h_item.sets, 3)
            hybrid_exercises.append(h_item)

        hybrid_plan = DayWorkoutPlan(
            day_number=next_day["day_number"],
            day_name=f"Hybrid Consolidation Session ({next_day['day_name']})",
            session_title=f"Hybrid Power: {', '.join(missed_muscles[:2])} + {', '.join(next_day['target_muscle_groups'][:2])}",
            target_muscle_groups=list(set(missed_muscles[:2] + next_day["target_muscle_groups"][:2])),
            estimated_duration_min=50,
            is_rest_day=False,
            exercises=hybrid_exercises
        )

        options.append(AdaptiveOption(
            strategy=AdaptiveStrategyType.HYBRID_CONSOLIDATION,
            title="Option 2: Hybrid Compound Consolidation (Time-Saver)",
            description="Merges the most impactful compound lifts from your missed workout with your next session, eliminating accessory fatigue and finishing in 50 minutes.",
            pros=[
                "Maintains stimulus on all prime movers without extending your weekly calendar",
                "Keeps your scheduled rest days on their original dates",
                "Maximizes compound efficiency and mechanical tension"
            ],
            adjusted_routine=hybrid_plan,
            new_weekly_schedule_overview=[
                f"Next Session: Hybrid workout combining {missed_day['target_muscle_groups'][0]} & {next_day['target_muscle_groups'][0]}",
                "Remaining split days continue as normal"
            ]
        ))

        # -------------------------------------------------------------
        # OPTION 3: 25-Minute Express Micro-Session
        # -------------------------------------------------------------
        express_exercises = []
        for ex in missed_exercises[:3]:
            e_item = ExerciseItem(**ex)
            e_item.sets = 3
            e_item.reps_range = "10-12 (Rest-Pause)"
            e_item.rest_seconds = 45
            express_exercises.append(e_item)

        express_plan = DayWorkoutPlan(
            day_number=missed_day_num,
            day_name="Express Catch-Up",
            session_title=f"25-Min Express Density: {missed_day['session_title']}",
            target_muscle_groups=missed_muscles,
            estimated_duration_min=25,
            is_rest_day=False,
            exercises=express_exercises
        )

        options.append(AdaptiveOption(
            strategy=AdaptiveStrategyType.EXPRESS_MICRO_SESSION,
            title="Option 3: 25-Minute High-Density Express Session",
            description="A condensed, high-density superset routine designed for busy days to stimulate muscle protein synthesis in under 25 minutes.",
            pros=[
                "Requires only 25 minutes of gym or home equipment time",
                "High metabolic burn and pump through shortened rest periods",
                "Prevents muscle deconditioning"
            ],
            adjusted_routine=express_plan,
            new_weekly_schedule_overview=[
                "Complete the 25-minute micro-session today or tomorrow morning",
                "Resume standard schedule immediately afterward"
            ]
        ))

        ai_advice = (
            f"Missing a session for {', '.join(missed_muscles)} happens to everyone! "
            f"Consistency across months matters far more than a single day. "
            f"If your schedule permits, **Option 1 (Roll-Over)** will keep 100% of your gains on track. "
            f"If you are short on time this week, choose **Option 2 (Hybrid Consolidation)** to hit the essential compound lifts."
        )

        return AdaptiveRecoveryResponse(
            missed_day_number=missed_day_num,
            missed_day_name=missed_day.get("day_name", f"Day {missed_day_num}"),
            missed_muscles=missed_muscles,
            ai_coach_advice=ai_advice,
            recommended_options=options
        )

    @classmethod
    def apply_strategy_to_split(
        cls,
        current_split: Dict[str, Any],
        strategy: AdaptiveStrategyType,
        missed_day_num: int
    ) -> List[Dict[str, Any]]:
        """Updates the active split schedule based on selected recovery strategy."""
        schedule = copy.deepcopy(current_split.get("weekly_schedule", []))
        
        if strategy == AdaptiveStrategyType.ROLLOVER:
            # Shift workout days forward
            active_workouts = [d for d in schedule if not d.get("is_rest_day")]
            rest_days = [d for d in schedule if d.get("is_rest_day")]
            
            # Rotate workouts so missed day is next
            reordered = []
            # Find the missed index among active workouts
            missed_idx = 0
            for i, w in enumerate(active_workouts):
                if w["day_number"] == missed_day_num:
                    missed_idx = i
                    break
            
            reordered_active = active_workouts[missed_idx:] + active_workouts[:missed_idx]
            
            # Reassign into 7-day calendar
            new_schedule = []
            act_ptr = 0
            for day_i in range(1, 8):
                if act_ptr < len(reordered_active) and day_i <= len(reordered_active) + 1:
                    w = reordered_active[act_ptr]
                    w["day_number"] = day_i
                    w["day_name"] = f"Day {day_i}"
                    new_schedule.append(w)
                    act_ptr += 1
                else:
                    new_schedule.append({
                        "day_number": day_i,
                        "day_name": f"Day {day_i}",
                        "session_title": "Rest & Recovery Day",
                        "target_muscle_groups": ["Recovery"],
                        "estimated_duration_min": 0,
                        "is_rest_day": True,
                        "exercises": []
                    })
            return new_schedule
            
        elif strategy == AdaptiveStrategyType.HYBRID_CONSOLIDATION:
            # Find next workout day and replace with hybrid
            missed_day = next((d for d in schedule if d["day_number"] == missed_day_num), schedule[0])
            for d in schedule:
                if d["day_number"] > missed_day_num and not d.get("is_rest_day"):
                    # Consolidate into this day
                    missed_compounds = [e for e in missed_day.get("exercises", []) if e.get("priority_order", 3) <= 2][:2]
                    next_compounds = [e for e in d.get("exercises", []) if e.get("priority_order", 3) <= 2][:3]
                    d["session_title"] = f"Hybrid: {missed_day['target_muscle_groups'][0]} & {d['target_muscle_groups'][0]}"
                    d["target_muscle_groups"] = list(set(missed_day["target_muscle_groups"][:2] + d["target_muscle_groups"][:2]))
                    d["exercises"] = missed_compounds + next_compounds
                    break
            return schedule

        return schedule
