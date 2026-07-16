import keyboard

from utils.numbers import clamp_percentage


def volume_up(amount: int = 5) -> None:
    for _ in range(max(1, amount)):
        keyboard.send("volume up")


def volume_down(amount: int = 5) -> None:
    for _ in range(max(1, amount)):
        keyboard.send("volume down")


def mute() -> None:
    keyboard.send("volume mute")


def set_volume(value: int) -> None:
    try:
        from ctypes import POINTER, cast

        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        endpoint_volume = cast(interface, POINTER(IAudioEndpointVolume))
        endpoint_volume.SetMasterVolumeLevelScalar(clamp_percentage(value) / 100, None)
    except Exception:
        mute()
        volume_up(max(1, clamp_percentage(value) // 2))
