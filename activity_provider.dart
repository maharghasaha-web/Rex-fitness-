import 'package:flutter/material.dart';
import '../models/activity_model.dart';
import '../services/api_service.dart';
import '../services/health_service.dart';

class ActivityProvider extends ChangeNotifier {
  int _todaySteps = 0;
  double _todayCaloriesBurned = 0.0;
  int _activeMinutes = 0;
  String _syncSource = 'Pending';
  bool _isSyncing = false;
  List<ActivityLog> _recentLogs = [];

  int get todaySteps => _todaySteps;
  double get todayCaloriesBurned => _todayCaloriesBurned;
  int get activeMinutes => _activeMinutes;
  String get syncSource => _syncSource;
  bool get isSyncing => _isSyncing;
  List<ActivityLog> get recentLogs => _recentLogs;

  Future<void> syncDeviceHealth(int userId) async {
    _isSyncing = true;
    notifyListeners();

    final healthData = await HealthKitService.fetchTodayActivity();
    _todaySteps = healthData['steps'] ?? 0;
    _todayCaloriesBurned = (healthData['active_calories'] ?? 0.0).toDouble();
    _activeMinutes = healthData['active_minutes'] ?? 0;
    _syncSource = healthData['source'] ?? 'HealthKit';

    try {
      await FitnessApiService.syncActivityData(
        userId: userId,
        steps: _todaySteps,
        activeCalories: _todayCaloriesBurned,
        activeMinutes: _activeMinutes,
        syncSource: _syncSource,
      );
    } catch (e) {
      debugPrint('Sync upload note: $e');
    }

    _isSyncing = false;
    notifyListeners();
  }
}
