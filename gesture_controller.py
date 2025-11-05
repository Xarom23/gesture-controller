from landmark_detector import HandsResults, FaceResults
from mouse_simulator import MouseSimulator
from keyboard_simulator import KeyboardSimulator
from trajectory_detector import TrajectoryDetector
from blink_detector import BlinkDetector
import pyautogui
import json
import os

class GestureController:
    def __init__(self, movement_threshold=60, smoothing_factor=0.5, position_history_size=5):
        self.mouse_simulator = MouseSimulator(smoothing_factor, position_history_size)
        self.keyboard_simulator = KeyboardSimulator()
        self.trajectory_detector = TrajectoryDetector(movement_threshold)
        self.blink_detector = BlinkDetector()
        width, height = pyautogui.size()
        self.trajectory_detector.set_screen_size(width, height)

        # Configuration file tracking
        self.config_file = 'config.json'
        self.last_modified_time = None

        # Load configuration from config.json
        self._load_config()

    def _load_config(self):
        """Load configuration from config.json file and update last modified time"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.left_hand_mode = config.get('left_hand_mode', 'keyboard')
                self.right_hand_mode = config.get('right_hand_mode', 'mouse')
                self.left_blink_mode = config.get('left_blink_mode', 'left_click')
                self.right_blink_mode = config.get('right_blink_mode', 'right_click')

            # Update last modified time
            self.last_modified_time = os.path.getmtime(self.config_file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Use default configuration if file doesn't exist or is invalid
            self.left_hand_mode = 'keyboard'
            self.right_hand_mode = 'mouse'
            self.left_blink_mode = 'left_click'
            self.right_blink_mode = 'right_click'
            self.last_modified_time = None

    def _check_config_changes(self):
        """Check if config.json has been modified and reload if necessary"""
        try:
            current_modified_time = os.path.getmtime(self.config_file)
            if self.last_modified_time is None or current_modified_time > self.last_modified_time:
                self._load_config()
        except FileNotFoundError:
            pass

    def process_gestures(self, hand_results: HandsResults | None, face_landmarks: FaceResults | None):
        """Process detected hand and face landmarks and perform corresponding actions

        Args:
            hand_results: HandsResults object containing detected hand landmarks
            face_landmarks: Optional MediaPipe face landmarks for blink detection
            mp_face_mesh: Optional MediaPipe face mesh solution instance
        """
        # Check for configuration changes before processing
        self._check_config_changes()

        # Process face landmarks for blink detection if available
        if face_landmarks and face_landmarks.landmarks:
            # Detect left eye blink
            left_eye_blinked = self.blink_detector.detect_left_eye_blink(face_landmarks)
            right_eye_blinked = self.blink_detector.detect_right_eye_blink(face_landmarks)
            
            if left_eye_blinked and not right_eye_blinked:
                if self.left_blink_mode == 'left_click':
                    self.mouse_simulator.perform_left_click()
                elif self.left_blink_mode == 'right_click':
                    self.mouse_simulator.perform_right_click()

            # Detect right eye blink
            if right_eye_blinked and not left_eye_blinked:
                if self.right_blink_mode == 'right_click':
                    self.mouse_simulator.perform_right_click()
                elif self.right_blink_mode == 'left_click':
                    self.mouse_simulator.perform_left_click()
        
        # Process hand landmarks if available
        if hand_results and hand_results.landmarks:
            for hand_side, hand_landmarks in hand_results.landmarks.items():
                if hand_side == 'Right':
                    # Check configuration for right hand mode
                    if self.right_hand_mode == 'mouse':
                        self._process_hand_for_mouse(hand_landmarks, hand_results.mp_hands)
                    elif self.right_hand_mode == 'keyboard':
                        self._process_hand_for_keyboard(hand_landmarks, hand_results.mp_hands)
                elif hand_side == 'Left':
                    # Check configuration for left hand mode
                    if self.left_hand_mode == 'keyboard':
                        self._process_hand_for_keyboard(hand_landmarks, hand_results.mp_hands)
                    elif self.left_hand_mode == 'mouse':
                        self._process_hand_for_mouse(hand_landmarks, hand_results.mp_hands)
                
    def _process_hand_for_mouse(self, hand_landmarks, mp_hands):
        """Process hand gestures for mouse control

        Args:
            hand_landmarks: MediaPipe hand landmarks
            mp_hands: MediaPipe hands solution instance
        """
        # Get middle finger MCP (for cursor control) coordinates
        mx, my = self._get_landmark_coords(hand_landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_MCP)

        # Move cursor based on middle finger position
        self.mouse_simulator.move_cursor(mx, my)

    def _process_hand_for_keyboard(self, hand_landmarks, mp_hands):
        """Process hand gestures for directional controls

        Args:
            hand_landmarks: MediaPipe hand landmarks
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