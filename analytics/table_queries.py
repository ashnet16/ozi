def create_casts_table():
    return """
    CREATE TABLE IF NOT EXISTS casts (
        id BIGINT PRIMARY KEY,
        msg_type TEXT,
        fid BIGINT,
        msg_timestamp TIMESTAMP,
        text TEXT,
        lang TEXT,
        embeds TEXT,
        mentions TEXT,
        msg_hash TEXT
    );
    """

def create_comments_table():
    return """
    CREATE TABLE IF NOT EXISTS comments (
        id BIGINT PRIMARY KEY,
        msg_type TEXT,
        fid BIGINT,
        msg_timestamp TIMESTAMP,
        parent_fid BIGINT,
        parent_hash TEXT,
        text TEXT,
        lang TEXT,
        embeds TEXT,
        msg_hash TEXT
    );
    """


def create_reactions_table():
    return """
    CREATE TABLE IF NOT EXISTS reactions (
        id BIGINT PRIMARY KEY,
        msg_type TEXT,
        fid BIGINT,
        msg_timestamp TIMESTAMP,
        reaction_type TEXT,
        target_fid BIGINT,
        target_hash TEXT,
        msg_hash TEXT
    );
    """
