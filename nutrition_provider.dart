import 'package:flutter/material.dart';
import '../models/nutrition_model.dart';
import '../services/api_service.dart';

class NutritionProvider extends ChangeNotifier {
  FoodScanResponse? _latestScanResult;
  Map<String, dynamic> _dailySummary = {
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
  bool _isScanning = false;
  String? _errorMessage;

  FoodScanResponse? get latestScanResult => _latestScanResult;
  Map<String, dynamic> get dailySummary => _dailySummary;
  bool get isScanning => _isScanning;
  String? get errorMessage => _errorMessage;

  Future<void> loadDailySummary(int userId) async {
    try {
      _dailySummary = await FitnessApiService.getDailyNutritionSummary(userId);
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      notifyListeners();
    }
  }

  Future<FoodScanResponse?> scanMealImage({
    required int userId,
    String? imageBase64,
    String? imageUrl,
    String mealType = 'lunch',
  }) async {
    _isScanning = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _latestScanResult = await FitnessApiService.scanMealImage(
        userId: userId,
        imageBase64: imageBase64,
        imageUrl: imageUrl,
        mealType: mealType,
      );
      _isScanning = false;
      notifyListeners();
      return _latestScanResult;
    } catch (e) {
      _errorMessage = e.toString();
      _isScanning = false;
      notifyListeners();
      return null;
    }
  }

  Future<void> logScannedMealDirect(int userId, {required String mealTitle, required String mealType, required double calories, required double proteinG, required double carbsG, required double fatG}) async {
    try {
      await FitnessApiService.logMealDirect(
        userId: userId,
        mealTitle: mealTitle,
        mealType: mealType,
        calories: calories,
        proteinG: proteinG,
        carbsG: carbsG,
        fatG: fatG,
      );
      await loadDailySummary(userId);
    } catch (e) {
      _errorMessage = e.toString();
      notifyListeners();
    }
  }
}
