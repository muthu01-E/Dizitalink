from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from database import users_collection

app = FastAPI()
SECRET_KEY = "CHANGE_THIS_SECRET"
pwd_context = CryptContext(schemes=["bcrypt"])

class RegisterModel(BaseModel):
    name: str
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str

# ================= REGISTER =================
@app.post("/api/auth/register")
def register(data: RegisterModel):
    existing = users_collection.find_one({"email": data.email})

    if existing:
        raise HTTPException(400, "User already exists")

    hashed_password = pwd_context.hash(data.password)

    users_collection.insert_one({
        "name": data.name,
        "email": data.email,
        "password": hashed_password,
        "role": "user",   # default role
        "created_at": datetime.utcnow()
    })

    return {"success": True, "message": "User registered"}

# ================= LOGIN =================
@app.post("/api/auth/login")
def login(data: LoginModel):
    user = users_collection.find_one({"email": data.email})

    # ❌ NOT REGISTERED → LOGIN BLOCKED
    if not user:
        raise HTTPException(404, "User not registered")

    # ❌ PASSWORD WRONG
    if not pwd_context.verify(data.password, user["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = jwt.encode(
        {
            "user_id": str(user["_id"]),
            "role": user["role"],
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        SECRET_KEY
    )

    return {
        "token": token,
        "role": user["role"],
        "name": user["name"]
    }
