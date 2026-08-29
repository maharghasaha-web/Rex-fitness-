import 'package:flutter/material.dart';
import '../services/api_service.dart';

class OneRepMaxCalculatorDialog extends StatefulWidget {
  final String exerciseName;
  final double? initialWeight;
  final int? initialReps;

  const OneRepMaxCalculatorDialog({
    Key? key,
    required this.exerciseName,
    this.initialWeight,
    this.initialReps,
  }) : super(key: key);

  @override
  State<OneRepMaxCalculatorDialog> createState() => _OneRepMaxCalculatorDialogState();
}

class _OneRepMaxCalculatorDialogState extends State<OneRepMaxCalculatorDialog> {
  late TextEditingController _weightController;
  late TextEditingController _repsController;
  Map<String, dynamic>? _result;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _weightController = TextEditingController(text: (widget.initialWeight ?? 80.0).toString());
    _repsController = TextEditingController(text: (widget.initialReps ?? 8).toString());
    _calculate();
  }

  void _calculate() async {
    final w = double.tryParse(_weightController.text) ?? 80.0;
    final r = int.tryParse(_repsController.text) ?? 8;

    setState(() => _isLoading = true);
    try {
      final res = await FitnessApiService.calculate1RM(
        weightKg: w,
        reps: r,
        exerciseName: widget.exerciseName,
      );
      setState(() {
        _result = res;
      });
    } catch (e) {
      // Local fallback calculation if offline
      final epley = w * (1 + (r / 30.0));
      setState(() {
        _result = {
          'average_estimated_1rm_kg': double.parse(epley.toStringAsFixed(1)),
          'intensity_table': [
            {'percentage': 95, 'weight_kg': double.parse((epley * 0.95).toStringAsFixed(1)), 'estimated_reps': 2},
            {'percentage': 90, 'weight_kg': double.parse((epley * 0.90).toStringAsFixed(1)), 'estimated_reps': 4},
            {'percentage': 85, 'weight_kg': double.parse((epley * 0.85).toStringAsFixed(1)), 'estimated_reps': 6},
            {'percentage': 80, 'weight_kg': double.parse((epley * 0.80).toStringAsFixed(1)), 'estimated_reps': 8},
            {'percentage': 75, 'weight_kg': double.parse((epley * 0.75).toStringAsFixed(1)), 'estimated_reps': 10},
          ]
        };
      });
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: const Color(0xFF1E293B),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      "1RM Calculator: ${widget.exerciseName}",
                      style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close, color: Color(0xFF94A3B8), size: 20),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
              const SizedBox(height: 14),

              // Inputs
              Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _weightController,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      style: const TextStyle(color: Colors.white),
                      decoration: const InputDecoration(
                        labelText: "Weight (kg)",
                        labelStyle: TextStyle(color: Color(0xFF94A3B8), fontSize: 12),
                        filled: true,
                        fillColor: Color(0xFF0F172A),
                        border: OutlineInputBorder(),
                      ),
                      onChanged: (_) => _calculate(),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: TextField(
                      controller: _repsController,
                      keyboardType: TextInputType.number,
                      style: const TextStyle(color: Colors.white),
                      decoration: const InputDecoration(
                        labelText: "Reps Completed",
                        labelStyle: TextStyle(color: Color(0xFF94A3B8), fontSize: 12),
                        filled: true,
                        fillColor: Color(0xFF0F172A),
                        border: OutlineInputBorder(),
                      ),
                      onChanged: (_) => _calculate(),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),

              if (_result != null) ...[
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: const Color(0xFF0F172A),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFF10B981).withOpacity(0.4)),
                  ),
                  child: Column(
                    children: [
                      const Text("ESTIMATED ONE REP MAX (1RM)", style: TextStyle(color: Color(0xFF94A3B8), fontSize: 11, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 4),
                      Text(
                        "${_result!['average_estimated_1rm_kg']} kg",
                        style: const TextStyle(color: Color(0xFF10B981), fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 14),

                const Text("Intensity & Training Load Matrix", style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),

                Table(
                  border: TableBorder.all(color: const Color(0xFF334155), width: 0.5),
                  children: [
                    const TableRow(
                      decoration: BoxDecoration(color: Color(0xFF0F172A)),
                      children: [
                        Padding(padding: EdgeInsets.all(6), child: Text("Intensity", style: TextStyle(color: Color(0xFF94A3B8), fontSize: 11, fontWeight: FontWeight.bold))),
                        Padding(padding: EdgeInsets.all(6), child: Text("Load (kg)", style: TextStyle(color: Color(0xFF94A3B8), fontSize: 11, fontWeight: FontWeight.bold))),
                        Padding(padding: EdgeInsets.all(6), child: Text("Reps", style: TextStyle(color: Color(0xFF94A3B8), fontSize: 11, fontWeight: FontWeight.bold))),
                      ],
                    ),
                    ...?((_result!['intensity_table'] as List?)?.map<TableRow>((item) {
                      return TableRow(
                        children: [
                          Padding(padding: const EdgeInsets.all(6), child: Text("${item['percentage']}%", style: const TextStyle(color: Colors.white, fontSize: 11))),
                          Padding(padding: const EdgeInsets.all(6), child: Text("${item['weight_kg']} kg", style: const TextStyle(color: Color(0xFF10B981), fontSize: 11, fontWeight: FontWeight.w600))),
                          Padding(padding: const EdgeInsets.all(6), child: Text("${item['estimated_reps']}", style: const TextStyle(color: Color(0xFFCBD5E1), fontSize: 11))),
                        ],
                      );
                    }).toList()),
                  ],
                ),
              ],
              const SizedBox(height: 16),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF3B82F6),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                  ),
                  onPressed: () => Navigator.pop(context),
                  child: const Text("Apply Load to Current Set", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
