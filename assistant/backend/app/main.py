import logging
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("assistant-api")

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    request_id = uuid4().hex
    reply = "How can I help?"

    logger.info("[%s] [USER_INPUT] %s", request_id, request.message)
    logger.info("[%s] [ASSISTANT_OUTPUT] %s", request_id, reply)

    return ChatResponse(reply=reply)
