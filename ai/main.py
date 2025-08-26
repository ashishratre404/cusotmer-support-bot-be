# main.py
from fastapi import FastAPI, Query, Body
from typing import Dict, List
from schemas import IngestRequest, QueryRequest, Answer
import vector_store  
from rag import answer_with_rag

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from AI service 👋"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(req: IngestRequest):
    docs = [{"page_content": it.page_content, "metadata": it.metadata or {}} for it in req.items]
    vector_store.upsert(req.tenant_id, docs)
    return {"status": "ok", "tenant_id": req.tenant_id, "count_added": len(docs)}

@app.post("/query", response_model=Answer)
def query(req: QueryRequest = Body(...)):
    docs = vector_store.similarity_search(req.tenant_id, req.query, k=req.k)
    return answer_with_rag(req.query, docs)

@app.get("/debug/peek")
def debug_peek(tenant_id: str = Query(...), limit: int = Query(5, ge=1, le=50)):
    """
    Example: GET /debug/peek?tenant_id=google&limit=5
    """
    return vector_store.peek(tenant_id, limit)