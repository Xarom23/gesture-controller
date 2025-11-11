"""
Unit tests for BlinkDetector module
"""

import unittest
from unittest.mock import Mock, MagicMock
from blink_detector import BlinkDetector
from landmark_detector import FaceResults


class TestBlinkDetector(unittest.TestCase):
    """Test cases for BlinkDetector class"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = BlinkDetector(ear_threshold=0.07)

    def test_initialization(self):
        """Test BlinkDetector initialization"""
        self.assertEqual(self.detector.ear_threshold, 0.07)

        # Test custom threshold
        custom_detector = BlinkDetector(ear_threshold=0.1)
        self.assertEqual(custom_detector.ear_threshold, 0.1)

    def test_detect_left_eye_blink_with_none_landmarks(self):
        """Test left eye blink detection with None landmarks"""
        result = self.detector.detect_left_eye_blink(None)
        self.assertFalse(result)

    def test_detect_right_eye_blink_with_none_landmarks(self):
        """Test right eye blink detection with None landmarks"""
        result = self.detector.detect_right_eye_blink(None)
        self.assertFalse(result)

    def test_detect_left_eye_blink_with_closed_eye(self):
        """Test left eye blink detection when eye is closed (low EAR)"""
        # Create mock face landmarks
        mock_face_results = self._create_mock_face_results(ear_value=0.05)

        result = self.detector.detect_left_eye_blink(mock_face_results)
        self.assertTrue(result)

    def test_detect_left_eye_blink_with_open_eye(self):
        """Test left eye blink detection when eye is open (high EAR)"""
        # Create mock face landmarks with high EAR (above threshold of 0.07)
        # Using 0.10 to ensure it's clearly above the threshold
        mock_face_results = self._create_mock_face_results(ear_value=0.10)

        result = self.detector.detect_left_eye_blink(mock_face_results)
        self.assertFalse(result)

    def test_detect_right_eye_blink_with_closed_eye(self):
        """Test right eye blink detection when eye is closed (low EAR)"""
        mock_face_results = self._create_mock_face_results(ear_value=0.05)

        result = self.detector.detect_right_eye_blink(mock_face_results)
        self.assertTrue(result)

    def test_detect_right_eye_blink_with_open_eye(self):
        """Test right eye blink detection when eye is open (high EAR)"""
        # Using 0.10 to ensure it's clearly above the threshold of 0.07
        mock_face_results = self._create_mock_face_results(ear_value=0.10)

        result = self.detector.detect_right_eye_blink(mock_face_results)
        self.assertFalse(result)

    def test_calculate_ear_with_zero_horizontal_distance(self):
        """Test EAR calculation with zero horizontal distance"""
        # Create eye landmarks with zero horizontal distance
        eye_landmarks = self._create_mock_eye_landmarks(h_distance=0, v_distance=0.1)

        ear = self.detector._calculate_ear(eye_landmarks)
        self.assertEqual(ear, 0)

    def test_calculate_ear_normal_values(self):
        """Test EAR calculation with normal values"""
        eye_landmarks = self._create_mock_eye_landmarks(h_distance=0.1, v_distance=0.02)

        ear = self.detector._calculate_ear(eye_landmarks)
        # EAR = (v1 + v2) / (2 * h) = (0.02 + 0.02) / (2 * 0.1) = 0.2
        self.assertAlmostEqual(ear, 0.2, places=2)

    def _create_mock_face_results(self, ear_value=0.1):
        """Helper method to create mock face results

        Args:
            ear_value (float): The EAR value to simulate

        Returns:
            Mock FaceResults object
        """
        mock_face_results = Mock(spec=FaceResults)
        mock_landmarks = Mock()

        # Left eye indices: 362, 382, 381, 380, 374, 373, 390, 463, 398, 384, 385, 386, 387, 388
        # Right eye indices: 33, 160, 158, 133, 153, 144, 163, 263, 249, 390, 373, 374, 380, 381
        # The _calculate_ear method uses indices: 0, 1, 2, 6, 7, 8 from the eye landmarks list

        # Create eye landmarks that will produce the desired EAR
        # EAR = (v1 + v2) / (2 * h)
        # We want: ear_value = (v1 + v2) / (2 * h)
        # So if h = 0.1, then: v1 + v2 = ear_value * 2 * 0.1 = ear_value * 0.2
        horizontal_distance = 0.1
        total_vertical = ear_value * 2 * horizontal_distance
        vertical_distance = total_vertical / 2  # Split equally between v1 and v2

        # Create landmarks list with proper indices
        landmarks_list = []

        # All eye indices we need to cover
        left_eye_indices = [362, 382, 381, 380, 374, 373, 390, 463, 398, 384, 385, 386, 387, 388]
        right_eye_indices = [33, 160, 158, 133, 153, 144, 163, 263, 249, 390, 373, 374, 380, 381]
        all_eye_indices = set(left_eye_indices + right_eye_indices)

        for i in range(500):
            mock_landmark = Mock()

            if i in all_eye_indices:
                # Map to the expected structure for _calculate_ear
                # _calculate_ear uses: [0], [1], [2], [6], [7], [8]
                idx_in_eye = left_eye_indices.index(i) if i in left_eye_indices else (
                    right_eye_indices.index(i) if i in right_eye_indices else 0
                )

                if idx_in_eye == 0:  # Horizontal left
                    mock_landmark.x = 0.0
                    mock_landmark.y = 0.5
                elif idx_in_eye == 6:  # Horizontal right
                    mock_landmark.x = horizontal_distance
                    mock_landmark.y = 0.5
                elif idx_in_eye == 1:  # Vertical top 1
                    mock_landmark.x = 0.05
                    mock_landmark.y = 0.5
                elif idx_in_eye == 8:  # Vertical bottom 1
                    mock_landmark.x = 0.05
                    mock_landmark.y = 0.5 + vertical_distance
                elif idx_in_eye == 2:  # Vertical top 2
                    mock_landmark.x = 0.075
                    mock_landmark.y = 0.5
                elif idx_in_eye == 7:  # Vertical bottom 2
                    mock_landmark.x = 0.075
                    mock_landmark.y = 0.5 + vertical_distance
                else:
                    mock_landmark.x = 0.05
                    mock_landmark.y = 0.5
            else:
                mock_landmark.x = 0.0
                mock_landmark.y = 0.0

            landmarks_list.append(mock_landmark)

        mock_landmarks.landmark = landmarks_list
        mock_face_results.landmarks = mock_landmarks

        return mock_face_results

    def _create_mock_eye_landmarks(self, h_distance=0.1, v_distance=0.02):
        """Helper method to create mock eye landmarks

        Args:
            h_distance (float): Horizontal distance between eye corners
            v_distance (float): Vertical distance between eyelids

        Returns:
            List of mock landmarks
        """
        landmarks = []
        for i in range(14):
            mock_landmark = Mock()
            if i == 0:
                mock_landmark.x = 0.0
            elif i == 6:
                mock_landmark.x = h_distance
            else:
                mock_landmark.x = 0.0

            if i == 1:
                mock_landmark.y = 0.0
            elif i == 8:
                mock_landmark.y = v_distance
            elif i == 2:
                mock_landmark.y = 0.0
            elif i == 7:
                mock_landmark.y = v_distance
            else:
                mock_landmark.y = 0.0

            landmarks.append(mock_landmark)

        return landmarks


if __name__ == '__main__':
    unittest.main()
