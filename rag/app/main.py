from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Ozi RAG is up and running!"}