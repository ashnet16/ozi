
async def classify_query(llm_client, user_query: str) -> str:
    prompt = (
        "Classify the following query as either 'semantic' or 'analytic'. "
        "Only answer with one word: 'semantic' or 'analytic'.\n\n"
        f"Query: {user_query}"
    )
    classification = await llm_client.summarize(user_query=prompt, documents=[])
    return classification.strip().lower()


async def generate_sql_from_query(llm_client, user_query: str) -> str:
    prompt = (
        "Given the following database schema:\n"
        "Table: messages (fid INT, text TEXT, timestamp TIMESTAMP, is_comment BOOLEAN, language STRING)\n\n"
        f"Write a SQL query that answers the following question:\n\n{user_query}\n\n"
        "Always include 'LIMIT 100' to restrict result size.\n"
        "Only output the SQL code without any explanations."
    )
    sql_code = await llm_client.summarize(user_query=prompt, documents=[])
    return sql_code.strip()
