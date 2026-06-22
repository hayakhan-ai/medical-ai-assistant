from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from uuid import uuid4
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))

db = client["test"]
# ==========================
# Medical collections
# ==========================

treatments_collection = db["treatments"]
doctors_collection = db["doctors"]
hospitals_collection = db["hospitals"]
laboratories_collection = db["laboratories"]
specialities_collection = db["specialities"]
tests_collection = db["tests"]

conversation_collection = db["conversations"]


def fetch_treatments():
    return list(
        treatments_collection.find(
            {},
            {
                "_id": 0,
                "subCategory": 1,
                "description": 1
             }
        )
    )

def fetch_doctors():
    return list(
        doctors_collection.find(
            {},
            {
                "_id": 0,
                "name": 1,
                "qualifications": 1,
                "speciality": 1,
                "clinicExperience": 1,
                "about": 1,
                "location.city": 1,
                "location.address": 1,
                "phoneNumber": 1,
                "email":1,
                "country":1
            }
        )
    )

def fetch_hospitals():
    return list(
        hospitals_collection.find(
            {},
            {
                "_id": 0,
                "name": 1,
                "location.city": 1,
                "location.address": 1,
                "emergencyNo": 1,
                "openTime": 1,
                "phoneNumber": 1,
                "email": 1,
                "country": 1
            }
        )
    )

def fetch_laboratories():
    return list(
        laboratories_collection.find(
            {},
            {
                "_id": 0,
                "name": 1,
                "description": 1,
                "location.city": 1,
                "location.address": 1,
                "phoneNumber": 1,
                "email": 1,
                "emergencyNo": 1,
                "openTime": 1
            }
        )
    )

def fetch_specialities():
    return list(
        specialities_collection.find(
            {},
            {
                "_id": 0,
                "specialityTitle": 1
            }
        )
    )

def fetch_tests():
    return list(
        tests_collection.find(
            {},
            {
                "_id": 0,
                "testDescription": 1,
                "discount": 1,
                "duration": 1
            }
        )
    )


def create_conversation():

    conversation_id = str(uuid4())

    conversation_collection.insert_one({
        "conversation_id": conversation_id,
        "title": "New Chat",
        "messages": [],
        "timestamp": datetime.utcnow(),
        "title_generated": False
    })

    return conversation_id       


def save_message(conversation_id, question, answer):

    conversation_collection.update_one(
        {
            "conversation_id": conversation_id
        },
        {
            "$push": {
                "messages": {
                    "question": question,
                    "answer": answer,
                    "timestamp": datetime.utcnow()
                }
            }
        }
    )

def get_conversation(conversation_id): 
    return conversation_collection.find_one( 
        { 
            "conversation_id": conversation_id 
        }, 
        { 
            "_id": 0 
        } 
    )

def get_messages(conversation_id):

    conversation = get_conversation(conversation_id)

    if conversation:
        return conversation["messages"]

    return []

def get_conversations():

    conversations = list(
        conversation_collection.find(
            {},
            {
                "_id": 0
            }
        ).sort("timestamp", -1)
    )

    return conversations

def update_conversation_title(conversation_id, title):

    conversation_collection.update_one(
        {
            "conversation_id": conversation_id
        },
        {
            "$set": {
                "title": title,
                "title_generated": True
            }
        }
    )

def get_user_questions(conversation_id):

    conversation = get_conversation(conversation_id)

    if conversation:

        return [
            msg["question"]
            for msg in conversation["messages"]
        ]

    return []