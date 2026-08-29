import sqlite3
import json
from contextlib import contextmanager
from app.core.config import settings

def get_db_connection():
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def db_session():
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with db_session() as conn:
        cursor = conn.cursor()
        
        # 1. Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            height_cm REAL,
            weight_kg REAL,
            fitness_goal TEXT DEFAULT 'hypertrophy',
            experience_level TEXT DEFAULT 'intermediate',
            target_days_per_week INTEGER DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. Physique Scans
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS physique_scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            image_url TEXT,
            body_fat_estimate_range TEXT,
            conditioning_summary TEXT NOT NULL,
            muscular_strengths TEXT, -- JSON
            focus_areas TEXT, -- JSON
            recommended_split TEXT NOT NULL,
            training_recommendations TEXT, -- JSON
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """)

        # 3. Workout Splits
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workout_splits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            days_per_week INTEGER DEFAULT 5,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """)

        # 4. Workout Days
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workout_days (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            split_id INTEGER NOT NULL,
            day_number INTEGER NOT NULL,
            name TEXT NOT NULL,
            target_muscle_groups TEXT, -- JSON
            estimated_duration_minutes INTEGER DEFAULT 60,
            order_index INTEGER DEFAULT 0,
            FOREIGN KEY (split_id) REFERENCES workout_splits (id)
        );
        """)

        # 5. Exercises
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_day_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            target_muscle TEXT NOT NULL,
            sets INTEGER DEFAULT 3,
            rep_range TEXT DEFAULT '8-12',
            rpe_target REAL DEFAULT 8.0,
            rest_seconds INTEGER DEFAULT 90,
            notes TEXT,
            is_compound BOOLEAN DEFAULT 1,
            order_index INTEGER DEFAULT 0,
            FOREIGN KEY (workout_day_id) REFERENCES workout_days (id)
        );
        """)

        # 6. Workout Logs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workout_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            workout_day_id INTEGER NOT NULL,
            scheduled_date TEXT NOT NULL,
            completed_date TEXT,
            status TEXT DEFAULT 'completed',
            duration_minutes INTEGER,
            total_volume_kg REAL,
            calories_burned REAL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (workout_day_id) REFERENCES workout_days (id)
        );
        """)

        # 7. Nutrition Logs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS nutrition_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            meal_type TEXT NOT NULL,
            image_url TEXT,
            total_calories REAL DEFAULT 0.0,
            total_protein_g REAL DEFAULT 0.0,
            total_carbs_g REAL DEFAULT 0.0,
            total_fat_g REAL DEFAULT 0.0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """)

        # 8. Food Item Logs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_item_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nutrition_log_id INTEGER NOT NULL,
            food_name TEXT NOT NULL,
            estimated_portion TEXT,
            calories REAL DEFAULT 0.0,
            protein_g REAL DEFAULT 0.0,
            carbs_g REAL DEFAULT 0.0,
            fat_g REAL DEFAULT 0.0,
            confidence_score REAL DEFAULT 0.9,
            FOREIGN KEY (nutrition_log_id) REFERENCES nutrition_logs (id)
        );
        """)
