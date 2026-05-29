from fastapi import APIRouter

from src.infrastructure.api.v1 import auth_routes

api_v1_router = APIRouter()

api_v1_router.include_router(auth_routes.router, prefix="/auth" , tags=["Authentication"])