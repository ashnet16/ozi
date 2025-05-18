import json
import os
import time
from urllib.parse import quote
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import psycopg2
from pydantic import BaseModel
from api.services.search import search_vector
from api.utils.llm_prompts import classify_prompt, sql_generation_prompt, summarization_prompt
from api.utils.sql_formatter import clean_llm_sql, clean_sql
from api.utils.sql_validator import validate_safe_sql
from api.utils.markdown_formatter import format_as_markdown
from llm.chatgpt.connection import ChatGPTConnectionInfo
from llm.factory import LLMFactory

class QueryRequest(BaseModel):
    query: str
    n_results: int = 1500
    min_score: float = 0.5
    fid: str
    search_mode: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def ensure_tables():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS query_logs (
            id SERIAL PRIMARY KEY,
            fid TEXT,
            query TEXT,
            classification TEXT[],
            sql_query TEXT,
            response_time_ms INT,
            response JSONB,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            fid TEXT PRIMARY KEY,
            general_quota INT DEFAULT 20,
            deep_quota INT DEFAULT 10,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logins (
            id SERIAL PRIMARY KEY,
            fid TEXT NOT NULL,
            login_time TIMESTAMPTZ DEFAULT NOW(),
            FOREIGN KEY (fid) REFERENCES users(fid)
        );
    """)

def enforce_quota(fid, quota_type):
    if not fid:
        return False, "Missing FID"
    cur.execute(f"SELECT {quota_type}_quota FROM users WHERE fid = %s;", (fid,))
    row = cur.fetchone()
    if not row:
        return False, "User not found or not authenticated."
    if row[0] <= 0:
        return False, f"{quota_type.capitalize()} quota exceeded."
    cur.execute(f"UPDATE users SET {quota_type}_quota = {quota_type}_quota - 1 WHERE fid = %s;", (fid,))
    return True, None

def log_query(fid, query, classification, sql_code, response, start_time):
    response_time_ms = int((time.time() - start_time) * 1000)
    cur.execute(
        "INSERT INTO query_logs (fid, query, classification, sql_query, response_time_ms, response) VALUES (%s, %s, %s, %s, %s, %s);",
        (
            fid or "anonymous",
            query,
            classification,
            sql_code,
            response_time_ms,
            json.dumps(response),
        ),
    )

@app.post("/search/markup")
async def search_markup(request: QueryRequest):
    start = time.time()
    fid = request.fid
    search_mode = request.search_mode
    if search_mode not in ("general", "deep"):
        return JSONResponse(status_code=400, content={"error": "Invalid search mode"})
    quota_type = "general" if search_mode == "general" else "deep"
    allowed, error = enforce_quota(fid, quota_type)
    if not allowed:
        return JSONResponse(status_code=403, content={"error":  "You have exceeded your search quota. Please wait or upgrade access."})


    classification_raw = await llm_client.ask(classify_prompt(request.query))
    classification = classification_raw.strip().lower()
    intents = [c.strip() for c in classification.split(",")]
    sql_code_for_log = None
    summary = ""
    top_texts = []
    sql_code = ""
    short_results = []
    sql_summary = ""
    sql_encoded = ""

    if "semantic" in intents:
        vector_hits = await search_vector(request)
        async for line in vector_hits.body_iterator:
            hit = json.loads(line)
            if hit.get("payload", {}).get("text"):
                top_texts.append(hit["payload"]["text"])
        summary = await llm_client.summarize(request.query, top_texts[:request.n_results]) if top_texts else "No relevant casts found to summarize."

    if "analytic" in intents:
        sql_prompt = sql_generation_prompt(
            request.query,
            fid=request.fid,
            mode=request.search_mode
        )
        sql_code = clean_sql(clean_llm_sql(await llm_client.ask(sql_prompt)))
        validate_safe_sql(sql_code)
        sql_code_for_log = sql_code
        cur.execute(sql_code)
        short_results = cur.fetchall()[:10]
        flat_rows = [", ".join(map(str, row)) for row in short_results]
        sql_summary = await llm_client.ask(summarization_prompt(request.query, flat_rows))
        sql_encoded = quote(sql_code)

    markdown = format_as_markdown(
        query=request.query,
        classification=intents,
        semantic_summary=summary,
        top_casts=top_texts[:10],
        sql=sql_code,
        results=short_results,
        sql_summary=sql_summary,
        full_results_link=f"/query?sql={sql_encoded}" if sql_encoded else ""
    )

    log_query(fid, request.query, intents, sql_code_for_log, {"markup": markdown}, start)
    return {"markup": markdown}

@app.post("/search")
async def search_router(request: QueryRequest):
    start = time.time()
    fid = request.fid
    search_mode = request.search_mode
    if search_mode not in ("general", "deep"):
        return JSONResponse(status_code=400, content={"error": "Invalid search mode"})
    quota_type = "general" if search_mode == "general" else "deep"
    allowed, error = enforce_quota(fid, quota_type)
    if not allowed:
        return JSONResponse(status_code=403, content={"error": error})

    classification = (await llm_client.ask(classify_prompt(request.query))).strip().lower()
    intents = [c.strip() for c in classification.split(",")]
    response = {"query": request.query, "classification": intents}
    sql_code_for_log = None
    top_texts = []

    if "semantic" in intents:
        vector_hits = await search_vector(request)
        async for line in vector_hits.body_iterator:
            hit = json.loads(line)
            if hit.get("payload", {}).get("text"):
                top_texts.append(hit["payload"]["text"])
        summary = await llm_client.summarize(request.query, top_texts[:request.n_results]) if top_texts else "No relevant casts found to summarize."
        response["summary"] = summary
        response["semantic_results"] = top_texts

    if "analytic" in intents:
        sql_prompt = sql_generation_prompt(
            request.query,
            fid=request.fid,
            mode=request.search_mode
        )
        sql_code = clean_sql(clean_llm_sql(await llm_client.ask(sql_prompt)))
        validate_safe_sql(sql_code)
        sql_code_for_log = sql_code
        cur.execute(sql_code)
        short_results = cur.fetchall()[:request.n_results]
        flat_rows = [", ".join(map(str, row)) for row in short_results]
        summary = await llm_client.ask(summarization_prompt(request.query, flat_rows))
        sql_encoded = quote(sql_code)
        response["sql"] = sql_code
        response["sample_results"] = short_results
        response["sql_summary"] = summary.strip()
        response["full_results_link"] = f"/query?sql={sql_encoded}"

    log_query(fid, request.query, intents, sql_code_for_log, response, start)
    return response

@app.get("/query")
async def query_full(sql: str, fid: str = None):
    start = time.time()
    allowed, error = enforce_quota(fid, "general")
    if not allowed:
        return JSONResponse(status_code=403, content={"error": error})
    sql_code = clean_sql(clean_llm_sql(sql.strip()))
    validate_safe_sql(sql_code)
    cur.execute(sql_code)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    results = [dict(zip(columns, row)) for row in rows]
    log_query(fid, sql_code, [], sql_code, json.loads(json.dumps({"results": results}, default=str)), start)
    return {"results": results}

@app.get("/queries")
def list_queries(limit: int = 100):
    cur.execute("SELECT id, query, classification, sql_query, created_at FROM query_logs ORDER BY created_at DESC LIMIT %s;", (limit,))
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    return {"recent_queries": [dict(zip(columns, row)) for row in rows]}

@app.post("/auth")
async def auth_user(request: Request):
    try:
        body = await request.json()
        fid = body.get("fid")
        if not fid:
            return JSONResponse(status_code=400, content={"error": "Missing fid"})
        cur.execute("INSERT INTO users (fid) VALUES (%s) ON CONFLICT (fid) DO NOTHING;", (fid,))
        cur.execute("INSERT INTO logins (fid) VALUES (%s);", (fid,))
        cur.execute("SELECT general_quota, deep_quota FROM users WHERE fid = %s;", (fid,))
        row = cur.fetchone()
        return {
            "fid": fid,
            "general_quota": row[0],
            "deep_quota": row[1],
            "status": "authenticated"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
