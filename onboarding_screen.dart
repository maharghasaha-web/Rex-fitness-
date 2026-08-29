import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({Key? key}) : super(key: key);

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  String _goal = 'hypertrophy';
  String _splitPref = 'PPL';
  String _dietPref = 'high_protein';
  double _weightKg = 75.0;
  double _heightCm = 175.0;

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);

    return Scaffold(
      backgroundColor: const Color(0xFF12121A),
      appBar: AppBar(
        title: const Text('Athlete Profile Setup'),
        backgroundColor: Colors.transparent,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Personalize Your AI Coach', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
            const SizedBox(height: 8),
            const Text('Configure your goals and baseline physical parameters for optimized workout splits and macro ratios.', style: TextStyle(color: Colors.grey, fontSize: 13)),
            const SizedBox(height: 24),

            const Text('Primary Goal', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.cyanAccent)),
            DropdownButton<String>(
              value: _goal,
              dropdownColor: const Color(0xFF1E1E2F),
              isExpanded: true,
              items: const [
                DropdownMenuItem(value: 'hypertrophy', child: Text('Muscle Hypertrophy & Strength', style: TextStyle(color: Colors.white))),
                DropdownMenuItem(value: 'fat_loss', child: Text('Fat Loss & Conditioning', style: TextStyle(color: Colors.white))),
                DropdownMenuItem(value: 'recomposition', child: Text('Body Recomposition', style: TextStyle(color: Colors.white))),
              ],
              onChanged: (v) => setState(() => _goal = v!),
            ),
            const SizedBox(height: 16),

            const Text('Preferred Split Style', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.cyanAccent)),
            DropdownButton<String>(
              value: _splitPref,
              dropdownColor: const Color(0xFF1E1E2F),
              isExpanded: true,
              items: const [
                DropdownMenuItem(value: 'PPL', child: Text('Push / Pull / Legs (5-6 Days)', style: TextStyle(color: Colors.white))),
                DropdownMenuItem(value: 'UpperLower', child: Text('Upper / Lower (4 Days)', style: TextStyle(color: Colors.white))),
                DropdownMenuItem(value: 'FullBody', child: Text('Full Body (3 Days)', style: TextStyle(color: Colors.white))),
              ],
              onChanged: (v) => setState(() => _splitPref = v!),
            ),
            const SizedBox(height: 24),

            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () async {
                  await auth.updateProfile({
                    'fitness_goal': _goal,
                    'split_preference': _splitPref,
                    'dietary_preference': _dietPref,
                    'weight_kg': _weightKg,
                    'height_cm': _heightCm,
                  });
                  Navigator.pop(context);
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.cyanAccent,
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: const Text('Save & Apply Settings', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
