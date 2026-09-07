from collections.abc import Awaitable, Callable

from pydantic import BaseModel


class ToolResult(BaseModel):
      success: bool
      output: str = ""
      error: str | None = None

class Tool(BaseModel):
    name: str
    description: str
    executable: Callable[[], Awaitable[ToolResult]]
