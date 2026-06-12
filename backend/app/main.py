from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.rag import search_medical_data
from app.llm import generate_response, classify_query

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

@app.get("/")
def home():
    return {"message": "Medical AI Assistant Running"}

@app.post("/chat")
async def chat(req: ChatRequest):

    query_type = classify_query(req.message)

    if query_type == "GREETING":
        return {
            "query": req.message,
            "context": None,
            "response": (
                "Hello! I am a Medical AI Assistant. "
                "You can ask me about symptoms, diseases, treatments, medicines, "
                "or which medical specialist to consult."
            )
        }

    if query_type == "NON_MEDICAL":
        return {
            "query": req.message,
            "context": None,
            "response": "I can only answer medical-related questions."
        }

    context = search_medical_data(req.message)
    answer = generate_response(req.message, context)

    return {
        "query": req.message,
        "context": context,
        "response": answer
    }
