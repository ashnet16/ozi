import re
import duckdb

DANGEROUS_KEYWORDS = [
    "DROP",
    "DELETE",
    "INSERT",
    "UPDATE",
    "ALTER",
    "TRUNCATE",
    "GRANT",
    "REVOKE",
]

def validate_safe_sql(sql_query: str) -> None:
    sql_upper = sql_query.strip().upper()

    if not sql_upper.startswith("SELECT"):
        raise ValueError("Unsafe SQL: query must start with SELECT.")

    for keyword in DANGEROUS_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql_upper):
            raise ValueError(f"Unsafe SQL: detected dangerous keyword '{keyword}'.")



def validate_sql_query(sql_query: str) -> None:

    validate_safe_sql(sql_query)
    try:
        conn = duckdb.connect("duckdb_data/ozi.duckdb")
        conn.execute("BEGIN TRANSACTION;")
        conn.execute(sql_query)
        conn.execute("ROLLBACK;")
        conn.close()
    except Exception as e:
        raise ValueError(f"Invalid SQL query: {e}")

