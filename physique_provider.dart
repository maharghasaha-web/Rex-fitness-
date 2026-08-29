import 'package:flutter/material.dart';
import '../models/physique_scan_model.dart';
import '../services/api_service.dart';

class PhysiqueProvider extends ChangeNotifier {
  PhysiqueScanResult? _latestAssessment;
  List<PhysiqueScanResult> _history = [];
  bool _isAnalyzing = false;
  String? _errorMessage;

  PhysiqueScanResult? get latestAssessment => _latestAssessment;
  List<PhysiqueScanResult> get history => _history;
  bool get isAnalyzing => _isAnalyzing;
  String? get errorMessage => _errorMessage;

  Future<PhysiqueScanResult?> analyzePhysiquePhoto({
    required int userId,
    String? imageBase64,
    String? imageUrl,
    String? notes,
  }) async {
    _isAnalyzing = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _latestAssessment = await FitnessApiService.scanPhysique(
        userId: userId,
        imageBase64: imageBase64,
        imageUrl: imageUrl,
        notes: notes,
      );
      _isAnalyzing = false;
      notifyListeners();
      return _latestAssessment;
    } catch (e) {
      _errorMessage = e.toString();
      _isAnalyzing = false;
      notifyListeners();
      return null;
    }
  }

  Future<void> loadHistory(int userId) async {
    try {
      _history = await FitnessApiService.getPhysiqueHistory(userId);
      if (_history.isNotEmpty && _latestAssessment == null) {
        _latestAssessment = _history.first;
      }
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
    }
  }
}
