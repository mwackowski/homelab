from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel


@dataclass(frozen=True)
class ModelConfig:
    name: str
    temperature: float = 0.7
    max_tokens: int = 1_000


@dataclass(frozen=True)
class ModelRegistry:
    fast: ModelConfig
    medium: ModelConfig
    big: ModelConfig


MODELS = ModelRegistry(
    fast=ModelConfig(
        name="gpt-5.6-luna",
        temperature=0.3,
    ),
    medium=ModelConfig(
        name="gpt-5.6-terra",
        temperature=0.5,
    ),
    big=ModelConfig(name="gpt-5.6-sol", temperature=0.7),
)


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str | None = None
    tool_calls: list[dict[str, Any]] | None = None
    tool_call_id: str | None = None
