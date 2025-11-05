"""
Keyboard Simulator Module
--------------------------
Provides keyboard input simulation using PyAutoGUI.
Handles programmatic key press events for gesture-based keyboard control.
"""

import pyautogui


class KeyboardSimulator:
    @staticmethod
    def press_key(key: str):
        """Simulate a keyboard key press

        Args:
            key (str): Key identifier to press (e.g., 'up', 'down', 'left', 'right')
        """
        pyautogui.press(key)
