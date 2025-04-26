import json
import os
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue
from sentence_transformers import SentenceTransformer

app = FastAPI()

# --- Setup Qdrant connection
QDRANT_HOST = os.getenv("VECTOR_DB_HOST", "qdrant")
QDRANT_PORT = int(os.getenv("VECTOR_DB_PORT", "6333"))

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

collection_name = "farcaster_casts"

# --- Setup embedding model
embed_model = SentenceTransformer("intfloat/multilingual-e5-base")


@app.get("/health")
def health_check():
    return {"message": "Ozi API is up and running!"}


@app.get("/debug")
def debug_check():
    count = client.count(collection_name=collection_name).count
    scroll = client.scroll(collection_name=collection_name, limit=5, with_payload=True)
    samples = [{"payload": point.payload} for point in scroll[0]]

    return {"count": count, "sample": samples}


class QueryRequest(BaseModel):
    query: str
    n_results: int = 100
    language: Optional[str] = None
    is_comment: Optional[bool] = None
    min_score: float = 0.7


@app.post("/query")
async def stream_query(request: QueryRequest):
    query_vector = embed_model.encode(request.query).tolist()

    filters = []

    if request.language:
        filters.append(
            FieldCondition(key="language", match=MatchValue(value=request.language))
        )

    if request.is_comment is not None:
        filters.append(
            FieldCondition(key="is_comment", match=MatchValue(value=request.is_comment))
        )

    filter_obj = Filter(must=filters) if filters else None

    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=request.n_results,
        query_filter=filter_obj,
        with_payload=True,
    )

    async def event_generator():
        for hit in results:
            if hit.score >= request.min_score:
                yield json.dumps({"score": hit.score, "payload": hit.payload}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")
