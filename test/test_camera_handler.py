"""
Unit tests for CameraHandler module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk
from camera_handler import CameraHandler


class TestCameraHandler(unittest.TestCase):
    """Test cases for CameraHandler class"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_canvas = Mock(spec=tk.Canvas)

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    def test_initialization(self, mock_mp, mock_landmark, mock_gesture):
        """Test CameraHandler initialization"""
        handler = CameraHandler(self.mock_canvas, camera_index=0, width=640, height=480)

        self.assertEqual(handler.camera_index, 0)
        self.assertEqual(handler.width, 640)
        self.assertEqual(handler.height, 480)
        self.assertFalse(handler.is_running)
        self.assertTrue(handler.show_video)
        self.assertFalse(handler.show_landmarks)
        self.assertIsNone(handler.cap)

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    @patch('camera_handler.cv2.VideoCapture')
    def test_start_success(self, mock_video_capture, mock_mp, mock_landmark, mock_gesture):
        """Test successful camera start"""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap

        handler = CameraHandler(self.mock_canvas)

        with patch.object(handler, '_update_frame'):
            handler.start()

        self.assertTrue(handler.is_running)
        mock_cap.set.assert_any_call(3, 600)  # CAP_PROP_FRAME_WIDTH = 3
        mock_cap.set.assert_any_call(4, 351)  # CAP_PROP_FRAME_HEIGHT = 4

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    @patch('camera_handler.cv2.VideoCapture')
    def test_start_failure(self, mock_video_capture, mock_mp, mock_landmark, mock_gesture):
        """Test camera start failure"""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = False
        mock_video_capture.return_value = mock_cap

        handler = CameraHandler(self.mock_canvas)

        with self.assertRaises(Exception):
            handler.start()

        self.assertFalse(handler.is_running)

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    @patch('camera_handler.cv2.VideoCapture')
    def test_stop(self, mock_video_capture, mock_mp, mock_landmark, mock_gesture):
        """Test camera stop"""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap

        handler = CameraHandler(self.mock_canvas)

        with patch.object(handler, '_update_frame'):
            handler.start()

        handler.stop()

        self.assertFalse(handler.is_running)
        mock_cap.release.assert_called_once()
        self.assertIsNone(handler.cap)

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    def test_set_show_video(self, mock_mp, mock_landmark, mock_gesture):
        """Test setting video display on/off"""
        handler = CameraHandler(self.mock_canvas)

        handler.set_show_video(False)
        self.assertFalse(handler.show_video)

        handler.set_show_video(True)
        self.assertTrue(handler.show_video)

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    def test_set_show_landmarks(self, mock_mp, mock_landmark, mock_gesture):
        """Test setting landmarks display on/off"""
        handler = CameraHandler(self.mock_canvas)

        handler.set_show_landmarks(True)
        self.assertTrue(handler.show_landmarks)

        handler.set_show_landmarks(False)
        self.assertFalse(handler.show_landmarks)

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    @patch('camera_handler.cv2.VideoCapture')
    def test_get_current_frame(self, mock_video_capture, mock_mp, mock_landmark, mock_gesture):
        """Test getting current frame"""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_frame = Mock()
        mock_cap.read.return_value = (True, mock_frame)
        mock_video_capture.return_value = mock_cap

        handler = CameraHandler(self.mock_canvas)

        with patch.object(handler, '_update_frame'):
            handler.start()

        frame = handler.get_current_frame()
        self.assertEqual(frame, mock_frame)

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    @patch('camera_handler.cv2.VideoCapture')
    def test_get_current_frame_no_capture(self, mock_video_capture, mock_mp, mock_landmark, mock_gesture):
        """Test getting frame when no capture is active"""
        handler = CameraHandler(self.mock_canvas)

        frame = handler.get_current_frame()
        self.assertIsNone(frame)

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    @patch('camera_handler.cv2.VideoCapture')
    def test_set_camera(self, mock_video_capture, mock_mp, mock_landmark, mock_gesture):
        """Test changing camera"""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap

        handler = CameraHandler(self.mock_canvas, camera_index=0)

        with patch.object(handler, '_update_frame'):
            handler.start()

        with patch.object(handler, 'start') as mock_start, \
             patch.object(handler, 'stop') as mock_stop:
            handler.is_running = True
            handler.set_camera(1)

            mock_stop.assert_called_once()
            mock_start.assert_called_once()
            self.assertEqual(handler.camera_index, 1)

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    def test_set_camera_not_running(self, mock_mp, mock_landmark, mock_gesture):
        """Test changing camera when not running"""
        handler = CameraHandler(self.mock_canvas, camera_index=0)

        # Ensure handler is not running
        handler.is_running = False

        # Don't use mocks here, just test the state changes
        handler.set_camera(1)

        # After changing camera, it should still not be running and camera index should change
        self.assertFalse(handler.is_running)
        self.assertEqual(handler.camera_index, 1)

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    @patch('camera_handler.cv2.VideoCapture')
    @patch('camera_handler.cv2.flip')
    @patch('camera_handler.cv2.cvtColor')
    @patch('camera_handler.cv2.resize')
    @patch('camera_handler.Image.fromarray')
    @patch('camera_handler.ImageTk.PhotoImage')
    @patch('config.gesture_control_enabled', True)
    def test_update_frame_with_detections_and_gesture_control(
        self, mock_photo, mock_fromarray, mock_resize, mock_cvtColor,
        mock_flip, mock_video_capture, mock_mp, mock_landmark_class, mock_gesture_class
    ):
        """Test _update_frame with hand/face detections and gesture control enabled"""
        # Setup mocks
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_frame = Mock()
        mock_cap.read.return_value = (True, mock_frame)
        mock_video_capture.return_value = mock_cap

        mock_flip.return_value = mock_frame
        mock_rgb_frame = Mock()
        mock_cvtColor.return_value = mock_rgb_frame
        mock_resized = Mock()
        mock_resize.return_value = mock_resized

        # Mock landmark detector
        mock_landmark_instance = Mock()
        mock_detection_results = Mock()
        mock_hands = Mock()
        mock_face = Mock()
        mock_detection_results.hands = mock_hands
        mock_detection_results.face = mock_face
        mock_landmark_instance.detect_landmarks.return_value = mock_detection_results
        mock_landmark_class.return_value = mock_landmark_instance

        # Mock gesture controller
        mock_gesture_instance = Mock()
        mock_gesture_class.return_value = mock_gesture_instance

        handler = CameraHandler(self.mock_canvas)
        handler.landmark_detector = mock_landmark_instance
        handler.gesture_controller = mock_gesture_instance
        handler.is_running = True
        handler.show_video = True
        handler.cap = mock_cap

        # Call _update_frame
        with patch.object(handler.canvas, 'after'):
            handler._update_frame()

        # Verify gesture processing was called
        mock_gesture_instance.process_gestures.assert_called_once_with(
            hand_results=mock_hands,
            face_landmarks=mock_face
        )

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    @patch('camera_handler.cv2.VideoCapture')
    @patch('camera_handler.cv2.flip')
    @patch('camera_handler.cv2.cvtColor')
    @patch('camera_handler.cv2.resize')
    @patch('camera_handler.Image.fromarray')
    @patch('camera_handler.ImageTk.PhotoImage')
    def test_update_frame_with_landmarks_drawing(
        self, mock_photo, mock_fromarray, mock_resize, mock_cvtColor,
        mock_flip, mock_video_capture, mock_mp, mock_landmark_class, mock_gesture_class
    ):
        """Test _update_frame with landmarks drawing enabled"""
        # Setup mocks
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_frame = Mock()
        mock_cap.read.return_value = (True, mock_frame)
        mock_video_capture.return_value = mock_cap

        mock_flip.return_value = mock_frame
        mock_rgb_frame = Mock()
        mock_cvtColor.return_value = mock_rgb_frame
        mock_resized = Mock()
        mock_resize.return_value = mock_resized

        # Mock landmark detector with hands
        mock_landmark_instance = Mock()
        mock_detection_results = Mock()
        mock_hand_landmarks = Mock()
        mock_hands = Mock()
        mock_hands.landmarks = {'Right': mock_hand_landmarks}
        mock_detection_results.hands = mock_hands
        mock_detection_results.face = None
        mock_landmark_instance.detect_landmarks.return_value = mock_detection_results
        mock_landmark_class.return_value = mock_landmark_instance

        # Mock gesture controller
        mock_gesture_instance = Mock()
        mock_gesture_class.return_value = mock_gesture_instance

        # Mock MediaPipe drawing
        mock_mp_drawing = Mock()
        mock_mp.solutions.drawing_utils = mock_mp_drawing

        handler = CameraHandler(self.mock_canvas)
        handler.landmark_detector = mock_landmark_instance
        handler.gesture_controller = mock_gesture_instance
        handler.is_running = True
        handler.show_video = True
        handler.show_landmarks = True
        handler.cap = mock_cap
        handler.mp_drawing = mock_mp_drawing

        # Call _update_frame
        with patch.object(handler.canvas, 'after'):
            handler._update_frame()

        # Verify drawing was called
        self.assertTrue(mock_mp_drawing.draw_landmarks.called)

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    @patch('camera_handler.cv2.VideoCapture')
    @patch('camera_handler.cv2.flip')
    @patch('camera_handler.cv2.cvtColor')
    @patch('camera_handler.cv2.resize')
    @patch('camera_handler.Image.fromarray')
    @patch('camera_handler.ImageTk.PhotoImage')
    def test_update_frame_with_face_landmarks_drawing(
        self, mock_photo, mock_fromarray, mock_resize, mock_cvtColor,
        mock_flip, mock_video_capture, mock_mp, mock_landmark_class, mock_gesture_class
    ):
        """Test _update_frame with face landmarks drawing"""
        # Setup mocks
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_frame = Mock()
        mock_cap.read.return_value = (True, mock_frame)
        mock_video_capture.return_value = mock_cap

        mock_flip.return_value = mock_frame
        mock_rgb_frame = Mock()
        mock_cvtColor.return_value = mock_rgb_frame
        mock_resized = Mock()
        mock_resize.return_value = mock_resized

        # Mock landmark detector with face
        mock_landmark_instance = Mock()
        mock_detection_results = Mock()
        mock_face = Mock()
        mock_face.landmarks = Mock()
        mock_detection_results.hands = None
        mock_detection_results.face = mock_face
        mock_landmark_instance.detect_landmarks.return_value = mock_detection_results
        mock_landmark_class.return_value = mock_landmark_instance

        # Mock gesture controller
        mock_gesture_instance = Mock()
        mock_gesture_class.return_value = mock_gesture_instance

        # Mock MediaPipe drawing
        mock_mp_drawing = Mock()
        mock_mp.solutions.drawing_utils = mock_mp_drawing

        handler = CameraHandler(self.mock_canvas)
        handler.landmark_detector = mock_landmark_instance
        handler.gesture_controller = mock_gesture_instance
        handler.is_running = True
        handler.show_video = True
        handler.show_landmarks = True
        handler.cap = mock_cap
        handler.mp_drawing = mock_mp_drawing

        # Call _update_frame
        with patch.object(handler.canvas, 'after'):
            handler._update_frame()

        # Verify drawing was called
        self.assertTrue(mock_mp_drawing.draw_landmarks.called)

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    @patch('camera_handler.cv2.VideoCapture')
    def test_update_frame_schedules_next_update(self, mock_video_capture, mock_mp, mock_landmark, mock_gesture):
        """Test that _update_frame schedules the next update"""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (False, None)  # Return False to skip frame processing
        mock_video_capture.return_value = mock_cap

        handler = CameraHandler(self.mock_canvas)
        handler.is_running = True
        handler.cap = mock_cap

        # Call _update_frame
        handler._update_frame()

        # Verify canvas.after was called to schedule next update
        self.mock_canvas.after.assert_called()

    @patch('camera_handler.GestureController')
    @patch('camera_handler.LandmarkDetector')
    @patch('camera_handler.mp.solutions')
    def test_destructor(self, mock_mp, mock_landmark, mock_gesture):
        """Test __del__ method"""
        handler = CameraHandler(self.mock_canvas)

        with patch.object(handler, 'stop') as mock_stop, \
             patch.object(handler.landmark_detector, 'close') as mock_close:
            handler.__del__()

            mock_stop.assert_called_once()
            mock_close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
