from fastapi import Header, HTTPException
from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY")

def get_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid auth header")

    token = authorization.split(" ")[1]
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
