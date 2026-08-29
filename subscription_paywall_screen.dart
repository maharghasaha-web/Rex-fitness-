import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../services/api_service.dart';
import '../../services/ad_service.dart';

class SubscriptionPaywallScreen extends StatefulWidget {
  const SubscriptionPaywallScreen({Key? key}) : super(key: key);

  @override
  State<SubscriptionPaywallScreen> createState() => _SubscriptionPaywallScreenState();
}

class _SubscriptionPaywallScreenState extends State<SubscriptionPaywallScreen> {
  int _selectedPlanIndex = 1; // 0 = Monthly, 1 = Annual (Best Value)
  bool _isProcessing = false;
  Map<String, dynamic>? _userTierData;

  @override
  void initState() {
    super.initState();
    _loadUserTier();
  }

  void _loadUserTier() async {
    final user = Provider.of<AuthProvider>(context, listen: false).currentUser;
    final userId = user?.id ?? 1;
    final data = await FitnessApiService.getUserTier(userId);
    setState(() {
      _userTierData = data;
    });
  }

  void _upgradeToPro() async {
    final user = Provider.of<AuthProvider>(context, listen: false).currentUser;
    final userId = user?.id ?? 1;
    final targetTier = _selectedPlanIndex == 1 ? 'PRO_ANNUAL' : 'PRO_MONTHLY';

    setState(() => _isProcessing = true);
    try {
      final res = await FitnessApiService.upgradeTier(
        userId: userId,
        targetTier: targetTier,
      );
      setState(() {
        _userTierData = res;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Welcome to PRO! Unlimited AI scans and ad-free experience unlocked."),
          backgroundColor: Color(0xFF10B981),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Upgrade failed: $e"), backgroundColor: Colors.red),
      );
    } finally {
      setState(() => _isProcessing = false);
    }
  }

  void _watchRewardedAd() async {
    final user = Provider.of<AuthProvider>(context, listen: false).currentUser;
    final userId = user?.id ?? 1;

    setState(() => _isProcessing = true);
    // Trigger AdMob rewarded ad
    AdService.showRewardedAd(
      onUserEarnedReward: (reward) async {
        try {
          final res = await FitnessApiService.claimRewardedAd(
            userId: userId,
            adUnitId: "ca-app-pub-3940256099942544/5224354917",
          );
          _loadUserTier();
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(res['message'] ?? "+1 AI Scan Credit Earned!"),
              backgroundColor: const Color(0xFF10B981),
            ),
          );
        } catch (e) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text("Failed to claim reward: $e"), backgroundColor: Colors.red),
          );
        }
      },
    );
    setState(() => _isProcessing = false);
  }

  @override
  Widget build(BuildContext context) {
    final isPro = _userTierData?['is_pro'] ?? false;
    final scanCredits = _userTierData?['scan_credits_remaining'] ?? 3;

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.close, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        child: Column(
          children: [
            // Badge
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFF10B981), Color(0xFF3B82F6)],
                ),
                borderRadius: BorderRadius.circular(20),
              ),
              child: const Text(
                "⚡ PRO ATHLETE UPGRADE",
                style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
              ),
            ),
            const SizedBox(height: 14),

            const Text(
              "Unleash Your Full Potential",
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 6),
            const Text(
              "Unlimited AI physique assessments, precision meal macro scanning, and priority 24/7 coaching.",
              textAlign: TextAlign.center,
              style: TextStyle(color: Color(0xFF94A3B8), fontSize: 13),
            ),
            const SizedBox(height: 24),

            // Feature Comparison Card
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: const Color(0xFF1E293B),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFF334155)),
              ),
              child: Column(
                children: [
                  _buildFeatureRow("Ad-Free Experience", "Zero banners or interruptions", true),
                  const Divider(color: Color(0xFF334155), height: 16),
                  _buildFeatureRow("Unlimited AI Scans", "Physique conditioning & Meal macros", true),
                  const Divider(color: Color(0xFF334155), height: 16),
                  _buildFeatureRow("24/7 AI Coach Chat", "Biomechanics & exercise substitution", true),
                  const Divider(color: Color(0xFF334155), height: 16),
                  _buildFeatureRow("Progressive Overload Matrix", "Automated 1RM & next session weights", true),
                  const Divider(color: Color(0xFF334155), height: 16),
                  _buildFeatureRow("Exportable PDF Reports", "Monthly executive coaching analytics", true),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Pricing Plans Selector
            Row(
              children: [
                Expanded(
                  child: _buildPlanOption(
                    index: 0,
                    title: "Monthly",
                    price: "\$9.99",
                    subtitle: "Billed monthly",
                    isPopular: false,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildPlanOption(
                    index: 1,
                    title: "Annual",
                    price: "\$6.66/mo",
                    subtitle: "\$79.99/yr (Save 33%)",
                    isPopular: true,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),

            // Upgrade Button
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF10B981),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  elevation: 4,
                ),
                onPressed: _isProcessing || isPro ? null : _upgradeToPro,
                child: _isProcessing
                    ? const CircularProgressIndicator(color: Colors.white)
                    : Text(
                        isPro ? "YOU ARE CURRENTLY PRO" : "UPGRADE TO PRO NOW",
                        style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Colors.white),
                      ),
              ),
            ),
            const SizedBox(height: 20),

            // Free alternative: Watch Rewarded Ad
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFF0F172A),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: const Color(0xFF334155), style: BorderStyle.solid),
              ),
              child: Row(
                children: [
                  const Icon(Icons.video_library, color: Color(0xFF3B82F6), size: 24),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text("Need 1 Quick Scan?", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13)),
                        Text("Current Credits: $scanCredits. Watch 1 short video for +1 instant scan.", style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 11)),
                      ],
                    ),
                  ),
                  OutlinedButton(
                    style: OutlinedButton.styleFrom(
                      side: const BorderSide(color: Color(0xFF3B82F6)),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                    ),
                    onPressed: _isProcessing ? null : _watchRewardedAd,
                    child: const Text("Watch Ad", style: TextStyle(color: Color(0xFF3B82F6), fontSize: 12, fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }

  Widget _buildFeatureRow(String title, String subtitle, bool isIncluded) {
    return Row(
      children: [
        const Icon(Icons.check_circle, color: Color(0xFF10B981), size: 18),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600)),
              Text(subtitle, style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 11)),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildPlanOption({
    required int index,
    required String title,
    required String price,
    required String subtitle,
    required bool isPopular,
  }) {
    final isSelected = _selectedPlanIndex == index;

    return InkWell(
      onTap: () => setState(() => _selectedPlanIndex = index),
      child: Stack(
        clipBehavior: Clip.none,
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: const Color(0xFF1E293B),
              borderRadius: BorderRadius.circular(14),
              border: Border.all(
                color: isSelected ? const Color(0xFF10B981) : const Color(0xFF334155),
                width: isSelected ? 2 : 1,
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold)),
                const SizedBox(height: 6),
                Text(price, style: const TextStyle(color: Color(0xFF10B981), fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 4),
                Text(subtitle, style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 11)),
              ],
            ),
          ),
          if (isPopular)
            Positioned(
              top: -10,
              right: 12,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: const Color(0xFF10B981),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: const Text("BEST VALUE", style: TextStyle(color: Colors.white, fontSize: 9, fontWeight: FontWeight.bold)),
              ),
            ),
        ],
      ),
    );
  }
}
