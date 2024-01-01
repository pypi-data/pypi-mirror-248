"""Utility functions for mirascope chat."""
from openai.types.chat import ChatCompletionMessageParam

from ..prompts import Prompt


def get_messages(
    prompt: Prompt,
) -> list[ChatCompletionMessageParam]:
    """Returns a list of messages parsed from the prompt."""
    if hasattr(prompt, "messages"):
        return [{"role": role, "content": content} for role, content in prompt.messages]
    return [{"role": "user", "content": str(prompt)}]
