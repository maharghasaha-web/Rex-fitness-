class Exercise {
  final int id;
  final String name;
  final String targetMuscle;
  final int sets;
  final String repRange;
  final double rpeTarget;
  final int restSeconds;
  final bool isCompound;

  Exercise({
    required this.id,
    required this.name,
    required this.targetMuscle,
    required this.sets,
    required this.repRange,
    required this.rpeTarget,
    required this.restSeconds,
    required this.isCompound,
  });

  factory Exercise.fromJson(Map<String, dynamic> json) {
    return Exercise(
      id: json['id'] ?? 0,
      name: json['name'] ?? '',
      targetMuscle: json['target_muscle'] ?? '',
      sets: json['sets'] ?? 3,
      repRange: json['rep_range'] ?? '8-12',
      rpeTarget: (json['rpe_target'] ?? 8.0).toDouble(),
      restSeconds: json['rest_seconds'] ?? 90,
      isCompound: json['is_compound'] == true || json['is_compound'] == 1,
    );
  }
}

class WorkoutDay {
  final int id;
  final int dayNumber;
  final String name;
  final List<String> targetMuscleGroups;
  final int estimatedDurationMinutes;
  final List<Exercise> exercises;

  WorkoutDay({
    required this.id,
    required this.dayNumber,
    required this.name,
    required this.targetMuscleGroups,
    required this.estimatedDurationMinutes,
    required this.exercises,
  });

  factory WorkoutDay.fromJson(Map<String, dynamic> json) {
    return WorkoutDay(
      id: json['id'] ?? 0,
      dayNumber: json['day_number'] ?? 1,
      name: json['name'] ?? '',
      targetMuscleGroups: List<String>.from(json['target_muscle_groups'] ?? []),
      estimatedDurationMinutes: json['estimated_duration_minutes'] ?? 60,
      exercises: (json['exercises'] as List? ?? [])
          .map((e) => Exercise.fromJson(e))
          .toList(),
    );
  }
}

class WorkoutSplit {
  final int id;
  final String name;
  final String? description;
  final int daysPerWeek;
  final List<WorkoutDay> days;

  WorkoutSplit({
    required this.id,
    required this.name,
    this.description,
    required this.daysPerWeek,
    required this.days,
  });

  factory WorkoutSplit.fromJson(Map<String, dynamic> json) {
    return WorkoutSplit(
      id: json['id'] ?? 0,
      name: json['name'] ?? '',
      description: json['description'],
      daysPerWeek: json['days_per_week'] ?? 5,
      days: (json['days'] as List? ?? [])
          .map((d) => WorkoutDay.fromJson(d))
          .toList(),
    );
  }
}
