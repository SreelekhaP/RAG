from pydantic import BaseModel
from typing import List, Dict, Any

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResult(BaseModel):
    content: str
    score: float
    metadata: Dict[str, Any]

class QueryResponse(BaseModel):
    query: str
    count: int
    results: List[QueryResult]

class DocumentResponse(BaseModel):
    filename: str
    status: str
    text_length: int
    chunks_indexed: int

class IndexStatus(BaseModel):
    index_exists: bool
    vectorstore_loaded: bool