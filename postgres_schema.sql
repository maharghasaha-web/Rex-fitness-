-- PostgreSQL / Supabase Migration Schema
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(50) NOT NULL,
    height_cm NUMERIC(5,2) NOT NULL,
    weight_kg NUMERIC(5,2) NOT NULL,
    fitness_goal VARCHAR(100) NOT NULL,
    experience_level VARCHAR(50) NOT NULL,
    split_preference VARCHAR(100) NOT NULL,
    days_per_week_available INT NOT NULL DEFAULT 4,
    dietary_preference VARCHAR(100),
    daily_calorie_target INT NOT NULL,
    daily_protein_target_g NUMERIC(6,2) NOT NULL,
    daily_carb_target_g NUMERIC(6,2) NOT NULL,
    daily_fat_target_g NUMERIC(6,2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS physique_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    conditioning_json JSONB NOT NULL,
    recommendations_json JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS workout_splits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    split_name VARCHAR(255) NOT NULL,
    total_days_per_week INT NOT NULL,
    schedule_json JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workout_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    workout_plan_id UUID NOT NULL REFERENCES workout_splits(id),
    day_number INT NOT NULL,
    date DATE NOT NULL,
    duration_minutes INT NOT NULL,
    calories_burned_estimated INT NOT NULL,
    exercise_logs_json JSONB NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS meal_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    meal_type VARCHAR(50) NOT NULL,
    food_items_json JSONB NOT NULL,
    total_calories NUMERIC(7,2) NOT NULL,
    total_protein_g NUMERIC(6,2) NOT NULL,
    total_carbs_g NUMERIC(6,2) NOT NULL,
    total_fat_g NUMERIC(6,2) NOT NULL,
    image_url TEXT
);

CREATE TABLE IF NOT EXISTS activity_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    step_count INT NOT NULL DEFAULT 0,
    active_energy_burned_kcal NUMERIC(7,2) NOT NULL DEFAULT 0,
    resting_energy_burned_kcal NUMERIC(7,2),
    source VARCHAR(100) NOT NULL,
    CONSTRAINT unique_user_date UNIQUE(user_id, date)
);
