import asyncio
import json
import os
from datetime import datetime
from urllib.parse import quote

import psycopg2
from api.models.models import QueryRequest
from api.services.search import search_vector
from api.utils.llm_prompts import (
    classify_prompt,
    sql_generation_prompt,
    summarization_prompt,
)
from api.utils.sql_formatter import clean_llm_sql, clean_sql
from api.utils.sql_validator import validate_safe_sql
from fastapi import FastAPI
from llm.chatgpt.connection import ChatGPTConnectionInfo
from llm.factory import LLMFactory

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

@app.get("/health")
def health_check():
    try:
        cur.execute("SELECT 1;")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

@app.on_event("startup")
def ensure_user_queries_table():
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_queries (
            id SERIAL PRIMARY KEY,
            query TEXT NOT NULL,
            classification TEXT[],
            sql_query TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """
    )
    print("[INFO] Ensured user_queries table exists.")


@app.post("/search")
async def search_router(request: QueryRequest):
    classification = (
        (await llm_client.ask(classify_prompt(request.query))).strip().lower()
    )
    print(f"[DEBUG] classify_query → {classification}")

    intents = [c.strip() for c in classification.split(",")]
    response = {"query": request.query, "classification": intents}
    sql_code_for_log = None

    if "semantic" in intents:
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
        response["summary"] = summary
        response["semantic_results"] = top_texts

    if "analytic" in intents:
        sql_prompt = sql_generation_prompt(request.query)
        sql_code = (await llm_client.ask(sql_prompt)).strip()
        sql_code = clean_llm_sql(sql_code)
        sql_code = clean_sql(sql_code)
        validate_safe_sql(sql_code)

        sql_code_for_log = sql_code

        cur.execute(sql_code)
        results = cur.fetchall()
        short_results = results[:100]
        flat_rows = [", ".join(map(str, row)) for row in short_results]

        summary = await llm_client.ask(summarization_prompt(request.query, flat_rows))
        sql_encoded = quote(sql_code)

        response["sql"] = sql_code
        response["sample_results"] = short_results
        response["sql_summary"] = summary.strip()
        response["full_results_link"] = f"/query?sql={sql_encoded}"

    cur.execute(
        "INSERT INTO user_queries (query, classification, sql_query) VALUES (%s, %s, %s)",
        (request.query, intents, sql_code_for_log),
    )

    return response


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


@app.get("/queries")
def list_queries(limit: int = 100):
    cur.execute(
        """
        SELECT id, query, classification, sql_query, created_at
        FROM user_queries
        ORDER BY created_at DESC
        LIMIT %s;
    """,
        (limit,),
    )
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    return {"recent_queries": [dict(zip(columns, row)) for row in rows]}
