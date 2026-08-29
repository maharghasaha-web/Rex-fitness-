import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../providers/workout_provider.dart';
import '../../widgets/exercise_card.dart';
import '../../widgets/ad_banner_widget.dart';
import 'active_workout_screen.dart';

class WorkoutHubScreen extends StatefulWidget {
  const WorkoutHubScreen({Key? key}) : super(key: key);

  @override
  State<WorkoutHubScreen> createState() => _WorkoutHubScreenState();
}

class _WorkoutHubScreenState extends State<WorkoutHubScreen> {
  int _selectedDayIndex = 0;

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    final workout = Provider.of<WorkoutProvider>(context);
    final split = workout.activeSplit;
    final userId = auth.currentUser?.id ?? 1;

    return Scaffold(
      backgroundColor: const Color(0xFF12121A),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: const Text('Workout Split & Routines', style: TextStyle(fontWeight: FontWeight.bold)),
        actions: [
          IconButton(
            icon: const Icon(Icons.bolt, color: Colors.amberAccent),
            tooltip: 'Missed Workout Recovery Plan',
            onPressed: () => _showMissedWorkoutDialog(context, userId),
          ),
        ],
      ),
      body: workout.isLoading
          ? const Center(child: CircularProgressIndicator(color: Colors.cyanAccent))
          : split == null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text('No active split generated yet.', style: TextStyle(color: Colors.grey)),
                      const SizedBox(height: 12),
                      ElevatedButton(
                        onPressed: () => workout.loadWorkoutData(userId),
                        child: const Text('Generate AI Split'),
                      ),
                    ],
                  ),
                )
              : Column(
                  children: [
                    // Day Selector Tabs
                    Container(
                      height: 52,
                      padding: const EdgeInsets.symmetric(vertical: 6),
                      child: ListView.builder(
                        scrollDirection: Axis.horizontal,
                        padding: const EdgeInsets.symmetric(horizontal: 12),
                        itemCount: split.days.length,
                        itemBuilder: (context, index) {
                          final day = split.days[index];
                          final isSelected = index == _selectedDayIndex;
                          return Padding(
                            padding: const EdgeInsets.only(right: 8),
                            child: ChoiceChip(
                              label: Text('Day ${day.dayNumber}: ${day.name}'),
                              selected: isSelected,
                              selectedColor: Colors.deepPurpleAccent,
                              backgroundColor: const Color(0xFF1E1E2F),
                              labelStyle: TextStyle(
                                color: isSelected ? Colors.white : Colors.grey[400],
                                fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                                fontSize: 12,
                              ),
                              onSelected: (_) {
                                setState(() {
                                  _selectedDayIndex = index;
                                });
                              },
                            ),
                          );
                        },
                      ),
                    ),
                    const Divider(color: Colors.white10, height: 1),

                    // Exercise List for Selected Day
                    Expanded(
                      child: ListView.builder(
                        itemCount: split.days[_selectedDayIndex].exercises.length,
                        itemBuilder: (context, index) {
                          final exercise = split.days[_selectedDayIndex].exercises[index];
                          final completed = workout.completedSets[exercise.id] ?? List.generate(exercise.sets, (_) => false);
                          return ExerciseCard(
                            exercise: exercise,
                            completedSets: completed,
                            onToggleSet: (setIdx) {
                              workout.toggleSetCompleted(exercise.id, setIdx);
                            },
                          );
                        },
                      ),
                    ),

                    // Start Workout Button & Banner Ad
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      child: SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(builder: (_) => const ActiveWorkoutScreen()),
                            );
                          },
                          icon: const Icon(Icons.play_circle_fill),
                          label: const Text('Start Active Session Tracker', style: TextStyle(fontWeight: FontWeight.bold)),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.cyanAccent,
                            foregroundColor: Colors.black,
                            padding: const EdgeInsets.symmetric(vertical: 14),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                        ),
                      ),
                    ),
                    const AdBannerWidget(),
                  ],
                ),
    );
  }

  void _showMissedWorkoutDialog(BuildContext context, int userId) {
    String selectedStrategy = 'hybrid_consolidation';
    final workout = Provider.of<WorkoutProvider>(context, listen: false);

    showDialog(
      context: context,
      builder: (ctx) => StatefulBuilder(
        builder: (context, setModalState) => AlertDialog(
          backgroundColor: const Color(0xFF1E1E2F),
          title: const Row(
            children: [
              Icon(Icons.warning_amber_rounded, color: Colors.amberAccent),
              SizedBox(width: 8),
              Text('Missed a Workout?', style: TextStyle(color: Colors.white, fontSize: 16)),
            ],
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Select how your AI personal trainer should adjust your schedule:',
                style: TextStyle(color: Colors.grey, fontSize: 12),
              ),
              const SizedBox(height: 12),
              RadioListTile<String>(
                value: 'hybrid_consolidation',
                groupValue: selectedStrategy,
                activeColor: Colors.cyanAccent,
                title: const Text('Hybrid Consolidation (Recommended)', style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold)),
                subtitle: const Text('Merges key compound lifts from missed day with next workout without extra fatigue.', style: TextStyle(color: Colors.grey, fontSize: 11)),
                onChanged: (val) => setModalState(() => selectedStrategy = val!),
              ),
              RadioListTile<String>(
                value: 'roll_over',
                groupValue: selectedStrategy,
                activeColor: Colors.cyanAccent,
                title: const Text('Roll Over / Shift Split', style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold)),
                subtitle: const Text('Pushes the entire weekly calendar back by 1 day and absorbs a rest day.', style: TextStyle(color: Colors.grey, fontSize: 11)),
                onChanged: (val) => setModalState(() => selectedStrategy = val!),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel', style: TextStyle(color: Colors.grey)),
            ),
            ElevatedButton(
              onPressed: () async {
                Navigator.pop(context);
                final plan = await workout.requestAdaptiveFallback(
                  userId: userId,
                  missedDayNumber: _selectedDayIndex + 1,
                  strategy: selectedStrategy,
                );
                if (plan != null) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Adaptive Backup Plan Activated: ${plan.title}'), backgroundColor: Colors.green),
                  );
                }
              },
              style: ElevatedButton.styleFrom(backgroundColor: Colors.cyanAccent, foregroundColor: Colors.black),
              child: const Text('Apply Plan'),
            ),
          ],
        ),
      ),
    );
  }
}
