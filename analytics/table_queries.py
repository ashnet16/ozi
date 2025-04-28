def create_casts_table():
    return """
    CREATE TABLE IF NOT EXISTS casts (
        id BIGINT PRIMARY KEY,
        msg_type TEXT,
        fid BIGINT,
        msg_timestamp TIMESTAMP,
        network TEXT,
        parent_fid BIGINT,
        parent_hash TEXT,
        text TEXT,
        lang TEXT,
        embeds TEXT,
        hash TEXT,
        signature TEXT,
        signer TEXT
    );
    """

def create_comments_table():
    return """
    CREATE TABLE IF NOT EXISTS comments (
        id BIGINT PRIMARY KEY,
        msg_type TEXT,
        fid BIGINT,
        msg_timestamp TIMESTAMP,
        network TEXT,
        parent_fid BIGINT,
        parent_hash TEXT,
        text TEXT,
        lang TEXT,
        embeds TEXT,
        hash TEXT,
        signature TEXT,
        signer TEXT
    );
    """


def create_reactions_table():
    return """
    CREATE TABLE IF NOT EXISTS reactions (
        id BIGINT PRIMARY KEY,
        msg_type TEXT,
        fid BIGINT,
        msg_timestamp TIMESTAMP,
        network TEXT,
        reaction_type TEXT,
        target_fid BIGINT,
        target_hash TEXT,
        hash TEXT,
        signature TEXT,
        signer TEXT
    );
    """
