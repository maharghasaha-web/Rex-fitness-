from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    full_name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    fitness_goal: Optional[str] = "hypertrophy"
    experience_level: Optional[str] = "intermediate"
    target_days_per_week: Optional[int] = 5

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    fitness_goal: Optional[str] = None
    experience_level: Optional[str] = None
    target_days_per_week: Optional[int] = None

class UserOut(UserBase):
    id: int
    created_at: Optional[str] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
