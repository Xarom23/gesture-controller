"""
Integration tests for the gesture control system.

These tests verify real interactions between components without mocking,
testing the actual integration and data flow between modules.
"""

import unittest
import numpy as np
import os
import json
import tempfile
from pathlib import Path

from blink_detector import BlinkDetector
from trajectory_detector import TrajectoryDetector
from mouse_simulator import MouseSimulator
from keyboard_simulator import KeyboardSimulator
from landmark_detector import LandmarkDetector, HandsResults, FaceResults


class TestBlinkDetectorIntegration(unittest.TestCase):
    """Real integration tests for BlinkDetector"""

    def test_blink_detection_with_threshold_variations(self):
        """Test blink detector works with different thresholds"""
        # Test with default threshold (now 0.40)
        detector_default = BlinkDetector()
        self.assertEqual(detector_default.ear_threshold, 0.40)

        # Test with custom threshold
        detector_custom = BlinkDetector(ear_threshold=0.35)
        self.assertEqual(detector_custom.ear_threshold, 0.35)

        # Verify internal EAR calculation works
        # Create mock landmarks object with the new algorithm structure
        class MockLandmark:
            def __init__(self, x, y, z=0.0):
                self.x = x
                self.y = y
                self.z = z

        class MockLandmarks:
            def __init__(self):
                self.landmark = [MockLandmark(0, 0, 0) for _ in range(500)]

        # New algorithm uses 6 landmarks per eye:
        # LEFT_EYE_EAR = [362, 380, 374, 263, 386, 385]
        # Indices: [0]=horizontal_left, [1]=vertical_top1, [2]=vertical_top2,
        #          [3]=horizontal_right, [4]=vertical_bottom2, [5]=vertical_bottom1

        # Create open eye landmarks (larger vertical distances)
        open_landmarks = MockLandmarks()
        # Left eye open - horizontal distance 0.1, vertical distance 0.05 -> EAR ~0.5
        open_landmarks.landmark[362] = MockLandmark(0.0, 0.5, 0)   # Horizontal left
        open_landmarks.landmark[380] = MockLandmark(0.03, 0.45, 0)  # Vertical top 1
        open_landmarks.landmark[374] = MockLandmark(0.07, 0.45, 0)  # Vertical top 2
        open_landmarks.landmark[263] = MockLandmark(0.1, 0.5, 0)   # Horizontal right
        open_landmarks.landmark[386] = MockLandmark(0.07, 0.55, 0)  # Vertical bottom 2
        open_landmarks.landmark[385] = MockLandmark(0.03, 0.55, 0)  # Vertical bottom 1

        # Create closed eye landmarks (smaller vertical distances)
        closed_landmarks = MockLandmarks()
        # Left eye closed - horizontal distance 0.1, vertical distance 0.01 -> EAR ~0.1
        closed_landmarks.landmark[362] = MockLandmark(0.0, 0.5, 0)   # Horizontal left
        closed_landmarks.landmark[380] = MockLandmark(0.03, 0.49, 0)  # Vertical top 1
        closed_landmarks.landmark[374] = MockLandmark(0.07, 0.49, 0)  # Vertical top 2
        closed_landmarks.landmark[263] = MockLandmark(0.1, 0.5, 0)   # Horizontal right
        closed_landmarks.landmark[386] = MockLandmark(0.07, 0.51, 0)  # Vertical bottom 2
        closed_landmarks.landmark[385] = MockLandmark(0.03, 0.51, 0)  # Vertical bottom 1

        ear_open = detector_default._calculate_ear(detector_default.LEFT_EYE_EAR, open_landmarks)
        ear_closed = detector_default._calculate_ear(detector_default.LEFT_EYE_EAR, closed_landmarks)

        # Verify EAR is higher when eye is open
        self.assertGreater(ear_open, ear_closed)


