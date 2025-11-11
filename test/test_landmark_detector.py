"""
Unit tests for LandmarkDetector module
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import numpy as np
from landmark_detector import (
    HandsResults,
    FaceResults,
    DetectionsResults,
    LandmarkDetector
)


class TestHandsResults(unittest.TestCase):
    """Test cases for HandsResults class"""

    def test_initialization(self):
        """Test HandsResults initialization"""
        mock_landmarks = {'Left': Mock(), 'Right': Mock()}
        mock_mp_hands = Mock()

        results = HandsResults(mock_landmarks, mock_mp_hands)

        self.assertEqual(results.landmarks, mock_landmarks)
        self.assertEqual(results.mp_hands, mock_mp_hands)

    def test_empty_landmarks(self):
        """Test HandsResults with empty landmarks"""
        results = HandsResults({}, Mock())
        self.assertEqual(len(results.landmarks), 0)


class TestFaceResults(unittest.TestCase):
    """Test cases for FaceResults class"""

    def test_initialization(self):
        """Test FaceResults initialization"""
        mock_landmarks = Mock()
        mock_mp_face = Mock()

        results = FaceResults(mock_landmarks, mock_mp_face)

        self.assertEqual(results.landmarks, mock_landmarks)
        self.assertEqual(results.mp_face, mock_mp_face)

    def test_with_none_landmarks(self):
        """Test FaceResults with None landmarks"""
        results = FaceResults(None, Mock())
        self.assertIsNone(results.landmarks)


class TestDetectionsResults(unittest.TestCase):
    """Test cases for DetectionsResults class"""

    def test_initialization_with_both(self):
        """Test DetectionsResults with both hands and face"""
        mock_hands = Mock(spec=HandsResults)
        mock_face = Mock(spec=FaceResults)

        results = DetectionsResults(mock_hands, mock_face)

        self.assertEqual(results.hands, mock_hands)
        self.assertEqual(results.face, mock_face)

    def test_initialization_with_none(self):
        """Test DetectionsResults with None values"""
        results = DetectionsResults(None, None)

        self.assertIsNone(results.hands)
        self.assertIsNone(results.face)

    def test_initialization_hands_only(self):
        """Test DetectionsResults with hands only"""
        mock_hands = Mock(spec=HandsResults)
        results = DetectionsResults(mock_hands, None)

        self.assertEqual(results.hands, mock_hands)
        self.assertIsNone(results.face)

    def test_initialization_face_only(self):
        """Test DetectionsResults with face only"""
        mock_face = Mock(spec=FaceResults)
        results = DetectionsResults(None, mock_face)

        self.assertIsNone(results.hands)
        self.assertEqual(results.face, mock_face)


class TestLandmarkDetector(unittest.TestCase):
    """Test cases for LandmarkDetector class"""

    @patch('landmark_detector.mp.solutions')
    def test_initialization_with_both(self, mock_mp):
        """Test LandmarkDetector initialization with both hands and face detection"""
        # Setup mocks
        mock_mp.hands = Mock()
        mock_mp.face_mesh = Mock()
        mock_hands_instance = Mock()
        mock_face_instance = Mock()
        mock_mp.hands.Hands.return_value = mock_hands_instance
        mock_mp.face_mesh.FaceMesh.return_value = mock_face_instance

        detector = LandmarkDetector(
            detect_hands=True,
            detect_face=True,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.assertTrue(detector.detect_hands)
        self.assertTrue(detector.detect_face)
        self.assertIsNotNone(detector.hands)
        self.assertIsNotNone(detector.face_mesh)

    @patch('landmark_detector.mp.solutions')
    def test_initialization_hands_only(self, mock_mp):
        """Test LandmarkDetector initialization with hands only"""
        mock_mp.hands = Mock()
        mock_hands_instance = Mock()
        mock_mp.hands.Hands.return_value = mock_hands_instance

        detector = LandmarkDetector(
            detect_hands=True,
            detect_face=False
        )

        self.assertTrue(detector.detect_hands)
        self.assertFalse(detector.detect_face)
        self.assertIsNotNone(detector.hands)
        self.assertIsNone(detector.face_mesh)

    @patch('landmark_detector.mp.solutions')
    def test_initialization_face_only(self, mock_mp):
        """Test LandmarkDetector initialization with face only"""
        mock_mp.face_mesh = Mock()
        mock_face_instance = Mock()
        mock_mp.face_mesh.FaceMesh.return_value = mock_face_instance

        detector = LandmarkDetector(
            detect_hands=False,
            detect_face=True
        )

        self.assertFalse(detector.detect_hands)
        self.assertTrue(detector.detect_face)
        self.assertIsNone(detector.hands)
        self.assertIsNotNone(detector.face_mesh)

    @patch('landmark_detector.mp.solutions')
    def test_initialization_neither(self, mock_mp):
        """Test LandmarkDetector initialization with neither hands nor face"""
        detector = LandmarkDetector(
            detect_hands=False,
            detect_face=False
        )

        self.assertFalse(detector.detect_hands)
        self.assertFalse(detector.detect_face)
        self.assertIsNone(detector.hands)
        self.assertIsNone(detector.face_mesh)

    @patch('landmark_detector.mp.solutions')
    def test_initialization_with_custom_parameters(self, mock_mp):
        """Test LandmarkDetector initialization with custom parameters"""
        mock_mp.hands = Mock()
        mock_mp.face_mesh = Mock()
        mock_hands_instance = Mock()
        mock_face_instance = Mock()
        mock_mp.hands.Hands.return_value = mock_hands_instance
        mock_mp.face_mesh.FaceMesh.return_value = mock_face_instance

        detector = LandmarkDetector(
            detect_hands=True,
            detect_face=True,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6
        )

        # Verify Hands was called with correct parameters
        mock_mp.hands.Hands.assert_called_once_with(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6
        )

        # Verify FaceMesh was called with correct parameters
        mock_mp.face_mesh.FaceMesh.assert_called_once_with(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6
        )

    @patch('landmark_detector.mp.solutions')
    def test_detect_landmarks_with_hands(self, mock_mp):
        """Test landmark detection with hand landmarks"""
        # Setup
        mock_mp.hands = Mock()
        mock_hands_instance = Mock()
        mock_mp.hands.Hands.return_value = mock_hands_instance

        # Create mock hand detection results
        mock_hand_landmarks = Mock()
        mock_hand_results = Mock()
        mock_hand_results.multi_hand_landmarks = [mock_hand_landmarks]

        # Create mock handedness
        mock_classification = Mock()
        mock_classification.label = 'Right'
        mock_handedness = Mock()
        mock_handedness.classification = [mock_classification]
        mock_hand_results.multi_handedness = [mock_handedness]

        mock_hands_instance.process.return_value = mock_hand_results

        detector = LandmarkDetector(detect_hands=True, detect_face=False)

        # Create dummy image
        image = np.zeros((100, 100, 3), dtype=np.uint8)

        # Test
        results = detector.detect_landmarks(image)

        # Verify
        self.assertIsNotNone(results.hands)
        self.assertIsNone(results.face)
        self.assertIn('Right', results.hands.landmarks)
        mock_hands_instance.process.assert_called_once()

    @patch('landmark_detector.mp.solutions')
    def test_detect_landmarks_with_face(self, mock_mp):
        """Test landmark detection with face landmarks"""
        # Setup
        mock_mp.face_mesh = Mock()
        mock_face_instance = Mock()
        mock_mp.face_mesh.FaceMesh.return_value = mock_face_instance

        # Create mock face detection results
        mock_face_landmarks = Mock()
        mock_face_results = Mock()
        mock_face_results.multi_face_landmarks = [mock_face_landmarks]

        mock_face_instance.process.return_value = mock_face_results

        detector = LandmarkDetector(detect_hands=False, detect_face=True)

        # Create dummy image
        image = np.zeros((100, 100, 3), dtype=np.uint8)

        # Test
        results = detector.detect_landmarks(image)

        # Verify
        self.assertIsNone(results.hands)
        self.assertIsNotNone(results.face)
        self.assertEqual(results.face.landmarks, mock_face_landmarks)
        mock_face_instance.process.assert_called_once()

    @patch('landmark_detector.mp.solutions')
    def test_detect_landmarks_with_both(self, mock_mp):
        """Test landmark detection with both hands and face"""
        # Setup mocks
        mock_mp.hands = Mock()
        mock_mp.face_mesh = Mock()
        mock_hands_instance = Mock()
        mock_face_instance = Mock()
        mock_mp.hands.Hands.return_value = mock_hands_instance
        mock_mp.face_mesh.FaceMesh.return_value = mock_face_instance

        # Create mock hand results
        mock_hand_landmarks = Mock()
        mock_hand_results = Mock()
        mock_hand_results.multi_hand_landmarks = [mock_hand_landmarks]
        mock_classification = Mock()
        mock_classification.label = 'Left'
        mock_handedness = Mock()
        mock_handedness.classification = [mock_classification]
        mock_hand_results.multi_handedness = [mock_handedness]
        mock_hands_instance.process.return_value = mock_hand_results

        # Create mock face results
        mock_face_landmarks = Mock()
        mock_face_results = Mock()
        mock_face_results.multi_face_landmarks = [mock_face_landmarks]
        mock_face_instance.process.return_value = mock_face_results

        detector = LandmarkDetector(detect_hands=True, detect_face=True)

        # Create dummy image
        image = np.zeros((100, 100, 3), dtype=np.uint8)

        # Test
        results = detector.detect_landmarks(image)

        # Verify
        self.assertIsNotNone(results.hands)
        self.assertIsNotNone(results.face)
        self.assertIn('Left', results.hands.landmarks)

    @patch('landmark_detector.mp.solutions')
    def test_detect_landmarks_no_detections(self, mock_mp):
        """Test landmark detection with no detections"""
        # Setup
        mock_mp.hands = Mock()
        mock_mp.face_mesh = Mock()
        mock_hands_instance = Mock()
        mock_face_instance = Mock()
        mock_mp.hands.Hands.return_value = mock_hands_instance
        mock_mp.face_mesh.FaceMesh.return_value = mock_face_instance

        # No detections
        mock_hand_results = Mock()
        mock_hand_results.multi_hand_landmarks = None
        mock_hands_instance.process.return_value = mock_hand_results

        mock_face_results = Mock()
        mock_face_results.multi_face_landmarks = None
        mock_face_instance.process.return_value = mock_face_results

        detector = LandmarkDetector(detect_hands=True, detect_face=True)

        # Create dummy image
        image = np.zeros((100, 100, 3), dtype=np.uint8)

        # Test
        results = detector.detect_landmarks(image)

        # Verify
        self.assertIsNone(results.hands)
        self.assertIsNone(results.face)

    @patch('landmark_detector.mp.solutions')
    def test_detect_landmarks_multiple_hands(self, mock_mp):
        """Test landmark detection with multiple hands"""
        # Setup
        mock_mp.hands = Mock()
        mock_hands_instance = Mock()
        mock_mp.hands.Hands.return_value = mock_hands_instance

        # Create mock for two hands
        mock_hand_left = Mock()
        mock_hand_right = Mock()
        mock_hand_results = Mock()
        mock_hand_results.multi_hand_landmarks = [mock_hand_left, mock_hand_right]

        # Create handedness for both hands
        mock_class_left = Mock()
        mock_class_left.label = 'Left'
        mock_handedness_left = Mock()
        mock_handedness_left.classification = [mock_class_left]

        mock_class_right = Mock()
        mock_class_right.label = 'Right'
        mock_handedness_right = Mock()
        mock_handedness_right.classification = [mock_class_right]

        mock_hand_results.multi_handedness = [mock_handedness_left, mock_handedness_right]
        mock_hands_instance.process.return_value = mock_hand_results

        detector = LandmarkDetector(detect_hands=True, detect_face=False, max_num_hands=2)

        # Create dummy image
        image = np.zeros((100, 100, 3), dtype=np.uint8)

        # Test
        results = detector.detect_landmarks(image)

        # Verify
        self.assertIsNotNone(results.hands)
        self.assertEqual(len(results.hands.landmarks), 2)
        self.assertIn('Left', results.hands.landmarks)
        self.assertIn('Right', results.hands.landmarks)

    @patch('landmark_detector.mp.solutions')
    def test_detect_landmarks_empty_face_list(self, mock_mp):
        """Test landmark detection with empty face landmarks list"""
        # Setup
        mock_mp.face_mesh = Mock()
        mock_face_instance = Mock()
        mock_mp.face_mesh.FaceMesh.return_value = mock_face_instance

        # Empty face landmarks list
        mock_face_results = Mock()
        mock_face_results.multi_face_landmarks = []
        mock_face_instance.process.return_value = mock_face_results

        detector = LandmarkDetector(detect_hands=False, detect_face=True)

        # Create dummy image
        image = np.zeros((100, 100, 3), dtype=np.uint8)

        # Test
        results = detector.detect_landmarks(image)

        # Verify - should be None because list is empty
        self.assertIsNone(results.face)

    @patch('landmark_detector.mp.solutions')
    def test_close_with_both(self, mock_mp):
        """Test closing detector with both hands and face"""
        # Setup
        mock_mp.hands = Mock()
        mock_mp.face_mesh = Mock()
        mock_hands_instance = Mock()
        mock_face_instance = Mock()
        mock_mp.hands.Hands.return_value = mock_hands_instance
        mock_mp.face_mesh.FaceMesh.return_value = mock_face_instance

        detector = LandmarkDetector(detect_hands=True, detect_face=True)

        # Test
        detector.close()

        # Verify
        mock_hands_instance.close.assert_called_once()
        mock_face_instance.close.assert_called_once()
        self.assertIsNone(detector.hands)
        self.assertIsNone(detector.face_mesh)

    @patch('landmark_detector.mp.solutions')
    def test_close_when_already_closed(self, mock_mp):
        """Test closing detector when already closed"""
        detector = LandmarkDetector(detect_hands=False, detect_face=False)

        # Should not raise any exception
        detector.close()

        self.assertIsNone(detector.hands)
        self.assertIsNone(detector.face_mesh)

    @patch('landmark_detector.mp.solutions')
    def test_close_hands_only(self, mock_mp):
        """Test closing detector with hands only"""
        mock_mp.hands = Mock()
        mock_hands_instance = Mock()
        mock_mp.hands.Hands.return_value = mock_hands_instance

        detector = LandmarkDetector(detect_hands=True, detect_face=False)
        detector.close()

        mock_hands_instance.close.assert_called_once()
        self.assertIsNone(detector.hands)


if __name__ == '__main__':
    unittest.main()
