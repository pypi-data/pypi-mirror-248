from ..utils import *


def create_template_functions(modules: list) -> dict[str, Callable]:
    template_functions = {}
    for module in modules:
        for name, fn in inspect.getmembers(module, inspect.isfunction):
            if name.endswith("_template"):
                template_functions[name] = fn
    return template_functions


def json_to_prompt(
    prompt_file: str | Path, template_functions: Optional[dict[str, Callable]] = None
) -> str:
    prompt_file = str(prompt_file)
    if not os.path.exists(prompt_file):
        return ""
    with open(prompt_file, "r") as f:
        prompt_data = json.load(f)
    # print(f"\n\nPROMPT DATA: {prompt_data}\n\n")
    if template_functions is None or "template_function" not in prompt_data:
        if "template_args" in prompt_data:
            template_args = prompt_data["template_args"]
        else:
            template_args = prompt_data
        if is_dict(template_args) and "titles_dict" not in template_args:
            template_args = {"titles_dict": template_args}
        return titles_w_content_template(**template_args)
    template_function = template_functions[prompt_data["template_function"]]
    # print(f"\n\nTEMPLATE ARGS: {prompt_data['template_args']}\n\n")
    return template_function(**prompt_data["template_args"])


def txt_to_prompt(prompt_file: str | Path) -> str:
    prompt_file = str(prompt_file)
    if not os.path.exists(prompt_file):
        return ""
    with open(prompt_file, "r") as f:
        prompt = f.read()
    return cleandoc(prompt)


def process_prompt(
    prompt: str | Path | list[str], template_functions: Optional[dict[str, Callable]] = None
) -> str:
    if not prompt:
        return ""
    if is_list(prompt):
        prompt = "\n---\n".join(prompt)
    elif path_or_str(prompt):
        prompt = str(prompt)
        if prompt.endswith(".txt"):
            prompt = txt_to_prompt(prompt)
        elif prompt.endswith(".json"):
            prompt = json_to_prompt(prompt, template_functions=template_functions)
    return cleandoc(prompt)


def titles_w_content_template(
    titles_dict: dict[str, str | Path | list[str]] = {}, prefix: str = "", suffix: str = ""
) -> str:
    prompt = cleandoc(prefix)
    for title, content in titles_dict.items():
        if content:
            title = " ".join(title.split("_")).strip().title()
            content = process_prompt(content)
            if content:
                if len(prompt) > 0:
                    prompt += "\n\n"
                prompt += cleandoc(f"## {title} ##\n\n{cleandoc(content)}")
    prompt += "\n\n" + cleandoc(suffix)
    return cleandoc(prompt)


def rag_template(info: str | list[str], prefix: str = "") -> str:
    if not prefix:
        prefix = "Get help from this retrieved information for your response."
    return titles_w_content_template(
        titles_dict={"retrieved information": info},
        prefix=prefix,
    )


def message_template(message: dict[str, str]) -> str:
    assert "role" in message and ("content" in message or "parts" in message)
    role = message["role"]
    content = message["content"] if "content" in message else message["parts"]
    return f"{role.upper()}:\n{content}"


def chat_template(chat: list[dict[str, str]] = []) -> str:
    return "\n\n".join([message_template(message) for message in chat]).strip()


def generic_summary_template(line_count: int = 10) -> str:
    return cleandoc(
        f"""
    As a professional summarizer, create a concise and comprehensive summary of the provided text, be it an article, post, conversation, or passage, while adhering to these guidelines:
    1. Craft a summary that is detailed, thorough, in-depth, and complex, while maintaining clarity and conciseness.
    2. Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.
    3. Keep all the important information in the summary.
    4. Rely strictly on the provided text, without including external information.
    5. Format the summary in paragraph form for easy understanding.
    6. It should be no more than {line_count} lines long.
    """
    )


def repeat_template(num_steps: int = 1) -> str:
    if num_steps == 1:
        return "Repeat the previous step that you did for this new prompt."
    else:
        return f"Repeat the previous {num_steps} steps that you did for this new prompt."
