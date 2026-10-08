from fastapi import FastAPI
from app.schemas import ChatRequest, ChatResponse
from app.agent import run_agent

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = run_agent(request.message)
    return ChatResponse(reply=reply)