from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))

db = client["test"]
collection = db["treatments"]

def fetch_treatments():
    return list(collection.find({}, {"_id": 0}))