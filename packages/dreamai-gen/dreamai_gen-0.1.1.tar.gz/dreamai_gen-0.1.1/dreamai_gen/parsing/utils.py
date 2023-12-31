from .imports import *


def clean_text(text: str) -> str:
    try:
        text = clean_extra_whitespace(text)
    except:
        pass
    try:
        text = bytes_string_to_string(text)
    except:
        pass
    try:
        text = clean_non_ascii_chars(text)
    except:
        pass
    try:
        text = replace_unicode_quotes(text)
    except:
        pass
    try:
        text = replace_mime_encodings(text)
    except:
        pass
    try:
        text = group_bullet_paragraph(text)
        text = "\n".join(text)
    except:
        pass
    try:
        text = group_broken_paragraphs(text)
    except:
        pass
    text = re.sub(r"[\t+]", " ", text)
    text = re.sub(r"[. .]", " ", text)
    return text
