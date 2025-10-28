import pyautogui

class MouseSimulator:
    def __init__(self, smoothing_factor=0.5, position_history_size=5):
        self.smoothing_factor = smoothing_factor
        self.screen_width, self.screen_height = pyautogui.size()
        self.position_history = []
        self.position_history_size = position_history_size

    def move_cursor(self, x_normalized: float, y_normalized: float):
        cursor_x = int(x_normalized * self.screen_width)
        cursor_y = int(y_normalized * self.screen_height)
        pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

    def perform_click(self):
        pyautogui.click()

    def should_click(self, index_x: float, index_y: float, thumb_x: float, thumb_y: float) -> bool:
        distance = ((index_x - thumb_x)**2 + (index_y - thumb_y)**2) ** 0.5
        return distance < 0.05