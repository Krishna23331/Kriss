
from pymongo import MongoClient
from app.config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB_NAME]
users_collection = db["users"]
