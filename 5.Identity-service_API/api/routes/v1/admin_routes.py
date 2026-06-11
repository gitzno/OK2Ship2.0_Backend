from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def index():
    return {"message": "Hello Admin!"}