from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    account: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    
    return {"messsage": "Login successful"}