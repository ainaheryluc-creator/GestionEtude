from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = None
db = None

def connect():
    global client, db
    try:
        if client is None:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
            db = client[DB_NAME]
            db.command("ping")
        return True
    except Exception as e:
        print(f"Erreur de connexion à MongoDB : {e}")
        return False

def disconnect():
    global client
    if client:
        client.close()
        client = None

def get_collection(name):
    return db[name]
