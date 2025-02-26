import uvicorn
from app.create_db import setup_chroma
from app.api import app

if __name__ == "__main__":
    print("🚀 Starting up...")

    # Step 1: Initialize ChromaDB
    setup_chroma()

    # Step 2: Start FastAPI Server
    uvicorn.run(app, host="0.0.0.0", port=8000)
