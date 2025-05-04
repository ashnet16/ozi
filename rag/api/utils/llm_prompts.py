def classify_prompt(user_query: str) -> str:
    return f"""
You are a classifier for a Farcaster search engine.

Your job is to classify the user’s question into one of two categories:

1. "semantic" — if the user is asking for **content of casts or comments**, such as opinions, conversations, or natural language text search.
2. "analytic" — if the user is asking for **counts, metrics, aggregates, or trends**, like number of likes, top users, frequency over time, etc.

Be conservative — only classify as "analytic" if the user is clearly asking for structured data or metrics.

Return just one word: "semantic" or "analytic".

User question: "{user_query}"
""".strip()


def sql_generation_prompt(user_query: str) -> str:
    return f"""
You are an expert SQL engineer working only with Farcaster event data.

You have access to the following PostgreSQL tables:

- "casts":
    - id: BIGINT
    - text: TEXT (the actual content of the user's post)
    - lang: TEXT (short for language, e.g., "en", "es")
    - embeds: TEXT (a JSON string representing media, links, or attached content)
    - mentions: TEXT (a JSON string listing user mentions)
    - msg_timestamp: TIMESTAMP WITH TIME ZONE

- "comments":
    - id: BIGINT
    - parent_fid: BIGINT
    - parent_hash: TEXT
    - text: TEXT (the actual content of the user's comment)
    - lang: TEXT (short for language, e.g., "en", "es")
    - embeds: TEXT (a JSON string representing media, links, or attached content)
    - msg_timestamp: TIMESTAMP WITH TIME ZONE

- "reactions":
    - id: BIGINT
    - reaction_type: TEXT (e.g., "like", "recast")
    - target_fid: BIGINT
    - target_hash: TEXT
    - msg_timestamp: TIMESTAMP WITH TIME ZONE

Guidelines:
- Generate valid PostgreSQL SQL syntax.
- If using a subquery in FROM, always give it an alias, e.g., FROM (SELECT ...) AS sub.
- Do not return markdown or wrap code in triple backticks.
- Only return valid SQL. No explanation or commentary.

User question: {user_query}
""".strip()


def summarization_prompt(user_query: str, flat_results: list[str]) -> str:
    rows_text = "\n".join(flat_results)
    return f"""
Summarize the results below based on the user question: "{user_query}"

Results:
{rows_text}
""".strip()
