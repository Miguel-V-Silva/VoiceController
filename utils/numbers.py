import re

from utils.parser import normalize_text


NUMBER_WORDS = {
    "zero": 0,
    "um": 1,
    "uma": 1,
    "dois": 2,
    "duas": 2,
    "tres": 3,
    "quatro": 4,
    "cinco": 5,
    "seis": 6,
    "sete": 7,
    "oito": 8,
    "nove": 9,
    "dez": 10,
    "onze": 11,
    "doze": 12,
    "treze": 13,
    "quatorze": 14,
    "catorze": 14,
    "quinze": 15,
    "dezesseis": 16,
    "dezessete": 17,
    "dezoito": 18,
    "dezenove": 19,
    "vinte": 20,
    "trinta": 30,
    "quarenta": 40,
    "cinquenta": 50,
    "sessenta": 60,
    "setenta": 70,
    "oitenta": 80,
    "noventa": 90,
    "cem": 100,
    "cento": 100,
}

NUMBER_PATTERN = re.compile(
    r"\b([0-9]{1,3}|" + "|".join(re.escape(key) for key in NUMBER_WORDS) + r")\b"
)


def extract_number(text: str, default: int | None = None) -> int | None:
    normalized = normalize_text(text)
    match = NUMBER_PATTERN.search(normalized)
    if not match:
        return default

    token = match.group(1)
    if token.isdigit():
        return int(token)
    return NUMBER_WORDS[token]


def clamp_percentage(value: int) -> int:
    return max(0, min(100, value))
