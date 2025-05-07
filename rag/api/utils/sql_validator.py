import re

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
    print(f"Validating SQL: {sql_query}")
    sql_clean = sql_query.strip().upper()

    if not sql_clean.startswith("SELECT"):
        raise ValueError("Unsafe SQL: query must start with SELECT.")

    for keyword in DANGEROUS_KEYWORDS:
        if keyword in sql_clean:
            raise ValueError(f"Unsafe SQL: contains dangerous keyword '{keyword}'")
