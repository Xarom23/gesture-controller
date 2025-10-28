import pyautogui

class KeyboardSimulator:    
    @staticmethod
    def press_key(key: str):
        pyautogui.press(key)
