"""
Unit tests for TrajectoryDetector module
"""

import unittest
from trajectory_detector import TrajectoryDetector


class TestTrajectoryDetector(unittest.TestCase):
    """Test cases for TrajectoryDetector class"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = TrajectoryDetector(movement_threshold=60)
        self.detector.set_screen_size(1920, 1080)

    def test_initialization(self):
        """Test TrajectoryDetector initialization"""
        self.assertEqual(self.detector.movement_threshold, 60)
        self.assertIsNone(self.detector.prev_x)
        self.assertIsNone(self.detector.prev_y)

    def test_set_screen_size(self):
        """Test setting screen size"""
        detector = TrajectoryDetector()
        detector.set_screen_size(1920, 1080)
        self.assertEqual(detector.screen_width, 1920)
        self.assertEqual(detector.screen_height, 1080)

    def test_detect_direction_without_screen_size(self):
        """Test direction detection without setting screen size"""
        detector = TrajectoryDetector()
        with self.assertRaises(ValueError):
            detector.detect_direction(0.5, 0.5)

    def test_detect_direction_first_call(self):
        """Test that first call returns None (no previous position)"""
        direction = self.detector.detect_direction(0.5, 0.5)
        self.assertIsNone(direction)

    def test_detect_direction_right(self):
        """Test detection of rightward movement"""
        # Set initial position
        self.detector.detect_direction(0.3, 0.5)
        # Move right significantly
        direction = self.detector.detect_direction(0.5, 0.5)
        self.assertEqual(direction, 'right')

    def test_detect_direction_left(self):
        """Test detection of leftward movement"""
        # Set initial position
        self.detector.detect_direction(0.5, 0.5)
        # Move left significantly
        direction = self.detector.detect_direction(0.3, 0.5)
        self.assertEqual(direction, 'left')

    def test_detect_direction_up(self):
        """Test detection of upward movement"""
        # Set initial position
        self.detector.detect_direction(0.5, 0.5)
        # Move up significantly
        direction = self.detector.detect_direction(0.5, 0.3)
        self.assertEqual(direction, 'up')

    def test_detect_direction_down(self):
        """Test detection of downward movement"""
        # Set initial position
        self.detector.detect_direction(0.5, 0.3)
        # Move down significantly
        direction = self.detector.detect_direction(0.5, 0.5)
        self.assertEqual(direction, 'down')

    def test_detect_direction_no_movement(self):
        """Test that small movements return None"""
        # Set initial position
        self.detector.detect_direction(0.5, 0.5)
        # Very small movement (below threshold)
        direction = self.detector.detect_direction(0.501, 0.501)
        self.assertIsNone(direction)

    def test_detect_direction_diagonal_horizontal_dominant(self):
        """Test diagonal movement where horizontal is dominant"""
        # Set initial position
        self.detector.detect_direction(0.3, 0.5)
        # Move diagonally with horizontal dominance
        direction = self.detector.detect_direction(0.6, 0.52)
        self.assertEqual(direction, 'right')

    def test_detect_direction_diagonal_vertical_dominant(self):
        """Test diagonal movement where vertical is dominant"""
        # Set initial position
        self.detector.detect_direction(0.5, 0.3)
        # Move diagonally with vertical dominance
        direction = self.detector.detect_direction(0.52, 0.6)
        self.assertEqual(direction, 'down')

    def test_reset_position(self):
        """Test position reset functionality"""
        # Set a position
        self.detector.detect_direction(0.5, 0.5)
        self.assertIsNotNone(self.detector.prev_x)
        self.assertIsNotNone(self.detector.prev_y)

        # Reset
        self.detector.reset_position()
        self.assertIsNone(self.detector.prev_x)
        self.assertIsNone(self.detector.prev_y)

    def test_custom_threshold(self):
        """Test with custom movement threshold"""
        detector = TrajectoryDetector(movement_threshold=100)
        detector.set_screen_size(1920, 1080)

        # Movement that would trigger default threshold but not custom
        detector.detect_direction(0.3, 0.5)
        direction = detector.detect_direction(0.35, 0.5)  # Small movement
        self.assertIsNone(direction)

        # Larger movement that exceeds custom threshold
        direction = detector.detect_direction(0.45, 0.5)
        self.assertEqual(direction, 'right')


if __name__ == '__main__':
    unittest.main()
