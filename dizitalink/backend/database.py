import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

# Load the .env located next to this file (dizitalink/backend/.env)
dotenv_path = find_dotenv(filename=".env", usecwd=True) or os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL or "xxxxx" in MONGO_URL:
    print("[database] WARNING: MONGO_URL not set or contains placeholder. Falling back to mongodb://localhost:27017", file=sys.stderr)
    MONGO_URL = "mongodb://localhost:27017"

try:
    client = MongoClient(MONGO_URL)
except Exception as e:
    print(f"[database] ERROR connecting to MongoDB with URL '{MONGO_URL}': {e}", file=sys.stderr)
    raise

db = client["dizitalink"]

users_collection = db["users"]
subscriptions_collection = db["subscriptions"]
