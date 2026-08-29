# AI Personal Fitness Trainer Mobile App (Flutter iOS & Android)

A modern, high-performance cross-platform mobile application for iOS and Android powered by Flutter, Provider state architecture, and Google AdMob monetization.

---

## 📱 Key Screens & Modules

1. **Dashboard & Macro Tracker (`lib/screens/home/dashboard_screen.dart`):**
   * Daily calorie budget and interactive Protein/Carb/Fat progress bars.
   * HealthKit / Google Health Connect background step and active calorie burn sync.
   * Today's workout session launcher and Pro athlete upgrade banner.

2. **AI Personal Coach Chat (`lib/screens/coach/ai_coach_chat_screen.dart`):**
   * Real-time conversational interface with quick prompt chips for exercise substitution, joint pain modifications, and nutrition timing.

3. **Workout Hub & Adaptive Missed Day Handler (`lib/screens/workouts/`):**
   * Active Split browser with full exercise lists, sets, reps, and RPE targets.
   * Modal dialog for selecting adaptive backup recovery options when missing a workout.
   * **Live Active Workout Tracker:** Sound/haptic rest countdown timer, set completion checkmarks, and integrated 1RM calculator.

4. **AI Meal Photo Macro Scanner (`lib/screens/nutrition/nutrition_scanner_screen.dart`):**
   * Camera and gallery integration for instant meal photo scanning.
   * Itemized food breakdown with confidence scores and one-tap daily logging.

5. **AI Physique Conditioning Scanner (`lib/screens/physique/physique_scan_screen.dart`):**
   * Visual scan upload with symmetry ratings, body fat estimation, and split generator.

6. **Monetization & AdMob Integration (`lib/screens/subscription/subscription_paywall_screen.dart`):**
   * Free vs Pro subscription tier paywall (Monthly & Annual with savings highlight).
   * AdMob Rewarded Video ad watcher for earning free scan credits.
   * Banner ads and frequency-capped Interstitial ads on workout completion.

---

## 🔧 Setup & Running

```bash
# 1. Install Flutter dependencies
flutter pub get

# 2. Run on connected device or simulator
flutter run
```
