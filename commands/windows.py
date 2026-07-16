import os
import subprocess

import pyautogui


PROGRAM_ALIASES = {
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "discord": r"C:\Program Files\Discord\Discord.exe",
    "steam": r"C:\Program Files (x86)\Steam\steam.exe",
    "notepad": r"C:\Windows\System32\notepad.exe",
    "bloco de notas": r"C:\Windows\System32\notepad.exe",
}


def open_program(name: str) -> None:
    program = PROGRAM_ALIASES.get(name.lower().strip(), name)
    subprocess.Popen(program, shell=True)


def close_program(name: str) -> None:
    process_name = name if name.lower().endswith(".exe") else f"{name}.exe"
    subprocess.run(["taskkill", "/IM", process_name, "/F"], check=False)


def alt_f4() -> None:
    pyautogui.hotkey("alt", "f4")


def shutdown() -> None:
    os.system("shutdown /s /t 1")


def restart() -> None:
    os.system("shutdown /r /t 1")
