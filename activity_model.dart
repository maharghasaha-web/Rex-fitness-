class ActivityLog {
  final int id;
  final int userId;
  final String date;
  final int stepCount;
  final double activeCaloriesBurned;
  final double totalCaloriesBurned;
  final int activeMinutes;
  final double? distanceMeters;
  final String? syncSource;

  ActivityLog({
    required this.id,
    required this.userId,
    required this.date,
    required this.stepCount,
    required this.activeCaloriesBurned,
    required this.totalCaloriesBurned,
    required this.activeMinutes,
    this.distanceMeters,
    this.syncSource,
  });

  factory ActivityLog.fromJson(Map<String, dynamic> json) {
    return ActivityLog(
      id: json['id'] ?? 0,
      userId: json['user_id'] ?? 0,
      date: json['date'] ?? '',
      stepCount: json['step_count'] ?? 0,
      activeCaloriesBurned: (json['active_calories_burned'] ?? 0.0).toDouble(),
      totalCaloriesBurned: (json['total_calories_burned'] ?? 0.0).toDouble(),
      activeMinutes: json['active_minutes'] ?? 0,
      distanceMeters: json['distance_meters'] != null ? (json['distance_meters'] as num).toDouble() : null,
      syncSource: json['sync_source'],
    );
  }
}
