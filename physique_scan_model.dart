class PhysiqueScanResult {
  final int? id;
  final String bodyFatEstimateRange;
  final String conditioningSummary;
  final List<String> muscularStrengths;
  final List<String> focusAreas;
  final String recommendedSplit;
  final List<String> trainingRecommendations;

  PhysiqueScanResult({
    this.id,
    required this.bodyFatEstimateRange,
    required this.conditioningSummary,
    required this.muscularStrengths,
    required this.focusAreas,
    required this.recommendedSplit,
    required this.trainingRecommendations,
  });

  factory PhysiqueScanResult.fromJson(Map<String, dynamic> json) {
    return PhysiqueScanResult(
      id: json['id'],
      bodyFatEstimateRange: json['body_fat_estimate_range'] ?? '',
      conditioningSummary: json['conditioning_summary'] ?? '',
      muscularStrengths: List<String>.from(json['muscular_strengths'] ?? []),
      focusAreas: List<String>.from(json['focus_areas'] ?? []),
      recommendedSplit: json['recommended_split'] ?? '',
      trainingRecommendations: List<String>.from(json['training_recommendations'] ?? []),
    );
  }
}
