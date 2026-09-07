import json
import logging

from agent.registry import ToolRegistry
from llm.client import LLMClient
from llm.models import Message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("assistant-api")


ENTRY_PROMPT = (
    "You are a homelab assistant. "
    "Use the available tools to answer questions about the current "
    "state of the homelab. "
    "Do not invent inspection results. "
    "If a tool fails, explain the failure."
)


async def run_agent(
    llm_client: LLMClient,
    user_message: str,
    registry: ToolRegistry,
    max_steps: int = 5,
):

    tool_definitions = registry.definitions()
    messages = [
            Message(role="system", content=ENTRY_PROMPT),
            Message(role="user", content=user_message),
        ]

    for step in range(max_steps):
        logger.info("Agent step %d: requesting model response", step + 1)
        message = await llm_client.complete(
            messages=messages, definitions=tool_definitions
        )
        if not message.tool_calls:
            logger.info("Agent finished at step %d", step + 1)
            return message

        # Update the context
        messages.append(
            Message(
                role="assistant",
                content=message.content,
                tool_calls=[
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        },
                    }
                    for call in message.tool_calls
                ],
            )
        )

        # Execute tools and update context again

        for call in message.tool_calls:
            arguments = json.loads(call.function.arguments)
            if arguments != {}:
                raise ValueError("Arguments not implemented yet")
            logger.info("Executing tool: %s", call.function.name)
            result = await registry.execute(call.function.name)
            logger.info("Tool %s returned:\n%s", call.function.name, result)
            messages.append(
                Message(
                    role="tool",
                    content=result.model_dump_json(),
                    tool_call_id=call.id,
                )
            )

    raise RuntimeError("Agent reached its model request limit")
