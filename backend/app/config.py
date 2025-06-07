
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') 
    MONGO_URI = os.getenv('MONGO_URI') 
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    TESTING = os.environ.get('TESTING', 'False') == 'True'
    JSON_SORT_KEYS = False