from typing import List, Dict, Any
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini") 

SYSTEM = (
    "You are a helpful customer support assistant. "
    "Use the provided context to answer. If unsure, say you don't know. "
    "Cite sources when relevant."
)

def answer_with_rag(question: str, docs: List[Any]) -> Dict[str, Any]:
    # docs are LC Document objects from similarity_search
    context = "\n\n".join(
        f"[{i+1}] {d.page_content}\nMETA: {d.metadata}" for i, d in enumerate(docs)
    )
    prompt = f"{SYSTEM}\n\nContext:\n{context}\n\nUser question: {question}\n\nAnswer:"
    resp = llm.invoke(prompt)
    sources = [getattr(d, "metadata", {}) for d in docs]
    return {"answer": resp.content, "sources": sources}
