from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

WHISPER_MODEL_SIZE = "small"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"
LISTEN_SECONDS = 4
SAMPLE_RATE = 16000
CHANNELS = 1

FUZZY_SCORE_CUTOFF = 70
