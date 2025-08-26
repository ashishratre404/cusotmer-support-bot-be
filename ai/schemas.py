from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class IngestItem(BaseModel):
    page_content: str
    metadata: Optional[Dict[str, Any]] = None

class IngestRequest(BaseModel):
    tenant_id: str
    items: List[IngestItem]

class QueryRequest(BaseModel):
    tenant_id: str
    query: str
    k: int = 5

class Answer(BaseModel):
    answer: str
    sources: List[Dict[str, Any]] = []