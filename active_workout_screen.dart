import 'dart:async';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../providers/workout_provider.dart';
import '../../services/ad_service.dart';
import '../../widgets/exercise_card.dart';
import '../../widgets/one_rep_max_calculator_dialog.dart';
import '../coach/ai_coach_chat_screen.dart';

class ActiveWorkoutScreen extends StatefulWidget {
  const ActiveWorkoutScreen({Key? key}) : super(key: key);

  @override
  State<ActiveWorkoutScreen> createState() => _ActiveWorkoutScreenState();
}

class _ActiveWorkoutScreenState extends State<ActiveWorkoutScreen> {
  Timer? _sessionTimer;
  int _secondsElapsed = 0;

  // Rest interval countdown
  Timer? _restTimer;
  int _restSecondsRemaining = 0;

  @override
  void initState() {
    super.initState();
    _startSessionTimer();
  }

  void _startSessionTimer() {
    _sessionTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() {
        _secondsElapsed++;
      });
    });
  }

  void _startRestTimer(int seconds) {
    _restTimer?.cancel();
    setState(() {
      _restSecondsRemaining = seconds;
    });
    _restTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_restSecondsRemaining > 0) {
        setState(() {
          _restSecondsRemaining--;
        });
      } else {
        timer.cancel();
      }
    });
  }

  @override
  void dispose() {
    _sessionTimer?.cancel();
    _restTimer?.cancel();
    super.dispose();
  }

  String _formatTime(int totalSeconds) {
    final m = (totalSeconds ~/ 60).toString().padLeft(2, '0');
    final s = (totalSeconds % 60).toString().padLeft(2, '0');
    return '$m:$s';
  }

  void _open1RMCalculator(String exerciseName) {
    showDialog(
      context: context,
      builder: (_) => OneRepMaxCalculatorDialog(
        exerciseName: exerciseName,
        initialWeight: 80.0,
        initialReps: 8,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    final workout = Provider.of<WorkoutProvider>(context);
    final today = workout.todayWorkout;
    final userId = auth.currentUser?.id ?? 1;

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        elevation: 0,
        title: Text(today?.name ?? 'Active Training', style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 16)),
        actions: [
          IconButton(
            icon: const Icon(Icons.help_outline, color: Color(0xFF10B981)),
            tooltip: "Ask Coach for Exercise Substitution",
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const AICoachChatScreen()),
              );
            },
          ),
          Center(
            child: Padding(
              padding: const EdgeInsets.only(right: 16),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: const Color(0xFF0F172A),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: const Color(0xFF334155)),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.timer, size: 16, color: Color(0xFF10B981)),
                    const SizedBox(width: 4),
                    Text(_formatTime(_secondsElapsed), style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          // Rest Timer Widget
          if (_restSecondsRemaining > 0)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
              color: const Color(0xFF10B981),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('REST INTERVAL ACTIVE', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.black, fontSize: 12)),
                  Text(
                    '${_restSecondsRemaining}s remaining',
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black),
                  ),
                ],
              ),
            ),

          Expanded(
            child: today == null
                ? const Center(child: Text('No workout selected', style: TextStyle(color: Colors.grey)))
                : ListView.builder(
                    padding: const EdgeInsets.symmetric(vertical: 8),
                    itemCount: today.exercises.length,
                    itemBuilder: (context, index) {
                      final exercise = today.exercises[index];
                      final completed = workout.completedSets[exercise.id] ?? List.generate(exercise.sets, (_) => false);
                      return Column(
                        children: [
                          ExerciseCard(
                            exercise: exercise,
                            completedSets: completed,
                            onToggleSet: (setIdx) {
                              workout.toggleSetCompleted(exercise.id, setIdx);
                              if (!completed[setIdx]) {
                                _startRestTimer(exercise.restSeconds);
                              }
                            },
                          ),
                          Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 2),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.end,
                              children: [
                                TextButton.icon(
                                  onPressed: () => _open1RMCalculator(exercise.name),
                                  icon: const Icon(Icons.calculate, size: 14, color: Color(0xFF3B82F6)),
                                  label: const Text("1RM & Intensity Calculator", style: TextStyle(fontSize: 11, color: Color(0xFF3B82F6))),
                                ),
                              ],
                            ),
                          ),
                        ],
                      );
                    },
                  ),
          ),

          // Complete Workout Button
          Container(
            padding: const EdgeInsets.all(16),
            decoration: const BoxDecoration(
              color: Color(0xFF1E293B),
              borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
              border: Border(top: BorderSide(color: Color(0xFF334155))),
            ),
            child: SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () async {
                  final minutes = (_secondsElapsed / 60).ceil();
                  final calories = minutes * 7.5; // ~7.5 kcal/min resistance burn rate
                  await workout.completeSession(userId, durationMinutes: minutes, caloriesBurned: calories);

                  // Show AdMob Interstitial Ad upon completion (with frequency capping)
                  AdService.showWorkoutCompletedInterstitial(
                    onDismissed: () {
                      Navigator.pop(context);
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Great work! Logged $minutes mins and ${calories.toStringAsFixed(0)} kcal burned.'),
                          backgroundColor: const Color(0xFF10B981),
                        ),
                      );
                    },
                  );
                },
                icon: const Icon(Icons.check_circle_outline, color: Colors.white),
                label: const Text('Finish Workout Session', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 15)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF10B981),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
