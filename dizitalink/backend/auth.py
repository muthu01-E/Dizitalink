import os
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from .database import users_collection
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretjwtkey")
pwd_context = CryptContext(schemes=["bcrypt"])


class RegisterModel(BaseModel):
    name: str
    email: str
    password: str


class LoginModel(BaseModel):
    email: str
    password: str


@router.post("/api/auth/register")
def register(data: RegisterModel):
    if users_collection.find_one({"email": data.email}):
        raise HTTPException(400, "User already exists")

    users_collection.insert_one({
        "name": data.name,
        "email": data.email,
        "password": pwd_context.hash(data.password),
        "role": "user",
        "created_at": datetime.utcnow()
    })

    return {"success": True}


@router.post("/api/auth/login")
def login(data: LoginModel):
    user = users_collection.find_one({"email": data.email})

    if not user:
        raise HTTPException(404, "User not registered")

    if not pwd_context.verify(data.password, user["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = jwt.encode({
        "user_id": str(user["_id"]),
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=24)
    }, SECRET_KEY)

    return {
        "token": token,
        "role": user["role"],
        "name": user["name"]
    }


@router.get("/api/auth/me")
def me(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
