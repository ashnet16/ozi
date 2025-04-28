from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    query: str
    n_results: Optional[int] = 10
    min_score: Optional[float] = 0.5
    language: Optional[str] = None
    is_comment: Optional[bool] = None
    fid: Optional[int] = None
