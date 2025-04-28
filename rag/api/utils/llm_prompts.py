async def classify_query(llm_client, user_query: str) -> str:
    prompt = f"""
You are an assistant working with a Farcaster event database.
You must classify the following user question into one of two categories:
- "semantic" if the user wants to search text content of casts or comments.
- "analytic" if the user wants to query metadata like number of reactions, trends, etc.

Only answer "semantic" or "analytic".

User question: {user_query}
    """
    response = await llm_client.ask(prompt)
    return response.strip().lower()



async def generate_sql_from_query(llm_client, user_query: str) -> str:
    prompt = f"""
You are an expert SQL engineer working only with Farcaster event data.

You have these DuckDB tables:
- "casts" (fields: id, text, lang, embeds, mentions, msg_timestamp)
- "comments" (fields: id, parent_fid, parent_hash, text, lang, embeds, msg_timestamp)
- "reactions" (fields: id, reaction_type, target_fid, target_hash, msg_timestamp)

Generate a correct SQL query based ONLY on the user's request over this data.

User question: {user_query}

ONLY return the SQL code. Do not explain.
    """
    response = await llm_client.ask(prompt)
    return response.strip()
