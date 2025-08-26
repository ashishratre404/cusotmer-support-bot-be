# Customer Support Bot (Backend)

AI-powered backend service for a **multi-tenant customer support chatbot**.

Built with **FastAPI + LangChain + Chroma** (AI service) and **Node.js/Express** (API gateway).

## 📂 Project Structure

```
customer-support-bot-be/
  ├── ai/     # Python FastAPI service (RAG with LangChain + Chroma)
  └── api/    # Node.js Express API (gateway between frontend and AI service)
```

## 🚀 Features (MVP)

- Multi-tenant support (separate collections per company).
- `/ingest` → upload FAQs/docs into a vector DB.
- `/query` → retrieve relevant chunks & answer using OpenAI LLMs.
- `/debug/peek` → inspect stored vectors (dev only).
- FastAPI server on `:8001`, Node API gateway on `:3000`.

## 🛠️ Tech Stack

- **AI Service (Python)**: FastAPI, LangChain, ChromaDB, OpenAI API
- **API Gateway (Node.js)**: Express, Axios
- **Vector DB**: Chroma (local persistence, per-tenant collections)

## 🔑 Environment

In `ai/.env`:

```
OPENAI_API_KEY=sk-xxx
CHROMA_PERSIST_DIR=./data/chroma_db
```

In `api/.env`:

```
PORT=3000
AI_SERVICE_URL=http://localhost:8001
```

---

