import re

def clean_text(text: str) -> str:
    text = text.strip().replace('"', '').replace("'", "")
    return re.sub(r"[\ud800-\udfff]", "", text)
