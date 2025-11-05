"""
Landmark Detector Module
-------------------------
Detects hand and face landmarks using MediaPipe.
Provides a unified interface for landmark detection with result containers.

Key features:
- Hand landmark detection (up to 2 hands)
- Face mesh landmark detection
- Configurable detection and tracking confidence
- Structured result objects for easy access

Classes:
- HandsResults: Container for hand detection results
- FaceResults: Container for face detection results
- DetectionsResults: Combined container for all detections
- LandmarkDetector: Main detector class
"""

import mediapipe as mp


class HandsResults:
    """Container for hand detection results

    Attributes:
        landmarks (dict): Dictionary mapping hand side ('Left'/'Right') to landmarks
        mp_hands: MediaPipe hands solution instance
    """
    def __init__(self, landmarks: dict[str, any], mp_hands):
        self.landmarks = landmarks
        self.mp_hands = mp_hands


class FaceResults:
    """Container for face detection results

    Attributes:
        landmarks: MediaPipe face mesh landmarks
        mp_face: MediaPipe face mesh solution instance
    """
    def __init__(self, landmarks, mp_face):
        self.landmarks = landmarks
        self.mp_face = mp_face


class DetectionsResults:
    """Combined container for all detection results

    Attributes:
        hands (HandsResults | None): Hand detection results
        face (FaceResults | None): Face detection results
    """
    def __init__(self, hands: HandsResults | None, face: FaceResults | None):
        self.hands = hands
        self.face = face


class LandmarkDetector:
    """Main landmark detection class using MediaPipe

    Detects hand and face landmarks from images using MediaPipe solutions.
    """
    def __init__(
            self,
            detect_hands: bool = True,
            detect_face: bool = True,
            max_num_hands: int = 2,
            min_detection_confidence: float = 0.5,
            min_tracking_confidence: float = 0.5,):
        """Initialize the landmark detector

        Args:
            detect_hands (bool): Enable hand detection
            detect_face (bool): Enable face detection
            max_num_hands (int): Maximum number of hands to detect
            min_detection_confidence (float): Minimum confidence for detection
            min_tracking_confidence (float): Minimum confidence for tracking
        """
        self.detect_hands = detect_hands
        self.detect_face = detect_face

        self.mp_hands = mp.solutions.hands if detect_hands else None
        self.mp_face = mp.solutions.face_mesh if detect_face else None

        self.hands = None
        self.face_mesh = None

        if detect_hands:
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=max_num_hands,
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence
            )

        if detect_face:
            self.face_mesh = self.mp_face.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                refine_landmarks=False,
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence,
            )

    def detect_landmarks(self, image) -> DetectionsResults:
        """Detect landmarks in an image

        Args:
            image: RGB image array to process

        Returns:
            DetectionsResults: Combined detection results for hands and face
        """
        hands = None
        face = None
        if self.hands:
            hand_results = self.hands.process(image)
            landmarks = {}
            if hand_results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
                    hand_side = hand_results.multi_handedness[idx].classification[0].label
                    landmarks[hand_side] = hand_landmarks
                hands = HandsResults(landmarks, self.mp_hands)

        if self.face_mesh:
            face_results = self.face_mesh.process(image)
            if face_results.multi_face_landmarks and len(face_results.multi_face_landmarks) > 0:
                face = FaceResults(face_results.multi_face_landmarks[0], self.mp_face)

        return DetectionsResults(hands, face)

    def close(self):
        """Release MediaPipe resources"""
        if self.hands:
            self.hands.close()
            self.hands = None
        if self.face_mesh:
            self.face_mesh.close()
            self.face_mesh = None