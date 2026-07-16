import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

from config import CHANNELS, SAMPLE_RATE, WHISPER_COMPUTE_TYPE, WHISPER_DEVICE, WHISPER_MODEL_SIZE


class WhisperTranscriber:
    """Records short microphone windows and transcribes them with faster-whisper."""

    def __init__(
        self,
        model_size: str = WHISPER_MODEL_SIZE,
        device: str = WHISPER_DEVICE,
        compute_type: str = WHISPER_COMPUTE_TYPE,
    ) -> None:
        self._model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def record(self, seconds: int, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
        audio = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=CHANNELS, dtype="float32")
        sd.wait()
        return audio.reshape(-1)

    def transcribe_audio(self, audio: np.ndarray) -> str:
        segments, _ = self._model.transcribe(audio, language="pt", beam_size=3)
        return " ".join(segment.text.strip() for segment in segments).strip()

    def listen_once(self, seconds: int) -> str:
        audio = self.record(seconds)
        return self.transcribe_audio(audio)
