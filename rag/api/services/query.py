# services/query_service.py
import json
import duckdb
from fastapi.responses import StreamingResponse

DUCKDB_PATH = "/path/to/your/database.duckdb"

async def run_sql(sql: str):
    if "limit" not in sql.lower():
        sql = sql.rstrip(";") + " LIMIT 100"

    con = duckdb.connect(DUCKDB_PATH)
    cursor = con.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    con.close()

    return [dict(zip(columns, row)) for row in rows]


async def stream_full_query(sql_code: str):
    async def sql_event_stream():
        con = duckdb.connect(DUCKDB_PATH)
        cursor = con.execute(sql_code)
        columns = [desc[0] for desc in cursor.description]

        while True:
            row = cursor.fetchone()
            if row is None:
                break
            row_dict = dict(zip(columns, row))
            yield json.dumps(row_dict) + "\n"

        con.close()

    return StreamingResponse(sql_event_stream(), media_type="application/x-ndjson")
