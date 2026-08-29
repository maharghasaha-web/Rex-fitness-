# AI Personal Fitness Trainer — Build & APK Generation Guide

This package contains the complete, production-ready codebase for the **AI Personal Fitness Trainer Mobile App (Flutter for iOS & Android)** and its **FastAPI AI Backend Engine**.

---

## 📦 Project Structure

```
ai_fitness_trainer_full_project/
├── fitness_mobile_app/        # Cross-platform Flutter Mobile Application (iOS & Android)
│   ├── lib/
│   │   ├── models/            # Data models (User, Workout, Nutrition, Physique, Adaptive)
│   │   ├── providers/         # State management (Auth, Workout, Nutrition, Activity)
│   │   ├── screens/           # UI Screens (Dashboard, AI Coach, Scanners, Hub, Paywall)
│   │   ├── services/          # API Client, HealthKit/Health Connect, AdMob AdService
│   │   └── widgets/           # Reusable UI widgets, 1RM Calculator dialog, Macro bars
│   ├── android/               # Android native Gradle setup & manifest with Health Connect
│   ├── ios/                   # iOS native Runner & Info.plist with HealthKit & Camera
│   └── pubspec.yaml           # Flutter dependencies
│
└── fitness_backend_api/       # FastAPI Multimodal AI & Adaptive Backend Pipeline
    ├── app/
    │   ├── api/v1/            # API endpoints (Auth, Physique, Workouts, Nutrition, Coach, etc.)
    │   ├── core/              # App configuration & settings
    │   ├── db/                # Database schema & session management (SQLite / PostgreSQL)
    │   ├── models/            # Database entity models
    │   ├── schemas/           # Pydantic validation schemas
    │   └── services/          # AI Vision, Adaptive Scheduler, Progressive Overload, PDF Report
    ├── tests/                 # Full verification test suites
    ├── Dockerfile             # Multi-stage production container
    ├── docker-compose.yml     # Orchestration (API + PostgreSQL + Redis)
    └── run_local.py           # Single-command local dev runner
```

---

## 🤖 1. How to Build the Android APK

### Step A: Prerequisites
Make sure you have the [Flutter SDK](https://docs.flutter.dev/get-started/install) (version 3.0+) and Android Studio / Android SDK installed.

### Step B: Build Release APK
Navigate to the mobile app directory:
```bash
cd fitness_mobile_app
flutter pub get
```

To build a standalone installable release APK:
```bash
flutter build apk --release
```

* The generated APK will be available at:
  `build/app/outputs/flutter-apk/app-release.apk`
* Transfer this file directly to any Android phone to install and test the app.

To build an optimized split APK (smaller download size per CPU architecture):
```bash
flutter build apk --split-per-abi
```

To build an Android App Bundle (AAB) for Google Play Store upload:
```bash
flutter build appbundle --release
```

---

## 🍎 2. How to Build & Run for iOS

```bash
cd fitness_mobile_app
flutter pub get
cd ios && pod install && cd ..
flutter build ios --release
```
* Open `ios/Runner.xcworkspace` in Xcode to configure your Apple Developer Signing Certificate and deploy to a physical iPhone or upload to TestFlight.

---

## ⚡ 3. Starting the Backend API

```bash
cd fitness_backend_api
python run_local.py
```
* Interactive Swagger Docs: `http://localhost:8000/docs`
