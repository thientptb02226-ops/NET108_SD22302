from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Trello Clone AI-RAG Service", version="1.0.0")

class SearchQuery(BaseModel):
    query: str
    top_k: int = 5

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Trello-Clone-AI-RAG"}

@app.post("/api/v1/search")
def semantic_search(payload: SearchQuery):
    # Simulated vector similarity lookup
    return {
        "query": payload.query,
        "results": [
            {
                "card_id": "card-1",
                "title": "Setup Multi-Agent Architecture",
                "score": 0.94,
                "snippet": "Coordinating Claude Code CLI and Antigravity in shared workspace."
            }
        ]
    }

