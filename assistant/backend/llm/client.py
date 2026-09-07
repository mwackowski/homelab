from litellm import acompletion

from llm.models import Message, ModelConfig


class LLMClient:
    def __init__(self, model: ModelConfig):
        self.model = model

    async def complete(self, messages: list[Message], definitions: list[dict]):
        response = await acompletion(
            model=self.model.name,
            messages=[message.model_dump(exclude_none=True) for message in messages],
            tools=[
                {
                    "type": "function",
                    "function": definition,
                }
                for definition in definitions
            ],
            max_tokens=self.model.max_tokens,
        )

        content = response.choices[0].message
        return content
