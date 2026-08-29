from fastapi import APIRouter
from app.api.v1 import (
    auth_users, 
    physique, 
    workouts, 
    nutrition, 
    coach, 
    progression, 
    monetization, 
    reports
)

api_router = APIRouter()
api_router.include_router(auth_users.router)
api_router.include_router(physique.router)
api_router.include_router(workouts.router)
api_router.include_router(nutrition.router)
api_router.include_router(coach.router)
api_router.include_router(progression.router)
api_router.include_router(monetization.router)
api_router.include_router(reports.router)
