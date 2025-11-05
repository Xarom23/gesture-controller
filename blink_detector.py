from landmark_detector import FaceResults

class BlinkDetector:
    def __init__(self, ear_threshold=0.07):
        """Initialize the blink detector
        
        Args:
            ear_threshold (float): Eye Aspect Ratio threshold for blink detection
        """
        self.ear_threshold = ear_threshold
        
    def detect_left_eye_blink(self, face_landmarks: FaceResults) -> bool:
        """Detect if the left eye is blinking using Eye Aspect Ratio (EAR)

        Args:
            face_landmarks: MediaPipe face landmarks

        Returns:
            bool: True if left eye is blinking, False otherwise
        """
        if not face_landmarks:
            return False

        # Left eye indices in MediaPipe Face Mesh
        LEFT_EYE_INDICES = [
            362, 382, 381, 380, 374, 373, 390,  # Upper eyelid
            463, 398, 384, 385, 386, 387, 388,  # Lower eyelid
        ]

        # Get left eye landmarks
        left_eye_landmarks = [face_landmarks.landmarks.landmark[idx] for idx in LEFT_EYE_INDICES]

        # Calculate Eye Aspect Ratio (EAR)
        ear = self._calculate_ear(left_eye_landmarks)

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

        # Right eye indices in MediaPipe Face Mesh
        RIGHT_EYE_INDICES = [
            33, 160, 158, 133, 153, 144, 163,  # Upper eyelid
            263, 249, 390, 373, 374, 380, 381,  # Lower eyelid
        ]

        # Get right eye landmarks
        right_eye_landmarks = [face_landmarks.landmarks.landmark[idx] for idx in RIGHT_EYE_INDICES]

        # Calculate Eye Aspect Ratio (EAR)
        ear = self._calculate_ear(right_eye_landmarks)

        # Return True if eye is closed (EAR below threshold)
        return ear < self.ear_threshold
        
    def _calculate_ear(self, eye_landmarks) -> float:
        """Calculate the Eye Aspect Ratio (EAR) for blink detection
        
        The EAR is calculated using the formula:
        EAR = (|p2-p6| + |p3-p5|) / (2|p1-p4|)
        where p1-p6 are key points around the eye
        
        Args:
            eye_landmarks: List of landmarks for one eye
            
        Returns:
            float: The calculated Eye Aspect Ratio
        """
        # We'll use the vertical distances between the upper and lower eyelids
        # and the horizontal distance of the eye
        
        # Get vertical distances
        v1 = abs(eye_landmarks[1].y - eye_landmarks[8].y)  # Upper to lower lid
        v2 = abs(eye_landmarks[2].y - eye_landmarks[7].y)  # Upper to lower lid
        
        # Get horizontal distance
        h = abs(eye_landmarks[0].x - eye_landmarks[6].x)  # Eye width
        
        # Calculate EAR
        if h == 0:  # Prevent division by zero
            return 0
            
        ear = (v1 + v2) / (2.0 * h)
        return ear