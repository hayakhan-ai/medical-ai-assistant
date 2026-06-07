from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.app.rag import search_medical_data
from backend.app.llm import generate_response

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
    context = search_medical_data(req.message)
    answer = generate_response(req.message, context)
    return {
        "query": req.message,
        "context": context,
        "response": answer
    }