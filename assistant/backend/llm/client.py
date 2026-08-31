from litellm import acompletion

from llm.models import Message, ModelConfig


class LLMClient:
    def __init__(self, model: ModelConfig):
        self.model = model

    async def complete(self, messages: list[Message]) -> str:
        response = await acompletion(
            model=self.model.name,
            messages=[message.model_dump() for message in messages],
            max_tokens=self.model.max_tokens,
        )

        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("Model returned no text")

        return content
