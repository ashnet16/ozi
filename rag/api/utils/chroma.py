from chromadb import HttpClient
from chromadb.config import Settings
import os

def get_chroma_client():
    host = os.getenv("VECTOR_DB_HOST", "http://vector-db")
    port = os.getenv("VECTOR_DB_PORT", "8000")

    return HttpClient(
        host=f"{host}:{port}",
        settings=Settings(chroma_api_impl="rest")
    )

