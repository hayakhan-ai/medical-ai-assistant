# 🏥 MediTour Global – AI Medical Assistant

An intelligent AI-powered medical assistant built with **FastAPI**, **React**, **Qdrant**, and **LLMs** to provide multilingual healthcare-related conversational support.

The assistant combines **Retrieval-Augmented Generation (RAG)** with voice capabilities and conversation memory to deliver accurate and context-aware responses.

---

# ✨ Features

* 💬 AI-powered medical chatbot
* 🧠 Retrieval-Augmented Generation (RAG)
* 📚 Vector search using Qdrant
* 🌐 Multi-language support
* 🎙️ Speech-to-Text (Voice Input)
* 🔊 Text-to-Speech (Voice Responses)
* 🗂️ Conversation history management
* 🏷️ Automatic chat title generation
* ⚡ FastAPI backend
* ⚛️ React frontend
* 🔌 REST API architecture
* 🔒 Modular and scalable design

---

# 🛠️ Tech Stack

| Technology            | Purpose               |
| --------------------- | --------------------- |
| FastAPI               | Backend API Framework |
| React                 | Frontend UI           |
| Axios                 | API Communication     |
| Python                | Backend Logic         |
| JavaScript            | Frontend Logic        |
| MongoDB               | Conversation History  |
| Qdrant                | Vector Database       |
| Sentence Transformers | Embedding Generation  |
| Groq Llama 3.3 70B    | Large Language Model  |
| Whisper               | Speech-to-Text        |
| Edge-TTS              | Text-to-Speech        |
| Uvicorn               | ASGI Server           |

---

# 📂 Project Structure

```bash
medical-ai-assistant/
│
├── backend/
│   ├── app/
│   │   ├── llm.py
│   │   ├── rag.py
│   │   ├── main.py
│   │   ├── speech_to_text.py
│   │   ├── tts.py
│   │   ├── voice_service.py
│   │   └── mongodb_service.py
│   │
│   ├── audio/
│   ├── qdrant_db/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
└── README.md
```

---

# 🧠 AI Architecture

```text
User Query
     ↓
Conversation History
     ↓
Query Expansion
     ↓
Qdrant Vector Search
     ↓
Relevant Medical Context
     ↓
Llama 3.3 70B
     ↓
Response Generation
     ↓
Text Response / Voice Response
```

---

# ⚙️ Backend Setup

## Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run FastAPI

```bash
uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

---

# ⚛️ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# 🚀 Current Capabilities

* Medical RAG system
* Multi-turn conversation memory
* Voice chat support
* Automatic chat title generation
* Qdrant vector search
* Multilingual responses
* Fast and scalable architecture

---




This application is intended for informational purposes only and does not replace professional medical advice, diagnosis, or treatment.

