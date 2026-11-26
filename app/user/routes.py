from fastapi import APIRouter, Depends
from app.middleware import get_current_user
from app.auth.routes import UserResponse

router = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[Depends(get_current_user)])

@router.get("/profile", response_model=UserResponse)
def get_profile(user=Depends(get_current_user)):
    return user


