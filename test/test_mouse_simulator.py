"""
Unit tests for MouseSimulator module
"""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from mouse_simulator import MouseSimulator


class TestMouseSimulator(unittest.TestCase):
    """Test cases for MouseSimulator class"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a patcher for pyautogui module
        self.patcher = patch('mouse_simulator.pyautogui')
        self.mock_pyautogui = self.patcher.start()
        self.mock_pyautogui.size.return_value = (1920, 1080)
        self.mock_pyautogui.FAILSAFE = False
        self.simulator = MouseSimulator(smoothing_factor=0.5, position_history_size=5)

    def tearDown(self):
        """Clean up test fixtures"""
        self.patcher.stop()

    @patch('mouse_simulator.pyautogui')
    def test_initialization(self, mock_pyautogui):
        """Test MouseSimulator initialization"""
        mock_pyautogui.size.return_value = (1920, 1080)
        simulator = MouseSimulator(smoothing_factor=0.7, position_history_size=10)

        self.assertEqual(simulator.smoothing_factor, 0.7)
        self.assertEqual(simulator.position_history_size, 10)
        self.assertEqual(simulator.screen_width, 1920)
        self.assertEqual(simulator.screen_height, 1080)
        self.assertEqual(len(simulator.position_history), 0)

    def test_move_cursor(self):
        """Test cursor movement"""
        self.simulator.move_cursor(0.5, 0.5)

        # Verify moveTo was called with correct screen coordinates
        # 0.5 * 1920 = 960, 0.5 * 1080 = 540
        self.mock_pyautogui.moveTo.assert_called_once_with(960, 540, duration=0.1)

    def test_move_cursor_top_left(self):
        """Test cursor movement to top-left corner"""
        self.simulator.move_cursor(0.0, 0.0)

        self.mock_pyautogui.moveTo.assert_called_once_with(0, 0, duration=0.1)

    def test_move_cursor_bottom_right(self):
        """Test cursor movement to bottom-right corner"""
        self.simulator.move_cursor(1.0, 1.0)

        self.mock_pyautogui.moveTo.assert_called_once_with(1920, 1080, duration=0.1)

    def test_perform_left_click(self):
        """Test left mouse click"""
        self.simulator.perform_left_click()

        self.mock_pyautogui.click.assert_called_once_with(button='left')

    def test_perform_right_click(self):
        """Test right mouse click"""
        self.simulator.perform_right_click()

        self.mock_pyautogui.click.assert_called_once_with(button='right')

    def test_multiple_clicks(self):
        """Test multiple consecutive clicks"""
        self.simulator.perform_left_click()
        self.simulator.perform_right_click()
        self.simulator.perform_left_click()

        self.assertEqual(self.mock_pyautogui.click.call_count, 3)

    @patch('mouse_simulator.pyautogui')
    def test_different_screen_sizes(self, mock_pyautogui):
        """Test initialization with different screen sizes"""
        mock_pyautogui.size.return_value = (2560, 1440)
        simulator = MouseSimulator()

        self.assertEqual(simulator.screen_width, 2560)
        self.assertEqual(simulator.screen_height, 1440)

        # Test movement with new screen size
        simulator.move_cursor(0.5, 0.5)
        mock_pyautogui.moveTo.assert_called_once_with(1280, 720, duration=0.1)


if __name__ == '__main__':
    unittest.main()
