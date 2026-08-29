import 'dart:io' show Platform;
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user_model.dart';
import '../models/physique_scan_model.dart';
import '../models/workout_split_model.dart';
import '../models/nutrition_model.dart';
import '../models/activity_model.dart';
import '../models/adaptive_model.dart';

class FitnessApiService {
  // Use 10.0.2.2 for Android Emulator, 127.0.0.1 for iOS Simulator, or server IP
  static String get baseUrl {
    if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000/api/v1';
    } else if (Platform.isIOS) {
      return 'http://127.0.0.1:8000/api/v1';
    } else {
      return 'http://localhost:8000/api/v1';
    }
  }

  // 1. User & Authentication
  static Future<UserModel> registerOrLogin({
    required String email,
    required String fullName,
    String? password,
    String? goal,
    String? splitPref,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'full_name': fullName,
        'password': password ?? 'securepass123',
        'fitness_goal': goal ?? 'hypertrophy',
        'split_preference': splitPref ?? 'PPL',
      }),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      return UserModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Auth failed: ${response.body}');
    }
  }

  static Future<UserModel> getUserProfile(int userId) async {
    final response = await http.get(Uri.parse('$baseUrl/auth/users/$userId'));
    if (response.statusCode == 200) {
      return UserModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to fetch user profile: ${response.body}');
    }
  }

  static Future<UserModel> updateUserProfile(int userId, Map<String, dynamic> data) async {
    final response = await http.put(
      Uri.parse('$baseUrl/auth/users/$userId'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(data),
    );
    if (response.statusCode == 200) {
      return UserModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to update profile: ${response.body}');
    }
  }

  // 2. Physique Assessment & Conditioning
  static Future<PhysiqueScanResult> scanPhysique({
    required int userId,
    String? imageBase64,
    String? imageUrl,
    String? notes,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/physique/scan/$userId'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'image_base64': imageBase64,
        'image_url': imageUrl,
        'notes': notes,
      }),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      return PhysiqueScanResult.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Physique scan failed: ${response.body}');
    }
  }

  static Future<List<PhysiqueScanResult>> getPhysiqueHistory(int userId) async {
    final response = await http.get(Uri.parse('$baseUrl/physique/history/$userId'));
    if (response.statusCode == 200) {
      final list = jsonDecode(response.body) as List;
      return list.map((item) => PhysiqueScanResult.fromJson(item)).toList();
    } else {
      return [];
    }
  }

  // 3. Workout Splits & Daily Routine
  static Future<WorkoutSplit> generateSplit(int userId, {int? daysPerWeek}) async {
    final query = daysPerWeek != null ? '?custom_days_per_week=$daysPerWeek' : '';
    final response = await http.post(
      Uri.parse('$baseUrl/workouts/generate-split/$userId$query'),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      return WorkoutSplit.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to generate workout split: ${response.body}');
    }
  }

  static Future<WorkoutSplit> getActiveSplit(int userId) async {
    final response = await http.get(Uri.parse('$baseUrl/workouts/active-split/$userId'));
    if (response.statusCode == 200) {
      return WorkoutSplit.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('No active workout split found: ${response.body}');
    }
  }

  static Future<WorkoutDay> getTodayWorkout(int userId) async {
    final response = await http.get(Uri.parse('$baseUrl/workouts/today/$userId'));
    if (response.statusCode == 200) {
      return WorkoutDay.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to get today routine: ${response.body}');
    }
  }

  static Future<void> logWorkoutCompletion({
    required int userId,
    required int workoutDayId,
    required int durationMinutes,
    required double caloriesBurned,
    required double averageRpe,
    String? notes,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/workouts/log-completion/$userId'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'workout_day_id': workoutDayId,
        'duration_minutes': durationMinutes,
        'calories_burned': caloriesBurned,
        'average_rpe': averageRpe,
        'notes': notes,
      }),
    );
    if (response.statusCode != 200 && response.statusCode != 201) {
      throw Exception('Failed to log workout completion');
    }
  }

  // 4. Missed Workout Adaptive Recovery
  static Future<AdaptiveBackupPlan> handleMissedWorkout({
    required int userId,
    required int missedDayNumber,
    required String strategy, // "roll_over" or "hybrid_consolidation"
    int? timeConstraintMinutes,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/workouts/missed-workout/$userId'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'missed_day_number': missedDayNumber,
        'strategy': strategy,
        'time_constraint_minutes': timeConstraintMinutes,
      }),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      return AdaptiveBackupPlan.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to compute adaptive recovery plan: ${response.body}');
    }
  }

  // 5. Food Recognition & Nutrition Scanner
  static Future<FoodScanResponse> scanMealImage({
    required int userId,
    String? imageBase64,
    String? imageUrl,
    String mealType = 'lunch',
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/nutrition/scan-meal/$userId'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'image_base64': imageBase64,
        'image_url': imageUrl,
        'meal_type': mealType,
      }),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      return FoodScanResponse.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Food scan failed: ${response.body}');
    }
  }

  static Future<void> logMealDirect({
    required int userId,
    required String mealTitle,
    required String mealType,
    required double calories,
    required double proteinG,
    required double carbsG,
    required double fatG,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/nutrition/log-meal/$userId'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'meal_title': mealTitle,
        'meal_type': mealType,
        'calories': calories,
        'protein_g': proteinG,
        'carbs_g': carbsG,
        'fat_g': fatG,
      }),
    );
    if (response.statusCode != 200 && response.statusCode != 201) {
      throw Exception('Failed to log meal');
    }
  }

  static Future<Map<String, dynamic>> getDailyNutritionSummary(int userId, {String? date}) async {
    final dateParam = date != null ? '?date=$date' : '';
    final response = await http.get(Uri.parse('$baseUrl/nutrition/summary/$userId$dateParam'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      return {
        'total_calories': 0.0,
        'total_protein_g': 0.0,
        'total_carbs_g': 0.0,
        'total_fat_g': 0.0,
        'target_calories': 2400,
        'target_protein_g': 160.0,
        'target_carbs_g': 250.0,
        'target_fat_g': 65.0,
        'meals': [],
      };
    }
  }

  // 6. Activity & Step Sync (HealthKit / Google Fit)
  static Future<ActivityLog> syncActivityData({
    required int userId,
    required int steps,
    required double activeCalories,
    required int activeMinutes,
    double? distanceMeters,
    String syncSource = 'HealthKit',
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/activity/sync/$userId'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'step_count': steps,
        'active_calories_burned': activeCalories,
        'active_minutes': activeMinutes,
        'distance_meters': distanceMeters,
        'sync_source': syncSource,
      }),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      return ActivityLog.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to sync activity');
    }
  }

  static Future<Map<String, dynamic>> getActivitySummary(int userId, {int days = 7}) async {
    final response = await http.get(Uri.parse('$baseUrl/activity/summary/$userId?days=$days'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      return {'logs': []};
    }
  }
}

  // 7. AI Personal Coach & Exercise Substitution
  static Future<Map<String, dynamic>> chatWithCoach({
    required int userId,
    required String message,
    List<Map<String, String>> conversationHistory = const [],
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/coach/chat'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'user_id': userId,
        'message': message,
        'conversation_history': conversationHistory,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Coach chat error: ${response.body}');
    }
  }

  static Future<Map<String, dynamic>> getExerciseSubstitutions({
    required int userId,
    required String currentExercise,
    String reason = 'joint_pain',
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/coach/substitute'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'user_id': userId,
        'current_exercise': currentExercise,
        'reason': reason,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Substitution failed: ${response.body}');
    }
  }

  // 8. Progressive Overload & 1RM Calculator
  static Future<Map<String, dynamic>> calculate1RM({
    required double weightKg,
    required int reps,
    String exerciseName = 'Compound Movement',
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/progression/calculate-1rm'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'weight_kg': weightKg,
        'reps': reps,
        'exercise_name': exerciseName,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('1RM calculation failed: ${response.body}');
    }
  }

  static Future<Map<String, dynamic>> recommendNextSession({
    required int userId,
    required String exerciseName,
    required double lastWeightKg,
    required int lastRepsCompleted,
    required double lastRpe,
    String targetRepRange = '8-12',
    String targetMuscleType = 'upper',
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/progression/recommend-next-session'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'user_id': userId,
        'exercise_name': exerciseName,
        'target_muscle_type': targetMuscleType,
        'target_rep_range': targetRepRange,
        'last_weight_kg': lastWeightKg,
        'last_reps_completed': lastRepsCompleted,
        'last_rpe': lastRpe,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Next session prescription failed: ${response.body}');
    }
  }

  // 9. Monetization, Subscriptions & AdMob Rewards
  static Future<Map<String, dynamic>> getUserTier(int userId) async {
    final response = await http.get(Uri.parse('$baseUrl/monetization/tier/$userId'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      return {
        'tier': 'FREE',
        'is_pro': false,
        'scan_credits_remaining': 3,
        'ads_enabled': true,
      };
    }
  }

  static Future<Map<String, dynamic>> claimRewardedAd({
    required int userId,
    required String adUnitId,
    String rewardType = 'ai_scan_credit',
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/monetization/claim-reward'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'user_id': userId,
        'ad_unit_id': adUnitId,
        'reward_type': rewardType,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to claim reward: ${response.body}');
    }
  }

  static Future<Map<String, dynamic>> upgradeTier({
    required int userId,
    required String targetTier,
    String paymentProvider = 'apple_in_app_purchase',
    String purchaseToken = 'verified_token',
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/monetization/upgrade'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'user_id': userId,
        'target_tier': targetTier,
        'payment_provider': paymentProvider,
        'purchase_token': purchaseToken,
      }),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Upgrade failed: ${response.body}');
    }
  }
