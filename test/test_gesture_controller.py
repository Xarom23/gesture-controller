"""
Unit tests for GestureController module
"""

import unittest
from unittest.mock import Mock, patch, mock_open, MagicMock
import json
import os
from gesture_controller import GestureController
from landmark_detector import HandsResults, FaceResults


class TestGestureController(unittest.TestCase):
    """Test cases for GestureController class"""

    @patch('gesture_controller.pyautogui')
    @patch('gesture_controller.os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open, read_data='{"left_hand_mode": "keyboard", "right_hand_mode": "mouse", "left_blink_mode": "left_click", "right_blink_mode": "right_click"}')
    def setUp(self, mock_file, mock_getmtime, mock_pyautogui):
        """Set up test fixtures"""
        mock_pyautogui.size.return_value = (1920, 1080)
        mock_getmtime.return_value = 1234567890
        self.controller = GestureController()

    @patch('gesture_controller.pyautogui')
    @patch('gesture_controller.os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open, read_data='{"left_hand_mode": "keyboard", "right_hand_mode": "mouse", "left_blink_mode": "left_click", "right_blink_mode": "right_click"}')
    def test_initialization(self, mock_file, mock_getmtime, mock_pyautogui):
        """Test GestureController initialization"""
        mock_pyautogui.size.return_value = (1920, 1080)
        mock_getmtime.return_value = 1234567890
        controller = GestureController(movement_threshold=50, smoothing_factor=0.7, position_history_size=10)

        self.assertIsNotNone(controller.mouse_simulator)
        self.assertIsNotNone(controller.keyboard_simulator)
        self.assertIsNotNone(controller.trajectory_detector)
        self.assertIsNotNone(controller.blink_detector)

    @patch('gesture_controller.pyautogui')
    @patch('gesture_controller.os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open, read_data='{"left_hand_mode": "mouse", "right_hand_mode": "keyboard", "left_blink_mode": "right_click", "right_blink_mode": "left_click"}')
    def test_load_config(self, mock_file, mock_getmtime, mock_pyautogui):
        """Test configuration loading from JSON file"""
        mock_pyautogui.size.return_value = (1920, 1080)
        mock_getmtime.return_value = 1234567890
        controller = GestureController()

        self.assertEqual(controller.left_hand_mode, 'mouse')
        self.assertEqual(controller.right_hand_mode, 'keyboard')
        self.assertEqual(controller.left_blink_mode, 'right_click')
        self.assertEqual(controller.right_blink_mode, 'left_click')

    @patch('gesture_controller.pyautogui')
    @patch('gesture_controller.os.path.getmtime', side_effect=FileNotFoundError)
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_config_file_not_found(self, mock_file, mock_getmtime, mock_pyautogui):
        """Test default configuration when config file not found"""
        mock_pyautogui.size.return_value = (1920, 1080)
        controller = GestureController()

        # Should use default values
        self.assertEqual(controller.left_hand_mode, 'keyboard')
        self.assertEqual(controller.right_hand_mode, 'mouse')
        self.assertEqual(controller.left_blink_mode, 'left_click')
        self.assertEqual(controller.right_blink_mode, 'right_click')

    @patch('gesture_controller.pyautogui')
    @patch('gesture_controller.os.path.getmtime')
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    def test_load_config_invalid_json(self, mock_file, mock_getmtime, mock_pyautogui):
        """Test default configuration when JSON is invalid"""
        mock_pyautogui.size.return_value = (1920, 1080)
        mock_getmtime.return_value = 1234567890

        with patch('json.load', side_effect=json.JSONDecodeError("msg", "doc", 0)):
            controller = GestureController()

            # Should use default values
            self.assertEqual(controller.left_hand_mode, 'keyboard')
            self.assertEqual(controller.right_hand_mode, 'mouse')

    def test_process_gestures_with_none_inputs(self):
        """Test gesture processing with None inputs"""
        # Should not raise any exceptions
        self.controller.process_gestures(None, None)

    @patch('gesture_controller.os.path.getmtime')
    def test_process_gestures_left_eye_blink(self, mock_getmtime):
        """Test left eye blink detection and action"""
        mock_getmtime.return_value = 1234567890

        # Create mock face results
        mock_face = Mock(spec=FaceResults)
        mock_face.landmarks = Mock()

        # Mock blink detector to return left eye blink
        with patch.object(self.controller.blink_detector, 'detect_left_eye_blink', return_value=True), \
             patch.object(self.controller.blink_detector, 'detect_right_eye_blink', return_value=False), \
             patch.object(self.controller.mouse_simulator, 'perform_left_click') as mock_left_click:

            self.controller.process_gestures(None, mock_face)
            mock_left_click.assert_called_once()

    @patch('gesture_controller.os.path.getmtime')
    def test_process_gestures_right_eye_blink(self, mock_getmtime):
        """Test right eye blink detection and action"""
        mock_getmtime.return_value = 1234567890

        mock_face = Mock(spec=FaceResults)
        mock_face.landmarks = Mock()

        # Mock blink detector to return right eye blink
        with patch.object(self.controller.blink_detector, 'detect_left_eye_blink', return_value=False), \
             patch.object(self.controller.blink_detector, 'detect_right_eye_blink', return_value=True), \
             patch.object(self.controller.mouse_simulator, 'perform_right_click') as mock_right_click:

            self.controller.process_gestures(None, mock_face)
            mock_right_click.assert_called_once()

    @patch('gesture_controller.os.path.getmtime')
    def test_process_gestures_right_hand_mouse_mode(self, mock_getmtime):
        """Test right hand processing in mouse mode"""
        mock_getmtime.return_value = 1234567890

        # Create mock hand results
        mock_hands = Mock(spec=HandsResults)
        mock_hand_landmark = Mock()
        mock_landmark = Mock()
        mock_landmark.x = 0.5
        mock_landmark.y = 0.5
        mock_hand_landmark.landmark = {9: mock_landmark}  # MIDDLE_FINGER_MCP is index 9

        mock_mp_hands = Mock()
        mock_mp_hands.HandLandmark.MIDDLE_FINGER_MCP = 9

        mock_hands.landmarks = {'Right': mock_hand_landmark}
        mock_hands.mp_hands = mock_mp_hands

        with patch.object(self.controller.mouse_simulator, 'move_cursor') as mock_move:
            self.controller.process_gestures(mock_hands, None)
            mock_move.assert_called()

    @patch('gesture_controller.os.path.getmtime')
    def test_process_gestures_left_hand_keyboard_mode(self, mock_getmtime):
        """Test left hand processing in keyboard mode"""
        mock_getmtime.return_value = 1234567890

        # Create mock hand results
        mock_hands = Mock(spec=HandsResults)
        mock_hand_landmark = Mock()
        mock_landmark = Mock()
        mock_landmark.x = 0.5
        mock_landmark.y = 0.5
        mock_hand_landmark.landmark = {8: mock_landmark}  # INDEX_FINGER_TIP is index 8

        mock_mp_hands = Mock()
        mock_mp_hands.HandLandmark.INDEX_FINGER_TIP = 8

        mock_hands.landmarks = {'Left': mock_hand_landmark}
        mock_hands.mp_hands = mock_mp_hands

        with patch.object(self.controller.trajectory_detector, 'detect_direction', return_value='up'), \
             patch.object(self.controller.keyboard_simulator, 'press_key') as mock_press:

            self.controller.process_gestures(mock_hands, None)
            mock_press.assert_called_once_with('up')

    def test_get_landmark_coords(self):
        """Test getting landmark coordinates"""
        mock_landmarks = Mock()
        mock_landmark = Mock()
        mock_landmark.x = 0.75
        mock_landmark.y = 0.25
        mock_landmarks.landmark = {5: mock_landmark}

        x, y = self.controller._get_landmark_coords(mock_landmarks, 5)
        self.assertEqual(x, 0.75)
        self.assertEqual(y, 0.25)

    @patch('gesture_controller.os.path.getmtime')
    def test_check_config_changes(self, mock_getmtime):
        """Test config change detection"""
        # Initial time
        mock_getmtime.return_value = 1234567890
        self.controller._check_config_changes()

        # Simulate file modification
        mock_getmtime.return_value = 1234567900

        with patch.object(self.controller, '_load_config') as mock_load:
            self.controller._check_config_changes()
            mock_load.assert_called_once()

    @patch('gesture_controller.os.path.getmtime', side_effect=FileNotFoundError)
    def test_check_config_changes_file_not_found(self, mock_getmtime):
        """Test config change detection when file is not found"""
        # Should not raise an exception
        self.controller._check_config_changes()

    @patch('gesture_controller.os.path.getmtime')
    def test_process_gestures_left_blink_right_click_mode(self, mock_getmtime):
        """Test left eye blink with right_click mode"""
        mock_getmtime.return_value = 1234567890

        # Configure left blink to trigger right click
        self.controller.left_blink_mode = 'right_click'

        mock_face = Mock(spec=FaceResults)
        mock_face.landmarks = Mock()

        with patch.object(self.controller.blink_detector, 'detect_left_eye_blink', return_value=True), \
             patch.object(self.controller.blink_detector, 'detect_right_eye_blink', return_value=False), \
             patch.object(self.controller.mouse_simulator, 'perform_right_click') as mock_right_click:

            self.controller.process_gestures(None, mock_face)
            mock_right_click.assert_called_once()

    @patch('gesture_controller.os.path.getmtime')
    def test_process_gestures_right_blink_left_click_mode(self, mock_getmtime):
        """Test right eye blink with left_click mode"""
        mock_getmtime.return_value = 1234567890

        # Configure right blink to trigger left click
        self.controller.right_blink_mode = 'left_click'

        mock_face = Mock(spec=FaceResults)
        mock_face.landmarks = Mock()

        with patch.object(self.controller.blink_detector, 'detect_left_eye_blink', return_value=False), \
             patch.object(self.controller.blink_detector, 'detect_right_eye_blink', return_value=True), \
             patch.object(self.controller.mouse_simulator, 'perform_left_click') as mock_left_click:

            self.controller.process_gestures(None, mock_face)
            mock_left_click.assert_called_once()

    @patch('gesture_controller.os.path.getmtime')
    def test_process_gestures_right_hand_keyboard_mode(self, mock_getmtime):
        """Test right hand processing in keyboard mode"""
        mock_getmtime.return_value = 1234567890

        # Configure right hand to keyboard mode
        self.controller.right_hand_mode = 'keyboard'

        mock_hands = Mock(spec=HandsResults)
        mock_hand_landmark = Mock()
        mock_landmark = Mock()
        mock_landmark.x = 0.5
        mock_landmark.y = 0.5
        mock_hand_landmark.landmark = {8: mock_landmark}

        mock_mp_hands = Mock()
        mock_mp_hands.HandLandmark.INDEX_FINGER_TIP = 8

        mock_hands.landmarks = {'Right': mock_hand_landmark}
        mock_hands.mp_hands = mock_mp_hands

        with patch.object(self.controller.trajectory_detector, 'detect_direction', return_value='down'), \
             patch.object(self.controller.keyboard_simulator, 'press_key') as mock_press:

            self.controller.process_gestures(mock_hands, None)
            mock_press.assert_called_once_with('down')

    @patch('gesture_controller.os.path.getmtime')
    def test_process_gestures_left_hand_mouse_mode(self, mock_getmtime):
        """Test left hand processing in mouse mode"""
        mock_getmtime.return_value = 1234567890

        # Configure left hand to mouse mode
        self.controller.left_hand_mode = 'mouse'

        mock_hands = Mock(spec=HandsResults)
        mock_hand_landmark = Mock()
        mock_landmark = Mock()
        mock_landmark.x = 0.6
        mock_landmark.y = 0.4
        mock_hand_landmark.landmark = {9: mock_landmark}

        mock_mp_hands = Mock()
        mock_mp_hands.HandLandmark.MIDDLE_FINGER_MCP = 9

        mock_hands.landmarks = {'Left': mock_hand_landmark}
        mock_hands.mp_hands = mock_mp_hands

        with patch.object(self.controller.mouse_simulator, 'move_cursor') as mock_move:
            self.controller.process_gestures(mock_hands, None)
            mock_move.assert_called()


if __name__ == '__main__':
    unittest.main()
