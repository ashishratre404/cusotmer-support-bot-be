import os
from typing import List, Dict, Any, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
load_dotenv() 

PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
EMBEDDINGS = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

def _collection_name(tenant_id: str) -> str:
    # one collection per tenant for strong isolation
    return f"kb_{tenant_id}"

def _store_for_tenant(tenant_id: str) -> Chroma:
    return Chroma(
        collection_name=_collection_name(tenant_id),
        embedding_function=EMBEDDINGS,
        persist_directory=PERSIST_DIR,
    )

def upsert(tenant_id: str, docs: List[Dict[str, Any]]) -> None:
    texts = [d["page_content"] for d in docs]
    metadatas = [d.get("metadata", {}) for d in docs]
    # from_texts creates the collection if missing and adds new vectors
    Chroma.from_texts(
        texts=texts,
        embedding=EMBEDDINGS,
        metadatas=metadatas,
        collection_name=_collection_name(tenant_id),
        persist_directory=PERSIST_DIR,
    )
    # ensure persisted to disk locally
    _store_for_tenant(tenant_id).persist()

def similarity_search(tenant_id: str, query: str, k: int = 5):
    store = _store_for_tenant(tenant_id)
    return store.similarity_search(query, k=k)

def similarity_search_with_threshold(tenant_id: str, query: str, k: int = 8, min_score: float = 0.3):
    """
    Returns only (doc, score) pairs where score >= min_score.
    Note: Chroma returns smaller distance = more similar if using cosine distance.
    LangChain normalizes to 'score' where higher is better for some stores,
    but Chroma via LC typically returns distances. We'll invert if needed.

    We’ll use the LC wrapper’s API:
      store.similarity_search_with_score returns (Document, score)
    For Chroma, score is distance (lower=better). We convert to 'sim' = 1 - distance.
    """
    store = _store_for_tenant(tenant_id)
    results = store.similarity_search_with_score(query, k=k)
    filtered = []
    for doc, score in results:
        # 'score' from Chroma is distance in [0, 2] for cosine. Convert to similarity.
        # A common quick mapping is sim = 1 - distance (approx). Clamp to [0,1].
        sim = max(0.0, min(1.0, 1.0 - float(score)))
        if sim >= min_score:
            # stash similarity so caller can decide display
            doc.metadata = {**(doc.metadata or {}), "_similarity": round(sim, 3)}
            filtered.append((doc, sim))
    return filtered

def peek(tenant_id: str, limit: int = 5):
    """
    Return the first N raw docs + metadata from the tenant's collection.
    Read-only; safe for debugging.
    """
    store = _store_for_tenant(tenant_id)
    data = store._collection.get(  # access underlying Chroma collection
        include=["documents", "metadatas"],
        limit=limit,
    )
    # Normalize shape for JSON
    docs = data.get("documents", []) or []
    metas = data.get("metadatas", []) or []
    items = []
    for doc, meta in zip(docs, metas):
        items.append({"page_content": doc, "metadata": meta or {}})
    return {
        "tenant_id": tenant_id,
        "count_returned": len(items),
        "items": items,
    }
