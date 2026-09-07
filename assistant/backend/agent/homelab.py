import asyncio

from agent.homelab_utils import ssh
from agent.models import Tool, ToolResult


async def list_containers() -> ToolResult:
    return await asyncio.to_thread(ssh)


list_containers_tool = Tool(
    name="list_containers",
    description="List running and stopped Docker containers on the edge host.",
    executable=list_containers,
)
