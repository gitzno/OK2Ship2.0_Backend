from fastapi import FastAPI
from src.infrastructure.api.router_registration import api_v1_router

app = FastAPI(
    title="OK2Ship 2.0 - Hệ thống Định danh & Phân quyền",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(api_v1_router, prefix="/v1")

@app.get("/", tags=["Root"])
def health_check():
    return {"status": "Hello World"}