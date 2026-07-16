from typing import Any

from ai.fuzzy import FuzzyCommandRecognizer
from commands.executor import CommandExecutionError, CommandExecutor
from utils.numbers import extract_number
from utils.parser import normalize_text
from voice.listener import VoiceListener


class VoiceController:
    def __init__(self) -> None:
        self._executor = CommandExecutor()
        self._fuzzy = FuzzyCommandRecognizer()
        self._active = True

    def handle_text(self, text: str) -> bool:
        normalized = normalize_text(text)
        if normalized in {"parar", "para", "encerrar", "sair"}:
            return False
        if normalized in {"desativar", "desativa"}:
            self._active = False
            print("Comandos desativados. Diga 'ativar' para reativar.")
            return True
        if normalized in {"ativar", "ativa"}:
            self._active = True
            print("Comandos ativados.")
            return True
        if not self._active:
            print(f"Ignorado enquanto desativado: {text}")
            return True

        intent = self._fuzzy.recognize(text)
        source = "RapidFuzz"
        if intent is None:
            intent = self._fallback_intent(text)
            source = "Fallback"

        if intent is None:
            print(f"Comando não reconhecido: {text}")
            return True

        try:
            self._executor.execute_intent(intent)
            print(f"{source}: {intent}")
        except CommandExecutionError as error:
            print(f"Erro de comando: {error}")
        return True

    @staticmethod
    def _fallback_intent(text: str) -> dict[str, Any] | None:
        normalized = normalize_text(text)
        amount = extract_number(normalized) or 1

        if "abrir" in normalized:
            if "chrome" in normalized or "navegador" in normalized:
                return {"command": "open_program", "name": "chrome"}
            if "brave" in normalized:
                return {"command": "open_program", "name": "brave"}
            if "discord" in normalized:
                return {"command": "open_program", "name": "discord"}
            if "steam" in normalized:
                return {"command": "open_program", "name": "steam"}
            if "notepad" in normalized or "bloco de notas" in normalized:
                return {"command": "open_program", "name": "notepad"}

        if any(keyword in normalized for keyword in ("fechar", "fecha", "feche")):
            if "chrome" in normalized:
                return {"command": "close_program", "name": "chrome"}
            if "discord" in normalized:
                return {"command": "close_program", "name": "discord"}
            if "steam" in normalized:
                return {"command": "close_program", "name": "steam"}
            if "notepad" in normalized or "bloco de notas" in normalized:
                return {"command": "close_program", "name": "notepad"}
            return {"command": "alt_f4"}

        if "silenciar" in normalized or "mutar" in normalized:
            return {"command": "mute"}
        if any(keyword in normalized for keyword in ("aumentar volume", "aumenta volume", "aumentar", "aumenta")):
            return {"command": "volume_up", "amount": amount}
        if any(keyword in normalized for keyword in ("diminuir volume", "abaixar volume", "diminuir", "abaixa", "baixar")):
            return {"command": "volume_down", "amount": amount}
        if "volume em" in normalized or ("volume" in normalized and "em" in normalized):
            return {"command": "set_volume", "value": amount}
        if any(keyword in normalized for keyword in ("pausar", "play", "pausa")):
            return {"command": "space"}
        if any(keyword in normalized for keyword in ("enter", "confirmar", "confirma")):
            return {"command": "enter"}
        if any(keyword in normalized for keyword in ("esc", "escape")):
            return {"command": "esc"}
        if "tab" in normalized or "próximo" in normalized or "proxima" in normalized:
            return {"command": "tab", "amount": amount}
        if "alt f4" in normalized or "alt+f4" in normalized:
            return {"command": "alt_f4"}
        if "copiar" in normalized:
            return {"command": "ctrl_c"}
        if "colar" in normalized:
            return {"command": "ctrl_v"}
        if "desfazer" in normalized or "ctrl z" in normalized:
            return {"command": "ctrl_z"}
        if "tela cheia" in normalized:
            return {"command": "fullscreen"}
        if "avançar" in normalized or "avancar" in normalized or "avança" in normalized:
            return {"command": "video_forward", "amount": amount}
        if "voltar" in normalized or "retroceder" in normalized:
            return {"command": "video_back", "amount": amount}
        if "desligar" in normalized:
            return {"command": "shutdown"}
        if "reiniciar" in normalized:
            return {"command": "restart"}

        return None


def main() -> None:
    controller = VoiceController()
    listener = VoiceListener()
    listener.listen(controller.handle_text)
    print("Encerrando o programa...")


if __name__ == "__main__":
    main()