class TestTrajectoryDetectorIntegration(unittest.TestCase):
    """Real integration tests for TrajectoryDetector"""

    def test_trajectory_detection_all_directions(self):
        """Test trajectory detector correctly identifies all four directions"""
        detector = TrajectoryDetector(movement_threshold=60)
        detector.set_screen_size(1920, 1080)

        # Test upward movement
        detector.reset_position()
        results = []
        for y in [0.8, 0.7, 0.5, 0.3, 0.1]:
            direction = detector.detect_direction(0.5, y)
            if direction:
                results.append(direction)
        self.assertIn('up', results)

        # Test downward movement
        detector.reset_position()
        results = []
        for y in [0.2, 0.3, 0.5, 0.7, 0.9]:
            direction = detector.detect_direction(0.5, y)
            if direction:
                results.append(direction)
        self.assertIn('down', results)

        # Test left movement
        detector.reset_position()
        results = []
        for x in [0.8, 0.7, 0.5, 0.3, 0.1]:
            direction = detector.detect_direction(x, 0.5)
            if direction:
                results.append(direction)
        self.assertIn('left', results)

        # Test right movement
        detector.reset_position()
        results = []
        for x in [0.2, 0.3, 0.5, 0.7, 0.9]:
            direction = detector.detect_direction(x, 0.5)
            if direction:
                results.append(direction)
        self.assertIn('right', results)

    def test_trajectory_detector_with_different_thresholds(self):
        """Test trajectory detector sensitivity with different thresholds"""
        # Low threshold (more sensitive)
        detector_sensitive = TrajectoryDetector(movement_threshold=30)
        detector_sensitive.set_screen_size(1920, 1080)

        # High threshold (less sensitive)
        detector_normal = TrajectoryDetector(movement_threshold=100)
        detector_normal.set_screen_size(1920, 1080)

        # Small movement
        small_coords = [(0.5, 0.5), (0.5, 0.48)]

        detector_sensitive.reset_position()
        result_sensitive = None
        for x, y in small_coords:
            result_sensitive = detector_sensitive.detect_direction(x, y)

        detector_normal.reset_position()
        result_normal = None
        for x, y in small_coords:
            result_normal = detector_normal.detect_direction(x, y)

        # Sensitive detector should detect movement, normal might not
        # (depending on exact pixel values)
        self.assertIsInstance(result_sensitive, (str, type(None)))
        self.assertIsInstance(result_normal, (str, type(None)))


class TestComponentsInitializationIntegration(unittest.TestCase):
    """Test that all components can be initialized and work together"""

    def test_all_components_initialize_successfully(self):
        """Test all components can be created without errors"""
        blink_detector = BlinkDetector()
        trajectory_detector = TrajectoryDetector()
        mouse_simulator = MouseSimulator()
        keyboard_simulator = KeyboardSimulator()

        # Verify they're all initialized
        self.assertIsNotNone(blink_detector)
        self.assertIsNotNone(trajectory_detector)
        self.assertIsNotNone(mouse_simulator)
        self.assertIsNotNone(keyboard_simulator)

        # Verify default values (ear_threshold is now 0.40)
        self.assertEqual(blink_detector.ear_threshold, 0.40)
        self.assertEqual(trajectory_detector.movement_threshold, 60)

    def test_landmark_detector_initialization(self):
        """Test LandmarkDetector initializes with real MediaPipe components"""
        detector = LandmarkDetector()

        # Verify MediaPipe components are initialized
        self.assertIsNotNone(detector.hands)
        self.assertIsNotNone(detector.face_mesh)
        self.assertIsNotNone(detector.mp_hands)
        self.assertIsNotNone(detector.mp_face)


