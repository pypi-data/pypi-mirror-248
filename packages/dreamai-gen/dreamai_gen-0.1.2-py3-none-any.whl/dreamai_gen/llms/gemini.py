from ..utils import *
import google.generativeai as google_ai


def is_gemini_message(message: dict[str, str]) -> bool:
    return "role" in message and "parts" in message and "content" not in message


def to_gemini_message(message: dict[str, str]) -> dict[str, str]:
    assert "role" in message and ("content" in message or "parts" in message)
    role = message["role"]
    if role == "assistant":
        role = "model"
    elif role == "system":
        role = "user"
    parts = message["content"] if "content" in message else message["parts"]
    return {"role": role, "parts": parts}


def process_gemini_messages(messages: list[dict[str, str]] | dict[str, str]) -> list:
    messages = copy.deepcopy(messages)
    if len(messages) == 0:
        return messages
    if is_dict(messages):
        messages = [messages]
    new_messages = []
    last_user_message = None
    for message in messages:
        message = to_gemini_message(message)
        if message["role"] == "user":
            if last_user_message is None:
                last_user_message = message
            else:
                last_user_message["parts"] += "\n\n" + message["parts"]
        else:
            if last_user_message is not None:
                new_messages.append(last_user_message)
                last_user_message = None
            new_messages.append(message)
    if last_user_message is not None:
        new_messages.append(last_user_message)
    return new_messages


def ask_gemini(
    messages: list[dict[str, str]], model: str | google_ai.GenerativeModel = "gemini-pro"
) -> list[dict[str, str]]:
    if is_str(model):
        model = google_ai.GenerativeModel(model)
    gemini_messages = process_gemini_messages(messages)
    answer = model.generate_content(gemini_messages).text
    messages.append({"role": "assistant", "content": answer})
    return messages
