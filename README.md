# 🏥 Medical AI Assistant

An intelligent AI-powered medical assistant built with **FastAPI**, **React**, and modern AI tooling to provide fast, scalable, and modular healthcare-related conversational support.

This project is designed as a backend API + frontend chatbot interface that can integrate with:

* 🤖 LLMs (OpenAI, Gemini, Claude, etc.)
* 🧠 Vector Databases (Qdrant, Pinecone)
* 📄 RAG Pipelines
* 🌐 Multi-platform Bots & APIs

---

# ✨ Features

* ⚡ FastAPI-powered backend
* 💬 AI chatbot interaction system
* 🌐 React frontend interface
* 🔌 REST API architecture
* 🧠 Easily extendable for AI integrations
* 📡 Frontend ↔ Backend API communication
* 🔒 Modular project structure

---

# 🛠️ Tech Stack

| Technology | Purpose               |
| ---------- | --------------------- |
| FastAPI    | Backend API Framework |
| React      | Frontend UI           |
| Axios      | API Communication     |
| Uvicorn    | ASGI Server           |
| Python     | Backend Logic         |
| JavaScript | Frontend Logic        |
| Qdrant     | RAG database          |
| llama-3.3-70b-versatile | LLM      |
| sentence transformers | embedding vectors |

---

# 📂 Project Structure

```bash id="u0f7kq"
medical-ai-assistant/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
└── README.md
```

---

# ⚙️ Backend Setup (FastAPI)

## 1️⃣ Navigate to backend

```bash id="42ls3m"
cd backend
```

## 2️⃣ Create virtual environment

### Windows

```bash id="r8q9wz"
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash id="tw6m8v"
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install dependencies

```bash id="9up7c2"
pip install -r requirements.txt
```

---

## 4️⃣ Run FastAPI server

```bash id="1af3kj"
uvicorn app.main:app --reload
```

Backend runs on:

```bash id="s6elx9"
http://127.0.0.1:8000
```

---

# ⚛️ Frontend Setup (React)

## 1️⃣ Navigate to frontend

```bash id="y1v2k8"
cd frontend
```

## 2️⃣ Install dependencies

```bash id="u7m4qp"
npm install
```

---

## 3️⃣ Start React app

```bash id="k0d9nx"
npm run dev
```

or

```bash id="9g2sfd"
npm start
```

depending on your setup.

Frontend usually runs on:

```bash id="v4n8cb"
http://localhost:5173
---



