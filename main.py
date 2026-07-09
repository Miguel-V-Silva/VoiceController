from voice_commands import VoiceCommandProcessor
from speech_listener import SpeechListener


def main() -> None:
    processor = VoiceCommandProcessor()
    listener = SpeechListener()
    listener.listen(processor.execute)
    print("Encerrando o programa...")


if __name__ == "__main__":
    main()
