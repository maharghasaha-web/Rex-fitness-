import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../providers/workout_provider.dart';
import '../../providers/nutrition_provider.dart';
import '../../providers/activity_provider.dart';
import '../../widgets/macro_progress_bar.dart';
import '../../widgets/ad_banner_widget.dart';
import '../workouts/active_workout_screen.dart';
import '../coach/ai_coach_chat_screen.dart';
import '../subscription/subscription_paywall_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final auth = Provider.of<AuthProvider>(context, listen: false);
      if (auth.currentUser != null) {
        final userId = auth.currentUser!.id;
        Provider.of<WorkoutProvider>(context, listen: false).loadWorkoutData(userId);
        Provider.of<NutritionProvider>(context, listen: false).loadDailySummary(userId);
        Provider.of<ActivityProvider>(context, listen: false).syncDeviceHealth(userId);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    final workout = Provider.of<WorkoutProvider>(context);
    final nutrition = Provider.of<NutritionProvider>(context);
    final activity = Provider.of<ActivityProvider>(context);
    final user = auth.currentUser;

    final double totalCalories = (nutrition.dailySummary['total_calories'] ?? 0.0).toDouble();
    final double targetCalories = (user?.targetCalories ?? 2400).toDouble();
    final double protein = (nutrition.dailySummary['total_protein_g'] ?? 0.0).toDouble();
    final double targetProtein = user?.targetProteinG ?? 160.0;
    final double carbs = (nutrition.dailySummary['total_carbs_g'] ?? 0.0).toDouble();
    final double targetCarbs = user?.targetCarbsG ?? 250.0;
    final double fat = (nutrition.dailySummary['total_fat_g'] ?? 0.0).toDouble();
    final double targetFat = user?.targetFatG ?? 65.0;

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        elevation: 0,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Welcome back, ${user?.fullName ?? 'Athlete'}',
              style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            Text(
              'Goal: ${(user?.fitnessGoal ?? 'Hypertrophy').toUpperCase()}',
              style: const TextStyle(fontSize: 11, color: Color(0xFF10B981), fontWeight: FontWeight.w600),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.workspace_premium, color: Color(0xFFF59E0B)),
            tooltip: 'Pro Membership',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const SubscriptionPaywallScreen()),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.sync, color: Color(0xFF10B981)),
            tooltip: 'Sync Health Sensors',
            onPressed: () {
              if (user != null) activity.syncDeviceHealth(user.id);
            },
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: const Color(0xFF10B981),
        icon: const Icon(Icons.chat_bubble_outline, color: Colors.white),
        label: const Text("Ask AI Coach", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const AICoachChatScreen()),
          );
        },
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          if (user != null) {
            await workout.loadWorkoutData(user.id);
            await nutrition.loadDailySummary(user.id);
            await activity.syncDeviceHealth(user.id);
          }
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          children: [
            // 1. Pro Member Banner
            InkWell(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const SubscriptionPaywallScreen()),
                );
              },
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF1E293B), Color(0xFF334155)],
                  ),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: const Color(0xFFF59E0B).withOpacity(0.4)),
                ),
                child: const Row(
                  children: [
                    Icon(Icons.bolt, color: Color(0xFFF59E0B), size: 20),
                    SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        "Unlock Unlimited AI Scans & Ad-Free Pro Experience",
                        style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600),
                      ),
                    ),
                    Icon(Icons.chevron_right, color: Color(0xFF94A3B8), size: 18),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 14),

            // 2. Daily Calorie & Macro Card
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF1E293B),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFF334155)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Nutrition & Calorie Budget',
                        style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Colors.white),
                      ),
                      Text(
                        '${totalCalories.toStringAsFixed(0)} / ${targetCalories.toStringAsFixed(0)} kcal',
                        style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF10B981)),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  MacroProgressBar(label: 'Protein', current: protein, target: targetProtein, color: Colors.redAccent),
                  MacroProgressBar(label: 'Carbohydrates', current: carbs, target: targetCarbs, color: Colors.amberAccent),
                  MacroProgressBar(label: 'Fats', current: fat, target: targetFat, color: Colors.blueAccent),
                ],
              ),
            ),
            const SizedBox(height: 14),

            // 3. Activity & Steps Bar
            Row(
              children: [
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: const Color(0xFF1E293B),
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: const Color(0xFF334155)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.directions_walk, size: 18, color: Color(0xFF10B981)),
                            SizedBox(width: 6),
                            Text('Daily Steps', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 12)),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          '${activity.todaySteps.toString().replaceAllMapped(RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))'), (m) => '${m[1]},')}',
                          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
                        ),
                        Text(
                          'Goal: 10,000 steps',
                          style: TextStyle(fontSize: 11, color: Colors.grey[400]),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: const Color(0xFF1E293B),
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: const Color(0xFF334155)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.local_fire_department, size: 18, color: Color(0xFFF97316)),
                            SizedBox(width: 6),
                            Text('Active Burn', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 12)),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          '${activity.todayCaloriesBurned.toStringAsFixed(0)} kcal',
                          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
                        ),
                        Text(
                          'Source: ${activity.syncSource}',
                          style: TextStyle(fontSize: 11, color: Colors.grey[400]),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),

            // 4. Today's Workout Routine Card
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFF1E293B), Color(0xFF0F172A)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFF10B981).withOpacity(0.4)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        "Today's Training Session",
                        style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Colors.white),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(
                          color: const Color(0xFF10B981),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(
                          workout.todayWorkout?.name ?? 'Assigned Routine',
                          style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.white),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    workout.todayWorkout != null
                        ? '${workout.todayWorkout!.exercises.length} Exercises • ~${workout.todayWorkout!.estimatedDurationMinutes} mins • Focus: ${workout.todayWorkout!.targetMuscleGroups.join(", ")}'
                        : 'Custom Push/Pull/Legs Split',
                    style: const TextStyle(fontSize: 12, color: Color(0xFFCBD5E1)),
                  ),
                  const SizedBox(height: 14),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (_) => const ActiveWorkoutScreen()),
                        );
                      },
                      icon: const Icon(Icons.play_arrow_rounded, color: Colors.white),
                      label: const Text('Start Workout Session', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF10B981),
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),

            // 5. AdMob Banner placement
            const AdBannerWidget(),
            const SizedBox(height: 70), // Spacing for FAB
          ],
        ),
      ),
    );
  }
}
