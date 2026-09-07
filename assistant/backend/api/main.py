import logging
from uuid import uuid4

from agent.loop import run_agent
from agent.setup import create_tool_registry
from fastapi import FastAPI, HTTPException
from llm.client import LLMClient
from llm.models import MODELS
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
    registry = create_tool_registry()
    try:
        message = await run_agent(llm_client, request.message, registry)
        reply = message.content or ""
    except Exception:
        logger.exception("[%s] Model request failed", request_id)
        raise HTTPException(
            status_code=502,
            detail="Model request failed",
        )

    return ChatResponse(reply=reply)
