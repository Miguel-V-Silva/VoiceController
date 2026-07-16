import json
import re
import unicodedata
from typing import Any


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return re.sub(r"\s+", " ", text)


def parse_json_object(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("A resposta nao contem um objeto JSON.")

    value = json.loads(text[start : end + 1])
    if not isinstance(value, dict):
        raise ValueError("A resposta JSON precisa ser um objeto.")
    return value
