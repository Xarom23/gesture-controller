import mediapipe as mp

class HandsResults:
    def __init__(self, landmarks: dict[str, any], mp_hands):
        self.landmarks = landmarks
        self.mp_hands = mp_hands

class FaceResults:
    def __init__(self, landmarks, mp_face):
        self.landmarks = landmarks
        self.mp_face = mp_face

class DetectionsResults:
    def __init__(self, hands: HandsResults | None, face: FaceResults | None):
        self.hands = hands
        self.face = face

class LandmarkDetector:
    def __init__(
            self,
            detect_hands: bool = True,
            detect_face: bool = True,
            max_num_hands: int = 2,
            min_detection_confidence: float = 0.5,
            min_tracking_confidence: float = 0.5,):
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
            face_landmarks_dict = {}
            if face_results.multi_face_landmarks:
                for idx, face_landmark in enumerate(face_results.multi_face_landmarks):
                    face_landmarks_dict[idx] = face_landmark
            face = FaceResults(face_landmarks_dict, self.mp_face)

        return DetectionsResults(hands, face)

    def close(self):
        if self.hands:
            self.hands.close()
            self.hands = None
        if self.face_mesh:
            self.face_mesh.close()
            self.face_mesh = None