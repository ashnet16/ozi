import json
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue
from fastapi.responses import StreamingResponse
from sentence_transformers import SentenceTransformer

client = QdrantClient(host="qdrant", port=6333)
embed_model = SentenceTransformer("intfloat/multilingual-e5-base")
collection_name = "farcaster_casts"

SUMMARY_LIMIT = 1000

async def search_vector(request):
    query_vector = embed_model.encode(request.query).tolist()

    filters = []
    if request.language:
        filters.append(FieldCondition(key="language", match=MatchValue(value=request.language)))
    if request.is_comment is not None:
        filters.append(FieldCondition(key="is_comment", match=MatchValue(value=request.is_comment)))

    filter_obj = Filter(must=filters) if filters else None

    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=request.n_results,
        query_filter=filter_obj,
        with_payload=True,
    )

    top_hits_for_summary: List[str] = [
        hit.payload.get("text", "") for hit in results[:SUMMARY_LIMIT]
    ]
    async def event_generator():
        for hit in results:
            if hit.score >= request.min_score:
                yield json.dumps({"score": hit.score, "payload": hit.payload}) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")
