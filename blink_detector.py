"""
Blink Detector Module
---------------------
Detects eye blinks using Eye Aspect Ratio (EAR) calculation from facial landmarks.
Uses MediaPipe face mesh landmarks to determine if eyes are open or closed.

Key features:
- Individual left and right eye blink detection
- EAR-based algorithm for reliable blink detection
- Configurable threshold for sensitivity adjustment (default: 0.40)
- Uses 6 key landmarks per eye for accurate EAR calculation

Algorithm:
The Eye Aspect Ratio (EAR) is calculated as:
    EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)

Where:
    - p1, p4: Horizontal corners of the eye
    - p2, p3, p5, p6: Vertical landmarks on upper and lower eyelids
    - Vertical distances (v1, v2) measure eyelid separation
    - Horizontal distance (h) measures eye width

Eye Landmarks Used:
    - Right Eye: [33, 159, 158, 133, 153, 145]
    - Left Eye: [362, 380, 374, 263, 386, 385]

Detection Logic:
- When the eye is open, EAR is relatively constant (~0.5-0.6)
- When blinking, EAR drops significantly below the threshold (~0.2-0.3)
- Current threshold: 0.40 (optimized for balanced detection)
"""

from landmark_detector import FaceResults
import numpy as np


class BlinkDetector:
    """Detects eye blinks using Eye Aspect Ratio (EAR) calculation

    This class implements a robust blink detection algorithm based on the
    Eye Aspect Ratio method, which analyzes the geometric relationship between
    vertical and horizontal eye distances to determine blink events.

    Attributes:
        ear_threshold (float): Threshold below which an eye is considered closed
        RIGHT_EYE_EAR (list): MediaPipe landmark indices for right eye EAR calculation
        LEFT_EYE_EAR (list): MediaPipe landmark indices for left eye EAR calculation

    Usage:
        detector = BlinkDetector(ear_threshold=0.40)
        is_blinking = detector.detect_left_eye_blink(face_landmarks)
    """
    def __init__(self, ear_threshold=0.40):
        """Initialize the blink detector with configurable threshold

        Args:
            ear_threshold (float): Eye Aspect Ratio threshold for blink detection.
                Default is 0.40. Lower values = less sensitive (fewer detections),
                Higher values = more sensitive (more detections).
                Typical range: 0.30 - 0.50
        """
        self.ear_threshold = ear_threshold
        # MediaPipe Face Mesh landmark indices for EAR calculation
        # Indices correspond to: [horizontal_left, vertical_top1, vertical_top2,
        #                         horizontal_right, vertical_bottom2, vertical_bottom1]
        self.RIGHT_EYE_EAR = [33, 159, 158, 133, 153, 145]
        self.LEFT_EYE_EAR = [362, 380, 374, 263, 386, 385]
        
    def detect_left_eye_blink(self, face_landmarks: FaceResults) -> bool:
        """Detect if the left eye is blinking using Eye Aspect Ratio (EAR)

        Args:
            face_landmarks: MediaPipe face landmarks

        Returns:
            bool: True if left eye is blinking, False otherwise
        """
        if not face_landmarks:
            return False

        # Calculate Eye Aspect Ratio (EAR)
        ear = self._calculate_ear(self.LEFT_EYE_EAR, face_landmarks.landmarks)

        # Return True if eye is closed (EAR below threshold)
        return ear < self.ear_threshold

    def detect_right_eye_blink(self, face_landmarks: FaceResults) -> bool:
        """Detect if the right eye is blinking using Eye Aspect Ratio (EAR)

        Args:
            face_landmarks: MediaPipe face landmarks
        Returns:
            bool: True if right eye is blinking, False otherwise
        """
        if not face_landmarks:
            return False

        # Calculate Eye Aspect Ratio (EAR)
        ear = self._calculate_ear(self.RIGHT_EYE_EAR, face_landmarks.landmarks)

        # Return True if eye is closed (EAR below threshold)
        return ear < self.ear_threshold
        
    def _calculate_ear(self, eye_landmarks, landmarks) -> float:
        """Calculate the Eye Aspect Ratio (EAR) for blink detection

        The EAR is calculated using the Euclidean distance formula:
            EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)

        Where:
            - p1, p4 (indices 0, 3): Horizontal corners of the eye
            - p2, p3 (indices 1, 2): Upper eyelid vertical points
            - p5, p6 (indices 4, 5): Lower eyelid vertical points
            - || || denotes Euclidean distance (np.linalg.norm)

        The ratio measures how "open" the eye is by comparing vertical
        distances (eyelid separation) to horizontal distance (eye width).

        Args:
            eye_landmarks (list): List of 6 MediaPipe landmark indices for one eye.
                Order: [horizontal_left, vertical_top1, vertical_top2,
                        horizontal_right, vertical_bottom2, vertical_bottom1]
            landmarks (NormalizedLandmarkList): MediaPipe face mesh landmarks object
                containing all 478 facial landmarks with x, y, z coordinates

        Returns:
            float: The calculated Eye Aspect Ratio (typically 0.2-0.6).
                Returns 0 if horizontal distance is 0 (prevents division by zero)

        Example:
            >>> ear = detector._calculate_ear([33, 159, 158, 133, 153, 145], face_landmarks)
            >>> print(ear)  # e.g., 0.52 (eye open) or 0.18 (eye closed)
        """
        # Convert MediaPipe landmarks to numpy arrays for distance calculation
        def get_landmark_point(idx):
            """Extract 3D coordinates of a specific landmark"""
            lm = landmarks.landmark[idx]
            return np.array([lm.x, lm.y, lm.z])

        # Get vertical distances
        v1 = np.linalg.norm(get_landmark_point(eye_landmarks[1]) -
                           get_landmark_point(eye_landmarks[5]))  # Upper to lower lid
        v2 = np.linalg.norm(get_landmark_point(eye_landmarks[2]) -
                           get_landmark_point(eye_landmarks[4]))  # Upper to lower lid

        # Get horizontal distance
        h = np.linalg.norm(get_landmark_point(eye_landmarks[0]) -
                          get_landmark_point(eye_landmarks[3]))  # Eye width

        # Calculate EAR
        if h == 0:  # Prevent division by zero
            return 0

        ear = (v1 + v2) / (2.0 * h)
        return ear