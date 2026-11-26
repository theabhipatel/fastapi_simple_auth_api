import os
import jwt

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pwdlib import PasswordHash
from pydantic import BaseModel
from uuid import uuid4, UUID


load_dotenv()

router = APIRouter(prefix="/auth", tags=["Auth"])

JWT_SECRET=os.environ["JWT_SECRET"]
password_hash = PasswordHash.recommended()

users_db = {}

class RegisterRequest(BaseModel):
    name:str
    email:str
    password:str

class LoginRequest(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:UUID
    name:str
    email:str

class RegisterResponse(BaseModel):
     message:str
     user: UserResponse
    

@router.post("/register", status_code=201, response_model=RegisterResponse)
def register(data:RegisterRequest):
    if data.email in users_db:
        raise HTTPException(409, "Email already registered.")

    users_db[data.email] = {
        "id": uuid4(),
        "name":data.name,
        "email":data.email,
        "password": password_hash.hash(data.password),
    }

    return {
        "message":"User registered successfully.",
        "user": users_db[data.email]
    }

@router.post("/login")
def login(data:LoginRequest):

    user = users_db.get(data.email)

    if not user or not password_hash.verify(data.password, user["password"]):
        raise HTTPException(401, "Invalid email or password.")

    token = jwt.encode(
        {
            "sub": user["email"],
        },
        JWT_SECRET,
    )

    return {
        "access_token":  token
    }