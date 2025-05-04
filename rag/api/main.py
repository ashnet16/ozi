import json
import asyncio
import psycopg2
import os
from datetime import datetime
from urllib.parse import quote
from fastapi import FastAPI
from api.models.models import QueryRequest
from api.services.search import search_vector
from api.utils.llm_prompts import (
    classify_prompt,
    sql_generation_prompt,
    summarization_prompt,
)
from api.utils.sql_validator import validate_safe_sql
from api.utils.sql_formatter import clean_sql, clean_llm_sql
from llm.factory import LLMFactory
from llm.chatgpt.connection import ChatGPTConnectionInfo

app = FastAPI()

connection_info = ChatGPTConnectionInfo(api_key=os.getenv("OPENAI_API_KEY"))
llm_client = LLMFactory.create(provider="chatgpt", connection_info=connection_info)

pg_conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB", "ozi"),
    user=os.getenv("POSTGRES_USER", "ozi_user"),
    password=os.getenv("POSTGRES_PASSWORD", "ozi_pass"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
)
pg_conn.autocommit = True
cur = pg_conn.cursor()


@app.post("/search")
async def search_router(request: QueryRequest):
    classification = (await llm_client.ask(classify_prompt(request.query))).strip().lower()
    print(f"[DEBUG] classify_query → {classification}")

    if classification == "semantic":
        vector_hits = await search_vector(request)
        top_texts = []
        async for line in vector_hits.body_iterator:
            hit = json.loads(line)
            if hit.get("payload", {}).get("text"):
                top_texts.append(hit["payload"]["text"])

        summary = (
            await llm_client.summarize(request.query, top_texts[:20])
            if top_texts
            else "No relevant casts found to summarize."
        )

        return {
            "query": request.query,
            "classification": "semantic",
            "summary": summary,
            "results": top_texts,
        }

    elif classification == "analytic":
        sql_prompt = sql_generation_prompt(request.query)
        sql_code = (await llm_client.ask(sql_prompt)).strip()
        sql_code = clean_llm_sql(sql_code)
        sql_code = clean_sql(sql_code)
        validate_safe_sql(sql_code)

        cur.execute(sql_code)
        results = cur.fetchall()
        short_results = results[:100]

        flat_rows = [", ".join(map(str, row)) for row in short_results]
        summary_input = "\n".join(flat_rows)
        summary = await llm_client.ask(summarization_prompt(request.query, summary_input))

        sql_encoded = quote(sql_code)

        return {
            "query": request.query,
            "classification": "analytic",
            "sql": sql_code,
            "sample_results": short_results,
            "summary": summary.strip(),
            "full_results_link": f"/query?sql={sql_encoded}",
        }

@app.get("/query")
async def query_full(sql: str):
    sql_code = clean_llm_sql(sql.strip())
    sql_code = clean_sql(sql_code)
    validate_safe_sql(sql_code)

    cur.execute(sql_code)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    results = [dict(zip(columns, row)) for row in rows]
    return {"results": results}
