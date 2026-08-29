import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../providers/nutrition_provider.dart';
import '../../widgets/ad_banner_widget.dart';

class NutritionScannerScreen extends StatefulWidget {
  const NutritionScannerScreen({Key? key}) : super(key: key);

  @override
  State<NutritionScannerScreen> createState() => _NutritionScannerScreenState();
}

class _NutritionScannerScreenState extends State<NutritionScannerScreen> {
  File? _mealImage;
  final ImagePicker _picker = ImagePicker();
  String _selectedMealType = 'lunch';

  Future<void> _pickImage(ImageSource source) async {
    final picked = await _picker.pickImage(source: source, imageQuality: 70);
    if (picked != null) {
      setState(() {
        _mealImage = File(picked.path);
      });
    }
  }

  Future<void> _analyzeMeal() async {
    if (_mealImage == null) return;
    final auth = Provider.of<AuthProvider>(context, listen: false);
    final nutrition = Provider.of<NutritionProvider>(context, listen: false);
    final userId = auth.currentUser?.id ?? 1;

    final bytes = await _mealImage!.readAsBytes();
    final base64String = base64Encode(bytes);

    final result = await nutrition.scanMealImage(
      userId: userId,
      imageBase64: base64String,
      mealType: _selectedMealType,
    );

    if (result != null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Identified: ${result.identifiedMealTitle} (${result.totalCalories.toStringAsFixed(0)} kcal)'),
          backgroundColor: Colors.green,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    final nutrition = Provider.of<NutritionProvider>(context);
    final scan = nutrition.latestScanResult;
    final userId = auth.currentUser?.id ?? 1;

    return Scaffold(
      backgroundColor: const Color(0xFF12121A),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: const Text('AI Food & Macro Scanner', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Meal Image Box
            GestureDetector(
              onTap: () => _showSourcePicker(),
              child: Container(
                height: 190,
                width: double.infinity,
                decoration: BoxDecoration(
                  color: const Color(0xFF1E1E2F),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.amberAccent.withOpacity(0.4)),
                ),
                child: _mealImage != null
                    ? ClipRRect(
                        borderRadius: BorderRadius.circular(16),
                        child: Image.file(_mealImage!, fit: BoxFit.cover),
                      )
                    : const Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.fastfood_outlined, size: 44, color: Colors.amberAccent),
                          SizedBox(height: 8),
                          Text('Take or Select Meal Photo', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                          Text('Estimates calories, protein, carbs & fats automatically', style: TextStyle(color: Colors.grey, fontSize: 11)),
                        ],
                      ),
              ),
            ),
            const SizedBox(height: 12),

            // Meal Type Selector
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: ['breakfast', 'lunch', 'dinner', 'snack'].map((type) {
                final isSelected = _selectedMealType == type;
                return ChoiceChip(
                  label: Text(type.toUpperCase()),
                  selected: isSelected,
                  selectedColor: Colors.amberAccent,
                  backgroundColor: const Color(0xFF1E1E2F),
                  labelStyle: TextStyle(
                    color: isSelected ? Colors.black : Colors.grey[400],
                    fontWeight: FontWeight.bold,
                    fontSize: 11,
                  ),
                  onSelected: (_) => setState(() => _selectedMealType = type),
                );
              }).toList(),
            ),
            const SizedBox(height: 12),

            // Analyze Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: nutrition.isScanning || _mealImage == null ? null : _analyzeMeal,
                icon: nutrition.isScanning
                    ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.black))
                    : const Icon(Icons.qr_code_scanner),
                label: Text(
                  nutrition.isScanning ? 'Extracting Nutrients...' : 'Scan & Identify Macros',
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.amberAccent,
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Scanned Result Card
            if (scan != null) ...[
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E1E2F),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.white10),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Expanded(
                          child: Text(
                            scan.identifiedMealTitle,
                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white),
                          ),
                        ),
                        Text(
                          '${scan.totalCalories.toStringAsFixed(0)} kcal',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.cyanAccent),
                        ),
                      ],
                    ),
                    const Divider(color: Colors.white10, height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        _macroBadge('Protein', '${scan.totalProteinG.toStringAsFixed(0)}g', Colors.redAccent),
                        _macroBadge('Carbs', '${scan.totalCarbsG.toStringAsFixed(0)}g', Colors.amberAccent),
                        _macroBadge('Fats', '${scan.totalFatG.toStringAsFixed(0)}g', Colors.blueAccent),
                      ],
                    ),
                    const SizedBox(height: 14),
                    const Text('Detected Food Items:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: Colors.grey)),
                    ...scan.foodItems.map((item) => Padding(
                          padding: const EdgeInsets.symmetric(vertical: 4),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text('${item.foodName} (${item.estimatedPortion})', style: const TextStyle(fontSize: 12, color: Colors.white70)),
                              Text('${item.calories.toStringAsFixed(0)} kcal | ${item.proteinG.toStringAsFixed(0)}g P', style: const TextStyle(fontSize: 12, color: Colors.cyanAccent)),
                            ],
                          ),
                        )),
                    const SizedBox(height: 16),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        onPressed: () async {
                          await nutrition.logScannedMealDirect(
                            userId,
                            mealTitle: scan.identifiedMealTitle,
                            mealType: _selectedMealType,
                            calories: scan.totalCalories,
                            proteinG: scan.totalProteinG,
                            carbsG: scan.totalCarbsG,
                            fatG: scan.totalFatG,
                          );
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Meal saved to daily diary!'), backgroundColor: Colors.green),
                          );
                        },
                        icon: const Icon(Icons.bookmark_add_outlined),
                        label: const Text('Add to Daily Log'),
                        style: ElevatedButton.styleFrom(backgroundColor: Colors.greenAccent, foregroundColor: Colors.black),
                      ),
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

  Widget _macroBadge(String name, String value, Color color) {
    return Column(
      children: [
        Text(value, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: color)),
        Text(name, style: const TextStyle(color: Colors.grey, fontSize: 11)),
      ],
    );
  }

  void _showSourcePicker() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1E1E2F),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(16))),
      builder: (_) => SafeArea(
        child: Wrap(
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt, color: Colors.amberAccent),
              title: const Text('Take Meal Photo', style: TextStyle(color: Colors.white)),
              onTap: () {
                Navigator.pop(context);
                _pickImage(ImageSource.camera);
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library, color: Colors.amberAccent),
              title: const Text('Select from Gallery', style: TextStyle(color: Colors.white)),
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
