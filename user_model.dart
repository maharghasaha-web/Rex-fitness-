class UserModel {
  final int id;
  final String email;
  final String fullName;
  final int? age;
  final String? gender;
  final double? heightCm;
  final double? weightKg;
  final String fitnessGoal;
  final String activityLevel;
  final String dietaryPreference;
  final String splitPreference;
  final int targetCalories;
  final double targetProteinG;
  final double targetCarbsG;
  final double targetFatG;

  UserModel({
    required this.id,
    required this.email,
    required this.fullName,
    this.age,
    this.gender,
    this.heightCm,
    this.weightKg,
    required this.fitnessGoal,
    required this.activityLevel,
    required this.dietaryPreference,
    required this.splitPreference,
    required this.targetCalories,
    required this.targetProteinG,
    required this.targetCarbsG,
    required this.targetFatG,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] ?? 0,
      email: json['email'] ?? '',
      fullName: json['full_name'] ?? 'Athlete',
      age: json['age'],
      gender: json['gender'],
      heightCm: json['height_cm'] != null ? (json['height_cm'] as num).toDouble() : null,
      weightKg: json['weight_kg'] != null ? (json['weight_kg'] as num).toDouble() : null,
      fitnessGoal: json['fitness_goal'] ?? 'hypertrophy',
      activityLevel: json['activity_level'] ?? 'moderate',
      dietaryPreference: json['dietary_preference'] ?? 'high_protein',
      splitPreference: json['split_preference'] ?? 'PPL',
      targetCalories: json['target_calories'] ?? 2400,
      targetProteinG: (json['target_protein_g'] ?? 160.0).toDouble(),
      targetCarbsG: (json['target_carbs_g'] ?? 250.0).toDouble(),
      targetFatG: (json['target_fat_g'] ?? 65.0).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'email': email,
      'full_name': fullName,
      'age': age,
      'gender': gender,
      'height_cm': heightCm,
      'weight_kg': weightKg,
      'fitness_goal': fitnessGoal,
      'activity_level': activityLevel,
      'dietary_preference': dietaryPreference,
      'split_preference': splitPreference,
      'target_calories': targetCalories,
      'target_protein_g': targetProteinG,
      'target_carbs_g': targetCarbsG,
      'target_fat_g': targetFatG,
    };
  }
}
