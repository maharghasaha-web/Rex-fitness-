# AI Fitness & Personal Trainer Backend API

An intelligent, production-ready backend service providing AI-driven physique conditioning analysis, dynamic workout split generation, adaptive missed-day rescheduling, meal photo macro estimation, and automated PDF progress report generation.

---

## 🛠️ Key Architectural Components

1. **AI Physique Conditioning Assessment (`/api/v1/physique`):**
   * Processes user physique photos using multimodal vision models.
   * Evaluates estimated body fat %, muscular symmetry (upper chest, lateral delts, back width, hamstrings), and prescribes optimal workout splits.

2. **Dynamic Workout & Adaptive Missed-Day Engine (`/api/v1/workouts`):**
   * Generates custom Push/Pull/Legs, Upper/Lower, or 5-Day Hybrid splits tailored to user experience and equipment.
   * **Adaptive Recovery Logic:** Automatically calculates recovery options upon a missed session:
     * *Option 1 (Push & Rollover):* Shifts subsequent days forward without volume loss.
     * *Option 2 (Hybrid Compound Consolidation):* Combines high-priority compound movements into the next workout while trimming accessories.
     * *Option 3 (30-min Express Session):* High-density workout with reduced rest periods.

3. **AI Nutrition & Meal Photo Scanner (`/api/v1/nutrition`):**
   * Multi-modal meal photo identification with macro breakdown (Calories, Protein, Carbs, Fat).
   * Supports global & Indian high-protein foods (Soya chunks, Paneer, Tofu, Pea/Soy Isolate, Lentils, Chicken, Eggs).

4. **24/7 AI Coach & Biomechanics Assistant (`/api/v1/coach`):**
   * Evidence-based exercise substitutions based on joint pain, unavailable equipment, or muscle focus.
   * Context-aware chat with active split awareness.

5. **Progressive Overload & 1RM Matrix (`/api/v1/progression`):**
   * Scientific 1RM estimation via Epley and Brzycki equations with percentage load tables.
   * Double progression prescription algorithm (+2.5kg upper / +5.0kg lower body).

6. **Monetization & AdMob Rewards (`/api/v1/monetization`):**
   * Free vs Pro subscription tier management.
   * Rewarded video ad token verification granting instant AI scan credits.
   * Configurable frequency capping for Interstitial and Banner ads.

7. **Client Progress Report PDF Generator (`/api/v1/reports`):**
   * Generates formatted client executive progress reports (ReportLab).

---

## 🚀 Getting Started

### Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run with Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger API documentation available at: `http://localhost:8000/docs`

### Production Deployment (Docker Compose)
```bash
docker-compose up -d --build
```
