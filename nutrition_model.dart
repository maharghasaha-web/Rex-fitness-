class FoodItem {
  final String foodName;
  final String estimatedPortion;
  final double calories;
  final double proteinG;
  final double carbsG;
  final double fatG;
  final double confidenceScore;

  FoodItem({
    required this.foodName,
    required this.estimatedPortion,
    required this.calories,
    required this.proteinG,
    required this.carbsG,
    required this.fatG,
    required this.confidenceScore,
  });

  factory FoodItem.fromJson(Map<String, dynamic> json) {
    return FoodItem(
      foodName: json['food_name'] ?? '',
      estimatedPortion: json['estimated_portion'] ?? '',
      calories: (json['calories'] ?? 0.0).toDouble(),
      proteinG: (json['protein_g'] ?? 0.0).toDouble(),
      carbsG: (json['carbs_g'] ?? 0.0).toDouble(),
      fatG: (json['fat_g'] ?? 0.0).toDouble(),
      confidenceScore: (json['confidence_score'] ?? 0.9).toDouble(),
    );
  }
}

class FoodScanResponse {
  final String identifiedMealTitle;
  final double totalCalories;
  final double totalProteinG;
  final double totalCarbsG;
  final double totalFatG;
  final List<FoodItem> foodItems;
  final String dietaryAnalysisNotes;

  FoodScanResponse({
    required this.identifiedMealTitle,
    required this.totalCalories,
    required this.totalProteinG,
    required this.totalCarbsG,
    required this.totalFatG,
    required this.foodItems,
    required this.dietaryAnalysisNotes,
  });

  factory FoodScanResponse.fromJson(Map<String, dynamic> json) {
    return FoodScanResponse(
      identifiedMealTitle: json['identified_meal_title'] ?? '',
      totalCalories: (json['total_calories'] ?? 0.0).toDouble(),
      totalProteinG: (json['total_protein_g'] ?? 0.0).toDouble(),
      totalCarbsG: (json['total_carbs_g'] ?? 0.0).toDouble(),
      totalFatG: (json['total_fat_g'] ?? 0.0).toDouble(),
      foodItems: (json['food_items'] as List? ?? [])
          .map((item) => FoodItem.fromJson(item))
          .toList(),
      dietaryAnalysisNotes: json['dietary_analysis_notes'] ?? '',
    );
  }
}
