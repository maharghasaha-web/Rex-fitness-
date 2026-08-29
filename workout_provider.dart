import 'package:flutter/material.dart';
import '../models/workout_split_model.dart';
import '../models/adaptive_model.dart';
import '../services/api_service.dart';

class WorkoutProvider extends ChangeNotifier {
  WorkoutSplit? _activeSplit;
  WorkoutDay? _todayWorkout;
  AdaptiveBackupPlan? _activeBackupPlan;
  bool _isLoading = false;
  String? _errorMessage;

  // Active workout tracking state
  final Map<int, List<bool>> _completedSets = {}; // exerciseId -> list of booleans

  WorkoutSplit? get activeSplit => _activeSplit;
  WorkoutDay? get todayWorkout => _todayWorkout;
  AdaptiveBackupPlan? get activeBackupPlan => _activeBackupPlan;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  Map<int, List<bool>> get completedSets => _completedSets;

  Future<void> loadWorkoutData(int userId) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      try {
        _activeSplit = await FitnessApiService.getActiveSplit(userId);
      } catch (_) {
        _activeSplit = await FitnessApiService.generateSplit(userId);
      }
      _todayWorkout = await FitnessApiService.getTodayWorkout(userId);
      _initializeSetTracking();
    } catch (e) {
      _errorMessage = e.toString();
    }

    _isLoading = false;
    notifyListeners();
  }

  void _initializeSetTracking() {
    _completedSets.clear();
    if (_todayWorkout != null) {
      for (var exercise in _todayWorkout!.exercises) {
        _completedSets[exercise.id] = List.generate(exercise.sets, (_) => false);
      }
    }
  }

  void toggleSetCompleted(int exerciseId, int setIndex) {
    if (_completedSets.containsKey(exerciseId) && setIndex < _completedSets[exerciseId]!.length) {
      _completedSets[exerciseId]![setIndex] = !_completedSets[exerciseId]![setIndex];
      notifyListeners();
    }
  }

  bool isWorkoutCompleted() {
    if (_completedSets.isEmpty) return false;
    for (var sets in _completedSets.values) {
      if (sets.any((completed) => !completed)) return false;
    }
    return true;
  }

  Future<void> completeSession(int userId, {required int durationMinutes, required double caloriesBurned, double rpe = 8.0}) async {
    if (_todayWorkout == null) return;
    _isLoading = true;
    notifyListeners();

    try {
      await FitnessApiService.logWorkoutCompletion(
        userId: userId,
        workoutDayId: _todayWorkout!.id,
        durationMinutes: durationMinutes,
        caloriesBurned: caloriesBurned,
        averageRpe: rpe,
      );
    } catch (e) {
      _errorMessage = e.toString();
    }

    _isLoading = false;
    notifyListeners();
  }

  Future<AdaptiveBackupPlan?> requestAdaptiveFallback({
    required int userId,
    required int missedDayNumber,
    required String strategy, // "roll_over" or "hybrid_consolidation"
    int? timeLimit,
  }) async {
    _isLoading = true;
    notifyListeners();

    try {
      _activeBackupPlan = await FitnessApiService.handleMissedWorkout(
        userId: userId,
        missedDayNumber: missedDayNumber,
        strategy: strategy,
        timeConstraintMinutes: timeLimit,
      );
      _isLoading = false;
      notifyListeners();
      return _activeBackupPlan;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return null;
    }
  }
}
