def create_cast_adds_table():
    return """
    CREATE TABLE IF NOT EXISTS cast_adds (
        id TEXT PRIMARY KEY,
        fid BIGINT,
        text TEXT,
        lang TEXT,
        consumer_ts TIMESTAMP
    );
    """


def create_cast_comments_table():
    return """
    CREATE TABLE IF NOT EXISTS cast_comments (
        id TEXT PRIMARY KEY,
        fid BIGINT,
        text TEXT,
        lang TEXT,
        consumer_ts TIMESTAMP
    );
    """


def create_cast_reactions_table():
    return """
    CREATE TABLE IF NOT EXISTS cast_comments (
        id TEXT PRIMARY KEY,
        fid BIGINT,
        text TEXT,
        lang TEXT,
        consumer_ts TIMESTAMP
    );
    """
