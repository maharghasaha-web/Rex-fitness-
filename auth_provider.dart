import 'package:flutter/material.dart';
import '../models/user_model.dart';
import '../services/api_service.dart';

class AuthProvider extends ChangeNotifier {
  UserModel? _currentUser;
  bool _isLoading = false;
  String? _errorMessage;

  UserModel? get currentUser => _currentUser;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  bool get isAuthenticated => _currentUser != null;

  AuthProvider() {
    // Default fallback demo user for instant test drive
    _currentUser = UserModel(
      id: 1,
      email: 'demo.athlete@fitai.com',
      fullName: 'Mahargha Saha',
      age: 27,
      gender: 'male',
      heightCm: 178.0,
      weightKg: 76.5,
      fitnessGoal: 'hypertrophy',
      activityLevel: 'moderate',
      dietaryPreference: 'high_protein',
      splitPreference: 'PPL',
      targetCalories: 2550,
      targetProteinG: 165.0,
      targetCarbsG: 270.0,
      targetFatG: 68.0,
    );
  }

  Future<bool> login(String email, String password) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _currentUser = await FitnessApiService.registerOrLogin(
        email: email,
        fullName: 'Athlete User',
        password: password,
      );
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> updateProfile(Map<String, dynamic> data) async {
    if (_currentUser == null) return;
    _isLoading = true;
    notifyListeners();

    try {
      _currentUser = await FitnessApiService.updateUserProfile(_currentUser!.id, data);
    } catch (e) {
      _errorMessage = e.toString();
    }
    _isLoading = false;
    notifyListeners();
  }

  void logout() {
    _currentUser = null;
    notifyListeners();
  }
}
