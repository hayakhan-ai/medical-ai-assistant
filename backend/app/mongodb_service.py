from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL"))

db = client["meditour"]
collection = db["treatments"]

def fetch_treatments():
    return list(collection.find({}, {"_id": 0}))