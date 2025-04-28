from typing import Optional
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    n_results: int = 100
    language: Optional[str] = None
    is_comment: Optional[bool] = None
    min_score: float = 0.7
