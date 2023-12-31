from ..utils import *
import tiktoken
from openai import OpenAI


def count_gpt_tokens(text: str, model: str = "gpt-4-1106-preview") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def is_gpt_message(message: dict[str, str]) -> bool:
    return "role" in message and "content" in message and "parts" not in message


def to_gpt_message(message: dict[str, str]) -> dict[str, str]:
    assert "role" in message and ("content" in message or "parts" in message)
    role = message["role"]
    if role == "model":
        role = "assistant"
    content = message["content"] if "content" in message else message["parts"]
    return {"role": role, "content": content}


def process_gpt_messages(messages: list[dict[str, str]] | dict[str, str]) -> list:
    messages = copy.deepcopy(messages)
    if len(messages) == 0:
        return messages
    if is_dict(messages):
        messages = [messages]
    if is_gpt_message(messages[0]) and is_gpt_message(messages[-1]):
        return messages
    return [to_gpt_message(message) for message in messages]


def ask_gpt(
    messages: list[dict[str, str]],
    model: str = "gpt-4-1106-preview",
    json_mode: Optional[bool] = None,
) -> list[dict[str, str]]:
    gpt = OpenAI()
    gpt_messages = process_gpt_messages(messages)
    if json_mode is None:
        json_mode = "json" in gpt_messages[-1]["content"].lower()
    response_format = {"type": "json_object" if json_mode else "text"}
    answer = (
        gpt.chat.completions.create(
            messages=gpt_messages, model=model, response_format=response_format
        )
        .choices[0]
        .message.content
    )
    messages.append({"role": "assistant", "content": answer})
    return messages
