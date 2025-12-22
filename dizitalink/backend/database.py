from pymongo import MongoClient

MONGO_URL = "mongodb+srv://eesaimuthu_db_user:SOgzcCMb0SZROAYd@auth.kwosr2d.mongodb.net/"
client = MongoClient(MONGO_URL)

db = client["dizitalink"]
users_collection = db["users"]
