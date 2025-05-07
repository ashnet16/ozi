def classify_prompt(user_query: str) -> str:
    return f"""
You are a classifier for a Farcaster search engine.

Your job is to detect one or more types of intents in a user's question.

Each intent must be one of:
- "semantic": asking for the content of casts/comments (opinions, discussions, etc.)
- "analytic": asking for metrics, aggregates, trends (e.g., counts, likes, top users)

If the user query involves **multiple actions**, such as summarizing AND ranking, return them **both**.

Return a comma-separated list of intents such as:
- semantic
- analytic
- semantic,analytic

User question: "{user_query}"
""".strip()


def sql_generation_prompt(user_query: str) -> str:
    return f"""
You are an expert SQL engineer working only with Farcaster event data.

You have access to the following PostgreSQL tables:

- "casts":
    - id: BIGINT
    - msg_type: TEXT
    - fid: BIGINT
    - msg_timestamp: TIMESTAMP WITH TIME ZONE
    - text: TEXT
    - lang: TEXT
    - embeds: TEXT
    - mentions: TEXT
    - msg_hash: TEXT
    - msg_hash_hex: TEXT
    - idx_time: TIMESTAMP WITH TIME ZONE

- "comments":
    - id: BIGINT
    - msg_type: TEXT
    - fid: BIGINT
    - msg_timestamp: TIMESTAMP WITH TIME ZONE
    - parent_fid: BIGINT
    - parent_hash: TEXT
    - parent_hash_hex: TEXT
    - text: TEXT
    - lang: TEXT
    - embeds: TEXT
    - msg_hash: TEXT
    - msg_hash_hex: TEXT
    - idx_time: TIMESTAMP WITH TIME ZONE

- "reactions":
    - id: BIGINT
    - msg_type: TEXT
    - fid: BIGINT
    - msg_timestamp: TIMESTAMP WITH TIME ZONE
    - reaction_type: TEXT
    - target_fid: BIGINT
    - target_hash: TEXT
    - target_hash_hex: TEXT
    - msg_hash: TEXT
    - msg_hash_hex: TEXT
    - idx_time: TIMESTAMP WITH TIME ZONE

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
