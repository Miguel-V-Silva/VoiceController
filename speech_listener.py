import json
import queue
from typing import Callable

import sounddevice as sd
from vosk import KaldiRecognizer, Model


class SpeechListener:
    """Escuta o microfone e converte áudio em texto por meio do VOSK."""

    def __init__(
        self,
        model_path: str = "vosk-model-small-pt-0.3",
        samplerate: int = 16000,
        blocksize: int = 8000,
        channels: int = 1,
    ):
        self._queue: queue.Queue[bytes] = queue.Queue()
        self._samplerate = samplerate
        self._recorder = self._initialize_recognizer(model_path)
        self._stream_args = {
            "samplerate": samplerate,
            "blocksize": blocksize,
            "dtype": "int16",
            "channels": channels,
            "callback": self._audio_callback,
        }

    def _initialize_recognizer(self, model_path: str) -> KaldiRecognizer:
        try:
            model = Model(model_path)
        except Exception as error:
            raise FileNotFoundError(
                f"Modelo VOSK não encontrado em: {model_path}."
                f" Detalhes: {error}"
            )

        return KaldiRecognizer(model, self._samplerate)

    def _audio_callback(self, indata, frames, time, status) -> None:
        if status:
            print(f"Status do fluxo de áudio: {status}")
        self._queue.put(bytes(indata))

    def listen(self, on_text: Callable[[str], bool]) -> None:
        try:
            with sd.RawInputStream(**self._stream_args):
                print("Estou ouvindo...")
                while True:
                    data = self._queue.get()
                    if self._recorder.AcceptWaveform(data):
                        resultado = json.loads(self._recorder.Result())
                        texto = resultado.get("text", "").strip()
                        if texto and not on_text(texto):
                            break
        except KeyboardInterrupt:
            print("Interrupção do teclado recebida. Encerrando.")
        except Exception as error:
            print(f"Erro ao capturar áudio: {error}")
