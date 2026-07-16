from collections.abc import Callable

from config import LISTEN_SECONDS
from voice.whisper import WhisperTranscriber


class VoiceListener:
    def __init__(self, transcriber: WhisperTranscriber | None = None, listen_seconds: int = LISTEN_SECONDS) -> None:
        self._transcriber = transcriber or WhisperTranscriber()
        self._listen_seconds = listen_seconds

    def listen(self, on_text: Callable[[str], bool]) -> None:
        print("Estou ouvindo...")
        try:
            while True:
                text = self._transcriber.listen_once(self._listen_seconds).strip()
                if text:
                    print(f"Ouvi: {text}")
                    if not on_text(text):
                        break
        except KeyboardInterrupt:
            print("Interrupcao do teclado recebida. Encerrando.")
