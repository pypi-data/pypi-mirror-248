from .tools import *
from .prompting import prompts, edu_prompts

TEMPLATE_FUNCTIONS = create_template_functions([prompts, edu_prompts])


def messages_to_chat(
    messages: list[dict[str, str]], chat_name: Optional[str] = ""
) -> dict[str, list[dict[str, str]]]:
    if not chat_name:
        chat_name = current_time()
    return {chat_name: messages}


def save_chats(chats: dict[str, list[dict[str, str]]], chats_dir: str | Path = "chats"):
    os.makedirs(chats_dir, exist_ok=True)
    for chat_name, messages in chats.items():
        with open(f"{chats_dir}/{chat_name}.json", "w") as f:
            json.dump(messages, f, indent=4)


def load_chats(chats_dir: str | Path = "chats") -> dict[str, list[dict[str, str]]]:
    os.makedirs(chats_dir, exist_ok=True)
    chats = {}
    for file in Path(chats_dir).glob("*.json"):
        chat_name = Path(file).stem
        messages = json.load(file)
        chats[chat_name] = messages
    try:
        chats = OrderedDict(
            {chat_name: chats[chat_name] for chat_name in sort_times(chats.keys())}
        )
    except:
        pass
    return chats


def run_task(
    task,
    asker: Callable,
    messages: list[dict[str, str]] = [],
    template_functions: Optional[dict[str, Callable]] = None,
) -> list[dict[str, str]]:
    messages = copy.deepcopy(messages)
    if not list_or_tuple(task):
        task = [task]
    for subtask in task:
        if callable(subtask):
            messages = call_tool(
                tool=subtask,
                messages=messages,
                asker=asker,
            )
        elif path_or_str(subtask) or is_list(subtask):
            task_content = process_prompt(subtask, template_functions=template_functions)
            messages = add_messages(messages, roles="user", contents=task_content)
        else:
            raise TypeError(f"Invalid task type: {type(subtask)}")
    return messages


def ask_(
    messages: list[dict[str, str]],
    asker: Callable,
    pre_tools: list[Callable] = [summarize_messages],
    post_tools: list[Callable] = [],
) -> list[dict[str, str]]:
    messages = copy.deepcopy(messages)
    if len(messages) == 0:
        return messages
    for tool in pre_tools:
        messages = call_tool(tool, messages=messages, asker=asker)
    messages = asker(messages=messages)
    for tool in post_tools:
        messages = call_tool(tool, messages=messages, asker=asker)
    return messages


def ask(
    *tasks,
    asker: Callable,
    messages: list[dict[str, str]] = [],
    pre_tools: list[Callable] | Callable = [summarize_messages],
    post_tools: list[Callable] | Callable = [],
    template_functions: Optional[dict[str, Callable]] = TEMPLATE_FUNCTIONS,
) -> tuple[list[dict[str, str]], dict[str, str]]:
    messages = copy.deepcopy(messages)
    tasks = list(tasks)
    if not list_or_tuple(pre_tools):
        pre_tools = [pre_tools]
    if not list_or_tuple(post_tools):
        post_tools = [post_tools]
    if len(messages) > 0 and messages[-1]["role"] in ["system", "user"]:
        tasks.insert(0, messages.pop(-1)["content"])
    gens = {}
    for task in tasks:
        curr_messages = copy.deepcopy(messages)
        gen_key = None
        if is_dict(task):
            gen_key = dict_keys(task)[0]
            task = task[gen_key]
        messages = run_task(
            task=task, asker=asker, messages=messages, template_functions=template_functions
        )
        if curr_messages != messages:
            messages = ask_(
                messages=messages,
                asker=asker,
                pre_tools=pre_tools,
                post_tools=post_tools,
            )
            if gen_key:
                gens[gen_key] = {
                    "index": len(messages) - 1,
                    "content": messages[-1]["content"],
                }
    return {"messages": messages, "gens": gens}
