from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json

from api.utils.chroma import get_chroma_client

app = FastAPI()

client = get_chroma_client()
collection = client.get_or_create_collection(name="farcaster_messages")


@app.get("/health")
def root():
    return {"message": "Ozi API is up and running!"}


class QueryRequest(BaseModel):
    query: str
    n_results: int = 10
    language: Optional[str] = None
    is_comment: Optional[bool] = None


@app.post("/query")
async def stream_query(request: QueryRequest):
    filters = {}
    if request.language:
        filters["language.code"] = request.language
    if request.is_comment is not None:
        filters["is_comment"] = request.is_comment

    results = collection.query(
        query_texts=[request.query],
        n_results=request.n_results,
        where=filters or None
    )

    async def event_generator():
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            yield json.dumps({"text": doc, "metadata": meta}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")
