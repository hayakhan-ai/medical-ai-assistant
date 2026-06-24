from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from app.rag import search_medical_data
from app.llm import generate_response, small_reply, generate_title, classify_query
from app.mongodb_service import create_conversation, save_message, get_conversations, get_messages, get_conversation, update_conversation_title, get_user_questions
from app.voice_service import voice_chat
import os

app = FastAPI()


app.mount(
    "/audio",
    StaticFiles(directory="audio"),
    name="audio"
)

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
    try:

        conversation_id = req.conversation_id

        if not conversation_id:
            conversation_id = create_conversation()

        history = get_messages(conversation_id)[-8:]

        conversation = get_conversation(conversation_id) or {}
        title_generated = conversation.get("title_generated", False)

        query_type = classify_query(
            req.message,
            history
        )

        # greetings
        if query_type in [
            "GREETING",
            "THANKS",
            "GOODBYE",
            "ACKNOWLEDGEMENT"
        ]:

            answer = small_reply(
                req.message,
                """
Respond naturally and briefly.
Reply in the user's language.
"""
            )

        else:

            # RAG ONLY uses current question
            context = search_medical_data(
                req.message,
                limit=20
            )

            print("\nQUESTION:")
            print(req.message)

            print("\nCONTEXT:")
            for item in context:
                print(item)

            answer = generate_response(
                req.message,
                context,
                history
            )

            print("\nFINAL ANSWER:")
            print(answer)

        save_message(
            conversation_id,
            req.message,
            answer
        )

        # generate title once
        if not title_generated:

            questions = get_user_questions(conversation_id)

            if len(questions) >= 3:

                title = generate_title(
                    get_messages(conversation_id)[-6:]
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

        print("ERROR:", e)

        return {
            "response":
            "I'm temporarily unavailable. Please try again in a few seconds."
        }

@app.get("/chat-history")
async def chat_history():
    conversations = get_conversations()
    return conversations

@app.post("/new-chat")
async def new_chat():
    conversation_id = create_conversation()
    return {"conversation_id": conversation_id}

@app.get("/conversation/{conversation_id}")
async def conversation(conversation_id: str):
    conversation = get_conversation(conversation_id)
    return conversation

@app.post("/voice-chat")
async def voice_endpoint(
    file: UploadFile = File(...),
    conversation_id: str = ""
):
    try:
        # create conversation if none exists
        if not conversation_id:
            conversation_id = create_conversation()

        path = "temp.webm"    

        with open(path, "wb") as f:
            f.write(await file.read())

        history = get_messages(conversation_id)[-8:]

        result = await voice_chat(
            path,
            history
        )

        save_message(
            conversation_id,
            result["query"],
            result["response"]
        )

        # title generation
        conversation = get_conversation(conversation_id) or {}
        title_generated = conversation.get("title_generated", False)

        if not title_generated:
            questions = get_user_questions(conversation_id)
            if len(questions) >= 3:
                title = generate_title(
                    get_messages(conversation_id)[-6:]
                )
                update_conversation_title(
                    conversation_id,
                    title
                )

        if os.path.exists(path):
            os.remove(path)        

        return {
            "conversation_id": conversation_id,
            "query": result["query"],
            "response": result["response"],
            "language": result["language"],
            "audio": f"audio/{result['audio_file']}"
        }
    except Exception as e:
        print("ERROR:", e)
        return {
            "response": "Voice service temporarily unavailable."
        }
