import keyboard
import pyautogui


COMMON_KEYS = {
    "space": "space",
    "enter": "enter",
    "esc": "esc",
    "escape": "esc",
    "tab": "tab",
    "backspace": "backspace",
    "delete": "delete",
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
    "f": "f",
    "f11": "f11",
    "prevtrack": "prevtrack",
    "nexttrack": "nexttrack",
    "playpause": "playpause"
}


def press_key(key: str, times: int = 1) -> None:
    mapped_key = COMMON_KEYS.get(key, key)
    for _ in range(max(1, times)):
        pyautogui.press(mapped_key)


def hotkey(*keys: str) -> None:
    pyautogui.hotkey(*keys)


def send_keyboard_shortcut(shortcut: str) -> None:
    keyboard.send(shortcut)
