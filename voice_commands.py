import os
import re

import keyboard
import pyautogui

NUMBERS = {
    "zero": 0,
    "um": 1,
    "dois": 2,
    "três": 3,
    "tres": 3,
    "quatro": 4,
    "cinco": 5,
    "seis": 6,
    "sete": 7,
    "oito": 8,
    "nove": 9,
    "dez": 10,
}
NUMBER_PATTERN = re.compile(r"\b([0-9]+|" + "|".join(re.escape(key) for key in NUMBERS) + r")\b", re.IGNORECASE)


def parse_quantity(text: str, default: int = 1) -> int:
    """Busca um número por extenso ou dígito em uma frase de comando."""
    for match in NUMBER_PATTERN.findall(text):
        if match.isdigit():
            return int(match)

        normalized = match.lower()
        if normalized in NUMBERS:
            return NUMBERS[normalized]

    return default


def adjust_volume(delta: int) -> None:
    """Ajusta o volume usando teclas de atalho do sistema."""
    action = "volume up" if delta > 0 else "volume down"
    for _ in range(abs(delta)):
        keyboard.send(action)


class VoiceCommandProcessor:
    """Interpreta texto reconhecido e executa comandos de sistema."""

    def execute(self, texto: str) -> bool:
        texto = texto.lower().strip()
        if not texto:
            return True

        print(f"Comando reconhecido: {texto}")

        if "abrir navegador" in texto:
            self._open_browser()

        if any(keyword in texto for keyword in ["pausar", "play", "pausa"]):
            self._play_pause()

        if "avançar" in texto:
            self._press_key("right")

        if "voltar" in texto:
            self._press_key("left")

        if any(keyword in texto for keyword in ["aumentar", "aumenta"]):
            quantidade = parse_quantity(texto)
            adjust_volume(quantidade)

        if any(keyword in texto for keyword in ["diminuir", "baixa", "baixar", "abaixar"]):
            quantidade = parse_quantity(texto)
            adjust_volume(-quantidade)

        if "mutar" in texto:
            self._press_key("volumemute")

        if self._should_stop(texto):
            return False

        if any(keyword in texto for keyword in ["fechar", "fecha"]):
            keyboard.send("alt+f4")

        if "desligar" in texto:
            os.system("shutdown /s /t 1")

        return True

    @staticmethod
    def _open_browser() -> None:
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.write("chrome")
            pyautogui.press("enter")
        except Exception as error:
            print(f"Erro ao abrir o navegador: {error}")

    @staticmethod
    def _play_pause() -> None:
        pyautogui.press("space")

    @staticmethod
    def _press_key(key: str) -> None:
        pyautogui.press(key)

    @staticmethod
    def _should_stop(texto: str) -> bool:
        stop_pattern = re.compile(r"\b(parar|para)\b", re.IGNORECASE)
        return bool(stop_pattern.search(texto))
