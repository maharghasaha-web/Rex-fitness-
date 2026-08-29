import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../providers/physique_provider.dart';
import '../../providers/workout_provider.dart';
import '../../services/ad_service.dart';
import '../../widgets/ad_banner_widget.dart';

class PhysiqueScanScreen extends StatefulWidget {
  const PhysiqueScanScreen({Key? key}) : super(key: key);

  @override
  State<PhysiqueScanScreen> createState() => _PhysiqueScanScreenState();
}

class _PhysiqueScanScreenState extends State<PhysiqueScanScreen> {
  File? _selectedImage;
  final ImagePicker _picker = ImagePicker();
  final TextEditingController _notesController = TextEditingController();

  Future<void> _pickImage(ImageSource source) async {
    final picked = await _picker.pickImage(source: source, imageQuality: 70);
    if (picked != null) {
      setState(() {
        _selectedImage = File(picked.path);
      });
    }
  }

  Future<void> _runAnalysis() async {
    if (_selectedImage == null) return;
    final auth = Provider.of<AuthProvider>(context, listen: false);
    final physique = Provider.of<PhysiqueProvider>(context, listen: false);
    final workout = Provider.of<WorkoutProvider>(context, listen: false);
    final userId = auth.currentUser?.id ?? 1;

    final bytes = await _selectedImage!.readAsBytes();
    final base64String = base64Encode(bytes);

    final result = await physique.analyzePhysiquePhoto(
      userId: userId,
      imageBase64: base64String,
      notes: _notesController.text.isNotEmpty ? _notesController.text : null,
    );

    if (result != null) {
      // Auto-generate split aligned with conditioning
      await workout.loadWorkoutData(userId);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Physique assessment completed & workout split updated!'),
          backgroundColor: Colors.green,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final physique = Provider.of<PhysiqueProvider>(context);
    final assessment = physique.latestAssessment;

    return Scaffold(
      backgroundColor: const Color(0xFF12121A),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: const Text('AI Physique Assessment', style: TextStyle(fontWeight: FontWeight.bold)),
        actions: [
          IconButton(
            icon: const Icon(Icons.stars, color: Colors.amberAccent),
            tooltip: 'Watch Ad for Pro Analysis',
            onPressed: () {
              AdService.showRewardedAiScanAd(
                onUserEarnedReward: (reward) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Pro Conditioning Analysis Unlocked!')),
                  );
                },
              );
            },
          )
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Upload & Camera preview
            GestureDetector(
              onTap: () => _showImageSourceBottomSheet(),
              child: Container(
                height: 200,
                width: double.infinity,
                decoration: BoxDecoration(
                  color: const Color(0xFF1E1E2F),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.cyanAccent.withOpacity(0.4), style: BorderStyle.solid),
                ),
                child: _selectedImage != null
                    ? ClipRRect(
                        borderRadius: BorderRadius.circular(16),
                        child: Image.file(_selectedImage!, fit: BoxFit.cover),
                      )
                    : const Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.camera_alt_outlined, size: 48, color: Colors.cyanAccent),
                          SizedBox(height: 8),
                          Text(
                            'Tap to Upload or Capture Physique Photo',
                            style: TextStyle(color: Colors.white70, fontWeight: FontWeight.bold),
                          ),
                          Text(
                            'Front, back, or side physique for posture & conditioning scan',
                            style: TextStyle(color: Colors.grey, fontSize: 11),
                          ),
                        ],
                      ),
              ),
            ),
            const SizedBox(height: 12),

            // Scan Action Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: physique.isAnalyzing || _selectedImage == null ? null : _runAnalysis,
                icon: physique.isAnalyzing
                    ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.black))
                    : const Icon(Icons.analytics_outlined),
                label: Text(
                  physique.isAnalyzing ? 'Analyzing Conditioning...' : 'Scan & Evaluate Conditioning',
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.cyanAccent,
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Assessment Results Section
            if (assessment != null) ...[
              const Text('Conditioning Breakdown', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E1E2F),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Body Fat Estimate:', style: TextStyle(color: Colors.grey, fontSize: 13)),
                        Text(
                          assessment.bodyFatEstimateRange,
                          style: const TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                    const Divider(color: Colors.white10, height: 18),
                    Text(
                      assessment.conditioningSummary,
                      style: const TextStyle(fontSize: 13, height: 1.4, color: Colors.white70),
                    ),
                    const SizedBox(height: 12),
                    const Text('Focus Areas:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: Colors.amberAccent)),
                    Wrap(
                      spacing: 6,
                      children: assessment.focusAreas
                          .map((f) => Chip(
                                label: Text(f, style: const TextStyle(fontSize: 11, color: Colors.white)),
                                backgroundColor: Colors.white10,
                                padding: EdgeInsets.zero,
                              ))
                          .toList(),
                    ),
                    const SizedBox(height: 8),
                    const Text('Recommended Split:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: Colors.greenAccent)),
                    Text(
                      assessment.recommendedSplit,
                      style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Colors.white),
                    ),
                  ],
                ),
              ),
            ],
            const SizedBox(height: 16),
            const AdBannerWidget(),
          ],
        ),
      ),
    );
  }

  void _showImageSourceBottomSheet() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1E1E2F),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(16))),
      builder: (_) => SafeArea(
        child: Wrap(
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt, color: Colors.cyanAccent),
              title: const Text('Take Photo', style: TextStyle(color: Colors.white)),
              onTap: () {
                Navigator.pop(context);
                _pickImage(ImageSource.camera);
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library, color: Colors.cyanAccent),
              title: const Text('Choose from Gallery', style: TextStyle(color: Colors.white)),
              onTap: () {
                Navigator.pop(context);
                _pickImage(ImageSource.gallery);
              },
            ),
          ],
        ),
      ),
    );
  }
}