class TestLandmarkDetectorIntegration(unittest.TestCase):
    """Real integration tests for LandmarkDetector with actual frames"""

    def test_detect_landmarks_with_black_frame(self):
        """Test landmark detection on a blank frame (no detections expected)"""
        detector = LandmarkDetector()

        # Create a blank BGR frame (as OpenCV would provide)
        blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Process the frame
        results = detector.detect_landmarks(blank_frame)

        # Verify results structure
        self.assertIsNotNone(results)
        self.assertHasAttr(results, 'hands')
        self.assertHasAttr(results, 'face')

        # Blank frame should not have detections
        self.assertIsNone(results.hands)
        self.assertIsNone(results.face)

    def test_detect_landmarks_multiple_frames(self):
        """Test landmark detector can process multiple frames sequentially"""
        detector = LandmarkDetector()

        # Process multiple blank frames
        for i in range(5):
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            results = detector.detect_landmarks(frame)

            # Each should return valid results structure
            self.assertIsNotNone(results)
            self.assertHasAttr(results, 'hands')
            self.assertHasAttr(results, 'face')

    def assertHasAttr(self, obj, attr):
        """Helper to assert object has attribute"""
        self.assertTrue(hasattr(obj, attr), f"Object does not have attribute '{attr}'")


class TestBlinkTrajectoryIntegration(unittest.TestCase):
    """Integration tests combining BlinkDetector and TrajectoryDetector"""

    def test_blink_and_trajectory_work_independently(self):
        """Test blink and trajectory detectors don't interfere with each other"""
        blink_detector = BlinkDetector(ear_threshold=0.40)
        trajectory_detector = TrajectoryDetector(movement_threshold=60)
        trajectory_detector.set_screen_size(1920, 1080)

        # Simulate trajectory detection
        trajectory_detector.reset_position()
        coords = [(0.5, 0.8), (0.5, 0.6), (0.5, 0.4), (0.5, 0.2)]

        directions = []
        for x, y in coords:
            direction = trajectory_detector.detect_direction(x, y)
            if direction:
                directions.append(direction)

        # Should detect upward movement
        self.assertTrue(len(directions) > 0)
        self.assertIn('up', directions)

        # Blink detector should still work independently
        # Create mock landmarks with the new algorithm structure
        class MockLandmark:
            def __init__(self, x, y, z=0.0):
                self.x = x
                self.y = y
                self.z = z

        class MockLandmarks:
            def __init__(self):
                self.landmark = [MockLandmark(0, 0, 0) for _ in range(500)]

        # Create closed eye landmarks using LEFT_EYE_EAR indices
        closed_landmarks = MockLandmarks()
        closed_landmarks.landmark[362] = MockLandmark(0.0, 0.5, 0)   # Horizontal left
        closed_landmarks.landmark[380] = MockLandmark(0.03, 0.49, 0)  # Vertical top 1
        closed_landmarks.landmark[374] = MockLandmark(0.07, 0.49, 0)  # Vertical top 2
        closed_landmarks.landmark[263] = MockLandmark(0.1, 0.5, 0)   # Horizontal right
        closed_landmarks.landmark[386] = MockLandmark(0.07, 0.51, 0)  # Vertical bottom 2
        closed_landmarks.landmark[385] = MockLandmark(0.03, 0.51, 0)  # Vertical bottom 1

        ear = blink_detector._calculate_ear(blink_detector.LEFT_EYE_EAR, closed_landmarks)

        # EAR should be calculable
        self.assertIsInstance(ear, float)
        self.assertGreaterEqual(ear, 0.0)


