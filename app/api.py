from fastapi import FastAPI
from app.rag import query_rag

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Super Smash Bros Melee RAG API is running!"}


@app.get("/query")
def get_answer(question: str):
    """Endpoint to get answers using the RAG system."""
    response = query_rag(question)
    return {"question": question, "answer": response, "test":"chest"}
