from dataclasses import dataclass
from typing import Any

from rapidfuzz import fuzz, process

from config import FUZZY_SCORE_CUTOFF
from utils.numbers import extract_number
from utils.parser import normalize_text


@dataclass(frozen=True)
class CommandExample:
    phrase: str
    intent: dict[str, Any]


DEFAULT_EXAMPLES = [
    CommandExample("espaco", {"command": "space"}),
    CommandExample("pausar", {"command": "space"}),
    CommandExample("play", {"command": "space"}),
    CommandExample("enter", {"command": "enter"}),
    CommandExample("confirmar", {"command": "enter"}),
    CommandExample("esc", {"command": "esc"}),
    CommandExample("escape", {"command": "esc"}),
    CommandExample("fechar janela", {"command": "alt_f4"}),
    CommandExample("fecha essa janela", {"command": "alt_f4"}),
    CommandExample("alt f4", {"command": "alt_f4"}),
    CommandExample("copiar", {"command": "ctrl_c"}),
    CommandExample("colar", {"command": "ctrl_v"}),
    CommandExample("proxima musica", {"command": "nexttrack"}),
    CommandExample("voltar musica", {"command": "prevtrack"}),
    CommandExample("pausar musica", {"command": "playpause"}),
    CommandExample("colar", {"command": "ctrl_v"}),
    CommandExample("desfazer", {"command": "ctrl_z"}),
    CommandExample("aumenta", {"command": "volume_up"}),
    CommandExample("aumentar volume", {"command": "volume_up"}),
    CommandExample("abaixa", {"command": "volume_down"}),
    CommandExample("diminuir volume", {"command": "volume_down"}),
    CommandExample("abaixar volume", {"command": "volume_down"}),
    CommandExample("volume em", {"command": "set_volume"}),
    CommandExample("silenciar", {"command": "mute"}),
    CommandExample("mutar", {"command": "mute"}),
    CommandExample("tela cheia", {"command": "fullscreen"}),
    CommandExample("avancar video", {"command": "video_forward"}),
    CommandExample("voltar video", {"command": "video_back"}),
    CommandExample("proximo campo", {"command": "tab"}),
    CommandExample("abrir chrome", {"command": "open_program", "name": "chrome"}),
    CommandExample("abrir discord", {"command": "open_program", "name": "discord"}),
    CommandExample("abrir steam", {"command": "open_program", "name": "steam"}),
    CommandExample("abrir brave", {"command": "open_program", "name": "brave"}),
    CommandExample("desligar computador", {"command": "shutdown"}),
    CommandExample("reiniciar computador", {"command": "restart"})
]


class FuzzyCommandRecognizer:
    def __init__(
        self,
        examples: list[CommandExample] | None = None,
        score_cutoff: int = FUZZY_SCORE_CUTOFF,
    ) -> None:
        self._examples = examples or DEFAULT_EXAMPLES
        self._score_cutoff = score_cutoff
        self._phrases = [normalize_text(example.phrase) for example in self._examples]

    def recognize(self, text: str) -> dict[str, Any] | None:
        normalized = normalize_text(text)
        result = process.extractOne(normalized, self._phrases, scorer=fuzz.WRatio)
        if not result:
            return None

        text_right, score, index = result
        print("Entendi: ", text_right, " com score: ", score)
        if score < self._score_cutoff:
            return None

        intent = dict(self._examples[index].intent)
        return self._enrich_intent(intent, text_right)

    @staticmethod
    def _enrich_intent(intent: dict[str, Any], text: str) -> dict[str, Any]:
        number = extract_number(text)
        command = intent.get("command")

        if command in {"volume_up", "volume_down", "video_forward", "video_back", "tab"}:
            default = 5 if command in {"volume_up", "volume_down"} else 1
            intent["amount"] = number or intent.get("amount", default)
        elif command == "set_volume" and number is not None:
            intent["value"] = number
        elif command == "open_program":
            for program in ("chrome", "brave", "discord", "steam", "notepad"):
                if program in text:
                    intent["name"] = program
                    break

        return intent
