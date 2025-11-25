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
        self.detector = BlinkDetector(ear_threshold=0.40)

    def test_initialization(self):
        """Test BlinkDetector initialization"""
        self.assertEqual(self.detector.ear_threshold, 0.40)

        # Test custom threshold
        custom_detector = BlinkDetector(ear_threshold=0.35)
        self.assertEqual(custom_detector.ear_threshold, 0.35)

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
        # Create mock face landmarks with EAR below threshold (0.40)
        mock_face_results = self._create_mock_face_results(ear_value=0.25)

        result = self.detector.detect_left_eye_blink(mock_face_results)
        self.assertTrue(result)

    def test_detect_left_eye_blink_with_open_eye(self):
        """Test left eye blink detection when eye is open (high EAR)"""
        # Create mock face landmarks with high EAR (above threshold of 0.40)
        # Using 0.55 to simulate an open eye
        mock_face_results = self._create_mock_face_results(ear_value=0.55)

        result = self.detector.detect_left_eye_blink(mock_face_results)
        self.assertFalse(result)

    def test_detect_right_eye_blink_with_closed_eye(self):
        """Test right eye blink detection when eye is closed (low EAR)"""
        # EAR below threshold (0.40) indicates closed eye
        mock_face_results = self._create_mock_face_results(ear_value=0.25)

        result = self.detector.detect_right_eye_blink(mock_face_results)
        self.assertTrue(result)

    def test_detect_right_eye_blink_with_open_eye(self):
        """Test right eye blink detection when eye is open (high EAR)"""
        # Using 0.55 to ensure it's clearly above the threshold of 0.40
        mock_face_results = self._create_mock_face_results(ear_value=0.55)

        result = self.detector.detect_right_eye_blink(mock_face_results)
        self.assertFalse(result)

    def test_calculate_ear_with_zero_horizontal_distance(self):
        """Test EAR calculation with zero horizontal distance"""
        # Create mock landmarks with zero horizontal distance
        mock_landmarks = self._create_mock_landmarks_for_ear(h_distance=0, v_distance=0.1)
        eye_indices = self.detector.LEFT_EYE_EAR

        ear = self.detector._calculate_ear(eye_indices, mock_landmarks)
        self.assertEqual(ear, 0)

    def test_calculate_ear_normal_values(self):
        """Test EAR calculation with normal values"""
        # Create mock landmarks that produce EAR = 0.5
        # EAR = (v1 + v2) / (2 * h)
        # With h=0.1 and v1=v2=0.05: EAR = (0.05 + 0.05) / (2 * 0.1) = 0.5
        mock_landmarks = self._create_mock_landmarks_for_ear(h_distance=0.1, v_distance=0.05)
        eye_indices = self.detector.LEFT_EYE_EAR

        ear = self.detector._calculate_ear(eye_indices, mock_landmarks)
        self.assertAlmostEqual(ear, 0.5, places=2)

    def _create_mock_face_results(self, ear_value=0.5):
        """Helper method to create mock face results

        Args:
            ear_value (float): The EAR value to simulate (default 0.5 for open eye)

        Returns:
            Mock FaceResults object
        """
        mock_face_results = Mock(spec=FaceResults)
        mock_landmarks = self._create_mock_landmarks_for_ear(
            h_distance=0.1,
            v_distance=ear_value * 0.1  # v_distance calculated to produce desired EAR
        )
        mock_face_results.landmarks = mock_landmarks

        return mock_face_results

    def _create_mock_landmarks_for_ear(self, h_distance=0.1, v_distance=0.05):
        """Helper method to create mock landmarks for EAR calculation

        The new algorithm uses 6 landmarks per eye:
        - LEFT_EYE_EAR = [362, 380, 374, 263, 386, 385]
        - RIGHT_EYE_EAR = [33, 159, 158, 133, 153, 145]

        Indices in the list:
        - [0]: horizontal left corner
        - [1]: vertical top 1
        - [2]: vertical top 2
        - [3]: horizontal right corner
        - [4]: vertical bottom 2
        - [5]: vertical bottom 1

        EAR = (v1 + v2) / (2 * h)
        where v1 = distance([1], [5]) and v2 = distance([2], [4])

        Args:
            h_distance (float): Horizontal distance between eye corners
            v_distance (float): Vertical distance between eyelids

        Returns:
            Mock landmarks object
        """
        mock_landmarks = Mock()

        # New landmark indices for the updated algorithm
        left_eye_indices = [362, 380, 374, 263, 386, 385]
        right_eye_indices = [33, 159, 158, 133, 153, 145]

        # Create a list of 500 landmarks (MediaPipe face mesh has 478)
        landmarks_list = []
        for i in range(500):
            mock_landmark = Mock()
            mock_landmark.x = 0.0
            mock_landmark.y = 0.0
            mock_landmark.z = 0.0
            landmarks_list.append(mock_landmark)

        # Configure left eye landmarks
        # Index 0 (362): horizontal left corner
        landmarks_list[362].x = 0.0
        landmarks_list[362].y = 0.5
        landmarks_list[362].z = 0.0

        # Index 1 (380): vertical top 1
        landmarks_list[380].x = 0.03
        landmarks_list[380].y = 0.5
        landmarks_list[380].z = 0.0

        # Index 2 (374): vertical top 2
        landmarks_list[374].x = 0.07
        landmarks_list[374].y = 0.5
        landmarks_list[374].z = 0.0

        # Index 3 (263): horizontal right corner
        landmarks_list[263].x = h_distance
        landmarks_list[263].y = 0.5
        landmarks_list[263].z = 0.0

        # Index 4 (386): vertical bottom 2
        landmarks_list[386].x = 0.07
        landmarks_list[386].y = 0.5 + v_distance
        landmarks_list[386].z = 0.0

        # Index 5 (385): vertical bottom 1
        landmarks_list[385].x = 0.03
        landmarks_list[385].y = 0.5 + v_distance
        landmarks_list[385].z = 0.0

        # Configure right eye landmarks
        # Index 0 (33): horizontal left corner
        landmarks_list[33].x = 0.0
        landmarks_list[33].y = 0.5
        landmarks_list[33].z = 0.0

        # Index 1 (159): vertical top 1
        landmarks_list[159].x = 0.03
        landmarks_list[159].y = 0.5
        landmarks_list[159].z = 0.0

        # Index 2 (158): vertical top 2
        landmarks_list[158].x = 0.07
        landmarks_list[158].y = 0.5
        landmarks_list[158].z = 0.0

        # Index 3 (133): horizontal right corner
        landmarks_list[133].x = h_distance
        landmarks_list[133].y = 0.5
        landmarks_list[133].z = 0.0

        # Index 4 (153): vertical bottom 2
        landmarks_list[153].x = 0.07
        landmarks_list[153].y = 0.5 + v_distance
        landmarks_list[153].z = 0.0

        # Index 5 (145): vertical bottom 1
        landmarks_list[145].x = 0.03
        landmarks_list[145].y = 0.5 + v_distance
        landmarks_list[145].z = 0.0

        mock_landmarks.landmark = landmarks_list
        return mock_landmarks


if __name__ == '__main__':
    unittest.main()
