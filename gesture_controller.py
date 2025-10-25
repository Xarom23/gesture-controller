import pyautogui
from landmark_detector import HandsResults

class GestureController:
    def __init__(self, movement_threshold=60, smoothing_factor=0.5, position_history_size=5):
        """Initialize the gesture controller
        
        Args:
            movement_threshold (int): Minimum distance to trigger directional gestures
            smoothing_factor (float): Factor for movement smoothing (0-1)
            position_history_size (int): Number of previous positions to store for smoothing
        """
        self.movement_threshold = movement_threshold
        self.smoothing_factor = smoothing_factor
        self.screen_width, self.screen_height = pyautogui.size()
        self.prev_x = None
        self.prev_y = None
        self.current_x = None
        self.current_y = None
        self.position_history = []
        self.position_history_size = position_history_size
        
    def process_hand_gestures(self, hand_results: HandsResults):
        """Process detected hand landmarks and perform corresponding actions
        
        Args:
            hand_results: HandsResults object containing detected hand landmarks
        """
        if not hand_results or not hand_results.landmarks:
            return
            
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
        
        # Get index finger and thumb tip coordinates (for click detection)
        ix, iy = self._get_landmark_coords(hand_landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP)
        tx, ty = self._get_landmark_coords(hand_landmarks, mp_hands.HandLandmark.THUMB_TIP)
        
        # Move cursor based on middle finger position
        cursor_x = int(mx * self.screen_width)
        cursor_y = int(my * self.screen_height)
        pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)
        
        # Check for click gesture (index finger and thumb proximity)
        distance = ((ix - tx)**2 + (iy - ty)**2) ** 0.5
        if distance < 0.05:  # Threshold for click detection
            pyautogui.click()
            
    def _process_left_hand(self, hand_landmarks, mp_hands):
        """Process left hand gestures for directional controls
        
        Args:
            hand_landmarks: MediaPipe hand landmarks for the left hand
            mp_hands: MediaPipe hands solution instance
        """
        # Get index finger tip coordinates
        ix, iy = self._get_landmark_coords(hand_landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP)
        x, y = int(ix * self.screen_width), int(iy * self.screen_height)
        
        if self.prev_x is not None and self.prev_y is not None:
            dx, dy = x - self.prev_x, y - self.prev_y
            
            # Process horizontal movement
            if abs(dx) > abs(dy):
                if dx > self.movement_threshold:
                    pyautogui.press('right')
                elif dx < -self.movement_threshold:
                    pyautogui.press('left')
            # Process vertical movement
            else:
                if dy > self.movement_threshold:
                    pyautogui.press('down')
                elif dy < -self.movement_threshold:
                    pyautogui.press('up')
                    
        self.prev_x, self.prev_y = x, y
        
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