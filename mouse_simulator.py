"""
Mouse Simulator Module
-----------------------
Provides mouse control simulation using PyAutoGUI.
Handles cursor movement and mouse click events for gesture-based mouse control.

Key features:
- Cursor position control with normalized coordinates
- Left and right click simulation
- Movement smoothing support
"""

import pyautogui


class MouseSimulator:
    def __init__(self, smoothing_factor=0.5, position_history_size=5):
        """Initialize the mouse simulator

        Args:
            smoothing_factor (float): Factor for movement smoothing (0-1)
            position_history_size (int): Number of previous positions to store for smoothing
        """
        self.smoothing_factor = smoothing_factor
        self.screen_width, self.screen_height = pyautogui.size()
        self.position_history = []
        self.position_history_size = position_history_size

    def move_cursor(self, x_normalized: float, y_normalized: float):
        """Move the cursor to the specified normalized coordinates
        
        Args:
            x_normalized (float): Normalized x coordinate (0-1)
            y_normalized (float): Normalized y coordinate (0-1)
        """
        cursor_x = int(x_normalized * self.screen_width)
        cursor_y = int(y_normalized * self.screen_height)
        pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

    def perform_left_click(self):
        """Perform a left mouse click"""
        pyautogui.click(button='left')

    def perform_right_click(self):
        """Perform a right mouse click"""
        pyautogui.click(button='right')