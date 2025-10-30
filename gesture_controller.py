from landmark_detector import HandsResults
from mouse_simulator import MouseSimulator
from keyboard_simulator import KeyboardSimulator
from trajectory_detector import TrajectoryDetector
from blink_detector import BlinkDetector
import pyautogui

class GestureController:
    def __init__(self, movement_threshold=60, smoothing_factor=0.5, position_history_size=5):
        self.mouse_simulator = MouseSimulator(smoothing_factor, position_history_size)
        self.keyboard_simulator = KeyboardSimulator()
        self.trajectory_detector = TrajectoryDetector(movement_threshold)
        self.blink_detector = BlinkDetector()
        width, height = pyautogui.size()
        self.trajectory_detector.set_screen_size(width, height)
        
    def process_gestures(self, hand_results: HandsResults, face_landmarks=None, mp_face_mesh=None):
        """Process detected hand and face landmarks and perform corresponding actions
        
        Args:
            hand_results: HandsResults object containing detected hand landmarks
            face_landmarks: Optional MediaPipe face landmarks for blink detection
            mp_face_mesh: Optional MediaPipe face mesh solution instance
        """
        # Process face landmarks for blink detection if available
        if face_landmarks and mp_face_mesh:
            if self.blink_detector.detect_left_eye_blink(face_landmarks, mp_face_mesh):
                self.mouse_simulator.perform_left_click()
        
        # Process hand landmarks if available
        if hand_results and hand_results.landmarks:
            for hand_side, hand_landmarks in hand_results.landmarks.items():
                if hand_side == 'Right':
                    self._process_right_hand(hand_landmarks, hand_results.mp_hands)
                elif hand_side == 'Left':
                    self._process_left_hand(hand_landmarks, hand_results.mp_hands)
                
    def _process_right_hand(self, hand_landmarks, mp_hands):
        """Process right hand gestures for mouse control
        
        Args:
            hand_landmarks: MediaPipe hand landmarks for the right hand
            mp_hands: MediaPipe hands solution instance
        """
        # Get middle finger MCP (for cursor control) coordinates
        mx, my = self._get_landmark_coords(hand_landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_MCP)
        
        # Move cursor based on middle finger position
        self.mouse_simulator.move_cursor(mx, my)
            
    def _process_left_hand(self, hand_landmarks, mp_hands):
        """Process left hand gestures for directional controls
        
        Args:
            hand_landmarks: MediaPipe hand landmarks for the left hand
            mp_hands: MediaPipe hands solution instance
        """
        # Get index finger tip coordinates
        ix, iy = self._get_landmark_coords(hand_landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP)
        
        # Detect movement direction
        direction = self.trajectory_detector.detect_direction(ix, iy)
        
        # Press corresponding key if direction detected
        if direction:
            self.keyboard_simulator.press_key(direction)
        
    def _get_landmark_coords(self, landmarks, index):
        """Get the x, y coordinates of a specific landmark
        
        Args:
            landmarks: MediaPipe hand landmarks
            index: Index of the landmark to get coordinates for
            
        Returns:
            tuple: (x, y) coordinates of the landmark
        """
        lm = landmarks.landmark[index]
        return lm.x, lm.y