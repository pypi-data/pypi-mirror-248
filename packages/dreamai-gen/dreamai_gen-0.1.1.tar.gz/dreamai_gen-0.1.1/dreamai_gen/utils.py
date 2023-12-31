from .imports import *


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


def current_time(format: str = "%m-%d-%Y_%H:%M:%S") -> str:
    return datetime.now().strftime(format)


def sort_times(times, format="%m-%d-%Y_%H:%M:%S"):
    return sorted(times, key=lambda time: datetime.strptime(time, format))


def count_words(text: str) -> int:
    return len(text.split())


def count_lines(text: str) -> int:
    return len(text.split("\n"))


def token_count_to_word_count(token_count) -> int:
    return max(int(token_count * 0.75), 1)


def token_count_to_line_count(token_count) -> int:
    return max(int(token_count * 0.066), 1)


def word_count_to_token_count(word_count) -> int:
    return max(int(word_count / 0.75), 1)


def count_tokens(text: str) -> int:
    return word_count_to_token_count(len(text.split()))
