import pyautogui
import time
for i in range(2):
    pyautogui.press('playpause')   
    time.sleep(1)  # Pequena pausa entre as iterações
print("Hotkey pressed: fn + f7")