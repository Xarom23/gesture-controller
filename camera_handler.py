"""
Camera Handler Module
----------------------
Manages camera capture, video display, and integration with gesture detection.
Handles video frame processing, landmark detection, and gesture control coordination.

Key responsibilities:
- Camera initialization and video capture
- Frame processing and display on Tkinter canvas
- Landmark detection coordination
- Gesture processing integration
"""

import cv2
from PIL import Image, ImageTk
import tkinter as tk
import mediapipe as mp
from landmark_detector import LandmarkDetector
from gesture_controller import GestureController


class CameraHandler:
    def __init__(self, canvas, camera_index=0, width=600, height=351):
        """Initialize the camera handler

        Args:
            canvas: Tkinter canvas widget for video display
            camera_index: Index of the camera to use (default: 0)
            width: Width of the video display (default: 600)
            height: Height of the video display (default: 351)
        """
        self.canvas = canvas
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap = None
        self.is_running = False
        self.show_video = True
        self.show_landmarks = False
        self.delay = 15

        self.landmark_detector = LandmarkDetector(
            detect_hands=True,
            detect_face=True,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # MediaPipe drawing utilities
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.mp_face_mesh = mp.solutions.face_mesh

        # Initialize gesture controller
        self.gesture_controller = GestureController()

    def start(self):
        """Start camera video capture"""
        if not self.is_running:
            self.cap = cv2.VideoCapture(self.camera_index)

            # Set camera resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

            if self.cap.isOpened():
                self.is_running = True
                self._update_frame()
            else:
                raise Exception(f"No se pudo abrir la cámara {self.camera_index}")

    def stop(self):
        """Stop video capture and release camera"""
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def set_show_video(self, show):
        """Control whether to display video on canvas

        Args:
            show: True to show video, False to stop canvas updates
        """
        self.show_video = show

    def set_show_landmarks(self, show):
        """Control whether to draw landmarks on video

        Args:
            show: True to show landmarks, False to hide them
        """
        self.show_landmarks = show

    def _update_frame(self):
        """Private method that updates the frame on canvas"""
        if self.is_running and self.cap is not None:
            # Only capture and display frame if show_video is enabled
            if self.show_video:
                ret, frame = self.cap.read()

                if ret:
                    frame = cv2.flip(frame, 1)
                    # Convert from BGR (OpenCV) to RGB for MediaPipe
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Detect hand and face landmarks
                    detection_results = self.landmark_detector.detect_landmarks(frame_rgb)

                    # Process gestures if detections exist and gesture control is enabled
                    from config import gesture_control_enabled
                    if (detection_results.hands or detection_results.face) and gesture_control_enabled:
                        self.gesture_controller.process_gestures(
                            hand_results=detection_results.hands,
                            face_landmarks=detection_results.face
                        )

                    # Draw landmarks if enabled
                    if self.show_landmarks:
                        # Draw hand landmarks
                        if detection_results.hands and detection_results.hands.landmarks:
                            for hand_landmarks in detection_results.hands.landmarks.values():
                                self.mp_drawing.draw_landmarks(
                                    frame_rgb,
                                    hand_landmarks,
                                    self.mp_hands.HAND_CONNECTIONS,
                                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                    self.mp_drawing_styles.get_default_hand_connections_style()
                                )

                        # Draw face landmarks
                        if detection_results.face and detection_results.face.landmarks:
                            self.mp_drawing.draw_landmarks(
                                frame_rgb,
                                detection_results.face.landmarks,
                                self.mp_face_mesh.FACEMESH_TESSELATION,
                            )

                    # Resize frame if necessary
                    frame_resized = cv2.resize(frame_rgb, (self.width, self.height))

                    # Convert to PIL Image format
                    img = Image.fromarray(frame_resized)

                    # Convert to PhotoImage for tkinter
                    self.photo = ImageTk.PhotoImage(image=img)

                    # Clear canvas and display new image
                    self.canvas.delete("all")
                    self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            # Schedule next update (always, even if not displaying)
            self.canvas.after(self.delay, self._update_frame)

    def get_current_frame(self):
        """Get current frame without displaying it on canvas

        Returns:
            numpy.ndarray: Current frame in BGR format (OpenCV)
        """
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def set_camera(self, camera_index):
        """Change the active camera

        Args:
            camera_index: Index of the new camera
        """
        was_running = self.is_running
        if was_running:
            self.stop()

        self.camera_index = camera_index

        if was_running:
            self.start()

    def __del__(self):
        """Destructor to ensure camera is released"""
        self.stop()
        if hasattr(self, 'landmark_detector'):
            self.landmark_detector.close()