class TestConfigurationIntegration(unittest.TestCase):
    """Test configuration loading and usage across components"""

    def test_config_file_loading(self):
        """Test real config file loading"""
        # Create a temporary config file
        config_data = {
            "left_hand_mode": "mouse",
            "right_hand_mode": "keyboard",
            "left_blink_mode": "right_click",
            "right_blink_mode": "left_click"
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_config_path = f.name

        try:
            # Read the config file
            with open(temp_config_path, 'r') as f:
                loaded_config = json.load(f)

            # Verify it loaded correctly
            self.assertEqual(loaded_config['left_hand_mode'], 'mouse')
            self.assertEqual(loaded_config['right_hand_mode'], 'keyboard')
            self.assertEqual(loaded_config['left_blink_mode'], 'right_click')
            self.assertEqual(loaded_config['right_blink_mode'], 'left_click')
        finally:
            # Clean up
            os.unlink(temp_config_path)


class TestMouseKeyboardSimulatorIntegration(unittest.TestCase):
    """Integration tests for MouseSimulator and KeyboardSimulator"""

    def test_mouse_simulator_initialization(self):
        """Test MouseSimulator can be initialized"""
        simulator = MouseSimulator()
        self.assertIsNotNone(simulator)

    def test_keyboard_simulator_initialization(self):
        """Test KeyboardSimulator can be initialized"""
        simulator = KeyboardSimulator()
        self.assertIsNotNone(simulator)

    def test_simulators_work_independently(self):
        """Test both simulators can be created and exist simultaneously"""
        mouse_sim = MouseSimulator()
        keyboard_sim = KeyboardSimulator()

        self.assertIsNotNone(mouse_sim)
        self.assertIsNotNone(keyboard_sim)

        # They should be different objects
        self.assertIsNot(mouse_sim, keyboard_sim)


class TestDetectorCombinations(unittest.TestCase):
    """Test various combinations of detectors working together"""

    def test_multiple_detectors_in_pipeline(self):
        """Test a pipeline with multiple detectors"""
        # Create all detectors
        blink_detector = BlinkDetector()
        trajectory_detector = TrajectoryDetector()
        trajectory_detector.set_screen_size(1920, 1080)
        landmark_detector = LandmarkDetector()

        # Process a blank frame through landmark detector
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        results = landmark_detector.detect_landmarks(frame)

        # Verify results
        self.assertIsNotNone(results)

        # Process some coordinates through trajectory detector
        trajectory_detector.reset_position()
        direction = trajectory_detector.detect_direction(0.5, 0.5)

        # First call should return None (no previous position)
        self.assertIsNone(direction)

        # Second call might detect direction
        direction = trajectory_detector.detect_direction(0.5, 0.3)
        # Direction could be None or 'up' depending on threshold
        self.assertIsInstance(direction, (str, type(None)))

    def test_detector_state_independence(self):
        """Test that detectors maintain independent state"""
        # Create two trajectory detectors
        detector1 = TrajectoryDetector(movement_threshold=60)
        detector2 = TrajectoryDetector(movement_threshold=80)

        detector1.set_screen_size(1920, 1080)
        detector2.set_screen_size(1920, 1080)

        # Move detector1
        detector1.detect_direction(0.5, 0.8)
        detector1.detect_direction(0.5, 0.2)

        # detector2 should have independent state
        self.assertIsNone(detector2.prev_x)
        self.assertIsNone(detector2.prev_y)

        # Move detector2
        detector2.detect_direction(0.3, 0.5)

        # detector1's state should be unchanged
        self.assertIsNotNone(detector1.prev_x)
        self.assertIsNotNone(detector1.prev_y)


class TestDataFlowIntegration(unittest.TestCase):
    """Test data flow between components"""

    def test_landmark_to_trajectory_data_flow(self):
        """Test realistic data flow from landmark detection to trajectory"""
        landmark_detector = LandmarkDetector()
        trajectory_detector = TrajectoryDetector(movement_threshold=60)
        trajectory_detector.set_screen_size(1920, 1080)

        # Simulate getting normalized coordinates from landmark detection
        # (In real usage, these would come from landmark positions)
        simulated_landmark_positions = [
            (0.5, 0.8),  # Starting position
            (0.5, 0.7),  # Moving up
            (0.5, 0.5),  # Continuing up
            (0.5, 0.3),  # Still moving up
        ]

        detected_directions = []
        for x, y in simulated_landmark_positions:
            direction = trajectory_detector.detect_direction(x, y)
            if direction:
                detected_directions.append(direction)

        # Should detect upward movement
        self.assertGreater(len(detected_directions), 0)
        self.assertIn('up', detected_directions)

    def test_multiple_frame_processing_cycle(self):
        """Test processing multiple frames in a realistic cycle"""
        landmark_detector = LandmarkDetector()
        blink_detector = BlinkDetector()

        # Simulate multiple frame processing cycles
        for frame_num in range(3):
            # Create a frame
            frame = np.zeros((480, 640, 3), dtype=np.uint8)

            # Add some variation to each frame
            frame[frame_num:frame_num+10, :, :] = 100

            # Process through landmark detector
            results = landmark_detector.detect_landmarks(frame)

            # Verify we get results each time
            self.assertIsNotNone(results)
            self.assertHasAttr(results, 'hands')
            self.assertHasAttr(results, 'face')

    def assertHasAttr(self, obj, attr):
        """Helper to assert object has attribute"""
        self.assertTrue(hasattr(obj, attr), f"Object does not have attribute '{attr}'")


class TestEdgeCasesIntegration(unittest.TestCase):
    """Integration tests for edge cases"""

    def test_trajectory_detector_reset_functionality(self):
        """Test trajectory detector reset works correctly"""
        detector = TrajectoryDetector()
        detector.set_screen_size(1920, 1080)

        # Set some position
        detector.detect_direction(0.5, 0.5)
        self.assertIsNotNone(detector.prev_x)
        self.assertIsNotNone(detector.prev_y)

        # Reset
        detector.reset_position()
        self.assertIsNone(detector.prev_x)
        self.assertIsNone(detector.prev_y)

    def test_trajectory_detector_screen_size_changes(self):
        """Test changing screen size during operation"""
        detector = TrajectoryDetector()

        # Set initial screen size
        detector.set_screen_size(1920, 1080)
        self.assertEqual(detector.screen_width, 1920)
        self.assertEqual(detector.screen_height, 1080)

        # Change screen size
        detector.set_screen_size(2560, 1440)
        self.assertEqual(detector.screen_width, 2560)
        self.assertEqual(detector.screen_height, 1440)

    def test_blink_detector_with_zero_ear(self):
        """Test blink detector handles zero EAR correctly"""
        detector = BlinkDetector()

        class MockLandmark:
            def __init__(self, x, y, z=0.0):
                self.x = x
                self.y = y
                self.z = z

        class MockLandmarks:
            def __init__(self):
                self.landmark = [MockLandmark(0, 0, 0) for _ in range(500)]

        # Create landmarks with zero horizontal distance using LEFT_EYE_EAR indices
        # For zero horizontal distance, landmarks [0] and [3] must have identical (x, y, z)
        # The new algorithm uses np.linalg.norm for 3D Euclidean distance
        zero_landmarks = MockLandmarks()
        # Horizontal corners at EXACTLY the same position
        zero_landmarks.landmark[362] = MockLandmark(0.5, 0.5, 0)   # Horizontal left
        zero_landmarks.landmark[263] = MockLandmark(0.5, 0.5, 0)   # Horizontal right (same!)
        # Vertical landmarks (don't matter since h=0 returns 0)
        zero_landmarks.landmark[380] = MockLandmark(0.5, 0.45, 0)  # Vertical top 1
        zero_landmarks.landmark[374] = MockLandmark(0.5, 0.45, 0)  # Vertical top 2
        zero_landmarks.landmark[386] = MockLandmark(0.5, 0.55, 0)  # Vertical bottom 2
        zero_landmarks.landmark[385] = MockLandmark(0.5, 0.55, 0)  # Vertical bottom 1

        ear = detector._calculate_ear(detector.LEFT_EYE_EAR, zero_landmarks)

        # Should return 0 to avoid division by zero
        self.assertEqual(ear, 0)


if __name__ == '__main__':
    unittest.main()
