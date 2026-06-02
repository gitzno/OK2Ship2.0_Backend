from fastapi import APIRouter

from api.routes.v1 import auth_routes

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])

router = APIRouter()

router.include_router(api_v1_router)