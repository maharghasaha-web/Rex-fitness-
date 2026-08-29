import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../providers/activity_provider.dart';
import '../../widgets/ad_banner_widget.dart';

class ActivityAnalyticsScreen extends StatelessWidget {
  const ActivityAnalyticsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    final activity = Provider.of<ActivityProvider>(context);
    final userId = auth.currentUser?.id ?? 1;

    return Scaffold(
      backgroundColor: const Color(0xFF12121A),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: const Text('Activity & Calorie Burn', style: TextStyle(fontWeight: FontWeight.bold)),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: Colors.cyanAccent),
            onPressed: () => activity.syncDeviceHealth(userId),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Daily Ring / Big Metrics Card
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFF1E1E2F), Color(0xFF2B1B4D)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _metricCol('Steps', activity.todaySteps.toString(), Icons.directions_walk, Colors.greenAccent),
                      _metricCol('Active Burn', '${activity.todayCaloriesBurned.toStringAsFixed(0)} kcal', Icons.local_fire_department, Colors.orangeAccent),
                      _metricCol('Active Time', '${activity.activeMinutes} mins', Icons.timer, Colors.cyanAccent),
                    ],
                  ),
                  const Divider(color: Colors.white10, height: 28),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text('Sync Source: ${activity.syncSource}', style: const TextStyle(fontSize: 11, color: Colors.grey)),
                      ElevatedButton.icon(
                        onPressed: activity.isSyncing ? null : () => activity.syncDeviceHealth(userId),
                        icon: const Icon(Icons.cloud_sync, size: 16),
                        label: const Text('Sync Sensors', style: TextStyle(fontSize: 11)),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.cyanAccent,
                          foregroundColor: Colors.black,
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            const Text('Weekly Calorie Burn Distribution', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Colors.white)),
            const SizedBox(height: 12),
            Container(
              height: 160,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF1E1E2F),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  _barItem('Mon', 0.65, '520 kcal'),
                  _barItem('Tue', 0.85, '680 kcal'),
                  _barItem('Wed', 0.40, '320 kcal'),
                  _barItem('Thu', 0.90, '720 kcal'),
                  _barItem('Fri', 0.75, '600 kcal'),
                  _barItem('Sat', 0.50, '400 kcal'),
                  _barItem('Sun', 0.30, '240 kcal'),
                ],
              ),
            ),
            const SizedBox(height: 16),
            const AdBannerWidget(),
          ],
        ),
      ),
    );
  }

  Widget _metricCol(String title, String val, IconData icon, Color color) {
    return Column(
      children: [
        Icon(icon, color: color, size: 26),
        const SizedBox(height: 6),
        Text(val, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.white)),
        Text(title, style: const TextStyle(color: Colors.grey, fontSize: 11)),
      ],
    );
  }

  Widget _barItem(String day, double heightFactor, String tooltip) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.end,
      children: [
        Container(
          width: 18,
          height: 100 * heightFactor,
          decoration: BoxDecoration(
            color: Colors.cyanAccent,
            borderRadius: BorderRadius.circular(6),
          ),
        ),
        const SizedBox(height: 6),
        Text(day, style: const TextStyle(color: Colors.grey, fontSize: 11)),
      ],
    );
  }
}
