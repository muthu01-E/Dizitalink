from fastapi import APIRouter, HTTPException, Depends
from jose import jwt, JWTError
from database import users_collection
import os

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY")

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/api/admin/users")
def get_all_users(token: str):
    user = get_current_user(token)

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    users = list(users_collection.find({}, {"password": 0}))
    return users
