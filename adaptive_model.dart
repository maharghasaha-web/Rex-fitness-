import 'workout_split_model.dart';

class AdaptiveBackupPlan {
  final String strategy; // "roll_over" or "hybrid_consolidation"
  final String title;
  final String explanation;
  final List<String> modifiedSchedule;
  final List<Exercise>? hybridExercises;
  final int? estimatedDurationMinutes;
  final List<String> recoveryTips;

  AdaptiveBackupPlan({
    required this.strategy,
    required this.title,
    required this.explanation,
    required this.modifiedSchedule,
    this.hybridExercises,
    this.estimatedDurationMinutes,
    required this.recoveryTips,
  });

  factory AdaptiveBackupPlan.fromJson(Map<String, dynamic> json) {
    return AdaptiveBackupPlan(
      strategy: json['strategy'] ?? 'roll_over',
      title: json['title'] ?? 'Adaptive Adjustment',
      explanation: json['explanation'] ?? '',
      modifiedSchedule: List<String>.from(json['modified_schedule'] ?? []),
      hybridExercises: json['hybrid_exercises'] != null
          ? (json['hybrid_exercises'] as List)
              .map((e) => Exercise.fromJson(e))
              .toList()
          : null,
      estimatedDurationMinutes: json['estimated_duration_minutes'],
      recoveryTips: List<String>.from(json['recovery_tips'] ?? []),
    );
  }
}
