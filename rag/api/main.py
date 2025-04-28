from fastapi import FastAPI
from models import QueryRequest
from services.search import search_vector
from services.query import run_sql, stream_full_query
from utils.llm_prompts import classify_query, generate_sql_from_query

from llm.factory import LLMFactory
from llm.chatgpt.connection import ChatGPTConnectionInfo
from utils.sql_validator import validate_safe_sql
import os

app = FastAPI()

connection_info = ChatGPTConnectionInfo(api_key=os.getenv("OPENAI_API_KEY"))
llm_client = LLMFactory.create(provider="chatgpt", connection_info=connection_info)


@app.post("/search")
async def search_router(request: QueryRequest):
    classification = await classify_query(llm_client, request.query)

    if classification == "semantic":
        return await search_vector(request)

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
    sql_code = await generate_sql_from_query(llm_client, original_query)
    return await stream_full_query(sql_code)
