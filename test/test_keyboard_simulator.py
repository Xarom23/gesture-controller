"""
Unit tests for KeyboardSimulator module
"""

import unittest
from unittest.mock import patch
from keyboard_simulator import KeyboardSimulator


class TestKeyboardSimulator(unittest.TestCase):
    """Test cases for KeyboardSimulator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.simulator = KeyboardSimulator()

    @patch('keyboard_simulator.pyautogui')
    def test_press_key_up(self, mock_pyautogui):
        """Test pressing up arrow key"""
        KeyboardSimulator.press_key('up')
        mock_pyautogui.press.assert_called_once_with('up')

    @patch('keyboard_simulator.pyautogui')
    def test_press_key_down(self, mock_pyautogui):
        """Test pressing down arrow key"""
        KeyboardSimulator.press_key('down')
        mock_pyautogui.press.assert_called_once_with('down')

    @patch('keyboard_simulator.pyautogui')
    def test_press_key_left(self, mock_pyautogui):
        """Test pressing left arrow key"""
        KeyboardSimulator.press_key('left')
        mock_pyautogui.press.assert_called_once_with('left')

    @patch('keyboard_simulator.pyautogui')
    def test_press_key_right(self, mock_pyautogui):
        """Test pressing right arrow key"""
        KeyboardSimulator.press_key('right')
        mock_pyautogui.press.assert_called_once_with('right')

    @patch('keyboard_simulator.pyautogui')
    def test_press_multiple_keys(self, mock_pyautogui):
        """Test pressing multiple keys in sequence"""
        KeyboardSimulator.press_key('up')
        KeyboardSimulator.press_key('down')
        KeyboardSimulator.press_key('left')
        KeyboardSimulator.press_key('right')

        self.assertEqual(mock_pyautogui.press.call_count, 4)

    @patch('keyboard_simulator.pyautogui')
    def test_press_any_key(self, mock_pyautogui):
        """Test pressing any arbitrary key"""
        KeyboardSimulator.press_key('space')
        mock_pyautogui.press.assert_called_once_with('space')

        mock_pyautogui.reset_mock()
        KeyboardSimulator.press_key('enter')
        mock_pyautogui.press.assert_called_once_with('enter')


if __name__ == '__main__':
    unittest.main()
