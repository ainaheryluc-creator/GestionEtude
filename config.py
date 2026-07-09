import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "gestion_etude")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-moi")
