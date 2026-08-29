import 'package:flutter/material.dart';
import '../models/workout_split_model.dart';

class ExerciseCard extends StatelessWidget {
  final Exercise exercise;
  final List<bool> completedSets;
  final Function(int setIndex) onToggleSet;

  const ExerciseCard({
    Key? key,
    required this.exercise,
    required this.completedSets,
    required this.onToggleSet,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      color: const Color(0xFF1E1E2C),
      margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(14.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Text(
                    exercise.name,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: exercise.isCompound ? Colors.amber.withOpacity(0.2) : Colors.blue.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    exercise.isCompound ? 'Compound' : 'Accessory',
                    style: TextStyle(
                      fontSize: 11,
                      color: exercise.isCompound ? Colors.amber : Colors.blueAccent,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            Text(
              '${exercise.targetMuscle.toUpperCase()} • ${exercise.sets} Sets × ${exercise.repRange} Reps • RPE ${exercise.rpeTarget} • ${exercise.restSeconds}s Rest',
              style: TextStyle(fontSize: 12, color: Colors.grey[400]),
            ),
            const Divider(color: Colors.white10, height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: List.generate(exercise.sets, (index) {
                final isDone = index < completedSets.length && completedSets[index];
                return InkWell(
                  onTap: () => onToggleSet(index),
                  borderRadius: BorderRadius.circular(8),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                    decoration: BoxDecoration(
                      color: isDone ? Colors.green.withOpacity(0.2) : Colors.white10,
                      border: Border.all(
                        color: isDone ? Colors.greenAccent : Colors.transparent,
                        width: 1.5,
                      ),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          isDone ? Icons.check_circle : Icons.circle_outlined,
                          size: 16,
                          color: isDone ? Colors.greenAccent : Colors.grey,
                        ),
                        const SizedBox(width: 4),
                        Text(
                          'Set ${index + 1}',
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                            color: isDone ? Colors.greenAccent : Colors.white70,
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              }),
            ),
          ],
        ),
      ),
    );
  }
}
