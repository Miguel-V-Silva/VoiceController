import pyautogui


def click(button: str = "left") -> None:
    pyautogui.click(button=button)
