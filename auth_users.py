from fastapi import APIRouter, HTTPException, status
import hashlib
import json
from app.db.database import db_session
from app.schemas.user import UserCreate, UserOut, UserUpdate, Token

router = APIRouter(prefix="/users", tags=["Users & Authentication"])

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (user_in.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="User with this email already exists")

        cursor.execute("""
        INSERT INTO users (email, hashed_password, full_name, age, gender, height_cm, weight_kg, fitness_goal, experience_level, target_days_per_week)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_in.email,
            hash_pw(user_in.password),
            user_in.full_name,
            user_in.age,
            user_in.gender,
            user_in.height_cm,
            user_in.weight_kg,
            user_in.fitness_goal,
            user_in.experience_level,
            user_in.target_days_per_week
        ))
        user_id = cursor.lastrowid
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = dict(cursor.fetchone())
        return UserOut(**row)

@router.post("/login", response_model=Token)
def login_user(email: str, password: str):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, hashed_password FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if not row or row["hashed_password"] != hash_pw(password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        return Token(access_token=f"user-token-{row['id']}", token_type="bearer")

@router.get("/{user_id}", response_model=UserOut)
def get_user_profile(user_id: int):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        return UserOut(**dict(row))

@router.patch("/{user_id}", response_model=UserOut)
def update_user_profile(user_id: int, user_update: UserUpdate):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")

        updates = user_update.dict(exclude_unset=True)
        if updates:
            set_clauses = [f"{k} = ?" for k in updates.keys()]
            values = list(updates.values()) + [user_id]
            cursor.execute(f"UPDATE users SET {', '.join(set_clauses)} WHERE id = ?", values)

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return UserOut(**dict(cursor.fetchone()))
