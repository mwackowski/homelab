import logging
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from llm.client import LLMClient
from llm.models import MODELS, Message
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("assistant-api")
app = FastAPI()
llm_client = LLMClient(model=MODELS.fast)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    request_id = uuid4().hex
    try:
        reply = await llm_client.complete(
            [
                Message(role="system", content="you are a helpful assistant"),
                Message(role="user", content=request.message),
            ]
        )
    except Exception:
        logger.exception("[%s] Model request failed", request_id)
        raise HTTPException(
            status_code=502,
            detail="Model request failed",
        )

    return ChatResponse(reply=reply)
