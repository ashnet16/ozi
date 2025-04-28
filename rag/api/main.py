from fastapi import FastAPI
import json
from api.models.models import QueryRequest
from api.services.search import search_vector
from api.services.query import run_sql, stream_full_query
from api.utils.llm_prompts import classify_query, generate_sql_from_query
from api.utils.sql_validator import validate_safe_sql, validate_sql_query

from llm.factory import LLMFactory
from llm.chatgpt.connection import ChatGPTConnectionInfo

import os

app = FastAPI()

connection_info = ChatGPTConnectionInfo(api_key=os.getenv("OPENAI_API_KEY"))
llm_client = LLMFactory.create(provider="chatgpt", connection_info=connection_info)

@app.post("/search")
async def search_router(request: QueryRequest):
    classification = await classify_query(llm_client, request.query)

    if classification == "semantic":
        vector_hits = await search_vector(request)

        top_texts = []
        async for line in vector_hits.body_iterator:
            hit = json.loads(line)
            if hit.get("payload", {}).get("text"):
                top_texts.append(hit["payload"]["text"])

        if top_texts:
            summary = await llm_client.summarize(request.query, top_texts[:20])
        else:
            summary = "No relevant casts found to summarize."

        return {
            "query": request.query,
            "classification": "semantic",
            "summary": summary,
            "results": top_texts
        }

    elif classification == "analytic":
        sql_code = await generate_sql_from_query(llm_client, request.query)

        validate_safe_sql(sql_code)

        results = await run_sql(sql_code)
        short_results = results[:100]

        return {
            "query": request.query,
            "classification": "analytic",
            "sql": sql_code,
            "sample_results": short_results,
            "full_results_link": f"/query?original_query={request.query}"
        }

@app.get("/query")
async def query_full(original_query: str):
    validate_sql_query(original_query)
    return await stream_full_query(original_query)
