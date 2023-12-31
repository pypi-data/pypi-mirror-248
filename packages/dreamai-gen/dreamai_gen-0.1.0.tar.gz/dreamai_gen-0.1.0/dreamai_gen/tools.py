from .prompting.prompts import *
from .rag.chroma import *


def get_param_names(func):
    return inspect.signature(func).parameters.keys()


def call_tool(
    tool: Callable, messages: list[dict[str, str]], asker: Callable, **kwargs
) -> list[dict[str, str]]:
    params = {"messages": messages, "asker": asker, **kwargs}
    tool_params = get_param_names(tool)
    if "messages" in tool_params:
        if "kwargs" in tool_params:
            return tool(**params)
        elif "asker" in tool_params:
            return tool(messages=messages, asker=asker)
        else:
            return tool(messages=messages)
    elif "kwargs" in tool_params:
        tool(**params)
    else:
        params = {k: v for k, v in params.items() if k in tool_params}
        tool(**params)
    return messages


def chroma_retriever(
    messages: list[dict[str, str]],
    collection: chromadb.Collection,
    **kwargs,
) -> list[dict[str, str]]:
    messages = copy.deepcopy(messages)
    if len(messages) == 0:
        return messages
    if collection.metadata is None or "retrieved_ids" not in collection.metadata:
        collection.modify(metadata={"retrieved_ids": ""})
    retrieved_ids = collection.metadata["retrieved_ids"]
    if retrieved_ids:
        retrieved_ids = retrieved_ids.split(",")
    else:
        retrieved_ids = []
    query_texts = [messages[-1]["content"]]
    query_res = collection.query(query_texts=query_texts)
    retrieval_res = {k: v[0] for k, v in query_res.items() if v}
    if "documents" in retrieval_res and "ids" in retrieval_res:
        info_data = {
            k: [v[i] for i, id in enumerate(retrieval_res["ids"]) if id not in retrieved_ids]
            for k, v in retrieval_res.items()
        }
        if len(info_data["documents"]) > 0:
            messages.append(
                {"role": "user", "content": rag_template(info=info_data["documents"])}
            )
    retrieved_ids += info_data["ids"]
    collection.modify(metadata={"retrieved_ids": ",".join(retrieved_ids)})
    return messages


def summarize_messages(
    messages: list[dict[str, str]],
    asker: Callable,
    max_tokens: int = 25_000,
    **kwargs,
) -> list[dict[str, str]]:
    messages = copy.deepcopy(messages)
    if len(messages) == 0:
        return messages
    chat_token_count = count_tokens(chat_template(messages))
    if chat_token_count <= max_tokens:
        return messages
    line_count = token_count_to_line_count(max_tokens)
    system_message = None
    user_message = None
    if messages[0]["role"] == "system":
        system_message = messages.pop(0)
    if len(messages) > 1 and messages[-1]["role"] == "user":
        other_messages = messages[:-1]
        user_message = messages[-1]
        other_messages_token_count = count_tokens(chat_template(other_messages))
        user_message_token_count = count_tokens(user_message["content"])
        if user_message_token_count < other_messages_token_count:
            user_message = messages.pop(-1)
        else:
            user_message = None

    if len(messages) == 0:
        return [message for message in [system_message, user_message] if message]

    chat_str = chat_template(messages)
    summary_prompt = titles_w_content_template(
        titles_dict={"conversation": chat_str},
        suffix=generic_summary_template(line_count=line_count),
    )
    messages = [
        {"role": "user", "content": summary_prompt},
    ]
    print(f"\n\nSUMMARY PROMPT: {summary_prompt}\n\n")
    messages = asker(messages=messages)
    chat_summary = messages[-1]["content"]
    messages = [
        {
            "role": "user",
            "content": titles_w_content_template(titles_dict={"chat_summary": chat_summary}),
        },
    ]
    if system_message:
        messages.insert(0, system_message)
    if user_message:
        messages.append(user_message)
    return messages
