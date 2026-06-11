from fastapi import APIRouter, Depends

from api.dependencies.auth_deps import verify_global_token
from api.routes.v1 import auth_routes, admin_routes

api_v1_router = APIRouter(prefix="/v1")

api_v1_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(admin_routes.router, prefix="/admin", tags=["admin"], dependencies=[Depends(verify_global_token)])


router = APIRouter()

router.include_router(api_v1_router)