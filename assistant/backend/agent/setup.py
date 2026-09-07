from agent.homelab import list_containers_tool
from agent.registry import ToolRegistry


def create_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    for tool in [list_containers_tool]:
        registry.register(tool)
    return registry
