import os
from platform import processor
import re
import time
import keyboard
import pyautogui

from speech_listener import SpeechListener

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


def tab(delta: int) -> None:
    """Simula a tecla Tab para navegação entre elementos da interface."""
    if delta > 0:
        for _ in range(abs(delta)):
            pyautogui.press("tab")

def adjust_volume(delta: int) -> None:
    """Ajusta o volume usando teclas de atalho do sistema."""
    action = "volume up" if delta > 0 else "volume down"
    for _ in range(abs(delta)):
        keyboard.send(action)

def search(texto: str) -> bool:
    """Realiza uma pesquisa no Google com o texto fornecido."""
    
    if texto is not None:
        pyautogui.write(texto)
        return False
    return True

class VoiceCommandProcessor:
    """Interpreta texto reconhecido e executa comandos de sistema."""

    desativar = False

    def activate(self) -> None:
        """Ativa o processamento de comandos."""
        self.desativar = False
        print("Comandos ativados.")
    
    def deactivate(self) -> None:
        """Desativa o processamento de comandos."""
        self.desativar = True
        print("Comandos desativados.")

    def execute(self, texto: str) -> bool:
        """Executa o comando correspondente ao texto reconhecido."""
        texto = texto.lower().strip()
        if not texto:
            return True
        
        if "ativar" == texto or "ativa" == texto:
            self.activate()
            
        if self.desativar:
            print("Comandos desativados. Diga 'ativar' para reativar: ", texto)
            return True

        if "abrir" in texto:
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

        if "multa" in texto:
            self._press_key("volumemute")

        if self._should_stop(texto):
            return False

        if any(keyword in texto for keyword in ["fechar", "fecha"]):
            keyboard.send("alt+f4")

        if "desligar" in texto:
            os.system("shutdown /s /t 1")

        if "desativar" in texto:
            self.deactivate()
            
        if "youtube" in texto:
            pyautogui.write("https://www.youtube.com")
            pyautogui.press("enter")
        
        if "copa" in texto:
            pyautogui.write("https://www.youtube.com/live/Mh9xGj3XOPM?si=rzX9YzYC3JMCnPmv")
            pyautogui.press("enter")
        
        if "próximo" in texto or "próxima" in texto:
            tab(parse_quantity(texto))
            
        if "confirmar" in texto or "confirma" in texto:
            pyautogui.press("enter")
            
        if "pesquisar" in texto or "pesquisa" in texto:
            listener = SpeechListener()
            listener.listen(search)
       
        
        if "aumentar" in texto or "aumenta" in texto or "tela cheia" in texto:
            self._press_key("f")

        print("Comando executado:", texto)
        return True

    @staticmethod
    def _open_browser() -> None:
        try:
            pyautogui.hotkey("win", "r")
            pyautogui.write("brave")
            pyautogui.press("enter")
            time.sleep(0.6)
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
