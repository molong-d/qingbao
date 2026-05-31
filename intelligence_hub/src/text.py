import html
import re


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    text = html.unescape(value).replace("\xa0", " ")
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(text.split())
