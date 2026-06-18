from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from app.rag import search_medical_data
from app.llm import generate_response, classify_query, generate_chat_title
from app.mongodb_service import create_conversation, save_message, get_conversations, get_messages, get_conversation, update_conversation_title, get_user_questions


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    

@app.get("/")
def home():
    return {"message": "Medical AI Assistant Running"}

@app.post("/chat")
async def chat(req: ChatRequest):

    query_type = classify_query(req.message)

    try:

        conversation_id = req.conversation_id

        if not conversation_id:
            conversation_id = create_conversation()

        # Recent history only
        history = get_messages(conversation_id)[-6:]

        # Current conversation
        conversation = get_conversation(conversation_id) or {}

        # Has title already been generated?
        title_generated = conversation.get(
            "title_generated",
            False
        )

        if query_type in ["GREETING","NON-MEDICAL","THANKS","GOODBYE","ACKNOWLEDGEMENT"]:

            answer = generate_response(
            req.message,
            [],
            history
            )

            save_message(
            conversation_id,
            req.message,
            answer
            )
   
        elif query_type == "FOLLOW_UP" and len(history) > 0:
              
            recent_questions = [
                msg["question"]
                for msg in history[-3:]
            ]

            search_query = " ".join(recent_questions)
            search_query += " " + req.message

            context = search_medical_data(search_query, limit=5)

            print("\nSEARCH QUERY:", search_query)
            print("CONTEXT:", context)

            answer = generate_response(
                req.message,
                context,
                history
            )

        else:
            recent_questions = [
                msg["question"]
                for msg in history[-3:]
            ]

            search_query = " ".join(recent_questions)
            search_query += " " + req.message

            context = search_medical_data(search_query)

            print("\nSEARCH QUERY:", search_query)
            print("CONTEXT:", context)

            answer = generate_response(
                req.message,
                context,
                history
            )

            save_message(
                conversation_id,
                req.message,
                answer
            )

            # Generate title once after 3 messages
            if not title_generated:

                 questions = get_user_questions(conversation_id)

                 if len(questions) >= 3:

                     title = generate_chat_title(
                         "\n".join(questions[:4])
                    )

                     update_conversation_title(
                         conversation_id,
                         title
                    )

        return {
            "conversation_id": conversation_id,
            "response": answer
        }

    except Exception as e:

        return {
            "response": f"Internal error: {str(e)}"
        }
       

@app.get("/chat-history")
async def chat_history():

    conversations = get_conversations()

    return conversations

@app.post("/new-chat")
async def new_chat():

    conversation_id = create_conversation()

    return {
        "conversation_id": conversation_id
    }

@app.get("/conversation/{conversation_id}")
async def conversation(conversation_id: str):

    conversation = get_conversation(conversation_id)

    return conversation